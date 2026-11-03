import pytest
from app import models, schemas


@pytest.fixture
def test_comment(test_posts, session, test_user):
    new_comment = models.Comment(
        content="here is a funny comment", post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment

# Authorized user can comment


def test_authorized_comment(authorized_client, test_user, test_posts):
    res = authorized_client.post(f"/posts/{test_posts[3].id}/comments/",
                                 json={"content": "a comment from an authorized user!"})

    new_comment = schemas.CommentOut(**res.json())
    assert res.status_code == 201
    assert new_comment.user.id == test_user["id"]

# Authorized user can delete a comment


def test_delete_comment_success(authorized_client, test_user, test_posts, test_comment):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}/comments/{test_comment.id}/")
    assert res.status_code == 204

# Authorized user can get all comments for a specific post


def test_get_post_comments(authorized_client, test_user, test_posts, test_comment):
    res = authorized_client.get(
        f"/posts/{test_posts[3].id}/comments/")
    assert res.status_code == 200


# Authorized user receives 200 status code for post with no comments
def test_get_all_comments(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}/comments/")
    assert res.status_code == 200
    assert res.json().get("detail") == "No comments found for the specified post id."

# Authorized user can't delete a comment that doesn't exist


def test_delete_comments_no_post(authorized_client, test_posts, test_comment):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}/comments/000000/")
    assert res.status_code == 404
    assert res.json().get("detail") == "Comment does not exist."


# Authorized user can't delete a comment that is not theirs
def test_delete_other_user_comment(second_authorized_client, test_user, test_second_user, test_comment, test_posts):
    res = second_authorized_client.delete(
        f"/posts/{test_posts[3].id}/comments/{test_comment.id}/")
    assert res.status_code == 403
    assert res.json().get("detail") == "You are not authorized to perform this action."


# Unathorized user can't delete any comment
def test_delete_comment_unathorized(client, test_user, test_comment, test_posts):
    res = client.delete(
        f"/posts/{test_posts[3].id}/comments/{test_comment.id}/")
    assert res.status_code == 401

# Unauthorized user can't comment on any post


def test_authorized_comment(client, test_user, test_posts):
    res = client.post(f"/posts/{test_posts[3].id}/comments/",
                      json={"content": "this comment won't post"})
    assert res.status_code == 401
