from aiogram.types import TelegramObject, User

ADMIN_TG_IDS: set[int] = {
    863821159,
}


def extract_user(event: TelegramObject) -> User | None:
    user = getattr(event, "from_user", None)
    return user if isinstance(user, User) else None


def is_admin(event: TelegramObject) -> bool:
    user = extract_user(event)
    return user is not None and user.id in ADMIN_TG_IDS
