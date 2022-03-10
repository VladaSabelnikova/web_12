from requests import get, post, delete


def test_user_get_correct():
    correct = {
        "user": {
            "address": "module_3",
            "age": 77,
            "email": "ruzin@mars.org",
            "hashed_password": "pass_1",
            "name": "Ivan",
            "position": "colonist",
            "speciality": "research engineer",
            "surname": "Ruzin"
        }
    }
    variant = get('http://localhost:8080/api/v2/users/3').json()

    assert correct == variant


def test_user_get_invalid_type_id():
    correct = {
        "error": "404 Not Found: "
                 "The requested URL was not found on the server."
                 " If you entered the URL manually "
                 "please check your spelling and try again."
    }
    variant = get('http://localhost:8080/api/v2/users/not_gut').json()

    assert correct == variant


def test_user_add_correct():
    correct = {'info': ' successfully'}

    variant = post(
        'http://localhost:8080/api/v2/users',
        json={
            'surname': 'Ivanov',
            'name': 'Ivan',
            'age': 14,
            'position': 'text',
            'speciality': 'text',
            'address': 'text',
            'email': 'ivanov@ivan.com',
            'password': '123hhh'
        }
    ).json()
    print(variant)

    assert correct == variant


def test_user_delete_correct():
    correct = {'info': ' successfully'}

    variant = delete('http://localhost:8080/api/v2/users/9').json()

    assert correct == variant
