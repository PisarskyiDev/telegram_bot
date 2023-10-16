from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Users, Base

engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)


def test_users_model():
    Base.metadata.create_all(engine)

    session = Session()

    user = Users(id=1, username="testuser", name="Test User", admin=True)

    session.add(user)

    session.commit()

    queried_user = session.query(Users).filter_by(id=1).first()

    assert queried_user is not None
    assert queried_user.id == 1
    assert queried_user.username == "testuser"
    assert queried_user.name == "Test User"
    assert queried_user.admin == True

    # Close the session
    session.close()
