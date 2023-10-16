import asyncio

from sqlalchemy.exc import IntegrityError

from db.engine import engine, session
from db.models import Users


async def register_user(message):
    username = (
        message.from_user.username if message.from_user.username else None
    )

    user = Users(
        id=int(message.from_user.id),
        username=username,
        name=message.from_user.full_name,
    )

    async with session() as local_session:
        try:
            local_session.add(user)
            await local_session.commit()

            return True
        except IntegrityError as e:
            if "UniqueViolation" in str(e.args):
                print(e)
                return "Login was successful"
            else:
                await local_session.rollback()
                print(e)
                return False


async def select_user(user_id):
    async with session() as local_session:
        user = await local_session.get(Users, user_id)
        return user
