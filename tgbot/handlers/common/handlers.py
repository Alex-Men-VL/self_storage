from telegram import ParseMode, Update

from tgbot.models import User
from tgbot.handlers.common import static_text


def command_start(update: Update, context) -> None:
    user_info = update.message.from_user.to_dict()
    user, created = User.objects.get_or_create(
        user_id=user_info['id'],
        username=user_info['username'],
        first_name=user_info['first_name'],
        last_name=user_info['last_name'],
    )

    if created:
        text = static_text.start_created.format(first_name=user.first_name)
    else:
        text = static_text.start_not_created.format(first_name=user.first_name)

    update.message.reply_text(text=text)
