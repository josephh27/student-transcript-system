import numpy as np
import time
from datetime import datetime
import sys
import os
import statistics
import math

class Program: 
    def readData():
        data = np.loadtxt('studentDetails.csv', dtype=str, delimiter=',', skiprows=1)
        # for each_data in data:
        #     print(each_data)
        return data


    def startFeature():
        # levels_chosen = []
        # initial_student_level = input("What is your student level?\n[U]ndergraduate\n[G]raduate\n[B]oth? ")
        # if initial_student_level.upper() == "U":
        #     levels_chosen.append("U")
        #     self.getStudentID(levels_chosen)
        # elif initial_student_level.upper() == "G":
        #     secondary_student_level = input("Please specify graduate level.\n[M]aster\n[D]octorate\n[B0]th? ")
        #     if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "B0":
        #         levels_chosen.append("M")
        #     if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "B0":
        #         levels_chosen.append("D")
        #     self.getStudentID(levels_chosen)

        # elif initial_student_level.upper() == "B":
        #     levels_chosen.append("U")
        #     secondary_student_level = input("Please specify graduate level.\n[M]aster\n[D]octorate\n[BO]th? ")
        #     if secondary_student_level.upper() == "M" or secondary_student_level.upper() == "BO":
        #         levels_chosen.append("M")
        #     if secondary_student_level.upper() == "D" or secondary_student_level.upper() == "BO":
        #         levels_chosen.append("D")
        #     self.getStudentID(levels_chosen)
        self.getStudentID()



    def getStudentID():
        # student_level
        # try:
        #     transcript_records = self.readData()
        #     student_id = input("What is your student id? ")
        #     chosen_records = []
        #     for record in transcript_records:
        #         if "U" in student_level:
        #             if "BS" in record[6] and student_id == record[1]:
        #                 chosen_records.append(record)
        #         if "M" in student_level or "D" in student_level:
        #             if "M" in record[6] and student_id == record[1]:
        #                 chosen_records.append(record)
        #             if "D" in record[6] and student_id == record[1]:
        #                 chosen_records.append(record)
        #     if not chosen_records:
        #         raise ValueError()
        #     else:
        #         self.menuFeature(chosen_records)
        transcript_records = self.readData()
        chosen_records = []
        for record in transcript_records:
            if record[2] == "Harold Amad":
                chosen_records.append(record)
       
        self.majorTranscriptFeature(chosen_records)
        
        # except ValueError:
        #     print("No corresponding records found.\n\n")
        #     self.startFeature()

    def menuFeature(corresponding_records):
        # print("Student Transcription Generation System")
        # print("==================================================")
        # print("1. Student details")
        # print("2. Statistics")
        # print("3. Transcript Based on Major Courses")
        # print("4. Transcript Based on Minor Courses")
        # print("5. Full Transcript")
        # print("6. Previous Transcript Requests")
        # print("7. Select Another Student")
        # print("8. Terminate the System")
        # print("==================================================")
        # choice = int(input("Enter Your Feature: "))

        # if choice == 1:
        #     self.detailsFeature(corresponding_records)
        # elif choice == 2:
        #     self.statisticsFeature(corresponding_records)
        # elif choice == 3:
            # self.majorTranscriptFeature()
        
        pass

    def detailsFeature(current_records):
        name = current_records[0][2]
        stdID = current_records[0][1]
        levels = ", ".join(record[5] for record in current_records) 
        term_numbers = ", ".join(record[9] for record in current_records)
        colleges = ", ".join(record[3] for record in current_records)
        departments =", ".join(record[4] for record in current_records)
        print(self.printDetails(name, stdID, levels, term_numbers, colleges, departments))
        with open("std{}details.txt".format(stdID), "w") as file:
            file.write(self.printDetails(name, stdID, levels, term_numbers, colleges, departments))
    
    def printDetails(name, stdID, levels, term_numbers, colleges, departments):
        name_detail = f"Name: {name}"
        std_ID = f"stdID: {stdID}"
        level_detail = f"Level(s): {levels}"
        term_number_detail = f"Number Of Terms: {term_numbers}"
        college_detail = f"College(s): {colleges}"
        department_detail = f"Department(s): {departments}"
        return f"{name_detail}\n{std_ID}\n{level_detail}\n{term_number_detail}\n{college_detail}\n{department_detail}"

    def statisticsFeature(current_records):
        current_id = current_records[0][1]
        # data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        data = np.loadtxt('201008000.csv', dtype=str, delimiter=',', skiprows=1)
        with open("std201008000statistics.txt", "w") as file:
            file.write(self.printStatistics(current_records, data))


    def printStatistics(statistics_records, current_data):
        text_container = ""
        for record in statistics_records:
            str_container = ""
            overall_average = 0
            scores = []
            max_term = 0
            is_repeating = False
            if "BS" in record[6]:
                level = "Undergraduate"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "BS" in row[1]:
                        scores.append(int(row[7]))
                        if int(row[2]) > max_term:
                            max_term = int(row[2])
                        if row[4] in courses:
                            is_repeating = True
                        courses.append(row[4])
                    print(courses)

            elif "M" in record[6]:
                level = "Graduate(M)"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "M" in row[1]:           
                        scores.append(int(row[7]))
                        if int(row[2]) > max_term:
                            max_term = int(row[2])
                        if row[4] in courses:
                            is_repeating = True
                        courses.append(row[4])

            elif "D" in record[6]:
                level = "Graduate(D)"
                overall_average = 0
                courses = []
                for row in current_data:
                    if "D" in row[1]:    
                        scores.append(int(row[7]))
                        if int(row[2]) > max_term:
                            max_term = int(row[2])
                        if row[4] in courses:
                            is_repeating = True
                        courses.append(row[4])

            overall_average = statistics.mean(scores)
            max_score = max(scores)
            min_score = min(scores)
            max_terms = []
            min_terms = []
            for row in current_data:
                if max_score == int(row[7]):
                    if not (row[2] in max_terms):
                        max_terms.append(row[2])
                if min_score == int(row[7]):
                    if not (row[2] in min_terms):
                        min_terms.append(row[2])

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


            text_container += str_container
            print(str_container)

        return text_container

    def majorTranscriptFeature(current_records_major):
        current_id = current_records_major[0][1]
        # data = np.loadtxt('{}.csv'.format(current_id), dtype=str, delimiter=',', skiprows=1)
        data = np.loadtxt('201008000.csv', dtype=str, delimiter=',', skiprows=1)
        with open("std201008000MajorTranscript.txt", "w") as file:
            file.write(self.printMajorTranscriptFeature(current_records_major, data))


    def printMajorTranscriptFeature(statistics_records, current_data):
        text_container = ""
        for degree in statistics_records:
            name = degree[2]
            college = degree[3]
            major = degree[7]
            level = degree[5]
            stdID = degree[1]
            department = degree[4]
            minor = degree[8]
            term_numbers = degree[9]
            str_container = ""
            str_container += f"{f'Name: {name}':<35}{f'stdID: {stdID}':<50}\n"
            str_container += f"{f'College: {college}':<35}{f'Department: {department}':<50}\n"
            str_container += f"{f'Major: {major}':<35}{f'Minor: {minor}':<50}\n"
            str_container += f"{f'Level: {level}':<35}{f'Number of terms: {term_numbers}':<50}\n"
            max_term = 0
            if "BS" in degree[6]:
                for row in current_data:
                    if "BS" in row[1]:
                        level = "Undergraduate"
                        if int(row[2]) > max_term:
                            max_term = int(row[2])
            elif "M" in degree[6]:
                for row in current_data:
                    if "M" in row[1]:
                        level = "Graduate(M)"
                        if int(row[2]) > max_term:
                            max_term = int(row[2])
            elif "D" in degree[6]:
                for row in current_data:
                    if "D" in row[1]:
                        level = "Graduate(D)"
                        if int(row[2]) > max_term:
                            max_term = int(row[2])
            print(str_container)
            
            for i in range(max_term):
                term_rows = []
                major_average = []
                overall_average = []
                term_container = ""
                term_container += f"============================================================\n"
                term_container += f"***************       Term {i+1}     ***************\n"
                term_container += f"============================================================\n"
                for row in current_data:
                    if int(row[2]) == i+1 and degree[6] == row[1]:
                        term_rows.append(row)
                        if row[5] == "Major":
                            
                
                term_container += f"{f'course ID':<15}{f'course name':<15}{f'credit hours':<15}{f'grade':<15}\n"
                for filtered_row in term_rows:
                    term_container += f"{f'{filtered_row[4]}':<15}{f'{filtered_row[3]}':<15}{f'{filtered_row[6]}':<15}{f'{filtered_row[7]}':<15}\n"
                
                term_container += f"Major Average = {sta}                   Overall Average = {}"
                print(term_container)
            

            text_container += str_container
        return text_container

if __name__ == "__main__":
    self.startFeature()















