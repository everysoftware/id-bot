import aiohttp
from aiogram import Router, types
from aiogram.filters import CommandStart, CommandObject

from .config import settings
from .schemas import OpenID

router = Router()


@router.message(CommandStart(deep_link=True))
async def start_command(
        message: types.Message, command: CommandObject
) -> None:
    assert command.args is not None
    assert message.from_user is not None

    bot_code, user = command.args, message.from_user
    open_id = OpenID(
        provider="telegram",
        id=str(user.id),
        first_name=user.first_name,
        last_name=user.last_name,
        display_name=f"{user.first_name} {user.last_name}",
    )
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{settings.callback_url}?bot_code={bot_code}",
                json=open_id.model_dump(mode="json"),
        ) as resp:
            resp_json = await resp.json()
            await message.answer(str(resp_json), parse_mode=None)
            if resp.status == 200:
                await message.answer("Connected ✅")
            else:
                await message.answer("Error ❌")
