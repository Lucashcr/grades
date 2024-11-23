import uuid
import pytest
import psycopg

from grades.domain.enitites.grade import Grade
from grades.environment import TEST_DATABASE_URL
from grades.infra.repositories.grade import GradeRepositoryPostgres


@pytest.fixture(scope="session", autouse=True)
def db_connection():
    with psycopg.connect(TEST_DATABASE_URL, autocommit=True) as db_connection:
        with db_connection.cursor() as cursor:
            with open("tests/fixtures/grades/create.sql", "rb") as f:
                query = f.read()
            cursor.execute(query)

        yield db_connection

        with db_connection.cursor() as cursor:
            with open("tests/fixtures/grades/drop.sql", "rb") as f:
                query = f.read()
            cursor.execute(query)


@pytest.fixture
def populate_grades(db_connection):
    with db_connection.cursor() as cursor:
        with open("tests/fixtures/grades/populate.sql", "rb") as f:
            query = f.read()
        cursor.execute(query)

    yield

    with db_connection.cursor() as cursor:
        with open("tests/fixtures/grades/clean.sql", "rb") as f:
            query = f.read()
        cursor.execute(query)


@pytest.fixture
def repository():
    repository = GradeRepositoryPostgres()
    repository.connection.close()
    repository.connection = psycopg.connect(TEST_DATABASE_URL)

    yield repository

    repository.connection.rollback()


@pytest.mark.database
def test_success_create_grade(repository):
    grade = Grade(
        id=None,
        student_id=uuid.uuid4(),
        exam="P1",
        value=10,
    )

    repository.save(grade)
    assert grade.id is not None


@pytest.mark.database
def test_success_count_empty_grades(repository):
    grades_count = repository.count()
    assert grades_count == 0


@pytest.mark.database
def test_success_count_populated_grades(repository, populate_grades):
    grades_count = repository.count()
    assert grades_count == 12


@pytest.mark.database
def test_success_get_grade(repository):
    grade = Grade(
        id=None,
        student_id=uuid.UUID("157c49a8-957a-4b0c-996a-5819833307a3"),
        exam="P1",
        value=9.6,
    )

    repository.save(grade)

    retrieved_grade = repository.get(grade.id)
    assert grade is not retrieved_grade
    assert grade == retrieved_grade


@pytest.mark.database
def test_success_list_empty_grades(repository):
    grades = repository.list()
    assert len(grades) == 0


@pytest.mark.database
def test_success_list_populated_grades(repository, populate_grades):
    grades = repository.list()
    assert len(grades) == 12


@pytest.mark.database
def test_success_list_by_student_empty_grades(repository):
    student_id = uuid.UUID("157c49a8-957a-4b0c-996a-5819833307a3")
    grades = repository.list_by_student(student_id)
    assert len(grades) == 0


@pytest.mark.database
def test_success_list_by_student_populated_grades(repository, populate_grades):
    student_id = uuid.UUID("157c49a8-957a-4b0c-996a-5819833307a3")
    grades = repository.list_by_student(student_id)
    assert len(grades) == 4
