# Author: Dave Kaushik
# References: N/A

def main():
    courses = createCoursesDict('courses.txt', ';')
    students = createStudentsDict('students.txt', ',')
    enrollment = createEnrollDict('enrollment.txt',':')
    enrollmentCount = getEnrolledCountDict(enrollment,courses)

    createIntro('Welcome to Mini-Beartracks')
    isQuit = False


    while not isQuit:
        displayMenu()
        userChoice = validateInput(input('> ').strip())

        if userChoice == 1:
            printTimetable(enrollment,courses,students,enrollmentCount)

        elif userChoice == 2:
            enroll(enrollment,courses,students,enrollmentCount)

        elif userChoice == 3:
            drop(enrollment,students,enrollmentCount)

        elif userChoice == 4:
            isQuit = True
            print('Goodbye')
            updateFileWithDict('enrollment.txt',enrollment,':')

        else:
            print('Sorry, invalid entry. Please enter a choice from 1 to 4.')

def createIntro(str):
    print('=' * len(str))
    print(str)
    print('=' * len(str))

def displayMenu():
    """
    This function displays the possible menu options, and prompts the user to enter an option
    :return: The menu option the user chose
    """

    print('What would you like to do?')
    print('1. Print time table\n2. Enroll in course\n3. Drop course\n4. Quit')

def validateInput(userInput):
    """
    This function checks if the user's input is a menu option
    :param userInput: the user's input for the menu option selection [str]
    :return: The menu choice [int], if the input is invalid, it returns [None]
    """
    if userInput in ('1','2','3','4'):
        return int(userInput)

def isValidId(students,id):
    return id in students


def createFileLines(filename):
    """
    creates the list of lines from a file
    :param filename: name of file [str]
    :return: list of lines in the file
    """
    file = open(filename,'r')
    fileContent = file.read()

    # Separate the file into a list of lines
    return fileContent.splitlines()


def createCoursesDict(filename,separator):
    """
    Creates a dictionary such that the first item in the line will be the key, and the rest will be
    values stored in a list. The values will be separated based on the identified separator. The key will
    be an integer if the string has ALL numeric values, otherwise it will stay a string.

    :param filename: [str] of filename with .txt extension
    :param separator: the symbol that separates each value in the line [str]
    :return: Dictionary in the format specified by the description [dict]
    """

    fileLines = createFileLines(filename)
    courseDict = {}

    # Iterate each line and put in the dictionary in the appropriate format
    for line in fileLines:

        # Split the line by the separator
        line = line.split(separator)
        lineValues = {}
        valueNames = ['time','capacity','prof']

        # Iterate each value out of the individual line
        for i in range(1,len(line)):   # Starts at 1 because first item in lineValues is the key
            value = line[i].strip()
            if value.isnumeric():
                value = int(value)
            lineValues[valueNames[i-1].lower()] = value

        # Assign the key and the list of values to the dictionary
        key = line[0]

        courseDict[key] = lineValues

    return courseDict

def createStudentsDict(filename,separator):
    """
    Creates a dictionary such that the first item in the line will be the key, and the rest will be
    values stored in a list. The values will be separated based on the identified separator. The key will
    be an integer if the string has ALL numeric values, otherwise it will stay a string.

    :param filename: [str] of filename with .txt extension
    :param separator: the symbol that separates each value in the line [str]
    :return:Dictionary in the format specified by the description [dict]
    """

    fileLines = createFileLines(filename)
    stuDict = {}
    valueNames = ['faculty','name']

    # Iterate each line and put in the dictionary in the appropriate format
    for line in fileLines:

        # Split the line by the separator
        line = line.split(separator)
        lineValues = {}

        # Iterate each value out of the individual line
        for i in range(1,len(line)):   # Starts at 1 because first item in lineValues is the key
            value = line[i].strip()
            if value.isnumeric():
                value = int(value)
            lineValues[valueNames[i-1].lower()] = value

        # Assign the key and the list of values to the dictionary
        key = int(line[0])

        stuDict[key] = lineValues

    return stuDict


def createEnrollDict(filename,separator):
    """
    Creates a dictionary such that the first item in the line will be the key, and the rest will be
    values stored in a list. The values will be separated based on the identified separator. The key will
    be an integer of the id number, which is going to be index 1 in the file lines.

    :param filename: [str] of filename with .txt extension
    :param separator: the symbol that separates each value in the line [str]
    :return:
    Dictionary in the format specified by the description [dict]
    """
    fileLines = createFileLines(filename)
    enrollDict = {}


    for line in fileLines:
        line = line.split(separator)
        key = int(line[1].strip())
        if key not in enrollDict:
            enrollDict[key] = []

        enrollDict[key].append(line[0].strip())


    return enrollDict

def isFull(courses,course,enrollmentCount):
    """
    Check if the course is full
    :param courses: Dictionary of all the courses and their times, capacity,
    :param course: Name of the course [str]
    :param enrollmentCount: Dictionary of the number of people enrolled in course
    :return: Boolean of if the course is full
    """

    maxCapacity = courses[course]['capacity']

    if maxCapacity == enrollmentCount[course]:
        return True

    return False

def getEnrolledCountDict(enrollment,courses):
    """
    Gets a dictionary of how many people are enrolled for each course
    :param enrollment: Dictionary of the enrolled courses for every student [dict]
    :param courses: Dictionary of all the courses and their times, capacity,
    :return: Dictionary of the courses enrolled count
    """

    enrolledCountDict = {}

    enrolledCourses = list(enrollment.values())


    # Iterate the courses for each student and check how many students have taken that course
    for course in courses:
        enrolledCountDict[course] = 0
        for courseList in enrolledCourses:
            if course in courseList:
                enrolledCountDict[course] = enrolledCountDict[course] + 1

    return enrolledCountDict

def validId(students,id):
    """
    Asks the id and checks if the id is in the students dictionary to validate it, also checking if it is a number
    :param students: dictionary of students
    :return: boolean of if the id is valid
    """

    if id.strip().isnumeric() and int(id.strip()) in students:
        return True

    return False

def isConflict(selectedCourse,courses,studentCourses):
    """
    Checks if a course conflicts with another course based on the time provided
    :param selectedCourse: The course that we are checking is conflicting with another [str]
    :param courses: the dictionary of available courses
    :param studentCourses: a list of all the student's courses
    :return: Boolean of if 2 courses conflict with each other
    """
    for course in studentCourses:
        if courses[selectedCourse]['time'] == courses[course]['time']:
            return True

    return False

def enroll(enrollment,courses,students,enrollmentCount):
    """
    Checks if the course for a particular student conflicts with another course in their schedule
    :param enrollment: Dictionary of the enrolled courses for every student [dict]
    :param courses: Dictionary of all the courses and their times, capacity,
    :param enrollmentCount: Dictionary of the number of people enrolled in course
    :return: Boolean of if the course is full or is conflicting
    """
    id = input('Student ID: ')
    if validId(students,id):
        selectedCourse = input('Course name: ').upper().strip()
        # Convert the id to integer form
        id = int(id)
        studentName = students[id]['name']

        if selectedCourse not in courses:
            print('Invalid course name.')

        else:
            # Get the list of enrolled courses, if there aren't any, then assign an empty list to the id
            enrollment[id] = enrollment.get(id,[])
            studentCourses = enrollment[id]
            courseValues = courses[selectedCourse]
            courseTime = courseValues['time']

            # Check if the student is already enrolled in the course

            if isConflict(selectedCourse,courses,studentCourses):
                print(f'Schedule conflict: already registered for course on {courseTime}')

            elif isFull(courses,selectedCourse,enrollmentCount):
                print(f'Cannot enroll. {selectedCourse} is already at capacity. Please contact advisor to get on '
                      'waiting list')

            else:
                studentCourses.append(selectedCourse)
                print(f'Successfully enrolled {studentName} in {selectedCourse}.')

                # Increase the count of students enrolled in the course
                enrollmentCount[selectedCourse] = enrollmentCount.get(selectedCourse,0) + 1

            if len(studentCourses) == 0:
                del enrollment[id]
    else:
        print('Invalid student ID. Cannot continue with course enrollment')

def drop(enrollment,students,enrollmentCount):
    """
    Displays the timetable of a particular student onto the screen
    :param enrollment: Dictionary of the courses the student is enrolled in
    :param students: Dictionary of all students and their information
    :param enrollmentCount: Dictionary of the number of people enrolled in course
    :return: None
    """
    id = input('Student ID: ')


    if validId(students,id):
        # Convert the id to integer form
        id = int(id)

        studentName = students[id]['name']

        # Display all the enrolled courses
        enrolledCourses = enrollment.get(id,[])

        print('Select a course to drop:')
        for course in enrolledCourses:
            print(f'- {course}')

        selectedCourse = input('Course name: ').upper().strip()


        if selectedCourse in enrolledCourses:
            enrolledCourses.remove(selectedCourse)
            print(f'{studentName} has successfully dropped {selectedCourse}.')

            # Decrease the count of students enrolled in the course
            enrollmentCount[selectedCourse] = enrollmentCount[selectedCourse] - 1

        else:
            print(f'{studentName} is not currently registered in {selectedCourse}.')

    else:
        print('Invalid student ID. Cannot continue with course drop')


def isCourseonTime(course,time,days,courses):
    if time in courses[course]['time'] and days in courses[course]['time']:
        return True
    return False


def displayTimetable(enrollment,courses,students,id,enrollmentCount):
    """
    Displays the timetable of a particular student onto the screen
    :param enrollment: Dictionary of the courses the student is enrolled in
    :param courses: Dictionary of the available courses
    :param students: Dictionary of all students and their information
    :param id: Integer of the student's id
    :param enrollmentCount: Dictionary of the number of people enrolled in course
    :return: None
    """
    # Print out the header
    print(f'Timetable for {students[id]["name"]} in the faculty of {students[id]["faculty"]}')

    days = ['Mon', 'Tues', 'Wed', 'Thrus', 'Fri']
    subjectFw = 10
    timeFw = 6
    verticalBorderSymbol = '|'
    horizontalBorderSymbol = '-'
    corner = '+'

    studentCourses = enrollment.get(id,[])

    # get a list of all the possible times
    times = []
    timeIntervals = 18
    earliestHour = 8
    latestHour = 16
    for hour in range(earliestHour, latestHour + 1):
        time = ''
        times.append(time + str(hour) + ':00')
        times.append(time + str(hour) + ':30')

    clusterSize = 18
    timesPerCluster = 5

    # there are 10 '-'s per subject and one '+' but the one at the end has and additional '+'
    horizontalSeperator = horizontalBorderSymbol*subjectFw
    horizontalBorderSingle = corner + horizontalSeperator
    horizontalBorder = ' ' * timeFw + horizontalBorderSingle * len(days) + corner

    # set up the baseline for the vertical border
    # - each border should have the field width + 1 of space (+1 because it is under corner)
    verticalBorderSingle = f'%{-(subjectFw + 1)}s' % verticalBorderSymbol

    # Each cluster has 18 lines inside it including the lower border
    # Within each cluster, there are 6 times
    # Therefore, the number of clusters is dependent on how many times there are in total / times per cluster
    # The time is printed on every tick that has the index divisible by 3
    # The separator for MWF is printed every 6 ticks
    # The separator for TR is printed every 9 ticks

    distanceBetweenTimes = clusterSize // timesPerCluster

    dayString = ''
    for day in days:
        dayString += day.center(subjectFw + 1)

    dayString = f'%{(len(dayString) + timeFw)}s' % dayString

    print(dayString)

    print(horizontalBorder)

    writeMWFCapacity = False
    writeTRCapacity = False

    for rowIndex in range(clusterSize * (timeIntervals//timesPerCluster)):

        time = ' ' * timeFw
        MWFString = verticalBorderSingle
        TRString = verticalBorderSingle
        horizontalBorderIndex = False
        MWFSeperatorDistance = 6
        TRSeperatorDistance = 9

        if rowIndex % distanceBetweenTimes == 0:
            # normalize the rowIndex for the list
            timeIndexRaw = rowIndex
            timeIndex = timeIndexRaw // distanceBetweenTimes
            time = times[timeIndex]

            for course in studentCourses:
                # Lets firstly check if the course name's letters exceeds 5 characters
                # - the last 3 characters are numbers, so we must check only the length without the last 3
                displayCourse = course
                courseNumber = course[len(course)-3:len(course) + 1]
                courseName = course[0:len(course)-3].strip()
                if len(courseName) > 4:
                    displayCourse = courseName[0:3] + '* ' + courseNumber

                # Check if a course occurs on MWF
                # - if it does, capture the capacity, and where it should be on based on the time
                if isCourseonTime(course,time,'MWF',courses):
                    MWFString = verticalBorderSymbol + displayCourse.center(subjectFw)
                    MWFcapacity = str(courses[course]['capacity'] - enrollmentCount[course]).center(subjectFw)
                    MWFTimeIndex = rowIndex
                    writeMWFCapacity = True

                # Check if a course occurs on TR
                # - if it does, capture the capacity, and where it should be on based on the time
                elif isCourseonTime(course,time,'TR',courses):
                    TRString = verticalBorderSymbol + displayCourse.center(subjectFw)
                    TRcapacity = str(courses[course]['capacity'] - enrollmentCount[course]).center(subjectFw)
                    TRTimeIndex = rowIndex
                    writeTRCapacity = True


            time = f'%{-timeFw}s' % time

        # The operations ahead are based on the observations made previously about the frequency of each line
        if writeMWFCapacity and rowIndex == MWFTimeIndex + 1:
            MWFString = verticalBorderSymbol + str(MWFcapacity).center(subjectFw)
            writeMWFCapacity = False

        if writeTRCapacity and rowIndex == TRTimeIndex + 1:  # made this "if" because issue when indices were same
            TRString = verticalBorderSymbol + str(TRcapacity).center(subjectFw)
            writeTRCapacity = False

        elif (rowIndex + 1) % clusterSize == 0:
            horizontalBorderIndex = True
            print(horizontalBorder)

        elif (rowIndex + 1) % MWFSeperatorDistance == 0:
            MWFString = verticalBorderSymbol + horizontalSeperator

        elif (rowIndex + 1) % TRSeperatorDistance == 0:
            TRString = verticalBorderSymbol + horizontalSeperator

        if not horizontalBorderIndex:
            print(time + (MWFString + TRString) * 2 + MWFString + verticalBorderSymbol)

def printTimetable(enrollment,courses,students,enrollmentCount):
    """
    Pass through function to the displayTimeTable
    Displays the timetable of a particular student onto the screen
    :param enrollment: Dictionary of the courses the student is enrolled in
    :param courses: Dictionary of the available courses
    :param students: Dictionary of all students and their information
    :param enrollmentCount: Dictionary of the number of people enrolled in course
    :return None
    """
    id = input('Student ID: ')

    if validId(students, id):
        id = int(id)
        displayTimetable(enrollment,courses,students,id,enrollmentCount)

    else:
        print('Invalid student ID. Cannot print timetable')

def updateFileWithDict(filename,dictionary,separator):
    """
    Updates the file chosen with the dictionary's contents in the format values[index] : key
    :param filename: [str] of filename with .txt extension
    :param dictionary: a dictionary with the format where the values are lists or other containers
    :param separator:
    :return: None
    """

    file = open(filename,'w')

    for key,values in dictionary.items():
        for value in values:
            line = ''
            line += value + separator + str(key) + '\n'
            file.write(line)


if __name__ == '__main__':
    main()