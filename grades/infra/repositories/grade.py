from abc import ABC, abstractmethod
import uuid

import psycopg
import psycopg.rows

from grades.domain.enitites.grade import Grade


class GradeRepository(ABC):
    @abstractmethod
    def list(self, limit: int = 20, offset: int = 0): ...

    @abstractmethod
    def list_by_student(
        self, student_id: uuid.UUID, limit: int = 20, offset: int = 0
    ): ...

    @abstractmethod
    def save(self, grade: Grade): ...


class GradeRepositoryDatabase(GradeRepository):
    def __init__(self):
        self.connection = psycopg.connect(
            "postgresql://admin:password@localhost:5432/grades"
        )

    def __del__(self):
        self.connection.close()

    def list(self, limit=20, offset=0):
        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute("select * from grades limit %s offset %s", [limit, offset])
            result = cursor.fetchall()
            print(result)

        return [Grade(**row) for row in result]

    def list_by_student(self, student_id, limit=20, offset=0):
        with self.connection.cursor(row_factory=psycopg.rows.dict_row) as cursor:
            cursor.execute(
                "select * from grades where student_id=%s limit %s offset %s",
                [student_id, limit, offset],
            )
            result = cursor.fetchall()

        return [Grade(**row) for row in result]

    def save(self, grade):
        return super().save(grade)
