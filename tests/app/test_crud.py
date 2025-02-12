import pytest


@pytest.mark.parametrize(
    "username, email, expected_status, expected_response",
    [
        (
            "user4",
            "user4@example.com",
            200,
            {"username": "user4", "email": "user4@example.com"},
        ),
        (
            "newuser",
            "newuser@example.com",
            200,
            {"username": "newuser", "email": "newuser@example.com"},
        ),
    ],
)
def test_create_user(client, username, email, expected_status, expected_response):
    response = client.post("/users/", json={"username": username, "email": email})

    assert response.status_code == expected_status
    assert expected_response.items() <= response.json().items()


@pytest.mark.parametrize(
    "username, email, expected_status, expected_response",
    [
        (
            "user1",
            "newemail@example.com",
            400,
            {"detail": "Username user1 is already taken."},
        ),
        (
            "newuser",
            "user1@example.com",
            400,
            {"detail": "Email user1@example.com is already in use."},
        ),
        (
            "user1",
            "user1@example.com",
            400,
            {"detail": "Username user1 and email user1@example.com are already taken."},
        ),
    ],
)
def test_create_duplicate_user(
    client, username, email, expected_status, expected_response
):
    response = client.post("/users/", json={"username": username, "email": email})

    assert response.status_code == expected_status
    assert expected_response.items() <= response.json().items()


def test_get_user(client):
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["username"] == "user1"
    assert response.json()["email"] == "user1@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert "User with ID 999 not found." in response.json()["detail"]


def test_list_users(client):
    response = client.get("/users/")

    assert response.status_code == 200
    users = response.json()
    assert len(users) == 3


def test_delete_user(client):
    response = client.delete("/users/1")

    assert response.status_code == 200
    assert "User deleted successfully" in response.json()["message"]

    response = client.get("/users/1")
    assert response.status_code == 404


def test_delete_user_not_found(client):
    response = client.delete("/users/999")

    assert response.status_code == 404
    assert "User with ID 999 not found." in response.json()["detail"]
