MIN_SCORE = 0
MAX_SCORE = 100

# (minimum score, letter) from the highest grade to the lowest
GRADE_BOUNDARIES = (
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
)
FAILING_GRADE = "F"


def letter_grade(score):
    if not MIN_SCORE <= score <= MAX_SCORE:
        raise ValueError(f"score must be between {MIN_SCORE} and {MAX_SCORE}")
    for minimum, letter in GRADE_BOUNDARIES:
        if score >= minimum:
            return letter
    return FAILING_GRADE
