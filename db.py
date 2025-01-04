import json
import random
from json import JSONDecodeError

import sqlalchemy as s

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select

from conf import DB_USER, DB_PASSWORD, HOSTNAME, PORT, DB_NAME
from models.student import Student, Base

TABLE_NAME = "students"

DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=HOSTNAME,
    port=PORT,
    database=DB_NAME,
)

engine = create_engine(DATABASE_URL)

class DataBaseManager:
    @staticmethod
    def table_exists(table_name):
        return s.inspect(engine).has_table(table_name)

    @staticmethod
    def fetch_all_students():
        with Session(engine) as session:
            stmd = select(Student)
            results = session.execute(stmd).scalars().all()
            return results

    @staticmethod
    def student_exists(student_id, student_number):
        with Session(engine) as session:
            stmt = select(Student).where(Student.id == student_id and Student.student_number == student_number)
            results = session.execute(stmt).scalars().first()
            return results is not None

    @staticmethod
    def add_students_from_file(file_name):
        try:
            with open(file_name, "r") as f:
                students = json.load(f)

            with Session(engine) as session:
                for student in students:
                    new_student = Student(
                        name=student["name"],
                        address=student["address"],
                        age=student["age"],
                        student_number=student["student_number"],
                    )

                    try:
                        session.add(new_student)
                        session.commit()
                        print(f'Student with student number {new_student.student_number} added successfully.')
                    except IntegrityError:
                        session.rollback()
                        print(f"Student {new_student.name} with student_number {new_student.student_number} already exists.")

                    except SQLAlchemyError as e:
                        session.rollback()
                        print(f"Database error occurred: {e}")
        except json.JSONDecodeError:
            print("Failed to decode JSON file.")
        except FileNotFoundError:
            print("The provided file path does not exist.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


    @staticmethod
    def update_student(student_id, data):
        try:
            with Session(engine) as session:
                stmt = select(Student).where(Student.id == student_id)
                results = session.execute(stmt).scalars().first()

                if results is None:
                    print(f'Student {student_id} does not exist')
                    return

                results.name = data['name']
                results.address = data['address']
                results.age = data['age']
                results.student_number = data['student_number']
                session.commit()
                print(f'Student {student_id} updated')


        except SQLAlchemyError as e:
            print(f"An error occurred while updating user data: {e}")

    @staticmethod
    def delete_student(student_id):
        try:
            with Session(engine) as session:
                stmt = select(Student).where(Student.id == student_id)
                result = session.execute(stmt).scalars().first()
                if result is not None:
                    session.delete(result)
                    session.commit()
                    print(f"Student with ID {student_id} successfully deleted.")
                else:
                    print(f"Student with ID {student_id} does not exist.")
        except SQLAlchemyError  as e:
            print(f"an error occurred while deleting student. {e}")

    @staticmethod
    def add_student(parameters):

        student_id = random.randint(100000, 999999) # generate random unique ID for each entry

        with Session(engine) as session:
            new_student = Student(id=student_id, name=parameters[0], address=parameters[1], age=parameters[2], student_number=parameters[3])

            if DataBaseManager.student_exists(new_student.id, new_student.student_number):
                print(f"Student {new_student.name} already exists.")

            else:
                session.add(new_student)
                session.commit()
                print(f"Table {TABLE_NAME} created.")
                print(f"Student {new_student.name} inserted successfully.")

if DataBaseManager.table_exists("students"):
    print(f"Table {TABLE_NAME} already exists.")
else:
    Base.metadata.create_all(bind=engine)
