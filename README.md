GUI Student Manager Documentation
Project Overview

The GUI Student Manager is a desktop application built using PyQt6 and SQLAlchemy. It is designed to allow users to manage student records through a graphical user interface (GUI). The application provides functionality for adding, updating, deleting, and viewing student details such as name, address, age, and student number. The backend utilizes SQLite (or another database, depending on your setup) to store student information persistently.

Features

    Add Student
    Users can add new student records to the database by entering their name, address, age, and student number.

    Edit Student
    Users can select a student record from the list and edit their details. The updated information is reflected in the database upon saving.

    Delete Student
    Users can delete student records from the database, ensuring that all associated data is permanently removed.

    Add Students from JSON File
    Users can upload a JSON file containing student records to add multiple students to the database at once. This is a convenient way to bulk-import student data.

    ![ezgif-5-a66b68c99e](https://github.com/user-attachments/assets/19e68c38-ddd0-4d05-8cec-179e1e8b6781)

Installation

    git clone https://github.com/yourusername/student-manager.git
    Make sure u have PostgreSQL installed active and running
    Install the necessary dependancies such as tkinter, sqlalchemy
    Provide the necessary database connection information in the conf.py file
    To convert to exe simply run :
    -  python -m PyInstaller --name student-manager --onefile --windowed --icon=./images/database-management.ico --add-data './images;images' gui.py
      
