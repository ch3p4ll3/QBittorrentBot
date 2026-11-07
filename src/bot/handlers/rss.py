import logging

from aiogram.dispatcher.router import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from src.client_manager.client_repo import ClientRepo
from src.settings import Settings
from src.settings.enums import UserRolesEnum
from src.utils import get_user_from_config

from ..filters import IsAuthorizedUser
from .rss_utils import (
    build_rule_def, chunk_text, feed_host, parse_add_feed_args, parse_add_rule_args, resolve_feed_urls,
    show_rule_options,
)

logger = logging.getLogger(__name__)

HELP = (
    "RSS commands (administrators only)\n\n"
    "/rss - open the RSS menu (buttons)\n"
    "/rss_list - show feeds and rules as text\n"
    "/rss_addfeed <name> <url> - add a feed (no spaces in the name)\n"
    "/rss_delfeed <name> - remove a feed\n"
    "/rss_addrule <name> | <feed or all> | <must contain> | [must not contain] | [category]\n"
    "/rss_delrule <name> - remove a rule\n"
    "/rss_toggle <name> - enable or disable a rule\n\n"
    "Example:\n"
    "/rss_addrule shows | myfeed | Foo 1080p | 720p | TV\n\n"
    "Feed URLs are never shown, they can contain passkeys."
)


def get_router():
    router = Router()

    def manager(settings: Settings):
        return ClientRepo.get_client_manager(settings.client.type)(settings)

    def is_admin(message: Message, settings: Settings) -> bool:
        user = get_user_from_config(message.from_user.id, settings)
        return bool(user) and user.role == UserRolesEnum.Administrator

    async def reply(message: Message, text: str) -> None:
        # parse_mode=None: feed and rule names may contain markdown characters
        for chunk in chunk_text(text):
            await message.reply(chunk, parse_mode=None)

    async def guard(message: Message, settings: Settings) -> bool:
        if not is_admin(message, settings):
            await reply(message, "RSS management is for administrators only.")
            return False
        return True

    @router.message(Command("rss_list"), IsAuthorizedUser())
    async def rss_overview(message: Message, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        try:
            qbt = manager(settings)
            feeds = await qbt.rss_get_feeds()
            rules = await qbt.rss_get_rules()
        except Exception as e:
            logger.exception(e)
            await reply(message, f"Could not read RSS from qBittorrent: {e}")
            return

        url_to_name = {url: name for name, url in feeds.items()}
        lines = [f"Feeds ({len(feeds)})"]
        lines += [f"  {name}  [{feed_host(url)}]" for name, url in feeds.items()] or ["  none"]
        lines += ["", f"Rules ({len(rules)})"]
        for name, rule in rules.items():
            state = "ON " if rule.get("enabled") else "OFF"
            names = [url_to_name.get(u, "?") for u in rule.get("affectedFeeds", [])]
            extra = []
            if rule.get("mustNotContain"):
                extra.append(f"not: {rule['mustNotContain']}")
            if rule.get("assignedCategory"):
                extra.append(f"cat: {rule['assignedCategory']}")
            lines.append(f"  [{state}] {name}")
            lines.append(f"        feeds: {', '.join(names) or '-'}")
            lines.append(f"        match: {rule.get('mustContain') or '-'}" + (f"  ({'; '.join(extra)})" if extra else ""))
        if not rules:
            lines.append("  none")
        lines += ["", "/rss opens the button menu. Text commands: /rss_addfeed /rss_delfeed /rss_addrule /rss_delrule /rss_toggle"]
        await reply(message, "\n".join(lines))

    @router.message(Command("rss_help"), IsAuthorizedUser())
    async def rss_help(message: Message, settings: Settings) -> None:
        if await guard(message, settings):
            await reply(message, HELP)

    @router.message(Command("rss_addfeed"), IsAuthorizedUser())
    async def rss_addfeed(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        parsed = parse_add_feed_args(command.args)
        if not parsed:
            await reply(message, "Usage: /rss_addfeed <name> <url>\n(name without spaces, url starting with http:// or https://)")
            return
        name, url = parsed
        try:
            qbt = manager(settings)
            if name in await qbt.rss_get_feeds():
                await reply(message, f"A feed named '{name}' already exists.")
                return
            await qbt.rss_add_feed(name, url)
        except Exception as e:
            logger.exception(e)
            await reply(message, f"Could not add the feed: {e}")
            return

        # the command contained the URL (may include a passkey): remove it from the chat history
        deleted = False
        try:
            await message.delete()
            deleted = True
        except Exception:
            pass
        await message.answer(
            f"Feed '{name}' added ({feed_host(url)})." + ("" if deleted else " Delete your message, it contains the URL."),
            parse_mode=None,
        )

    @router.message(Command("rss_delfeed"), IsAuthorizedUser())
    async def rss_delfeed(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        name = (command.args or "").strip()
        if not name:
            await reply(message, "Usage: /rss_delfeed <name>")
            return
        try:
            qbt = manager(settings)
            feeds = await qbt.rss_get_feeds()
            if name not in feeds:
                await reply(message, f"No feed named '{name}'. Send /rss to see them.")
                return
            await qbt.rss_remove_feed(name)
        except Exception as e:
            logger.exception(e)
            await reply(message, f"Could not remove the feed: {e}")
            return
        await reply(message, f"Feed '{name}' removed. Rules that used it keep working for their other feeds.")

    @router.message(Command("rss_addrule"), IsAuthorizedUser())
    async def rss_addrule(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        parsed = parse_add_rule_args(command.args)
        if not parsed:
            await reply(message, "Usage: /rss_addrule <name> | <feed or all> | <must contain> | [must not contain] | [category]\n\n"
                                 "Example: /rss_addrule shows | myfeed | Foo 1080p | 720p | TV")
            return
        try:
            qbt = manager(settings)
            feeds = await qbt.rss_get_feeds()
            urls = resolve_feed_urls(parsed["feed"], feeds)
            if not urls:
                await reply(message, f"No feed named '{parsed['feed']}'. Send /rss to see them.")
                return
            if parsed["name"] in await qbt.rss_get_rules():
                await reply(message, f"A rule named '{parsed['name']}' already exists. Remove it first with /rss_delrule.")
                return
            # TV shows (category "Shows"/"TV"): smart episode filter + a folder named after the rule
            options = show_rule_options(parsed["category"], parsed["name"], await qbt.get_categories() or {})
            await qbt.rss_set_rule(
                parsed["name"],
                build_rule_def(urls, parsed["must_contain"], parsed["must_not_contain"], parsed["category"], **options),
            )
        except Exception as e:
            logger.exception(e)
            await reply(message, f"Could not add the rule: {e}")
            return
        await reply(message, f"Rule '{parsed['name']}' added and enabled ({len(urls)} feed(s)).")

    @router.message(Command("rss_delrule"), IsAuthorizedUser())
    async def rss_delrule(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        name = (command.args or "").strip()
        if not name:
            await reply(message, "Usage: /rss_delrule <name>")
            return
        try:
            qbt = manager(settings)
            if name not in await qbt.rss_get_rules():
                await reply(message, f"No rule named '{name}'. Send /rss to see them.")
                return
            await qbt.rss_remove_rule(name)
        except Exception as e:
            logger.exception(e)
            await reply(message, f"Could not remove the rule: {e}")
            return
        await reply(message, f"Rule '{name}' removed.")

    @router.message(Command("rss_toggle"), IsAuthorizedUser())
    async def rss_toggle(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        name = (command.args or "").strip()
        if not name:
            await reply(message, "Usage: /rss_toggle <rule name>")
            return
        try:
            qbt = manager(settings)
            rules = await qbt.rss_get_rules()
            if name not in rules:
                await reply(message, f"No rule named '{name}'. Send /rss to see them.")
                return
            rule = dict(rules[name])
            rule["enabled"] = not rule.get("enabled", False)
            await qbt.rss_set_rule(name, rule)
        except Exception as e:
            logger.exception(e)
            await reply(message, f"Could not change the rule: {e}")
            return
        await reply(message, f"Rule '{name}' is now {'ENABLED' if rule['enabled'] else 'DISABLED'}.")

    return router
