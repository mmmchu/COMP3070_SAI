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
    student_range = Function('student_range', IntSort(), BoolSort())
    exam_range = Function('exam_range', IntSort(), BoolSort())
    room_range = Function('room_range', IntSort(), BoolSort())
    time_slot_range = Function('time_slot_range', IntSort(), BoolSort())
    invigilator_range = Function('invigilator_range', IntSort(), BoolSort())

    # Range constraints based on instance attributes
    s.add(ForAll([student], student_range(student) == And(student >= 0, student < instance.number_of_students)))
    s.add(ForAll([exam], exam_range(exam) == And(exam >= 0, exam < instance.number_of_exams)))
    s.add(ForAll([ts], time_slot_range(ts) == And(ts >= 0, ts < instance.number_of_slots)))
    s.add(ForAll([room], room_range(room) == And(room >= 0, room < instance.number_of_rooms)))
    s.add(
        ForAll([invigilator], invigilator_range(invigilator) == And(invigilator >= 1, invigilator < num_invigilators)))

    # Functions for assignments
    examroom = Function('examroom', IntSort(), IntSort())
    exam_time = Function('exam_time', IntSort(), IntSort())
    exam_student = Function('exam_student', IntSort(), IntSort(), BoolSort())
    room_invigilator = Function('room_invigilator', IntSort(), IntSort(), IntSort())

    # Adding students to exams
    for etos in instance.exams_to_students:
        s.add(exam_student(etos[0], etos[1]))

    # Constraint 1: Each exam must be timetabled in exactly one room and exactly one slot.
    s.add(
        ForAll([exam],
               Implies(
                   exam_range(exam),
                   Exists([room, ts],
                          And(
                              room_range(room),
                              time_slot_range(ts),
                              exam_time(exam) == ts,
                              examroom(exam) == room
                          )
                          )
               )
               )
    )

    # Constraint 2: There can be, at most, one exam timetabled in a room within a specific slot.
    s.add(
        ForAll([room, ts],
               Implies(
                   And(room_range(room), time_slot_range(ts)),
                   ForAll([exam1, exam2],
                          Implies(
                              And(exam_range(exam1), exam_range(exam2)),
                              Implies(
                                  And(examroom(exam1) == room, exam_time(exam1) == ts,
                                      examroom(exam2) == room, exam_time(exam2) == ts),
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
            s.add(Implies((examroom(ex2) == rm2), instance.student_exam_capacity[ex2] <= instance.room_capacities[rm2]))

    # Constraint 4: A student cannot take exams in consecutive time slots.
    s.add(
        ForAll(
            [student, nex, ts, nts, exam],
            Implies(
                And(
                    student_range(student),
                    exam_range(exam),
                    exam_range(nex),
                    time_slot_range(ts),
                    time_slot_range(nts),
                    Not((exam == nex))
                ),
                Implies(
                    And(
                        exam_time(exam) == ts,
                        exam_time(nex) == nts,
                        exam_student(exam, student),
                        exam_student(nex, student)
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
                   And(room_range(room), time_slot_range(ts)),  # If the room and time slot are valid
                   Exists([invigilator],  # There exists an invigilator
                          And(
                              invigilator_range(invigilator),  # The invigilator is valid
                              room_invigilator(room, ts) == invigilator,
                              # The invigilator is assigned to this room at this time slot
                              ForAll([other_room],  # For all other rooms
                                     Implies(
                                         And(room_range(other_room), other_room != room),
                                         # If the room is different from the current room
                                         room_invigilator(other_room, ts) != invigilator
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
                   student_range(student),  # If the student is valid
                   Sum([If(And(exam_time(exam) == ts, exam_student(exam, student)), 1, 0)
                        for exam in range(instance.number_of_exams)]) <= 2  # No more than 2 exams per day
               )
               )
    )

    # Constraint 7: An invigilator can supervise at most 2 exams
    s.add(
        ForAll([invigilator],
               Implies(
                   invigilator_range(invigilator),  # If the invigilator is valid
                   Sum(
                       [If(
                           And(exam_time(exam) == ts, examroom(exam) == room,
                               room_invigilator(room, ts) == invigilator),
                           1, 0)
                           for exam in range(instance.number_of_exams)
                           for room in range(instance.number_of_rooms)
                           for ts in range(instance.number_of_slots)]
                   ) <= max_exams_per_invigilator  # Limit the exams supervised by the invigilator
               )
               )
    )

    # Print "loading solutions..." before checking satisfiability
    print("loading...\n", end='', flush=True)

    # Check satisfiability and output results
    if s.check() == unsat:
        return 'UNSAT'
    else:
        result = 'SAT\n'
        for ex2 in range(instance.number_of_exams):
            room = s.model().eval(examroom(ex2))
            slot = s.model().eval(exam_time(ex2))
            invigilator = s.model().eval(room_invigilator(room, slot))
            result += f"Exam: {ex2}  Room: {room}  Slot: {slot} Invigilator: {invigilator}\n"

        result += "――――――――――――――――――――――――"
        return result
