from http import HTTPStatus

from src.app import Role, User, db


def test_get_user_true(client):
    # given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    user = User(username="john-doe", password="test", role_id=role.id)
    db.session.add(user)
    db.session.commit()
    # when
    response = client.get(f"/users/{user.id}")
    # then
    assert response.status_code == HTTPStatus.OK  # 200
    assert response.json == {
        "users": [
            {
                "id": user.id,
                "role": {
                    "id": role.id,
                    "name": role.name,
                },
                "username": user.username,
            }
        ]
    }


def test_get_user_false(client):
    # given
    role = Role(name="admin")
    db.session.add(role)
    db.session.commit()
    user_id = 1
    # when
    response = client.get(f"/users/{user_id}")
    # then
    assert response.status_code == HTTPStatus.NOT_FOUND  # 404


def test_create_user(client, access_token):
    # given
    rold_id = db.session.execute(
        db.select(Role.id).where(Role.name == "admin")
    ).scalar()
    payload = {"username": "usertest", "password": "test", "role_id": rold_id}
    # role = Role(name="admin")
    # db.session.add(role)
    # db.session.commit()
    # user = User(username="john-doe", password="test", role_id=role.id)
    # db.session.add(user)
    # db.session.commit()
    # when
    # response = client.post(
    #     "/auth/login", json={"username": user.username, "password": user.password}
    # )
    # access_token = response.json["access_token"]
    # payload = {"username": "usertest", "password": "test", "role_id": role.id}
    # when
    response = client.post(
        "/users/", json=payload, headers={"Authorization": f"Bearer {access_token}"}
    )
    # then
    assert response.status_code == HTTPStatus.CREATED  # 201
    assert response.json == {"message": "Usuário criado!"}
    assert User.query.filter_by(username="usertest").first() is not None
    assert db.session.query(User).count() == 2


def test_get_list(client, access_token):
    # given
    user = db.session.execute(
        db.select(User).where(User.username == "john-doe")
    ).scalar()
    role = db.session.execute(db.select(Role).where(Role.name == "admin")).scalar()
    # role = Role(name="admin")
    # db.session.add(role)
    # db.session.commit()
    # user = User(username="john-doe", password="test", role_id=role.id)
    # db.session.add(user)
    # db.session.commit()
    response = client.post(
        "/auth/login", json={"username": user.username, "password": user.password}
    )
    access_token = response.json["access_token"]
    # when
    response = client.get(
        "/users/", headers={"Authorization": f"Bearer {access_token}"}
    )
    # then
    assert response.status_code == HTTPStatus.OK  # 200
    assert response.json == {
        "identify": str(user.id),
        "users": [
            {
                "id": user.id,
                "username": user.username,
                "role": {
                    "id": role.id,
                    "name": role.name,
                },
            }
        ],
    }
