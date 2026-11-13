import logging

from aiogram.dispatcher.router import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _

from src.client_manager.client_repo import ClientRepo
from src.settings import Settings
from src.settings.enums import UserRolesEnum
from src.utils import get_user_from_config

from ..filters import IsAuthorizedUser
from .rss_utils import (
    build_rule_def, chunk_text, feed_host, parse_add_feed_args, parse_add_rule_args, resolve_category,
    resolve_feed_urls, show_rule_options,
)

logger = logging.getLogger(__name__)

RULE_USAGE = ("/rss_addrule <name> ; <feed or all> ; <must contain> ; [must not contain] ; [category] ; [show]")


def get_help() -> str:
    return _(
        "RSS commands (administrators only)\n\n"
        "/rss - open the RSS menu (buttons)\n"
        "/rss_list - show feeds and rules as text\n"
        "/rss_addfeed <name> <url> - add a feed (no spaces in the name)\n"
        "/rss_delfeed <name> - remove a feed\n"
        "/rss_addrule <name> ; <feed or all> ; <must contain> ; [must not contain] ; [category] ; [show]\n"
        "/rss_delrule <name> - remove a rule\n"
        "/rss_toggle <name> - enable or disable a rule\n\n"
        "The fields of /rss_addrule are separated by a semicolon (;). A | inside a field is kept as it is: "
        "qBittorrent reads it as \"or\" in the must-contain field.\n"
        "Write show as the last field to mark the rule as a TV show: the smart episode filter is turned on "
        "(an episode that was already downloaded is not downloaded again) and, if the category has a save path, "
        "the downloads go into a folder named after the rule. Without it, nothing extra is applied.\n\n"
        "Example:\n"
        "/rss_addrule Foo Show ; myfeed ; Foo 1080p ; 720p ; TV ; show\n\n"
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

    async def answer(message: Message, text: str) -> None:
        """Like reply(), but as a new message: used after the user's own message was deleted."""
        for chunk in chunk_text(text):
            await message.answer(chunk, parse_mode=None)

    async def delete_quietly(message: Message) -> None:
        try:
            await message.delete()
        except Exception as e:
            logger.debug(f"Could not delete the message: {e}")

    async def guard(message: Message, settings: Settings) -> bool:
        if not is_admin(message, settings):
            await reply(message, _("RSS management is for administrators only."))
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
            await reply(message, _("Could not read RSS from qBittorrent. See the bot log for details."))
            return

        url_to_name = {url: name for name, url in feeds.items()}
        lines = [_("Feeds ({count})").format(count=len(feeds))]
        lines += [f"  {name}  [{feed_host(url)}]" for name, url in feeds.items()] or ["  " + _("none")]
        lines += ["", _("Rules ({count})").format(count=len(rules))]
        for name, rule in rules.items():
            state = "ON " if rule.get("enabled") else "OFF"
            names = [url_to_name.get(u, "?") for u in rule.get("affectedFeeds", [])]
            extra = []
            if rule.get("mustNotContain"):
                extra.append(_("not: {value}").format(value=rule["mustNotContain"]))
            if rule.get("assignedCategory"):
                extra.append(_("cat: {value}").format(value=rule["assignedCategory"]))
            lines.append(f"  [{state}] {name}")
            lines.append("        " + _("feeds: {value}").format(value=", ".join(names) or "-"))
            lines.append("        " + _("match: {value}").format(value=rule.get("mustContain") or "-")
                         + (f"  ({'; '.join(extra)})" if extra else ""))
        if not rules:
            lines.append("  " + _("none"))
        lines += ["", _("/rss opens the button menu. Text commands: /rss_addfeed /rss_delfeed /rss_addrule /rss_delrule /rss_toggle")]
        await reply(message, "\n".join(lines))

    @router.message(Command("rss_help"), IsAuthorizedUser())
    async def rss_help(message: Message, settings: Settings) -> None:
        if await guard(message, settings):
            await reply(message, get_help())

    @router.message(Command("rss_addfeed"), IsAuthorizedUser())
    async def rss_addfeed(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        parsed = parse_add_feed_args(command.args)
        # the command may contain the feed URL (and a passkey): remove it from the chat as soon as it is parsed,
        # whatever happens next, and answer with new messages since replying to a deleted message can fail
        if command.args:
            await delete_quietly(message)
        if not parsed:
            await answer(message, _("Usage: /rss_addfeed <name> <url>\n(name without spaces, url starting with http:// or https://)"))
            return
        name, url = parsed
        try:
            qbt = manager(settings)
            if name in await qbt.rss_get_feeds():
                await answer(message, _("A feed named '{name}' already exists.").format(name=name))
                return
            await qbt.rss_add_feed(name, url)
        except Exception as e:
            logger.exception(e)
            await answer(message, _("Could not add the feed. See the bot log for details."))
            return
        await answer(message, _("Feed '{name}' added ({host}).").format(name=name, host=feed_host(url)))

    @router.message(Command("rss_delfeed"), IsAuthorizedUser())
    async def rss_delfeed(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        name = (command.args or "").strip()
        if not name:
            await reply(message, _("Usage: /rss_delfeed <name>"))
            return
        try:
            qbt = manager(settings)
            feeds = await qbt.rss_get_feeds()
            if name not in feeds:
                await reply(message, _("No feed named '{name}'. Send /rss to see them.").format(name=name))
                return
            await qbt.rss_remove_feed(name)
        except Exception as e:
            logger.exception(e)
            await reply(message, _("Could not remove the feed. See the bot log for details."))
            return
        await reply(message, _("Feed '{name}' removed. Rules that used it keep working for their other feeds.").format(name=name))

    @router.message(Command("rss_addrule"), IsAuthorizedUser())
    async def rss_addrule(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        parsed = parse_add_rule_args(command.args)
        if not parsed:
            await reply(message, _("Usage: {usage}\n\nExample: /rss_addrule Foo Show ; myfeed ; Foo 1080p ; 720p ; TV ; show\n\n"
                                   "Fields are separated by a semicolon (;). See /rss_help.").format(usage=RULE_USAGE))
            return
        try:
            qbt = manager(settings)
            feeds = await qbt.rss_get_feeds()
            urls = resolve_feed_urls(parsed["feed"], feeds)
            if not urls:
                await reply(message, _("No feed named '{name}'. Send /rss to see them.").format(name=parsed["feed"]))
                return
            if parsed["name"] in await qbt.rss_get_rules():
                await reply(message, _("A rule named '{name}' already exists. Remove it first with /rss_delrule.").format(name=parsed["name"]))
                return
            categories = await qbt.get_categories() or {}
            category = resolve_category(parsed["category"], categories)   # 'tv' -> 'TV'
            # only when the user asked for it: smart episode filter + a folder named after the rule
            options = show_rule_options(category, parsed["name"], categories) if parsed["show"] else {}
            await qbt.rss_set_rule(
                parsed["name"],
                build_rule_def(urls, parsed["must_contain"], parsed["must_not_contain"], category, **options),
            )
        except Exception as e:
            logger.exception(e)
            await reply(message, _("Could not add the rule. See the bot log for details."))
            return
        await reply(message, _("Rule '{name}' added and enabled ({count} feed(s)).").format(name=parsed["name"], count=len(urls)))

    @router.message(Command("rss_delrule"), IsAuthorizedUser())
    async def rss_delrule(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        name = (command.args or "").strip()
        if not name:
            await reply(message, _("Usage: /rss_delrule <name>"))
            return
        try:
            qbt = manager(settings)
            if name not in await qbt.rss_get_rules():
                await reply(message, _("No rule named '{name}'. Send /rss to see them.").format(name=name))
                return
            await qbt.rss_remove_rule(name)
        except Exception as e:
            logger.exception(e)
            await reply(message, _("Could not remove the rule. See the bot log for details."))
            return
        await reply(message, _("Rule '{name}' removed.").format(name=name))

    @router.message(Command("rss_toggle"), IsAuthorizedUser())
    async def rss_toggle(message: Message, command: CommandObject, settings: Settings) -> None:
        if not await guard(message, settings):
            return
        name = (command.args or "").strip()
        if not name:
            await reply(message, _("Usage: /rss_toggle <rule name>"))
            return
        try:
            qbt = manager(settings)
            rules = await qbt.rss_get_rules()
            if name not in rules:
                await reply(message, _("No rule named '{name}'. Send /rss to see them.").format(name=name))
                return
            rule = dict(rules[name])
            rule["enabled"] = not rule.get("enabled", False)
            await qbt.rss_set_rule(name, rule)
        except Exception as e:
            logger.exception(e)
            await reply(message, _("Could not change the rule. See the bot log for details."))
            return
        if rule["enabled"]:
            await reply(message, _("Rule '{name}' is now ENABLED.").format(name=name))
        else:
            await reply(message, _("Rule '{name}' is now DISABLED.").format(name=name))

    return router
