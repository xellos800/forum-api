from app import schemas
import pytest
import jwt
from app.oauth2 import SECRET_KEY, ALGORITHM


def test_root(client, session):
    res = client.get("/")
    assert res.json().get('message') == 'hello world!'
    assert res.status_code == 200


def test_create_user(client, session):
    res = client.post(
        "/users/", json={"email": "foo_bar@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "foo_bar@gmail.com"
    assert res.status_code == 200


def test_login(client, test_user):
    res = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
        }
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    assert res.status_code == 200
    assert username == test_user["email"]
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize("email, password, status_code", [
    ("wrongEmail@gmail.com", "password123", 401),
    ("foo_bar@gmail.com", "bad_password", 401),
    ("wrongEmail@gmail.com", "bad_password", 401),
    (None, "password123", 422),
    ("foo_bar@gmail.com", None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login",
                      data={
                          "username": email,
                          "password": password
                      }
                      )
    assert res.status_code == status_code
