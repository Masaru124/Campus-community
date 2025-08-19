from typing import List, Dict

GRADE_POINTS = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6, "C": 5, "P": 4, "F": 0
}

def calculate_gpa(courses: List[Dict]) -> float:
    # courses: [{ 'credits': 4, 'grade': 'A' }, ...]
    total_credits = 0.0
    total_points = 0.0
    for c in courses:
        credits = float(c.get("credits", 0))
        grade = str(c.get("grade", "F")).upper().strip()
        gp = GRADE_POINTS.get(grade, 0)
        total_credits += credits
        total_points += gp * credits
    return round(total_points / total_credits, 2) if total_credits else 0.0

def generate_timetable(subjects: List[str]):
    # naive spread across weekdays 5x6 grid
    days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
    slots = 6
    timetable = {d: [None]*slots for d in days}
    i = 0
    for s in subjects:
        d = days[i % len(days)]
        slot = (i // len(days)) % slots
        timetable[d][slot] = s
        i += 1
    return timetable
