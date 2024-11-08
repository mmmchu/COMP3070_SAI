from z3 import *
import re

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
    # Constraint 3 :The number of students taking an exam cannot exceed the capacity of
    # the room where the exam takes place.
    for ex2 in range(instance.number_of_exams):
        for rm2 in range(instance.number_of_rooms):
            s.add(Implies((ExamRoom(ex2) == rm2), instance.student_exam_capacity[ex2] <= instance.room_capacities[rm2]))

    # Constraint 4:A student cannot take exams in consecutive time slots.
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

    # Constraint 5

    # Check satisfiability and output results
    if s.check() == unsat:
        print('unsat')
    else:
        print('sat')
        for ex2 in range(instance.number_of_exams):
            print(" Exam:", ex2, " Room:", s.model().eval(ExamRoom(ex2)), " Slot:", s.model().eval(ExamTime(ex2)))
        print("――――――――――――――――――――――――")
