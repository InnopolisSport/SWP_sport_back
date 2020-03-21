import json

import requests

from app.core.config import getenv_boolean

LOCAL_URL = "http://localhost:81"


def test_fake_login_enable():
    fake_login = getenv_boolean("SWP_FAKE_LOGIN", False)
    assert fake_login is True


def test_main_page_unauthorized():
    response = requests.get(f"{LOCAL_URL}/")
    assert response.content.__contains__(b"/api/loginform")


def test_fake_auth():
    response = requests.post(f"{LOCAL_URL}/api/fake_login/setcookie",
                             data=json.dumps(
                                 {
                                     "first_name": "Ivan",
                                     "last_name": "Ivanov",
                                     "email": "i.ivanov@innopolis.university",
                                     "groups": [
                                         "Students"
                                     ],
                                     "role": "B19-02"
                                 })
                             )
    data = response.json()
    return data["access_token"]


def test_main_page_authorized():
    access_token = test_fake_auth()
    response = requests.get(f"{LOCAL_URL}/", cookies={"access_token": access_token})
    assert response.content.__contains__(b"logout-btn")

