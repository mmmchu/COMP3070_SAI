import re  # Import the 're' module for regular expressions to parse input files.


# Define a class to store instance data for scheduling problems.
class Instance:
    def __init__(self):
        # Initialize attributes for the number of students, exams, slots, and rooms.
        self.number_of_students = 0
        self.number_of_exams = 0
        self.number_of_slots = 0
        self.number_of_rooms = 0

        # Initialize lists for room capacities, exam-to-student assignments, and student exam capacities.
        self.room_capacities = []
        self.exams_to_students = []
        self.student_exam_capacity = []


# Define a function to read and parse the input file.
def read_file(filename):
    # Define a helper function to read and parse a specific attribute from a line in the file.
    def read_attribute(name, x):
        ls = x.readline().strip()  # Read a line, stripping leading/trailing whitespace.
        if not ls:
            # Raise an error if the line is empty or unexpected.
            raise Exception(f"Empty or unexpected line encountered while parsing {name}")

        # Use regular expressions to match the expected format of the attribute.
        match = re.match(f'{name}:\\s*(\\d+)$', ls)
        if match:
            return int(match.group(1))  # Return the parsed integer value.
        else:
            # Raise an error if the line does not match the expected format.
            raise Exception(f"Could not parse line '{ls}'; expected the {name} attribute")

    # Create an instance of the Instance class to store the parsed data.
    instance = Instance()

    # Open the file for reading.
    with open(filename) as f:
        try:
            # Read and parse the number of students, exams, slots, and rooms.
            instance.number_of_students = read_attribute("Number of students", f)
            instance.number_of_exams = read_attribute("Number of exams", f)
            instance.number_of_slots = read_attribute("Number of slots", f)
            instance.number_of_rooms = read_attribute("Number of rooms", f)

            # Read and parse the capacities of each room.
            for r in range(instance.number_of_rooms):
                instance.room_capacities.append(read_attribute(f"Room {r} capacity", f))

            # Read and parse the exam-to-student assignments.
            while True:
                line = f.readline().strip()  # Read the next line and strip whitespace.
                if not line:
                    break  # Stop if the line is empty.
                # Match the line format for exam-to-student assignments.
                m = re.match('^\\s*(\\d+)\\s+(\\d+)\\s*$', line)
                if m:
                    # Append the parsed assignment as a tuple (exam, student).
                    instance.exams_to_students.append((int(m.group(1)), int(m.group(2))))
                else:
                    # Raise an error if the line does not match the expected format.
                    raise Exception(f'Failed to parse this line: {line}')

            # Initialize a list to track the number of students assigned to each exam.
            for r in range(instance.number_of_exams):
                instance.student_exam_capacity.append(0)

            # Increment the count of students for each exam based on the parsed assignments.
            for r in instance.exams_to_students:
                instance.student_exam_capacity[r[0]] += 1

        # Catch any errors that occur during file reading or parsing.
        except Exception as e:
            print(f"Error while reading {filename}: {e}")
            raise

    # Return the populated instance object.
    return instance
