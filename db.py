from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import csv
from io import StringIO
from datetime import datetime

DATABASE_URL = "sqlite:///./employee_with_auth.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    date_of_joining = Column(Date, nullable=False)
    grade = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

class Database:
    def __init__(self):
        self.Session = SessionLocal

    def create_employee(self, employee):
        session = self.Session()
        existing_employee = session.query(Employee).filter(
            Employee.first_name == employee.first_name,
            Employee.last_name == employee.last_name,
            Employee.date_of_birth == employee.date_of_birth
        ).first()
        if existing_employee:
            session.close()
            return None  # Employee already exists
        session.add(employee)
        session.commit()
        session.refresh(employee)
        session.close()
        return employee
    
    def search_employees(self, first_name, last_name):
        session = self.Session()
        employees = session.query(Employee).filter(
            Employee.first_name == first_name,
            Employee.last_name == last_name
        ).all()
        session.close()
        return employees  

    def get_employee(self, emp_id):
        session = self.Session()
        employee = session.query(Employee).filter(Employee.id == emp_id).first()
        session.close()
        return employee

    def get_employee_by_details(self, first_name, last_name, date_of_birth):
        session = self.Session()
        employee = session.query(Employee).filter(
            Employee.first_name == first_name,
            Employee.last_name == last_name,
            Employee.date_of_birth == date_of_birth
        ).first()
        session.close()
        return employee

    def get_all_employees(self):
        session = self.Session()
        employees = session.query(Employee).all()
        session.close()
        return employees

    def update_employee(self, emp_id, updates):
        session = self.Session()
        employee = session.query(Employee).filter(Employee.id == emp_id).first()
        if employee:
            for key, value in updates.items():
                setattr(employee, key, value)
            session.commit()
            session.refresh(employee)
        session.close()
        return employee

    def upload_csv(self, csv_content):
        session = self.Session()
        csv_file = StringIO(csv_content)
        reader = csv.DictReader(csv_file)
        for row in reader:
            date_of_birth = datetime.strptime(row['date_of_birth'], '%m/%d/%Y').date()
            date_of_joining = datetime.strptime(row['date_of_joining'], '%m/%d/%Y').date()
            existing_employee = session.query(Employee).filter(
                Employee.first_name == row['first_name'],
                Employee.last_name == row['last_name'],
                Employee.date_of_birth == date_of_birth
            ).first()
            if not existing_employee:
                employee = Employee(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    date_of_birth=date_of_birth,
                    date_of_joining=date_of_joining,
                    grade=row['grade']
                )
                session.add(employee)
        session.commit()
        session.close()

