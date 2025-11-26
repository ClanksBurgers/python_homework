#assignment 2
import csv
import sys
import os
import custom_module
from datetime import datetime

#Task2
def read_employees():
    employees_dict = {}
    rows = []

    try:
        with open("../csv/employees.csv", "r", newline="") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                if i == 0:
                    employees_dict["fields"] = row
                else:
                    rows.append(row)

        employees_dict["rows"] = rows
        return employees_dict

    except Exception as e:
        print("Error reading employees.csv:", e)
        sys.exit(1)   

employees = read_employees()
print(employees)

#Task3
def column_index(column_name):
    return employees["fields"].index(column_name)
employee_id_column = column_index("employee_id")

#Task4
def first_name(row_number):
    first_name_column = column_index("first_name")
    row = employees["rows"][row_number]
    return row[first_name_column]

#Task5
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id
    
    matches = list(filter(employee_match, employees["rows"]))
    return matches

#Task6
def employee_find_2(employee_id):
    matches = list(
        filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"])
    )
    return matches

#Task7
def sort_by_last_name():
    lastName_column = column_index("last_name")
    employees["rows"].sort(key=lambda row: row[lastName_column])
    return employees["rows"]
print(sort_by_last_name())
print(employees)

#Task8
def employee_dict(row):
    emp_dict = {}
    fields = employees["fields"]
    for i, field in enumerate(fields):
        if i == employee_id_column:
            continue
        emp_dict[field] = row[i]
    return emp_dict

print(employee_dict(employees["rows"][0]))

#Task9
def all_employees_dict():
    result = {}

    for row in employees["rows"]:
        emp_id = row[employee_id_column]
        result[emp_id] = employee_dict(row)
    return result

print(all_employees_dict())

#Task10
def get_this_value():
    return os.getenv("THISVALUE")

#Task11
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret("my_new_secret")
print(custom_module.secret)

#Task12
def read_minutes():
    minutes1 = {"fields": [], "rows": []}
    minutes2 = {"fields": [], "rows": []}

    try:
        with open("../csv/minutes1.csv", "r", newline="") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                if i == 0:
                    minutes1["fields"] = row
                else:
                    minutes1["rows"].append(tuple(row))
    except Exception as e:
        print("Error reading minutes1.csv:", e)
        sys.exit(1)

    try:
        with open("../csv/minutes2.csv", "r", newline="") as f:
            reader = csv.reader(f)
            
            for i, row in enumerate(reader):
                if i == 0:
                    minutes2["fields"] = row
                else:
                    minutes2["rows"].append(tuple(row))
    except Exception as e:
        print("Error reading minutes2.csv:", e)
        sys.exit(1)
    
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()
print("Minutes1:", minutes1)
print("Minutes2:", minutes2)

#Task13
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    combined_set = set1.union(set2)
    return combined_set
minutes_set = create_minutes_set()
print("Combined Minutes Set:", minutes_set)

#Task14
def create_minutes_list():
    minutes = list(minutes_set)
    minutes_with_datetime = list(
        map(
            lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),
            minutes
        )
    )
    return minutes_with_datetime
minutes_list = create_minutes_list()
print("Minutes List with Datetime:", minutes_list)

#Task15
def write_sorted_list():
    sorted_minutes = sorted(minutes_list, key=lambda x: x[1])
    
    converted_list = list(
        map(
            lambda x: (x[0], x[1].strftime("%B %d, %Y")),
            sorted_minutes
        )
    )

    try:
        with open("./minutes.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(minutes1["fields"])
            
            for row in converted_list:
                writer.writerow(row)
    except Exception as e:
        print("Error writing minutes.csv:", e)
        sys.exit(1)
    
    return converted_list

sorted_minutes_list = write_sorted_list()
print("Sorted Minutes List Written to File:", sorted_minutes_list)
