import re


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
    def read_attribute(name, x):
        ls = x.readline().strip()  # Strip to avoid extra spaces
        if not ls:
            raise Exception(f"Empty or unexpected line encountered while parsing {name}")

        match = re.match(f'{name}:\\s*(\\d+)$', ls)
        if match:
            return int(match.group(1))
        else:
            raise Exception(f"Could not parse line '{ls}'; expected the {name} attribute")

    instance = Instance()
    with open(filename) as f:
        try:
            # Read Number of students, exams, slots, and rooms
            instance.number_of_students = read_attribute("Number of students", f)
            instance.number_of_exams = read_attribute("Number of exams", f)
            instance.number_of_slots = read_attribute("Number of slots", f)
            instance.number_of_rooms = read_attribute("Number of rooms", f)

            # Read room capacities
            for r in range(instance.number_of_rooms):
                instance.room_capacities.append(read_attribute(f"Room {r} capacity", f))

            # Read the exam-to-student assignments
            while True:
                line = f.readline().strip()
                if not line:
                    break
                m = re.match('^\\s*(\\d+)\\s+(\\d+)\\s*$', line)
                if m:
                    instance.exams_to_students.append((int(m.group(1)), int(m.group(2))))
                else:
                    raise Exception(f'Failed to parse this line: {line}')

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
