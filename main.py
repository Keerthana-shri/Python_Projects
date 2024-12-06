import re
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, ValidationError
from enum import Enum
from logic import Logic
import csv
import io
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
logic = Logic()
security = HTTPBasic()

VALID_USERNAME = os.getenv("VALID_USERNAME")
VALID_PASSWORD = os.getenv("VALID_PASSWORD")

def login_and_authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username == "" and credentials.password == "":
        raise HTTPException(status_code=401, detail="Username and password are missing")
    elif credentials.username == "":
        raise HTTPException(status_code=401, detail="Username is missing")
    elif credentials.password == "":
        raise HTTPException(status_code=401, detail="Password is missing")
    elif credentials.username != VALID_USERNAME or credentials.password != VALID_PASSWORD:
        raise HTTPException(
            status_code=401, 
            detail="Your login credentials are not right, try again with right one"
        )
    else:
        return {"message": "Login successful"}

class Grade(str, Enum):
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"

class EmployeeModel(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str  # Expecting MM/DD/YYYY format
    date_of_joining: str  # Expecting MM/DD/YYYY format
    grade: str

class UpdateEmployeeModel(BaseModel):
    first_name: str = None
    last_name: str = None
    date_of_birth: str = None  # Expecting MM/DD/YYYY format
    date_of_joining: str = None  # Expecting MM/DD/YYYY format
    grade: str = None

def validate_name(name):
    if re.match("^[A-Za-z]+$", name):
        return True
    else:
        return False

def validate_date_format(date_str):
    try:
        datetime.strptime(date_str, '%m/%d/%Y')
        return True
    except ValueError:
        return False

'''Login using credentials'''
@app.post("/login", dependencies=[Depends(login_and_authenticate)])
def login():
    return {"message": "Login successful"}

'''Add a new employee to the database'''
@app.post("/employees", dependencies=[Depends(login_and_authenticate)])
def create_employee(employee: EmployeeModel):
    errors = []

    if validate_date_format(employee.date_of_birth):
        pass
    else:
        errors.append(
            {"date_of_birth": "The provided date format is invalid. It should be in MM/DD/YYYY format."}
        )

    if validate_date_format(employee.date_of_joining):
        pass
    else:
        errors.append(
            {"date_of_joining": "The provided date format is invalid. It should be in MM/DD/YYYY format."}
        )

    if employee.grade in Grade.__members__:
        pass
    else:
        errors.append(
            {"grade": "The provided grade is invalid. It should be 'M1', 'M2', or 'M3'."}
        )

    if validate_name(employee.first_name):
        pass
    else:
        errors.append({"first_name": "The name you entered is invalid."})

    if validate_name(employee.last_name):
        pass
    else:
        errors.append({"last_name": "The name you entered is invalid."})

    '''Checking if the employee exists by first name, last name, and date of birth to avoid duplicates'''
    if len(errors) == 0:
        existing_emp = logic.get_employee_by_details(
            employee.first_name, 
            employee.last_name, 
            employee.date_of_birth
        )
        if existing_emp:
            errors.append(
                {"employee": f"Employee details of {employee.first_name}" 
                 f" {employee.last_name} are already available."}
            )

    if len(errors) > 0:
        raise HTTPException(status_code=422, detail=errors)

    try:
        emp = logic.create_employee(
            first_name=employee.first_name,
            last_name=employee.last_name,
            date_of_birth=employee.date_of_birth,
            date_of_joining=employee.date_of_joining,
            grade=employee.grade
        )
        if emp:
            return {
                "message": (
                    f"Employee details of {emp.first_name} {emp.last_name} have been added successfully."
                )
            }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail="The provided grade is invalid")

'''Search the details of an employee with first_name and last_name'''
@app.get("/search", dependencies=[Depends(login_and_authenticate)])
def search_employees(first_name: str, last_name: str):
    employees = logic.search_employees(first_name, last_name)
    if employees:
        return [
            {
                "id": emp.id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "date_of_birth": emp.date_of_birth,
                "date_of_joining": emp.date_of_joining,
                "grade": emp.grade
            }
            for emp in employees
        ]
    else:
        raise HTTPException(status_code=404, detail="No employees found matching the criteria")

'''Get the details of an employee using the ID'''
@app.get("/employees/{emp_id}", dependencies=[Depends(login_and_authenticate)])
def get_employee(emp_id: int):
    emp = logic.get_employee(emp_id)
    if emp:
        return {
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "date_of_birth": emp.date_of_birth,
            "date_of_joining": emp.date_of_joining,
            "grade": emp.grade
        }
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

'''Get the details of all the employees'''
@app.get("/employees", dependencies=[Depends(login_and_authenticate)])
def get_all_employees():
    employees = logic.get_all_employees()
    return [
        {
            "id": emp.id,
            "first_name": emp.first_name,
            "last_name": emp.last_name,
            "date_of_birth": emp.date_of_birth,
            "date_of_joining": emp.date_of_joining,
            "grade": emp.grade
        }
        for emp in employees
    ]

'''Update the details of an employee using ID'''
@app.put("/employees/{emp_id}", dependencies=[Depends(login_and_authenticate)])
def update_employee(emp_id: int, updates: UpdateEmployeeModel):
    '''Check if the employee exists by id before validating the updates'''
    existing_emp = logic.get_employee(emp_id)
    
    if existing_emp:
        errors = []

        if updates.date_of_birth:
            if validate_date_format(updates.date_of_birth):
                pass
            else:
                errors.append(
                    {"date_of_birth": "The provided date format is invalid. It should be in MM/DD/YYYY format."}
                )
        else:
            pass

        if updates.date_of_joining:
            if validate_date_format(updates.date_of_joining):
                pass
            else:
                errors.append(
                    {"date_of_joining": "The provided date format is invalid. It should be in MM/DD/YYYY format."}
                )
        else:
            pass

        if updates.first_name:
            if validate_name(updates.first_name):
                pass
            else:
                errors.append({"first_name": "The name you entered is invalid."})
        else:
            pass

        if updates.last_name:
            if validate_name(updates.last_name):
                pass
            else:
                errors.append({"last_name": "The name you entered is invalid."})
        else:
            pass

        if updates.grade:
            if updates.grade in Grade.__members__:
                pass
            else:
                errors.append(
                    {"grade": "The entered grade is invalid. It should be 'M1', 'M2', or 'M3'."}
                )
        else:
            pass

        if errors:
            raise HTTPException(status_code=422, detail=errors)

        '''If no validation errors, proceed with the update'''
        try:
            emp = logic.update_employee(emp_id, updates.model_dump(exclude_unset=True))
            return {
                "message": (
                    f"Employee details of {emp.first_name} {emp.last_name} have been updated successfully."
                )
            }
        except ValidationError as e:
            raise HTTPException(status_code=422, detail="The entered grade is invalid")
    else:
        raise HTTPException(status_code=404, detail="Employee not found")

'''Upload bulk employee details using csv file'''
@app.post("/upload-csv", dependencies=[Depends(login_and_authenticate)])
def upload_csv(file: UploadFile = File(...)):
    content = file.file.read().decode("utf-8")
    print(content)
    logic.upload_csv(content)
    return {"message": "CSV file uploaded successfully"}

