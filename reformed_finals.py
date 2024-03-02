import numpy as np
import time
from datetime import datetime
import sys
import os
import statistics
import math

class Program:
    def __init__(self):
        self.timestamps = []
        self.BOLD = '\033[1m'
        self.END = '\033[0m'
        self.YELLOW = '\033[93m'
        self.RED = '\033[91m'
        self.GREEN = '\033[92m'
        self.CYAN = '\033[96m'
        self.counter = 0

    def readData(self): # This is the csv reader, it will read the data inside the csv file and will be used as basis for the self.
        data = np.loadtxt('studentDetails.csv', dtype=str, delimiter=',', skiprows=1)
        return data
    
    def sleep(self):
        for pause_in_seconds in range(3, 0, -1):
            print (f"{self.BOLD}{self.GREEN}Loading in {pause_in_seconds} second ...{self.END}")
            time.sleep(1)

    def clear(self):
        clear = lambda: os.system("cls")
        clear()

    def errorMessage(self):
        return f'{self.BOLD}{self.RED}[Error] Invalid input. Please try again.{self.END}'

    def startFeature(self):
        try:
            self.clear()
            self.timestamps.clear()
            self.counter = 0
            levels_chosen = [] # Storage of the levels chosen
            # This is where the user will choose the level of the record he/she is looking for
            initial_student_level = input(f"{self.BOLD}{self.YELLOW}Student Level:{self.END}\n[U] Undergraduate\n[G] Graduate\n[B] Both?\n{self.CYAN}Enter student level:{self.END} ") 
            if initial_student_level.upper() == "U": # If undergraduate array will store choice then will look for the record using getStudentID
                levels_chosen.append("U")
                self.getStudentID(levels_chosen)
            elif initial_student_level.upper() == "G": # If graduate prompt asks what graduate level user is, if M or D or Both
                self.clear()
                # Then array stores choice then will look for the studentID using the choice.
                secondary_student_level = input(f"{self.BOLD}{self.YELLOW}Graduate Level:{self.END}\n[M] Master\n[D] Doctorate\n[BO] Both?\n{self.CYAN}Enter graduate level:{self.END} ")
                if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "BO":
                    levels_chosen.append("M")
                if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "BO":
                    levels_chosen.append("D")
                if secondary_student_level.upper() != "D" and secondary_student_level.upper() != "M" and secondary_student_level.upper() != "BO":
                    raise ValueError
                self.getStudentID(levels_chosen)
            elif initial_student_level.upper() == "B": # If both undergraduate and graduate, user's first choice (U) is stored then prompt
                self.clear()
                # asks whether graduate level is M, D, or Both then 2nd choice is stored then studentID is looked for using the getStudentID.
                levels_chosen.append("U")
                secondary_student_level = input(f"{self.BOLD}Graduate Level:{self.END}\n[M] Master\n[D] Doctorate\n[BO] Both?\n{self.CYAN}Enter graduate level:{self.END} ")
                if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "BO":
                    levels_chosen.append("M")
                if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "BO":
                    levels_chosen.append("D")
                if secondary_student_level.upper() != "D" and secondary_student_level.upper() != "M" and secondary_student_level.upper() != "BO":
                    raise ValueError
                self.getStudentID(levels_chosen)
            else: raise ValueError
        except ValueError:
            # self.clear()
            print(self.errorMessage())
            self.sleep()
            self.startFeature()


    def getStudentID(self, student_level): # Will look for the student ID based on your choice of student level in the beginning.
        try:
            self.clear()
            transcript_records = self.readData() # Stores the data on csv
            student_id = input("Enter student ID: ") # Prompt gets the StudentID of user
            chosen_records = []
            for record in transcript_records: # Then the records in the csv will be the data used to look for user. 
                if "U" in student_level: # If they chose U, if it is BS & matches the student ID chosen_records will store the user's record
                    if "BS" in record[6] and student_id == record[1]:
                        chosen_records.append(record)
                if "M" in student_level or "D" in student_level: # On the event that they choose Masteral or Doctoral.
                    if "M" in record[6] and student_id == record[1]: # If it's masteral and ID matches, chosen_records will store the data
                        chosen_records.append(record) 
                    if "D" in record[6] and student_id == record[1]: # If it's doctoral and ID matches, chosen_records will store the data
                        chosen_records.append(record)
            if not chosen_records: # If data provided is not in saved records, error will be raised.
                raise ValueError()
            else:
                self.menuFeature(chosen_records) # else. menu is launched.

        except ValueError: # If data provided is not in saved records, error will be raised.
            print(f"{self.RED}{self.BOLD}No corresponding records found.{self.END}")
            self.sleep()
            self.startFeature()

    def menuFeature(self, corresponding_records): # This will launch if all the data provided by the user matches the ones in record.
        while True:
            try:
                print("==================================================")
                print(f"{self.BOLD}Student Transcription Generation System{self.END}")
                print("==================================================")
                print("1. Student details") # Provides student details, presented by the detailsFeature function.
                print("2. Statistics") # Provides student's stats, presented by the statisticsFeature function.
                print("3. Transcript Based on Major Courses") # Provides the minor transcript of subjects, presented by minorTranscriptFeature func.
                print("4. Transcript Based on Minor Courses") # Provides the major transcript of subjects, presented by majorTranscriptFeature func.
                print("5. Full Transcript") # Provides the students's full transcript of subjects, presented by  fullTranscriptFeature function
                print("6. Previous Transcript Requests") # Provides the history of transcript record requests from the student
                print("7. Select Another Student") # Allows choosing another student for transcript record findings.
                print("8. Terminate the System") # Exits the program
                print("==================================================")
                choice = int(input(f"{self.CYAN}Enter your feature:{self.END} "))
                self.clear()
                if choice == 1:
                    self.clear()
                    self.requestCounter(1)
                    self.getTimeStamp('Details', self.timestamps, corresponding_records[0][1])
                    self.detailsFeature(corresponding_records)
                    # self.sleep()
                elif choice == 2:
                    self.clear()
                    self.requestCounter(1)
                    self.getTimeStamp('Statistics', self.timestamps, corresponding_records[0][1])
                    self.statisticsFeature(corresponding_records)
                elif choice == 3:
                    self.clear()
                    self.requestCounter(1)
                    self.getTimeStamp('Major', self.timestamps, corresponding_records[0][1])
                    self.majorTranscriptFeature(corresponding_records)
                elif choice == 4:
                    self.clear()
                    self.requestCounter(1)
                    self.getTimeStamp('Minor', self.timestamps, corresponding_records[0][1])
                    self.minorTranscriptFeature(corresponding_records)
                elif choice == 5:
                    self.clear()
                    self.requestCounter(1)
                    self.getTimeStamp('Full', self.timestamps, corresponding_records[0][1])
                    self.fullTranscriptFeature(corresponding_records)
                elif choice == 6:
                    self.clear()
                    self.previousRequestFeature(corresponding_records)
                elif choice == 7:
                    self.newStudentFeature()
                elif choice == 8:
                    self.terminateFeature()
                else:
                    print("what")
            except ValueError:
                self.clear()
                print("hello")
                print(self.errorMessage())
                self.menuFeature(corresponding_records)

    def detailsFeature(self, current_records): # Present student details, prints them in format then stores them in a list.
        self.clear()
        name = current_records[0][2]
        stdID = current_records[0][1]
        levels = ", ".join(record[5] for record in current_records) 
        term_numbers = ", ".join(record[9] for record in current_records)
        colleges = ", ".join(record[3] for record in current_records)
        departments =", ".join(record[4] for record in current_records)
        print(self.printDetails(name, stdID, levels, term_numbers, colleges, departments))
        with open("std{}details.txt".format(stdID), "w") as file:
            file.write(self.printDetails(name, stdID, levels, term_numbers, colleges, departments))
        # self.sleep()
    
    def printDetails(self, name, stdID, levels, term_numbers, colleges, departments): # This will be the printing function used in studentDetails func
        # This is the format to which the details are presented.
        name_detail = f"Name: {name}"
        std_ID = f"stdID: {stdID}"
        level_detail = f"Level(s): {levels}"
        term_number_detail = f"Number Of Terms: {term_numbers}"
        college_detail = f"College(s): {colleges}"
        department_detail = f"Department(s): {departments}"
        return f"{name_detail}\n{std_ID}\n{level_detail}\n{term_number_detail}\n{college_detail}\n{department_detail}"

    def statisticsFeature(self, current_records): # Presents statistics about student's grades, average of those grades, and highest grade per term.
        current_id = current_records[0][1]
        data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        with open(f"std{current_id}statistics.txt", "w") as file: # Saves the data in the text specified.
            file.write(self.printStatistics(current_records, data))

    def printStatistics(self, statistics_records, current_data):
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        for record in statistics_records:
            str_container = "" # Contains the format to which the data is to be presented.
            overall_average = 0 # Container for the overall average to be presented later.
            scores = [] # Stores the grades from the csv.
            max_term = 0 # Stores the max term recorded in the csv.
            is_repeating = False # Boolean whether student is a repeating or not.
            if "BS" in record[6]: # If student has BS as degree, he/she is labeled undergraduate and taking Bachelor of Science. 
                level = "Undergraduate"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "BS" in row[1]:
                        scores.append(int(row[7])) 
                        if int(row[2]) > max_term: # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
                        if row[4] in courses: # If course already exists in the container, is_repeating condition is true.
                            is_repeating = True
                        courses.append(row[4])

            elif "M" in record[6]: # If student has M as degree, he/she is labeled graduate and taking Masteral degree.
                level = "Graduate(M)"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "M" in row[1]:           
                        scores.append(int(row[7]))
                        if int(row[2]) > max_term:  # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
                        if row[4] in courses: # If course already exists in the container, is_repeating condition is true.
                            is_repeating = True
                        courses.append(row[4])

            elif "D" in record[6]: # If student has D as degree, he/she is labeled graduate and taking Doctoral degree.
                level = "Graduate(D)"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "D" in row[1]:    
                        scores.append(int(row[7]))
                        if int(row[2]) > max_term:  # Will check if the current term being checked is the highest term and will be stored as the max_term.
                            max_term = int(row[2])
                        if row[4] in courses: # If course already exists in the container, is_repeating condition is true.
                            is_repeating = True
                        courses.append(row[4])

            overall_average = statistics.mean(scores) # Will calculate the overall average of the student's grades.
            max_score = max(scores) # Contains minimum(lowest) grade
            min_score = min(scores) # Contains max(highest) grade
            max_terms = []
            min_terms = []
            for row in current_data:
                if max_score == int(row[7]):
                    if not (row[2] in max_terms): # If term recorded in csv is not found in the max_terms container. Append it to the list.
                        max_terms.append(row[2])
                if min_score == int(row[7]):
                    if not (row[2] in min_terms): # If term recorded in csv is not found in the min_terms container. Append it to the list.
                        min_terms.append(row[2])

            # Format to which the data is to be presented.
            str_container += f"""============================================================
***********        {level} Level        ***********
============================================================
Overall average (major and minor) for all terms: {overall_average}\n"""
            for i in range(max_term):
                term_grades = []
                for row in current_data :
                    if int(row[2]) == i+1 and row[1] == record[6]:
                        term_grades.append(int(row[7]))
                str_container += f"Term {i+1}: {statistics.mean(term_grades)}\n"
            str_container += f"""Maximum grade(s) and in which term(s): {max_score} in term {max_terms}
Minimum grade(s) and in which term(s): {min_score} in term {min_terms}
Do you have any repeated course(s)? {is_repeating}\n
            """

            text_container += str_container # Concatinates the format to the text_container to be presented in the text.
            print(str_container)

        return text_container # Returns the text_container.
    
    def majorTranscriptFeature(self, current_records_major): # Presents the major transcript of the student (major courses, the average of major courses in each term and the overall major average for all terms up to the last term.)
        current_id = current_records_major[0][1]
        data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        with open(f"std{current_id}MajorTranscript.txt", "w") as file: # Saves the data in the text specified.
            file.write(str(self.printMajorTranscriptFeature(current_records_major, data)))

    def printMajorTranscriptFeature(self, statistics_records, current_data): 
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        levels = list(set([level[5] for level in statistics_records])) # Stores the levels information from the 5th column of the studentDetails.csv
        levels.sort(reverse=True)
        for level in levels:
            overall_average = [] 
            header_value = self.transcriptHeader(statistics_records, level) # Presents the header
            text_container += header_value[0] 
            print(header_value[0])
            for i in range(header_value[1]): # This is iterating to each term
                major_average = []
                term_str_container = "" # Format to which the main info in the transcript is to be presented.
                term_str_container += f"====================================================\n"
                term_str_container += f"****************       Term {i+1}       ****************\n"
                term_str_container += f"====================================================\n"
                term_str_container += f"{f'Course ID':<15}{f'Course name':<15}{f'Credit hours':<15}{f'Grade':<15}\n"
                for row in current_data:
                    if row[0] == level and "Major" == row[5]:  
                        if int(row[2]) == i+1:
                            major_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                        overall_average.append(int(row[7])) 
                term_str_container += f"{f'Major Average = {statistics.mean(major_average)}':<30}{f'Overall Average = {statistics.mean(overall_average)}':<30}\n"
                text_container += term_str_container
                print(term_str_container)
            footer_container = '' # Presents the footer of the transript.
            footer_container += f"====================================================\n"
            footer_container += f'*******   End of transcript for level ({level})   *******\n'
            footer_container += f"====================================================\n"
            text_container += footer_container
            print(footer_container)

        return text_container

    def minorTranscriptFeature(self, current_records_minor): # Presents the minor transcript of the student (minor courses, the average of minor courses in each term and the overall minor average for all terms up to the last term.)
        current_id = current_records_minor[0][1]
        data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        with open(f"std{current_id}MinorTranscript.txt", "w") as file: # Saves the data in the text specified.
            file.write(str(self.printMinorTranscriptFeature(current_records_minor, data)))

    def printMinorTranscriptFeature(self, statistics_records, current_data):
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        levels = list(set([level[5] for level in statistics_records])) # Stores the levels information from the 5th column of the studentDetails.csv
        levels.sort(reverse=True)
        for level in levels:
            overall_average = []
            header_value = self.transcriptHeader(statistics_records, level) # Presents the header
            text_container += header_value[0]
            print(header_value[0])
            for i in range(header_value[1]): #This is iterating to each term
                minor_average = []
                term_str_container = "" # Format to which the main info in the transcript is to be presented.
                term_str_container += f"====================================================\n"
                term_str_container += f"****************       Term {i+1}       ****************\n"
                term_str_container += f"====================================================\n"
                term_str_container += f"{f'Course ID':<15}{f'Course name':<15}{f'Credit hours':<15}{f'Grade':<15}\n"
                for row in current_data:
                    if row[0] == level and "Minor" == row[5]:  
                        if int(row[2]) == i+1:
                            minor_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                        overall_average.append(int(row[7]))
                term_str_container += f"{f'Minor Average = {statistics.mean(minor_average)}':<30}{f'Overall Average = {statistics.mean(overall_average)}':<30}\n"
                text_container += term_str_container
                print(term_str_container)
            footer_container = '' # Presents the footer of the transript.
            footer_container += f"====================================================\n"
            footer_container += f'*******   End of transcript for level ({level})   *******\n'
            footer_container += f"====================================================\n"
            text_container += footer_container
            print(footer_container)

        return text_container

    def fullTranscriptFeature(self, current_records_full): # Presnts the full transcript information (major and minor courses, the average of major and minor courses in each term, the term average and the overall average.)
        current_id = current_records_full[0][1]
        data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        with open(f"std{current_id}MajorTranscript.txt", "w") as file: # Saves the data in the text specified.
            file.write(str(self.printFullTranscriptFeature(current_records_full, data)))

    def printFullTranscriptFeature(self, statistics_records, current_data):
        self.requestCounter(1)
        text_container = "" # Contains the data to be saved in the text based on the format presented by the str_container.
        levels = list(set([level[5] for level in statistics_records]))
        levels.sort(reverse=True)
        for level in levels:
            overall_average = []
            header_value = self.transcriptHeader(statistics_records, level) # Presents the header
            text_container += header_value[0]
            print(header_value[0])
            for i in range(header_value[1]): #This is iterating to each term
                minor_average = []
                major_average = []
                term_average = [] 
                term_str_container = "" # Format to which the main info in the transcript is to be presented.
                term_str_container += f"====================================================\n"
                term_str_container += f"****************       Term {i+1}       ****************\n"
                term_str_container += f"====================================================\n"
                term_str_container += f"{f'Course ID':<15}{f'Course name':<15}{f'Credit hours':<15}{f'Grade':<15}\n"
                for row in current_data:
                    if row[0] == level and "Minor" == row[5]:  
                        if int(row[2]) == i+1:
                            minor_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                            term_average.append(int(row[7]))
                        overall_average.append(int(row[7]))
                    if row[0] == level and "Major" == row[5]:  
                        if int(row[2]) == i+1:
                            major_average.append(int(row[7]))
                            term_str_container += f"{f'{row[4]}':<15}{f'{row[3]}':<15}{f'{row[6]}':<15}{f'{row[7]}':<15}\n"
                            term_average.append(int(row[7]))
                        overall_average.append(int(row[7]))
                term_str_container += f"{f'Major Average = {statistics.mean(major_average)}':<30}{f'Minor Average = {statistics.mean(minor_average)}':<30}\n"
                term_str_container += f"{f'Term Average = {statistics.mean(term_average)}':<30}{f'Overall Average = {statistics.mean(overall_average)}':<30}\n"
                text_container += term_str_container
                print(term_str_container)
            footer_container = '' # Presents the footer of the transript.
            footer_container += f"====================================================\n"
            footer_container += f'*******   End of transcript for level ({level})   *******\n'
            footer_container += f"====================================================\n"
            text_container += footer_container
            print(footer_container)
        self.sleep()

    def transcriptHeader(self, statistics_records, current_level): # Contains the header part of the data presented in the transcript.
        name = statistics_records[0][2] # Contains student's name found on 3rd column of the studentDetails.csv
        stdID = statistics_records[0][1] # Contains student's ID found on 2nd column of the studentDetails.csv
        term_numbers = 0
        departments = [] # Stores the student's department
        minors = [] # Stores the student's minor subjects
        majors = [] # Stores the student's major subjects
        colleges = [] # Stores the student's college
        for row in statistics_records:
            if row[5] == current_level: # If level provided by the user matches with level information in the csv
                departments.append(row[4])
                minors.append(row[8])
                majors.append(row[7])
                colleges.append(row[3])
                term_numbers = max(term_numbers, int(row[9])) 
        colleges_str = ', '.join([college for college in colleges]) # Contains the student's college separated by comma
        departments_str = ', '.join([department for department in departments]) # Contains the student's department separated by comma
        majors_str = ', '.join([major for major in majors]) # Contains the student's major subjects separated by comma
        minors_str = ', '.join([minor for minor in minors]) # Contains the student's minor subjects separated by comma

        str_container = "" # Contains format for which the first(Header) information is to be presented.
        str_container += f""
        str_container += f"\n{f'Name: {name}':<35}{f'stdID: {stdID}':<50}\n"
        str_container += f"{f'College: {colleges_str}':<35}{f'Department: {departments_str}':<50}\n"
        str_container += f"{f'Major: {majors_str}':<35}{f'Minor: {minors_str}':<50}\n"
        str_container += f"{f'Level: {current_level}':<35}{f'Number of terms: {term_numbers}':<50}\n"
        return [str_container, int(term_numbers)]

    def previousRequestFeature(self, previous_records): # Will present the history of the user's request for transcripts.
        current_id = previous_records[0][1]
        record = self.printRequests(self.timestamps, current_id)
        print(record)
    
    def getDataAndTime(self): #Function that will provide date and time to the system
        today = datetime.today() # Gets current date when session was held
        now = datetime.now() # Gets current time when session was held
        date = (today.strftime("%d/%m/%Y")) # Format to which the date is presented
        time = (now.strftime("%H:%M")) # Format to which the time is presented
        return now,date,time

    def getTimeStamp(self, request_type, timestamps, current_id): # Function that will record the timestamps on every function in the system
        date_now = self.getDataAndTime()[1] # Gets the date
        time_now = self.getDataAndTime()[2] # Gets the time
        timestamp_array = timestamps.append((request_type,date_now,time_now))
        record = self.printRequests(self.timestamps, current_id)
        with open(f"std{current_id}PreviousRequests.txt", "w") as file: # Saves the data in the text specified.
            file.write(record)
        self.timestamps = []

    def printRequests(self, timestamps, current_id): # Function that will print all the student requests in specified format
        if not os.path.isfile(f"std{current_id}PreviousRequests.txt"):
            lines = f'==================================================\n'
            lines += f"{f'Request':<20}{f'Date':<20}{f'Time':<10}\n"
            lines += f'=================================================='
        else:
            lines = ""
            with open(f"std{current_id}PreviousRequests.txt", "r") as file: 
                for line in file.readlines():
                    lines += line
        for request, date, time in timestamps:
            lines += f"\n{f'{request}':<20}{f'{date}':<20}{f'{time}':<10}"
        return lines
    
    def newStudentFeature(self): # Will give user the ability to look for another student.
        self.clear()
        self.startFeature()
    
    def terminateFeature(self):
        print(self.requestCounter(0))
        sys.exit("Come again another day")

    def requestCounter(self, num): # Provides counter for the sessions wherein the user requested transcripts.
        self.counter += num
        return f'==================================================\nNumber of requests: {self.counter}\n=================================================='

def main():
    if __name__ == "__main__":
        main_program = Program()
        main_program.startFeature()
main()