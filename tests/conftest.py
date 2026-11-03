from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
from app.oauth2 import generate_token
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from app import models

DATABASE_URL = f'postgresql+psycopg://postgres:hello@localhost:5432/fastapi_test'

# DATABASE_URL = f'postgresql+psycopg://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test'

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

testingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)


# returns database session
@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = testingSessionLocal()
    try:
        yield db
    finally:
        db.close()

 # returns new test client with new databse session


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(client):
    user_data = {"email": "foo_bar@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_second_user(client):
    user_data = {"email": "foo_bar1@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return generate_token({"sub": test_user["email"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user, test_second_user, session):
    post_data = [
        {"title": "first title",
         "content": "some content",
         "user_id": test_user["id"]},

        {"title": "second title",
         "content": "spam and eggs",
         "user_id": test_user["id"]},

        {"title": "third title",
         "content": "eggs and spam",
         "user_id": test_user["id"]},

        {"title": "fourth post",
         "content": "eggs and cheese",
         "user_id": test_second_user["id"]}
    ]

    def create_posts_model(post):
        return models.Post(**post)

    posts_map = map(create_posts_model, post_data)
    posts = list(posts_map)

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
