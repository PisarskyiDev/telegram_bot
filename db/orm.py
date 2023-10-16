import asyncio

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db.engine import session, engine
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

    async with AsyncSession(engine) as local_session:
        try:
            local_session.add(user)
            await local_session.commit()
            # You can keep the session open for a specified time
            await asyncio.sleep(60)  # Keep the session open for 60 seconds
            return True
        except IntegrityError as e:
            if "UniqueViolation" in str(e.args):
                print(e)
                return "Login was successful"
            else:
                await local_session.rollback()
                print(e)
                return False


def select_user(user_id):
    user = session.query(Users).filter(Users.id == user_id).first()
    return user
