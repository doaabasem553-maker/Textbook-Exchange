"""Tuition fee calculation for the Student Services App."""

from dataclasses import dataclass
from enum import Enum

RATE_PER_HOUR = 350
HIGH_FEE_THRESHOLD = 6000
HIGH_FEE_REDUCTION = 200
SUMMER_SURCHARGE = 150


@dataclass(frozen=True)
class Course:
    """A course the student is enrolled in, measured in credit hours."""

    hours: int


class StudentType(Enum):
    """Kinds of student, each with its own share of the hourly rate."""

    REGULAR = 1
    STAFF_CHILD = 2
    SCHOLARSHIP = 3


# share of the full hourly rate that each type of student pays
RATE_FACTOR = {
    StudentType.REGULAR: 1,
    StudentType.STAFF_CHILD: 0.5,
    StudentType.SCHOLARSHIP: 0,
}


def tuition_fee(courses, student_type, summer=False, discount=0, extras=()):
    """Return the total fee for one student."""
    factor = RATE_FACTOR[student_type]
    total = 0
    for course in courses:
        total = total + course.hours * RATE_PER_HOUR * factor
    if total > HIGH_FEE_THRESHOLD:
        total = total - HIGH_FEE_REDUCTION
    if summer:
        total = total + SUMMER_SURCHARGE
    total = total - discount
    for extra in extras:
        total = total + extra
    return total


def report(courses, student_type, summer=False, discount=0):
    """Return the fee report as text; printing is left to the caller."""
    fee = tuition_fee(courses, student_type, summer, discount)
    lines = []
    if student_type == StudentType.REGULAR:
        lines.append(f"Student fee: {fee}")
    elif student_type == StudentType.STAFF_CHILD:
        lines.append(f"Staff child fee: {fee}")
    if fee > HIGH_FEE_THRESHOLD:
        lines.append("High fee")
    return "\n".join(lines)


def process_all(students):
    """Return {name: fee} for every student, scholarship students included."""
    fees = {}
    for student in students:
        student_type = StudentType(student["type"])
        fees[student["name"]] = tuition_fee(
            student["courses"], student_type, student["summer"]
        )
    return fees
