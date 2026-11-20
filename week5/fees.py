def tuition_fee(courses, student_type, summer, discount, extras=[]):
    # student_type: 1=student, 2=staff child, 3=scholarship
    total = 0
    for course in courses:
        if student_type == 1:
            total = total + course["h"] * 350
        elif student_type == 2:
            total = total + course["h"] * 350 * 0.5
        elif student_type == 3:
            total = total + 0
    if total > 6000:
        total = total - 200
    if summer == True:
        total = total + 150
    if discount != None:
        total = total - discount
    for extra in extras:
        total = total + extra
    return total


def report(courses, student_type, summer, discount):
    fee = tuition_fee(courses, student_type, summer, discount)
    if student_type == 1:
        print("Student fee: " + str(fee))
    elif student_type == 2:
        print("Staff child fee: " + str(fee))
    if fee > 6000:
        print("High fee")
    return fee


def process_all(students):
    for student in students:
        if student["type"] == 1:
            fee = tuition_fee(student["courses"], 1, student["summer"], None)
        if student["type"] == 2:
            fee = tuition_fee(student["courses"], 2, student["summer"], None)
        print(student["name"], fee)
