
from z3 import *

def solve(instance):
    s = Solver()

    # Declarations
    exam = Int('exam')
    room = Int('room')
    ts = Int('ts')
    nex = Int('nex')
    nts = Int('nts')
    student = Int('student')
    invigilator = Int('invigilator')  # Define invigilator as Int variable
    other_room = Int('other_room')  # Define other_room as Int variable

    exam1 = Int('exam1')
    exam2 = Int('exam2')

    # Number of invigilators
    num_invigilators = 8
    max_exams_per_invigilator = 2

    # Range functions
    Student_Range = Function('Student_Range', IntSort(), BoolSort())
    Exam_Range = Function('Exam_Range', IntSort(), BoolSort())
    Room_Range = Function('Room_Range', IntSort(), BoolSort())
    TimeSlot_Range = Function('TimeSlot_Range', IntSort(), BoolSort())
    Invigilator_Range = Function('Invigilator_Range', IntSort(), BoolSort())

    # Range constraints based on instance attributes
    s.add(ForAll([student], Student_Range(student) == And(student >= 0, student < instance.number_of_students)))
    s.add(ForAll([exam], Exam_Range(exam) == And(exam >= 0, exam < instance.number_of_exams)))
    s.add(ForAll([ts], TimeSlot_Range(ts) == And(ts >= 0, ts < instance.number_of_slots)))
    s.add(ForAll([room], Room_Range(room) == And(room >= 0, room < instance.number_of_rooms)))
    s.add(
        ForAll([invigilator], Invigilator_Range(invigilator) == And(invigilator >= 1, invigilator < num_invigilators)))

    # Functions for assignments
    ExamRoom = Function('ExamRoom', IntSort(), IntSort())
    ExamTime = Function('ExamTime', IntSort(), IntSort())
    ExamStudent = Function('ExamStudent', IntSort(), IntSort(), BoolSort())
    RoomInvigilator = Function('RoomInvigilator', IntSort(), IntSort(), IntSort())

    # Adding students to exams
    for etos in instance.exams_to_students:
        s.add(ExamStudent(etos[0], etos[1]))

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

    # Constraint 3: The number of students taking an exam cannot exceed the capacity of the room.
    for ex2 in range(instance.number_of_exams):
        for rm2 in range(instance.number_of_rooms):
            s.add(Implies((ExamRoom(ex2) == rm2), instance.student_exam_capacity[ex2] <= instance.room_capacities[rm2]))

    # Constraint 4: A student cannot take exams in consecutive time slots.
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

    # Constraint 5: each room in a given time slot is assigned an invigilator,
    # and that the same invigilator is not assigned to multiple rooms in the same time slot.
    s.add(
        ForAll([room, ts],  # For all rooms and time slots
               Implies(
                   And(Room_Range(room), TimeSlot_Range(ts)),  # If the room and time slot are valid
                   Exists([invigilator],  # There exists an invigilator
                          And(
                              Invigilator_Range(invigilator),  # The invigilator is valid
                              RoomInvigilator(room, ts) == invigilator,
                              # The invigilator is assigned to this room at this time slot
                              ForAll([other_room],  # For all other rooms
                                     Implies(
                                         And(Room_Range(other_room), other_room != room),
                                         # If the room is different from the current room
                                         RoomInvigilator(other_room, ts) != invigilator
                                         # The same invigilator is not assigned to the other room at the same time
                                     )
                                     )
                          )
                          )
               )
               )
    )

    # Constraint 6: A student can take at most two exams in a day.
    s.add(
        ForAll([student, ts],  # For each student and time slot
               Implies(
                   Student_Range(student),  # If the student is valid
                   Sum([If(And(ExamTime(exam) == ts, ExamStudent(exam, student)), 1, 0)
                        for exam in range(instance.number_of_exams)]) <= 2  # No more than 2 exams per day
               )
               )
    )

    '''
    Constraint 7: An invigilator can supervise at most 2 exams
    s.add(
        ForAll([invigilator],
               Implies(
                   Invigilator_Range(invigilator),  # If the invigilator is valid
                   Sum(
                       [If(
                           And(ExamTime(exam) == ts, ExamRoom(exam) == room, RoomInvigilator(room, ts) == invigilator),
                           1, 0)
                           for exam in range(instance.number_of_exams)
                           for room in range(instance.number_of_rooms)
                           for ts in range(instance.number_of_slots)]
                   ) <= max_exams_per_invigilator  # Limit the exams supervised by the invigilator
               )
           )
    )
    '''

    # Check satisfiability and output results
    if s.check() == unsat:
        print('unsat')

    else:
        print('sat')
        for ex2 in range(instance.number_of_exams):
            room = s.model().eval(ExamRoom(ex2))
            slot = s.model().eval(ExamTime(ex2))
            invigilator = s.model().eval(RoomInvigilator(room, slot))
            print(f"Exam: {ex2}  Room: {room}  Slot: {slot} Invigilator: {invigilator}")

        print("――――――――――――――――――――――――")
