from app import schemas
import pytest


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200


def test_get_all_posts_unauthorized(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_one_post_unauthorized(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_no_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/55555555")
    assert res.status_code == 404


def test_get_one_post_authorized(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostWrapper(**res.json())
    assert post.post.id == test_posts[0].id
    assert post.post.title == test_posts[0].title
    assert post.post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("hello world!", "this is the first post", True),
    ("Lorem ipsum", "dolor sit amet", False),
    ("Recipe for peanut butter brownies", "1.) Preheat oven to 350 degrees", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner.id == test_user["id"]


def test_create_post_default_published(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "It was the best of times...", "content": "it was the worst of times."})
    created_post = schemas.Post(**res.json())
    assert created_post.title == "It was the best of times..."
    assert created_post.content == "it was the worst of times."
    assert created_post.published == True
    assert created_post.owner.id == test_user["id"]


def test_create_post_unauthorized(client, test_posts):
    res = client.post(
        "/posts/", json={"title": "Not logged in", "content": "Unauthorized content!"})
    assert res.status_code == 401


def test_delete_post_unathorized(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_no_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/00000000000")
    assert res.status_code == 404
    assert res.json().get("detail") == "post not found!"


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403
    assert res.json().get("detail") == "You are not authorized to perform this action."


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "UPDATED title",
        "content": "UPDATED content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]


def test_update_other_user_post(authorized_client, test_user, test_second_user, test_posts):
    data = {
        "title": "UPDATED title",
        "content": "UPDATED content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_update_other_user_post(authorized_client, test_user, test_second_user, test_posts):
    data = {
        "title": "UPDATED title",
        "content": "UPDATED content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_update_post_unathorized(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_update_no_post(authorized_client, test_user, test_posts):
    data = {
        "title": "null",
        "content": "null",
        "id": "null"
    }
    res = authorized_client.put(f"/posts/00000000", json=data)
    assert res.status_code == 404
