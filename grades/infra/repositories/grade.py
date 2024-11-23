from abc import ABC, abstractmethod
from typing import List, Optional
import uuid

import psycopg
import psycopg.rows

from grades.domain.enitites.grade import Grade
from grades.environment import DATABASE_URL


class GradeRepository(ABC):
    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def get(self, grade_id: int) -> Grade: ...

    @abstractmethod
    def list(self, limit: int = 20, offset: int = 0) -> List[Grade]: ...

    @abstractmethod
    def list_by_student(
        self, student_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> List[Grade]: ...

    @abstractmethod
    def save(self, grade: Grade): ...

    @abstractmethod
    def delete(self, grade: Grade): ...


class GradeRepositoryError(Exception): ...


class GradeRepositoryCursor:
    def __init__(
        self, connection: psycopg.Connection, schema: Optional[str] = None, **kwargs
    ):
        self.cursor = connection.cursor(**kwargs)
        if schema:
            self.cursor.execute(f"set search_path to {schema};".encode())

    def __enter__(self):
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()


class GradeRepositoryPostgres(GradeRepository):
    def __init__(self):
        self.connection = psycopg.connect(DATABASE_URL)

    def __del__(self):
        self.connection.close()

    def __create(self, grade: Grade) -> None:
        query = "insert into grades (student_id, exam, value) values (%s, %s, %s) RETURNING id"

        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(query, [grade.student_id, grade.exam, grade.value])
            if not (result := cursor.fetchone()):
                raise GradeRepositoryError("Error on create grade")
            grade.id = result["id"]

    def __update(self, grade: Grade) -> None:
        query = "update grades set student_id=%s, exam=%s, value=%s where id=%s"

        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(query, [grade.student_id, grade.exam, grade.value, grade.id])
            if not cursor.rowcount:
                raise GradeRepositoryError("Error on update grade")

    def count(self):
        with self.connection.cursor() as cursor:
            cursor.execute("select count(*) from grades")
            if not (result := cursor.fetchone()):
                raise GradeRepositoryError("Error on count grades")
            return result[0]

    def get(self, grade_id: int) -> Grade:
        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute("select * from grades where id=%s", [grade_id])
            if not (result := cursor.fetchone()):
                raise GradeRepositoryError("Error on get grade")

            result["student_id"] = uuid.UUID(result["student_id"])
            return Grade(**result)

    def list(self, limit=20, offset=0):
        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute("select * from grades limit %s offset %s", [limit, offset])
            result = cursor.fetchall()

        return [Grade(**row) for row in result]

    def list_by_student(self, student_id, limit=20, offset=0):
        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(
                "select * from grades where student_id=%s limit %s offset %s",
                [str(student_id), limit, offset],
            )
            result = cursor.fetchall()

        return [Grade(**row) for row in result]

    def save(self, grade) -> None:
        if grade.id:
            self.__update(grade)
        self.__create(grade)

    def delete(self, grade) -> None:
        query = "delete from grades where id=%s"

        with self.connection.cursor() as cursor:
            cursor.execute(query, [grade.id])
            if not cursor.rowcount:
                raise GradeRepositoryError("Error on delete grade")
