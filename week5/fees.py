from enum import Enum

RATE_PER_HOUR = 350
STAFF_CHILD_FACTOR = 0.5
HIGH_FEE_THRESHOLD = 6000
HIGH_FEE_REDUCTION = 200
SUMMER_SURCHARGE = 150


class StudentType(Enum):
    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


def tuition_fee(courses, student_type, summer, discount, extras=[]):
    total = 0
    for course in courses:
        if student_type == StudentType.REGULAR:
            total = total + course["h"] * RATE_PER_HOUR
        elif student_type == StudentType.STAFF_CHILD:
            total = total + course["h"] * RATE_PER_HOUR * STAFF_CHILD_FACTOR
        elif student_type == StudentType.SCHOLARSHIP:
            total = total + 0
    if total > HIGH_FEE_THRESHOLD:
        total = total - HIGH_FEE_REDUCTION
    if summer == True:
        total = total + SUMMER_SURCHARGE
    if discount != None:
        total = total - discount
    for extra in extras:
        total = total + extra
    return total


def report(courses, student_type, summer, discount):
    fee = tuition_fee(courses, student_type, summer, discount)
    if student_type == StudentType.REGULAR:
        print("Student fee: " + str(fee))
    elif student_type == StudentType.STAFF_CHILD:
        print("Staff child fee: " + str(fee))
    if fee > HIGH_FEE_THRESHOLD:
        print("High fee")
    return fee


def process_all(students):
    for student in students:
        if student["type"] == 1:
            fee = tuition_fee(
                student["courses"], StudentType.REGULAR, student["summer"], None
            )
        if student["type"] == 2:
            fee = tuition_fee(
                student["courses"], StudentType.STAFF_CHILD, student["summer"], None
            )
        print(student["name"], fee)
