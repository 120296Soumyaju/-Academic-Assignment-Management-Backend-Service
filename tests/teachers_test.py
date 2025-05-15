def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1


def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'

# NEW TESTS FOR grading API ADDED BELOW

def test_teacher_grades_assignment(client, h_teacher_1):
    """Success case: Teacher successfully grades a submitted assignment"""
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={'id': 3, 'grade': 'A'}  # Assuming ID 3 is assigned to teacher 1
    )
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['data']['grade'] == 'A'
    assert json_data['data']['state'] == 'GRADED'


def test_teacher_grades_wrong_assignment(client, h_teacher_1):
    """Failure case: A teacher cannot grade another teacher's assignment"""
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={'id': 5, 'grade': 'B'}  # Assuming ID 5 belongs to another teacher
    )
    assert response.status_code == 400
    assert b'This assignment is assigned to another teacher' in response.data


'''def test_teacher_grades_draft_assignment(client, h_teacher_1):
    """Failure case: A teacher cannot grade a draft assignment"""
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={'id': 6, 'grade': 'C'}  # Assuming ID 6 is in DRAFT state
    )
    assert response.status_code == 400
    assert b'only submitted assignments can be graded' in response.data
'''

'''def test_teacher_grades_without_grade(client, h_teacher_1):
    """Failure case: A teacher cannot grade without providing a grade"""
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={'id': 4, }  # Missing 'grade' field
    )
    assert response.status_code == 400
    assert b'assignment with empty grade cannot be graded' in response.data'''