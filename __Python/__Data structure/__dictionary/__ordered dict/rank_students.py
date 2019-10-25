import operator


def readStudentDetails():

    numberOfStudents = int(input("Enter the total number of students: "))
    # {"Ramesh": 560, "Amit": 925, "Harshal": 698, "Uday": 980, "lokesh": 792,
    # "Bhavin": 258, "Hansika":988, "Anuradha": 842}

    studentsRecord = {}

    for students in range(1, numberOfStudents+1):
        print("Enter the name", students, "th", "of the student: ")
        name = input()
        print("Enter the marks of the {}: ".format(name))
        marks = int(input())
        studentsRecord[name] = marks
        # numberOfStudents -= numberOfStudents

    return studentsRecord


def rank_students(studentsRecord):

    sortedstudentsrecord = sorted(studentsRecord.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedstudentsrecord)
    print("{} has secured first rank, scoring {} marks".format(sortedstudentsrecord[0][0], sortedstudentsrecord[0][1]))
    print("{} has secured second rank, scoring {} marks".format(sortedstudentsrecord[1][0], sortedstudentsrecord[1][1]))
    print("{} has secured third rank, scoring {} marks".format(sortedstudentsrecord[2][0], sortedstudentsrecord[2][1]))
    return sortedstudentsrecord


def reward_student(sortedstudentsrecord, reward):
    print("{} has received a cash reward of ${}".format(sortedstudentsrecord[0][0], reward[0]))
    print("{} has received a cash reward of ${}".format(sortedstudentsrecord[1][0], reward[1]))
    print("{} has received a cash reward of ${}".format(sortedstudentsrecord[2][0], reward[2]))


def appricate_student(sortedstudentsrecord):
    for record in sortedstudentsrecord:
        if record[1] >= 950:
            print("Congratulation scoring {} marks, {}".format(record[1], record[0]))
        else:
            break


studentsRecord = readStudentDetails()
sortedstudentsrecord = rank_students(studentsRecord)

reward = (500, 300, 100)
reward_student(sortedstudentsrecord, reward)
appricate_student(sortedstudentsrecord)
