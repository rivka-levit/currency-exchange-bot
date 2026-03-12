from aiogram.types import Chat, User

TEST_TG_USER = User(
    id=563248,
    is_bot=False,
    first_name='TestFirstName',
    last_name='TestLastName',
    username='TestUsername',
    language_code='ru',
)

TEST_CHAT = Chat(
    id=12,
    type='private',
    first_name=TEST_TG_USER.first_name,
    last_name=TEST_TG_USER.last_name,
    username=TEST_TG_USER.username,
)
