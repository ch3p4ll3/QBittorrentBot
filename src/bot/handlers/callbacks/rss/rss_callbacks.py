"""Button-driven RSS downloader menu (administrators only), reachable from /start -> RSS or /rss."""
import json
import logging
from typing import Optional

from aiogram import Bot
from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Filter
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.i18n import gettext as _

from src.bot.filters import HasRole, IsAuthorizedUser
from src.bot.filters.callbacks import (
    Menu, RssAddFeed, RssDelete, RssItem, RssList, RssMenu, RssToggle, RssWatch, RssWatchCat, RssWatchFeed,
    RssWatchShow,
)
from src.bot.handlers.rss_utils import (
    build_rule_def, feed_host, find_by_id, parse_add_feed_args, short_id, show_rule_options, unique_name,
)
from src.client_manager.client_repo import ClientRepo
from src.redis_helper.wrapper import RedisWrapper
from src.settings import Settings
from src.settings.enums import UserRolesEnum
from src.utils import get_user_from_config

logger = logging.getLogger(__name__)

ADMIN = HasRole(UserRolesEnum.Administrator)
STATE_TTL = 900  # seconds a half-finished flow is remembered


class HasRssAction(Filter):
    """Matches plain messages sent while the user is in the middle of an RSS flow."""

    async def __call__(self, message: Message, redis: RedisWrapper):
        if not message.text or message.text.startswith("/"):
            return False
        action = await redis.get(f"action:{message.from_user.id}")
        if isinstance(action, str) and action.startswith("rss_"):
            return {"rss_action": action}
        return False


def kb(*rows) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[list(r) for r in rows])


def btn(text: str, data) -> InlineKeyboardButton:
    return InlineKeyboardButton(text=text, callback_data=data.pack())


def back_to_rss() -> InlineKeyboardButton:
    return btn(_("🔙 RSS"), RssMenu())


def back_to_menu() -> InlineKeyboardButton:
    return btn(_("🏠 Menu"), Menu())


def get_router():
    router = Router()

    def manager(settings: Settings):
        return ClientRepo.get_client_manager(settings.client.type)(settings)

    async def show(bot: Bot, chat_id: int, message_id: Optional[int], text: str, markup: InlineKeyboardMarkup) -> None:
        """Edit the menu message in place; send a new one if it can't be edited. parse_mode=None: names may contain markdown."""
        if message_id:
            try:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                            reply_markup=markup, parse_mode=None)
                return
            except Exception as e:
                if "not modified" in str(e):
                    return
                logger.debug(f"edit failed, sending new message: {e}")
        await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode=None)

    async def get_state(redis: RedisWrapper, uid: int) -> dict:
        raw = await redis.get(f"rss_state:{uid}")
        try:
            return json.loads(raw) if raw else {}
        except (TypeError, ValueError):
            return {}

    async def set_state(redis: RedisWrapper, uid: int, action: Optional[str], **state) -> None:
        if action:
            await redis.set(f"action:{uid}", action, ex=STATE_TTL)
        await redis.set(f"rss_state:{uid}", json.dumps(state), ex=STATE_TTL)

    async def clear(redis: RedisWrapper, uid: int) -> None:
        await redis.delete(f"action:{uid}")
        await redis.delete(f"rss_state:{uid}")

    async def failure(bot: Bot, uid: int, message_id: Optional[int], e: Exception) -> None:
        logger.exception(e)
        await show(bot, uid, message_id, _("Something went wrong talking to qBittorrent. See the bot log for details."),
                   kb([back_to_rss()]))

    # ---------------------------------------------------------------- main RSS menu
    async def show_menu(bot: Bot, redis: RedisWrapper, uid: int, message_id: Optional[int], note: str = "") -> None:
        await clear(redis, uid)
        text = (note + "\n\n" if note else "") + _("RSS downloader")
        await show(bot, uid, message_id, text, kb(
            [btn(_("👀 Watch for a name"), RssWatch())],
            [btn(_("📡 Feeds"), RssList(kind="feeds")), btn(_("📋 Rules"), RssList(kind="rules"))],
            [btn(_("➕ Add feed"), RssAddFeed(watch=0))],
            [back_to_menu()],
        ))

    @router.callback_query(RssMenu.filter(), ADMIN)
    async def on_menu(q: CallbackQuery, bot: Bot, redis: RedisWrapper) -> None:
        await q.answer()
        await show_menu(bot, redis, q.from_user.id, q.message.message_id)

    @router.message(Command("rss", "rss_menu"), IsAuthorizedUser())
    async def on_menu_command(message: Message, bot: Bot, redis: RedisWrapper, settings: Settings) -> None:
        user = get_user_from_config(message.from_user.id, settings)
        if not user or user.role != UserRolesEnum.Administrator:
            await message.reply(_("RSS management is for administrators only."), parse_mode=None)
            return
        await show_menu(bot, redis, message.from_user.id, None)

    # ---------------------------------------------------------------- lists and details
    @router.callback_query(RssList.filter(), ADMIN)
    async def on_list(q: CallbackQuery, callback_data: RssList, bot: Bot, settings: Settings) -> None:
        await q.answer()
        uid, mid = q.from_user.id, q.message.message_id
        try:
            qbt = manager(settings)
            if callback_data.kind == "feeds":
                feeds = await qbt.rss_get_feeds()
                rows = [[btn(f"📡 {name[:40]}", RssItem(kind="feed", id=short_id(name)))] for name in feeds]
                rows.append([btn(_("➕ Add feed"), RssAddFeed(watch=0))])
                text = _("Feeds ({count}). Tap one to manage it.").format(count=len(feeds)) if feeds else _("No feeds yet.")
            else:
                rules = await qbt.rss_get_rules()
                rows = [[btn(f"{'✅' if r.get('enabled') else '⏸'} {name[:40]}", RssItem(kind="rule", id=short_id(name)))]
                        for name, r in rules.items()]
                rows.append([btn(_("👀 Watch for a name"), RssWatch())])
                text = _("Rules ({count}). Tap one to manage it.").format(count=len(rules)) if rules else _("No rules yet.")
        except Exception as e:
            await failure(bot, uid, mid, e)
            return
        rows.append([back_to_rss()])
        await show(bot, uid, mid, text, kb(*rows))

    async def show_item(bot: Bot, settings: Settings, uid: int, mid: int, kind: str, item_id: str) -> None:
        try:
            qbt = manager(settings)
            if kind == "feed":
                feeds = await qbt.rss_get_feeds()
                name = find_by_id(feeds.keys(), item_id)
                if not name:
                    await show(bot, uid, mid, _("That feed no longer exists."), kb([btn(_("🔙 Feeds"), RssList(kind="feeds"))]))
                    return
                await show(bot, uid, mid, _("Feed: {name}\nHost: {host}").format(name=name, host=feed_host(feeds[name])), kb(
                    [btn(_("🗑 Remove"), RssDelete(kind="feed", id=item_id, confirm=0))],
                    [btn(_("🔙 Feeds"), RssList(kind="feeds"))],
                ))
                return

            rules = await qbt.rss_get_rules()
            feeds = await qbt.rss_get_feeds()
            name = find_by_id(rules.keys(), item_id)
            if not name:
                await show(bot, uid, mid, _("That rule no longer exists."), kb([btn(_("🔙 Rules"), RssList(kind="rules"))]))
                return
            r = rules[name]
            url_to_name = {u: n for n, u in feeds.items()}
            on = bool(r.get("enabled"))
            lines = [
                _("Rule: {name}").format(name=name),
                _("Status: ENABLED") if on else _("Status: DISABLED"),
                _("Feeds: {value}").format(value=', '.join(url_to_name.get(u, '?') for u in r.get('affectedFeeds', [])) or '-'),
                _("Must contain: {value}").format(value=r.get('mustContain') or '-'),
            ]
            if r.get("mustNotContain"):
                lines.append(_("Must not contain: {value}").format(value=r['mustNotContain']))
            if r.get("assignedCategory"):
                lines.append(_("Category: {value}").format(value=r['assignedCategory']))
            lines.append(_("Last match: {value}").format(value=r.get('lastMatch') or _("never")))
            await show(bot, uid, mid, "\n".join(lines), kb(
                [btn(_("⏸ Disable") if on else _("▶️ Enable"), RssToggle(id=item_id))],
                [btn(_("🗑 Delete"), RssDelete(kind="rule", id=item_id, confirm=0))],
                [btn(_("🔙 Rules"), RssList(kind="rules"))],
            ))
        except Exception as e:
            await failure(bot, uid, mid, e)

    @router.callback_query(RssItem.filter(), ADMIN)
    async def on_item(q: CallbackQuery, callback_data: RssItem, bot: Bot, settings: Settings) -> None:
        await q.answer()
        await show_item(bot, settings, q.from_user.id, q.message.message_id, callback_data.kind, callback_data.id)

    @router.callback_query(RssToggle.filter(), ADMIN)
    async def on_toggle(q: CallbackQuery, callback_data: RssToggle, bot: Bot, settings: Settings) -> None:
        await q.answer()
        uid, mid = q.from_user.id, q.message.message_id
        try:
            qbt = manager(settings)
            rules = await qbt.rss_get_rules()
            name = find_by_id(rules.keys(), callback_data.id)
            if name:
                rule = dict(rules[name])
                rule["enabled"] = not rule.get("enabled", False)
                await qbt.rss_set_rule(name, rule)
        except Exception as e:
            await failure(bot, uid, mid, e)
            return
        await show_item(bot, settings, uid, mid, "rule", callback_data.id)

    @router.callback_query(RssDelete.filter(), ADMIN)
    async def on_delete(q: CallbackQuery, callback_data: RssDelete, bot: Bot, settings: Settings) -> None:
        await q.answer()
        uid, mid = q.from_user.id, q.message.message_id
        kind = callback_data.kind
        back = btn(_("🔙 Feeds") if kind == "feed" else _("🔙 Rules"), RssList(kind="feeds" if kind == "feed" else "rules"))
        try:
            qbt = manager(settings)
            items = await (qbt.rss_get_feeds() if kind == "feed" else qbt.rss_get_rules())
            name = find_by_id(items.keys(), callback_data.id)
            if not name:
                await show(bot, uid, mid, _("It no longer exists."), kb([back]))
                return
            if not callback_data.confirm:
                question = _("Remove the feed '{name}'?") if kind == "feed" else _("Remove the rule '{name}'?")
                await show(bot, uid, mid, question.format(name=name), kb(
                    [btn(_("✅ Yes, remove"), RssDelete(kind=kind, id=callback_data.id, confirm=1)),
                     btn(_("Cancel"), RssItem(kind=kind, id=callback_data.id))],
                ))
                return
            await (qbt.rss_remove_feed(name) if kind == "feed" else qbt.rss_remove_rule(name))
        except Exception as e:
            await failure(bot, uid, mid, e)
            return
        done = _("Removed the feed '{name}'.") if kind == "feed" else _("Removed the rule '{name}'.")
        await show(bot, uid, mid, done.format(name=name), kb([back], [back_to_rss()]))

    # ---------------------------------------------------------------- add feed
    @router.callback_query(RssAddFeed.filter(), ADMIN)
    async def on_add_feed(q: CallbackQuery, callback_data: RssAddFeed, bot: Bot, redis: RedisWrapper) -> None:
        await q.answer()
        await set_state(redis, q.from_user.id, "rss_addfeed", watch=callback_data.watch)
        await show(bot, q.from_user.id, q.message.message_id,
                   _("Send the feed as:\n\nname url\n\nExample:\nmyfeed https://example.org/rss?key=...\n\n"
                     "The name can't contain spaces. Your message is deleted afterwards because feed URLs often contain passkeys."),
                   kb([back_to_rss()]))

    # ---------------------------------------------------------------- watch for a name
    @router.callback_query(RssWatch.filter(), ADMIN)
    async def on_watch(q: CallbackQuery, bot: Bot, redis: RedisWrapper, settings: Settings) -> None:
        await q.answer()
        uid, mid = q.from_user.id, q.message.message_id
        await clear(redis, uid)
        try:
            feeds = await manager(settings).rss_get_feeds()
        except Exception as e:
            await failure(bot, uid, mid, e)
            return
        rows = [[btn(f"📡 {name[:40]}", RssWatchFeed(id=short_id(name)))] for name in feeds]
        rows.append([btn(_("➕ New feed"), RssAddFeed(watch=1))])
        rows.append([back_to_rss()])
        await show(bot, uid, mid, _("Which feed should I watch?") if feeds else _("No feeds yet. Add one first."), kb(*rows))

    async def ask_name(bot: Bot, redis: RedisWrapper, uid: int, mid: Optional[int], feed: str) -> None:
        await set_state(redis, uid, "rss_watchname", feed=feed)
        await show(bot, uid, mid,
                   _("Feed: {feed}\n\nSend the name to wait for.\nA new upload whose title contains all these words "
                     "will be downloaded.\n\nExample: Foo Show 1080p").format(feed=feed),
                   kb([back_to_rss()]))

    @router.callback_query(RssWatchFeed.filter(), ADMIN)
    async def on_watch_feed(q: CallbackQuery, callback_data: RssWatchFeed, bot: Bot, redis: RedisWrapper, settings: Settings) -> None:
        await q.answer()
        uid, mid = q.from_user.id, q.message.message_id
        try:
            feeds = await manager(settings).rss_get_feeds()
        except Exception as e:
            await failure(bot, uid, mid, e)
            return
        name = find_by_id(feeds.keys(), callback_data.id)
        if not name:
            await show(bot, uid, mid, _("That feed no longer exists."), kb([back_to_rss()]))
            return
        await ask_name(bot, redis, uid, mid, name)

    async def ask_category(bot: Bot, redis: RedisWrapper, settings: Settings, uid: int, feed: str, watch_name: str) -> None:
        await set_state(redis, uid, "rss_watchcat", feed=feed, name=watch_name)
        try:
            categories = await manager(settings).get_categories() or {}
        except Exception as e:
            logger.warning(f"Could not read the categories: {e}")
            categories = {}
        rows = [[btn(c[:40], RssWatchCat(id=short_id(c)))] for c in categories]
        rows.append([btn(_("No category"), RssWatchCat(id="-"))])
        rows.append([back_to_rss()])
        await show(bot, uid, None,
                   _("Watching '{name}' on {feed}.\n\nDownload new matches into which category?").format(name=watch_name, feed=feed),
                   kb(*rows))

    @router.callback_query(RssWatchCat.filter(), ADMIN)
    async def on_watch_cat(q: CallbackQuery, callback_data: RssWatchCat, bot: Bot, redis: RedisWrapper, settings: Settings) -> None:
        await q.answer()
        uid, mid = q.from_user.id, q.message.message_id
        state = await get_state(redis, uid)
        feed, watch_name = state.get("feed"), state.get("name")
        if not feed or not watch_name:
            await show(bot, uid, mid, _("That took too long, please start again."), kb([back_to_rss()]))
            return
        category = ""
        if callback_data.id != "-":
            try:
                categories = await manager(settings).get_categories() or {}
            except Exception as e:
                await failure(bot, uid, mid, e)
                return
            category = find_by_id(categories.keys(), callback_data.id) or ""
        # TV options are opt-in: ask, whatever the category is called
        await set_state(redis, uid, "rss_watchshow", feed=feed, name=watch_name, category=category)
        await show(bot, uid, mid,
                   _("Is '{name}' a TV show?\n\nIf so, the smart episode filter is turned on (an episode that was already "
                     "downloaded is not downloaded again)"
                     " and, if the category has a save path, the downloads go into a folder named after the show.\n\n"
                     "If not, the rule is created without any extra options.").format(name=watch_name),
                   kb([btn(_("📺 Yes, a TV show"), RssWatchShow(on=1)), btn(_("No"), RssWatchShow(on=0))],
                      [back_to_rss()]))

    @router.callback_query(RssWatchShow.filter(), ADMIN)
    async def on_watch_show(q: CallbackQuery, callback_data: RssWatchShow, bot: Bot, redis: RedisWrapper, settings: Settings) -> None:
        await q.answer()
        uid, mid = q.from_user.id, q.message.message_id
        state = await get_state(redis, uid)
        feed, watch_name, category = state.get("feed"), state.get("name"), state.get("category") or ""
        if not feed or not watch_name:
            await show(bot, uid, mid, _("That took too long, please start again."), kb([back_to_rss()]))
            return
        options = {}
        marked = True
        try:
            qbt = manager(settings)
            feeds = await qbt.rss_get_feeds()
            if feed not in feeds:
                await show(bot, uid, mid, _("That feed no longer exists."), kb([back_to_rss()]))
                return
            # only uploads that appear from now on should match: fetch the feed, then mark what it holds as read
            try:
                await qbt.rss_refresh_item(feed)
                await qbt.rss_mark_all_read(feed)
            except Exception as e:
                marked = False
                logger.warning(f"Could not refresh the feed and mark its articles as read: {e}")
            rule_name = unique_name(watch_name, (await qbt.rss_get_rules()).keys())
            if callback_data.on:
                options = show_rule_options(category, watch_name, await qbt.get_categories() or {})
            await qbt.rss_set_rule(rule_name, build_rule_def([feeds[feed]], watch_name, "", category, **options))
        except Exception as e:
            await failure(bot, uid, mid, e)
            return
        await clear(redis, uid)

        text = _("👀 Watching '{name}' on {feed}").format(name=watch_name, feed=feed)
        if category:
            text += f" -> {category}"
        if options.get("save_path"):
            text += "\n" + _("Smart episode filter on, saving to {path}").format(path=options["save_path"])
        elif options:
            text += "\n" + _("Smart episode filter on")
        text += ".\n\n"
        if marked:
            text += _("Only uploads that appear from now on will match. ")
        else:
            text += _("⚠️ I could not mark the existing items of the feed as read (the feed may be slow or unreachable), "
                      "so older uploads that match may be downloaded too. ")
        text += _("New uploads that match will be downloaded automatically and you'll get a notification "
                  "when they finish. qBittorrent checks the feed periodically.")
        await show(bot, uid, mid, text, kb([btn(_("📋 Rules"), RssList(kind="rules"))], [back_to_rss()]))

    # ---------------------------------------------------------------- text input for the flows above
    @router.message(IsAuthorizedUser(), HasRssAction())
    async def on_text(message: Message, rss_action: str, bot: Bot, redis: RedisWrapper, settings: Settings) -> None:
        uid = message.from_user.id
        user = get_user_from_config(uid, settings)
        if not user or user.role != UserRolesEnum.Administrator:
            return
        state = await get_state(redis, uid)

        if rss_action == "rss_addfeed":
            parsed = parse_add_feed_args(message.text)
            # the message contains the feed URL (may include a passkey): delete it right after parsing, whatever
            # happens next, and answer with new messages since replying to a deleted message can fail
            try:
                await message.delete()
            except Exception as e:
                logger.debug(f"Could not delete the message: {e}")
            if not parsed:
                await message.answer(_("I couldn't read that. Send: name url\n(name without spaces, url starting with http:// or https://)"),
                                     parse_mode=None)
                return
            name, url = parsed
            try:
                qbt = manager(settings)
                if name in await qbt.rss_get_feeds():
                    await message.answer(_("A feed named '{name}' already exists. Send a different name.").format(name=name), parse_mode=None)
                    return
                await qbt.rss_add_feed(name, url)
            except Exception as e:
                logger.exception(e)
                await message.answer(_("Could not add the feed. See the bot log for details."), parse_mode=None)
                return
            if state.get("watch"):
                await ask_name(bot, redis, uid, None, name)
            else:
                await show_menu(bot, redis, uid, None, note=_("Feed '{name}' added ({host}).").format(name=name, host=feed_host(url)))
            return

        if rss_action == "rss_watchname":
            watch_name = message.text.strip()
            if not watch_name or len(watch_name) > 120:
                await message.reply(_("Send the words to wait for (up to 120 characters)."), parse_mode=None)
                return
            await ask_category(bot, redis, settings, uid, state.get("feed", ""), watch_name)
            return

    return router
