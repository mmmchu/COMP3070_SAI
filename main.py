# Import necessary libraries
from z3 import *
from pathlib import Path
from timeit import default_timer as timer
import re
import os

# Start the timer
start = timer()


# Define the Instance class and read_file function
class Instance:
    def __init__(self):
        self.number_of_students = 0
        self.number_of_exams = 0
        self.number_of_slots = 0
        self.number_of_rooms = 0
        self.room_capacities = []
        self.exams_to_students = []
        self.student_exam_capacity = []


def read_file(filename):
    def read_attribute(name):
        line = f.readline().strip()  # Strip to avoid extra spaces
        if not line:
            raise Exception(f"Empty or unexpected line encountered while parsing {name}")

        match = re.match(f'{name}:\\s*(\\d+)$', line)
        if match:
            return int(match.group(1))
        else:
            raise Exception(f"Could not parse line '{line}'; expected the {name} attribute")

    instance = Instance()
    with open(filename) as f:
        try:
            instance.number_of_students = read_attribute("Number of students")
            instance.number_of_exams = read_attribute("Number of exams")
            instance.number_of_slots = read_attribute("Number of slots")
            instance.number_of_rooms = read_attribute("Number of rooms")

            # Read room capacities
            for r in range(instance.number_of_rooms):
                instance.room_capacities.append(read_attribute(f"Room {r} capacity"))

            # Read the exam-to-student assignments
            while True:
                l = f.readline().strip()
                if not l:
                    break
                m = re.match('^\\s*(\\d+)\\s+(\\d+)\\s*$', l)
                if m:
                    instance.exams_to_students.append((int(m.group(1)), int(m.group(2))))
                else:
                    raise Exception(f'Failed to parse this line: {l}')

            # Initialize an array for the number of exams
            for r in range(instance.number_of_exams):
                instance.student_exam_capacity.append(0)

            # Count and increment the number of students in each exam
            for r in instance.exams_to_students:
                instance.student_exam_capacity[r[0]] += 1

        except Exception as e:
            print(f"Error while reading {filename}: {e}")
            raise

    return instance


def solve(instance):
    s = Solver()

    # Declarations
    exam = Int('exam')
    room = Int('room')
    ts = Int('ts')
    nex = Int('nex')
    nts = Int('nts')
    student = Int('student')

    exam1 = Int('exam1')
    exam2 = Int('exam2')

    # Range functions
    Student_Range = Function('Student_Range', IntSort(), BoolSort())
    Exam_Range = Function('Exam_Range', IntSort(), BoolSort())
    Room_Range = Function('Room_Range', IntSort(), BoolSort())
    TimeSlot_Range = Function('TimeSlot_Range', IntSort(), BoolSort())

    # Range constraints for SAT/UNSAT files
    s.add(ForAll([student], Student_Range(student) == And(student >= 0, student < instance.number_of_students)))
    s.add(ForAll([exam], Exam_Range(exam) == And(exam >= 0, exam < instance.number_of_exams)))
    s.add(ForAll([ts], TimeSlot_Range(ts) == And(ts >= 0, ts < instance.number_of_slots)))
    s.add(ForAll([room], Room_Range(room) == And(room >= 0, room < instance.number_of_rooms)))

    # Functions for assignments
    ExamRoom = Function('ExamRoom', IntSort(), IntSort())
    ExamTime = Function('ExamTime', IntSort(), IntSort())
    ExamStudent = Function('ExamStudent', IntSort(), IntSort(), BoolSort())

    # Adding students to exams
    for etos in instance.exams_to_students:
        s.add(ExamStudent(etos[0], etos[1]))

    # Constraints
    # Constraint 1: Each exam must be timetabled in exactly one room and exactly one slot.
    s.add(
        ForAll([exam],
               Implies(
                   Exam_Range(exam),
                   Exists([room, ts],
                          And(
                              Room_Range(room),
                              TimeSlot_Range(ts),
                              ExamTime(exam) == ts,
                              ExamRoom(exam) == room
                          )
                          )
               )
               )
    )

    # Constraint 2: There can be, at most, one exam timetabled in a room within a specific slot.
    s.add(
        ForAll([room, ts],
               Implies(
                   And(Room_Range(room), TimeSlot_Range(ts)),
                   ForAll([exam1, exam2],
                          Implies(
                              And(Exam_Range(exam1), Exam_Range(exam2)),
                              Implies(
                                  And(ExamRoom(exam1) == room, ExamTime(exam1) == ts,
                                      ExamRoom(exam2) == room, ExamTime(exam2) == ts),
                                  exam1 == exam2  # They must be the same exam
                              )
                          )
                          )
               )
               )
    )
    # Constraint 3
    for ex2 in range(instance.number_of_exams):
        for rm2 in range(instance.number_of_rooms):
            s.add(Implies((ExamRoom(ex2) == rm2), instance.student_exam_capacity[ex2] <= instance.room_capacities[rm2]))

    # Constraint 4
    s.add(
        ForAll(
            [student, nex, ts, nts, exam],
            Implies(
                And(
                    Student_Range(student),
                    Exam_Range(exam),
                    Exam_Range(nex),
                    TimeSlot_Range(ts),
                    TimeSlot_Range(nts),
                    Not((exam == nex))
                ),
                Implies(
                    And(
                        ExamTime(exam) == ts,
                        ExamTime(nex) == nts,
                        ExamStudent(exam, student),
                        ExamStudent(nex, student)
                    ),
                    And((ts + 1 != nts), (ts - 1 != nts), (ts != nts))
                )
            )
        )
    )

    # Check satisfiability and output results
    if s.check() == unsat:
        print('unsat')
    else:
        print('sat')
        for ex2 in range(instance.number_of_exams):
            print(" Exam:", ex2, " Room:", s.model().eval(ExamRoom(ex2)), " Slot:", s.model().eval(ExamTime(ex2)))
        print("――――――――――――――――――――――――")


# Main code execution
if __name__ == "__main__":
    tests_dir = Path("C:/Users/mabel/PycharmProjects/SAI CW 1/test instances")  # Update this path
    instances_dir = tests_dir  # Since 'test instances' is the main folder now, no need for subdirectory

    # Iterate through files in the "test instances" directory
    for test_file in instances_dir.iterdir():
        if test_file.is_file() and test_file.name not in [".idea"]:  # Skip irrelevant files
            try:
                instance = read_file(str(test_file))
                print(f"{test_file.name}: ", end="")
                solve(instance)
            except Exception as e:
                print(f"Failed to process {test_file.name}: {e}")

end = timer()
print('\nElapsed time:', int((end - start) * 1000), 'milliseconds')
