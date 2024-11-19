from z3 import *


def solve(instance):
    s = Solver()  # Create a Z3 solver instance

    # Declare Z3 integer variables
    exam = Int('exam')
    room = Int('room')
    ts = Int('ts')  # Time slot
    nex = Int('nex')  # Next exam
    nts = Int('nts')  # Next time slot
    student = Int('student')  # Student identifier
    invigilator = Int('invigilator')  # Invigilator identifier
    other_room = Int('other_room')  # Identifier for other rooms
    ts1 = Int('ts1')  # First time slot
    ts2 = Int('ts2')  # Second time slot
    room1 = Int('room1')  # First room
    room2 = Int('room2')  # Second room
    exam1 = Int('exam1')  # First exam
    exam2 = Int('exam2')  # Second exam

    # Define constants for invigilators and their maximum exams
    num_invigilators = 8  # Total number of invigilators
    max_exams_per_invigilator = 2  # Maximum exams supervised by an invigilator

    # Define range functions to specify valid ranges for various entities
    student_range = Function('student_range', IntSort(), BoolSort())
    exam_range = Function('exam_range', IntSort(), BoolSort())
    room_range = Function('room_range', IntSort(), BoolSort())
    time_slot_range = Function('time_slot_range', IntSort(), BoolSort())
    invigilator_range = Function('invigilator_range', IntSort(), BoolSort())

    # Add constraints for the ranges of students, exams, rooms, and time slots
    s.add(ForAll([student], student_range(student) == And(student >= 0, student < instance.number_of_students)))
    s.add(ForAll([exam], exam_range(exam) == And(exam >= 0, exam < instance.number_of_exams)))
    s.add(ForAll([ts], time_slot_range(ts) == And(ts >= 0, ts < instance.number_of_slots)))
    s.add(ForAll([room], room_range(room) == And(room >= 0, room < instance.number_of_rooms)))
    s.add(
        ForAll([invigilator], invigilator_range(invigilator) == And(invigilator >= 1, invigilator < num_invigilators)))

    # Define functions for assigning exams to rooms and times
    examroom = Function('examroom', IntSort(), IntSort())
    exam_time = Function('exam_time', IntSort(), IntSort())
    exam_student = Function('exam_student', IntSort(), IntSort(), BoolSort())  # Map students to exams
    room_invigilator = Function('room_invigilator', IntSort(), IntSort(),
                                IntSort())  # Map invigilators to rooms and times

    # Add constraints to link students to their exams
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
    for ex2 in range(instance.number_of_exams):
        for rm2 in range(instance.number_of_rooms):
            s.add(Implies((examroom(ex2) == rm2), instance.student_exam_capacity[ex2]
                          <= instance.room_capacities[rm2]))

    # Constraint 3: The number of students taking an exam cannot exceed the capacity of the room.
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

    # Constraint 7: An invigilator can supervise at most 3 exams
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

    # Constraint 8: Minimum Breaks Between Supervision
    # An invigilator must have at least one time slot gap between two exams they supervise.
    s.add(
        ForAll([invigilator, ts1, ts2],
               Implies(
                   And(
                       invigilator_range(invigilator),  # Valid invigilator
                       time_slot_range(ts1),  # Valid first time slot
                       time_slot_range(ts2),  # Valid second time slot
                       ts1 != ts2  # Time slots are not the same
                   ),
                   Implies(
                       And(
                           Exists([room1],  # Invigilator is assigned to a room in the first time slot
                                  And(room_range(room1), room_invigilator(room1, ts1) == invigilator)),
                           Exists([room2],  # Invigilator is assigned to a room in the second time slot
                                  And(room_range(room2), room_invigilator(room2, ts2) == invigilator))
                       ),
                       Abs(ts1 - ts2) > 1  # Require at least one time slot gap
                   )
               )
               )
    )

    # Print "loading solutions..." before checking satisfiability
    print("loading...\n", end='', flush=True)

    # Set to store unique solutions
    unique_solutions = set()

    # Initialize the solution count
    solution_count = 0

    # Maximum number of solutions to display
    max_solutions = 3

    if s.check() == unsat:
        return 'UNSAT'
    else:
        result = 'SAT\n'
        while s.check() == sat and solution_count < max_solutions:
            model = s.model()
            solution = []
            for ex2 in range(instance.number_of_exams):
                room = model.eval(examroom(ex2))
                slot = model.eval(exam_time(ex2))
                invigilator = model.eval(room_invigilator(room, slot))
                students = []  # List to store students taking this exam

                # Check which students are assigned to this exam
                for student_id in range(instance.number_of_students):
                    if model.eval(exam_student(ex2, student_id)):
                        students.append(student_id)

                # Append the details of the exam; convert students to a tuple
                solution.append((ex2, room, slot, invigilator, tuple(students)))

            solution_tuple = tuple(solution)  # Now this is a tuple of tuples and hashable

            if solution_tuple not in unique_solutions:
                unique_solutions.add(solution_tuple)

                # Increment the solution count and label accordingly
                solution_count += 1
                result += f"\nSolution #{solution_count}:\n"

                # Print the solution
                for exam, room, slot, invigilator, students in solution:
                    result += (f"Exam: {exam}  Room: {room}  Slot: {slot}  "
                               f"Invigilator: {invigilator}  Students: {list(students)}\n")

                result += "――――――――――――――――――――――――――――――――――――――――――――――――――――"

        return result
