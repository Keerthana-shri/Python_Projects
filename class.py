class Employee:
    def __init__(self, id, first_name, last_name, date_of_birth, date_of_joining, grade):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.date_of_joining = date_of_joining
        self.grade = grade

    def __str__(self):
        return (
            f"Employee ID: {self.id}, "
            f"Name: {self.first_name} {self.last_name}, "
            f"DOB: {self.date_of_birth}, "
            f"DOJ: {self.date_of_joining}, "
            f"Grade: {self.grade}"
    )
    