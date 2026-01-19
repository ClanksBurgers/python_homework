#Task 3

import csv

employees = []

with open("../csv/employees.csv", newline="") as f:
    reader = csv.reader(f)
    for row in reader:
        employees.append(row)

names = [f"{row[0]} {row[1]}" for row in employees[1:]]
print("All Employee names:")
print(names)

names_with_e = [name for name in names if "e" in name.lower()]
print("\nEmployee names with 'e':")
print(names_with_e)
