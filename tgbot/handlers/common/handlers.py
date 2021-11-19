from telegram import ParseMode, Update

from tgbot.models import StorageUser
from tgbot.handlers.common import static_text
from .keyboard_utils import make_keyboard_for_start_command


def command_start(update: Update, context) -> None:
    user_info = update.message.from_user.to_dict()
    user, created = StorageUser.objects.get_or_create(
        telegram_id=user_info['id'],
        username=user_info['username']
    )

    if created:
        text = static_text.start_created.format(
            first_name=user_info['first_name']
        )
    else:
        text = static_text.start_not_created.format(
            first_name=user_info['first_name']
        )

    update.message.reply_text(
        text=text,
        reply_markup=make_keyboard_for_start_command(),
    )