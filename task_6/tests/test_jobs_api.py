from requests import get, post, delete


def test_job_get_correct():
    correct = {
        "job": {
            "collaborators": "2, 4, 5",
            "end_date": None,
            "id": 3,
            "is_finished": False,
            "job": "deployment of residential modules 1 and 2",
            "start_date": "2022-02-28 19:06:05",
            "user": {
                "name": "Ivan",
                "surname": "Ruzin"
            },
            "work_size": 15
        }
    }
    variant = get('http://localhost:8080/api/v2/jobs/3').json()

    assert correct == variant


def test_job_get_invalid_type_id():
    correct = {
        "error": "404 Not Found: "
                 "The requested URL was not found on the server. "
                 "If you entered the URL manually "
                 "please check your spelling and try again."
    }
    variant = get('http://localhost:8080/api/v2/jobs/no_gut').json()

    assert correct == variant


def test_job_add_correct():
    correct = {
        'info': ' successfully'
    }

    variant = post(
        'http://localhost:8080/api/v2/jobs', json={
            'job': 'lalalal',
            'work_size': 1,
            'collaborators': '1, 2, 5',
            'is_finished': 0,
            'team_leader': 5
        }
    ).json()

    assert correct == variant


def test_job_delete_correct():
    correct = {
        'info': ' successfully'
    }

    variant = delete('http://localhost:8080/api/v2/jobs/17').json()

    assert correct == variant
