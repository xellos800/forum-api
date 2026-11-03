import pytest
from app import models


@pytest.fixture
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    session.refresh(new_vote)


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={
        "post_id": test_posts[3].id,
        "dir": 1
    })
    assert res.status_code == 201
    assert res.json().get("message") == "Post liked."


def test_delete_vote(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={
        "post_id": test_posts[3].id,
        "dir": 0
    })
    assert res.status_code == 201
    assert res.json().get("message") == "You have unliked this post."


def test_vote_twice(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={
        "post_id": test_posts[3].id,
        "dir": 1
    })
    assert res.status_code == 409


def delete_no_vote(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={
        "post_id": test_posts[3].id,
        "dir": 0
    })
    assert res.status_code == 404


def test_vote_on_no_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={
        "post_id": 00000000000,
        "dir": 1
    })
    assert res.status_code == 404


def test_vote_non_authenticated(client, test_posts, test_user):
    res = client.post("/vote/", json={
        "post_id": test_posts[3].id,
        "dir": 1
    })
    assert res.status_code == 401
