# -------------------------------------------------------------------------------------------- #
# Title: Final Script for Foundations in Programming Course
# Description: Script reads, writes and deletes data from a csv file.
#              1) The csv file has rows of entries that track the number of hours
#              worked on a project by a employee on a specific date.
#              2) Added an EntryNum to the csv file to keep track of entries
#              updated with each save and reload using a counter - also used for
#              deleting a particular entry.
#              3) Added a list to keep track of projects - any new projects should
#              first be added to list before being used in an entry row.
#              4) The script can also create a new csv file (when one is not present)
#              and will write the headers for each column in this case.
#               5) The list of employee hours is sorted based on ProjectName and the
#               list of projects is sorted alphabetically.
#               6) On loading the EntryNumbers are rewritten to be in ascending order
#                for the sorted list. They are also rewritten before writing to file.
# ChangeLog: (Who, When, What)
#  Hedy Khalatbari, 08/23/2021, Created Script
#                   08/24/2021, Added a new menu option and additional methods
#                               for showing and adding to list of projects
#                   08/25/2021, Modified script for error handling (such as reading an empty file
#                               and removing from an empty list)
# ------------------------------------------------------------------------------------------------- #

import os     # module for file handling
import csv    # module for reading and writing to csv files

# -- Data -- #
USER_RETURN_NOTHING_ = """  Display a menu of choices to the user

        :return: nothing
        """
strFileName = 'EmployeeProjectHours.csv'  # Name of the csv data file
csvfile = None                            # Object that represents a csv file
lstOfEmployeeHours = []       # List of dictionary rows
strEmployeeName = ""          # Captures the employee name
strProjectName = ""           # Captures the project name
strDate = ""                  # Captures the date as a string (formatted as 02/02/2021)
floatHours = ""               # Captures the hours worked as a float. User input as a string; data saved as float
status = ""                   # Captures a message to return & print for user feedback
status_project = ""           # Captures a message to return that states whether project was present in list
counter = 0                   # Keeps track of number of entries in csv file/lstOfEmployeeHours
lstOfProjects = []            # List of projects employees currently working on
lstOfProjects_lower = []      # List of project names in lower case - to compare to new entries
strNewProject = ""            # Captures the new project name to add to project list
dictEntryRow = ""             # Captures the dictionary row that is to be removed & provides option to not remove it

class EmployeeHours():
    '''
    manages the user input with setter properties,
    dict_method() saves all the data for an entry as a dictionary row
    '''

    def __init__(self, entry_num='', employee_name='', project_name='', full_date='', hours_worked=''):
        self.__entry_num = entry_num
        self.__employee_name = employee_name
        self.__project_name = project_name
        self.__full_date = full_date
        self.__hours_worked = hours_worked

   # getters for all five data components
    @property
    def entry_num(self):
        return str(self.__entry_num)

    @property
    def employee_name(self):
        return str(self.__employee_name)

    @property
    def project_name(self):
        return str(self.__project_name)

    @property
    def full_date(self):
        return str(self.__full_date)

    @property
    def hours_worked(self):
        return str(self.__hours_worked)


    # setters for all five data components; if any are not set and remain '',
    # the user input is rejected in the next step
    @entry_num.setter
    def entry_num(self, value):
        self.__entry_num = str(value)    # value was assigned from the counter in the IO method

    @employee_name.setter
    def employee_name(self, value):
        if str(value).isnumeric() == False:  # checks that it is not numeric
            value = value.strip().lower().title()    # strip, lower, and title case
            self.__employee_name = value     # sets it if condition fulfilled
        # otherwise, it remains as '' (i.e., an empty string)

    @project_name.setter
    def project_name(self, value):
        value = value.strip()            # strip
        self.__project_name = value      # in the IO method it was verified that entry was
                                         # present in the lstOfProjects

    @full_date.setter
    def full_date(self, value):     # checks that entries for month, day and year are within a specific range
        value = value.strip()       # strip
        try:
            month, day, year = value.split('/')
            month_check = int(month) < 13 and int(month) > 0
            day_check = int(day) < 32 and int(day) > 0     # not account for variability of number of days/month
            year_check = int(year) > 2000 and int(year) < 2100
        except:                  # assigns false if entries are not evaluable as integers
            month_check = False
            day_check = False
            year_check = False
        if month_check and day_check and year_check:
            self.__full_date = value  # sets it if all conditions are True
        # otherwise, it remains as '' (i.e., an empty string)

    @hours_worked.setter
    def hours_worked(self, value):
        try:
            value = value.strip()
            value = float(value)
            if value > 0 and value < 24.05:  # checks that value is logical for number of hours in a day
                self.__hours_worked = value
        except:
            value = ''
        # otherwise, it remains as '' (i.e., an empty string)

    def dict_method(self):
        """
        method for composing all data into a dictionary row
        :return: entry_dictionary
        """
        entry_dictionary = {'EntryNum':self.__entry_num,'EmployeeName':self.__employee_name,
                            'ProjectName':self.__project_name,'FullDate':self.__full_date,
                            'HoursWorked':self.__hours_worked}
        return entry_dictionary    # this is used to add list of dictionaries which can be written to csv file


# -- Processing -- #
# read from csv file and write to csv file
# add and remove entry rows from a list of dictionary rows

class Processor:
    """
    reads and writes to csv files (as dictionary rows),
    adds and deletes entries from a list of dictionary rows

    """

    @staticmethod
    def read_data_from_file(file_name):
        '''
        reads data from csv file as rows of dictionaries
        :param file_name:
        :return:list_employee_hours,list_projects, list_projects_lower, status
        '''
        counter = 1                    # keeps track of number of row entries
        list_initial = []              # reset to t an empty list
        list_employee_hours = []       # reset to an empty list of dictionary rows
        list_projects = []             # reset to an empty list of strings
        list_projects_lower = []       # reset to an empty list of strings
        status = 'File does not currently exist or is empty.\n' \
                 'A file will be created once you save your entries.'  # circumvents an error message when file is empty
        if os.path.exists(file_name):  # used to check if the text file exists
            with open(file_name) as csvfile:
                fieldnames = ['EntryNum','EmployeeName', 'ProjectName', 'FullDate', 'HoursWorked']
                reader = csv.DictReader(csvfile, fieldnames)

                # read rows into a list and sort based on ProjectName
                for row in reader:
                    list_initial.append(row)
                list_initial = sorted(list_initial, key=lambda item: item['ProjectName'])

                # change EnrtyNum to ascending order
                for row in list_initial:
                    if row['EntryNum'] != 'EntryNum':      # do not append the column headers to list
                        row['EntryNum'] = str(counter)
                        list_employee_hours.append(row)    # populates the employee hours list
                        if row['ProjectName'] not in list_projects:
                            list_projects.append(row['ProjectName'])   # populates the project list (without redundancies)
                            list_projects_lower.append(row['ProjectName'].lower())
                        counter += 1
                status = 'Data read from file.'
        return list_employee_hours, list_projects, list_projects_lower, status, counter

    @staticmethod
    def write_data_to_file(file_name, list_employee_hours):
        '''
        writes data to csv file
        :param file_name:
        :param list_employee_hours:
        :return: status, counter
        '''
        counter = 1  # resets counter to one to renumber the entry rows saved to csv file
        status = 'No data to write to file!'
        if list_employee_hours != []:
            list_employee_hours = sorted(list_employee_hours, key=lambda item: item['ProjectName'])
            with open(file_name, 'w', newline='') as csvfile:
                fieldnames = ['EntryNum', 'EmployeeName', 'ProjectName', 'FullDate', 'HoursWorked']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()  # column headers are written
                for entry_row in list_employee_hours:
                    entry_row['EntryNum'] = str(counter)  # renumber EntryNum in sorted list
                    writer.writerow(entry_row)
                    counter += 1
                status = 'Data written to file.'
        return status, counter

    @staticmethod
    def add_data_to_list(new_entry, list_employee_hours):  # new_entry is the object instance
        '''appends the object instance as a dictionary row to the list of employee hours

        :param new_entry:
        :param list_employee_hours:
        :return:list_employee_hours, status
        '''
        new_dictionary = new_entry.dict_method()
        list_employee_hours.append(new_dictionary)   # appends as a dictionary row
        status = 'New entry was added to list.'
        return list_employee_hours, status


    @staticmethod
    def remove_data_from_list(remove_entry, list_employee_hours):
        '''
        removes the entry from the list
        :param remove_entry:
        :param list_employee_hours:
        :return:list_employee_hours, removed_row, status
        '''
        # status = ''
        # product = product.strip().lower()  # product to be removed
        status = 'Entry was not in list.'
        remove_entry = remove_entry.strip()      # remove_entry is a string
        for entry_row in list_employee_hours:
            entry_number = (entry_row['EntryNum'])   # this is also saved as a string
            if entry_number == remove_entry:  # remove the user selected entry
                removed_row = entry_row
                list_employee_hours.remove(entry_row)
                status = 'Entry was removed.'
        return list_employee_hours, removed_row, status

# -- Presentation (I/O) -- #
# user interface including menu options, capturing user's choice and
# displaying the list of project employee-hours as well as list of projects

class IO:
    """ Performs Input and Output functions """

    @staticmethod
    def print_header():
        """
        Displays a description of what the script does and
        instructions for valid input formats
        :return:
        """
        print('''
        This program keeps track of number of hours each employee has worked on a specific project.
        Employee and project names should only contain letters.
        Dates should be entered as 01/01/2021 and hours worked per project as decimals 
        - for example 3.5 represents 3 and a half hours.
        Add a new project name to the project list before adding it as a new entry.
        ''')
        print('-'*60)  # Add a line separator


    @staticmethod
    def print_menu_options():
        USER_RETURN_NOTHING_
        print('''
        Menu of Options:
        1) Add a new entry
        2) Delete an existing entry
        3) Save data to CSV File        
        4) Reload data from CSV File
        5) Show list of all entries
        6) Show & add to project list
        7) Exit program
        ''')
        print('-'*60)  # Add a line separator

    @staticmethod
    def input_menu_choice():
        """ Gets the menu choice from a user &
            enforces entering a project name (default choice 6) if
            project list is empty

        :return: string
        """
        if lstOfProjects == []:
            print("There are no projects in the list. Please enter a project name before "   
                  "starting to track employee work hours on a project.")
            choice = '6'
        else:
            choice = str(input("Which option would you like to perform? [1 to 7] - ")).strip()
        print()  # Add an extra line for looks
        return choice

    @staticmethod
    def print_current_Entries_in_list(list_employee_hours):
        """ Shows the current entries

        :param list_employee_hours
        :return: nothing
        """

        print("----    Current entries are:    ----")
        # checks whether list is empty; sorts list based on ProjectName and prints it
        # I re-ordered the print order for each row to highlight the hours worked per project
        if list_employee_hours != []:
            print('Entry #', '|', 'Project Name','|', 'Hours Worked','|','Date','|', 'Employee Name')
            for row in sorted(list_employee_hours, key=lambda item: item['ProjectName']):
                print(row['EntryNum'],'|', row['ProjectName'],'|',row['HoursWorked'],'|', row['FullDate'], '|',row['EmployeeName'])
        else:
            print("There are no entries in the list.")
        print('-'*60)  # Add a line separator


    @staticmethod
    def print_current_Projects_in_list(list_projects):
        """ Shows the current projects

        :param list_projects
        :return: nothing
        """

        print("----    Current projects are:    ----")
        if list_projects != []:   # check whether list is empty
            for project in sorted(list_projects):  # sorts projects alphabetically
                print(project)
        else:
            print("There are no projects in the list.\n"
                  "Before adding new entries, add projects \n"
                  "using MENU OPTION 6.")
        print('-'*60)  # Add a line separator

    @staticmethod
    def input_yes_no_choice(message):
        """ Gets a yes or no choice from the user

        :return: string
        """
        choice = str(input(message))
        choice = choice.strip().lower()
        return choice

    @staticmethod
    def input_press_to_continue(optional_message=''):
        """ Pause program and show a message before continuing

        :param optional_message:  An optional message you want to display
        :return: nothing
        """
        print(optional_message)
        input('Press the [Enter] key to continue.')


    @staticmethod
    def input_new_entry():
        """
        asks for user input for data in entry row,
        instantiates and EmployeeHours object,
        uses setter properties to validate appropriateness of entries,
        if all appropriate returns object, otherwise rejects it
        :return:new_entry_object, status, status_project
        """
        status_project = ""    # string for capturing the validity of the project name
        # Step 1: capture user input
        strEmployeeName =  input("Enter employee name: ")
        strProjectName = input("Enter project name: ")
        strDate = input("Enter date in 01/01/2020 format: ")
        floatHours = input("Enter number of hours: ")

        # Step 2A: instantiate an object of EmployeeHours & set values
        new_entry_object = EmployeeHours()
        new_entry_object.entry_num = counter   # once entry is verified will add one to counter
        new_entry_object.employee_name = strEmployeeName
        new_entry_object.full_date = strDate
        new_entry_object.hours_worked = floatHours

        # Step 2B: check if project name is in project list
        if strProjectName.strip().lower() in lstOfProjects_lower:    # project names are insensitive to case
            new_entry_object.project_name = strProjectName
        else:
            status_project = ('The project name was not in the list of projects.\n'
                              'Check for correct spelling \n'
                              'or add project to list of projects first.')

        # Step 3: ensure that all variables have been successfully set; otherwise, entry is rejected
        if new_entry_object.employee_name != '' and new_entry_object.project_name != '' and \
                new_entry_object.full_date !='' and new_entry_object.hours_worked != '':
            status = 'All entries were valid.'
            return new_entry_object, status, status_project
        else:
            new_entry_object = ''
            status = 'Data was not valid.'
            return new_entry_object, status, status_project

    @staticmethod
    def input_entry_to_remove():
        """ Asks user which entry row they would like to remove

        :return: (string) entry_number
        """
        entry_number = str(input("Enter the entry number to remove: "))
        return entry_number

    @staticmethod
    def input_new_project(list_projects, list_projects_lower):
        """
        asks user for a new project name and adds to to the project list
        and to the project list lower
        :param list_projects: appends new project to this list
        :param list_projects_lower: appends new project to this list in lower case
        :return: list_projects,list_projects_lower, status
        """
        strNewProject =  input("Enter name of new project: ")
        strNewProject = strNewProject.strip()    # strip input
        strNewProject_lower = strNewProject.lower()
        if strNewProject_lower not in list_projects_lower:
            list_projects.append(strNewProject)
            list_projects_lower.append(strNewProject_lower)
            status = 'New project was added to list of projects'
        else:
            status = 'Project was already in project list.'
        return list_projects, list_projects_lower, status


# -- Main Body of Script  -- #

# When the program starts, print header, load data from 'EmployeeProjectHours.csv' and print list of entries & list of
# projects
IO.print_header()
lstOfEmployeeHours,lstOfProjects,lstOfProjects_lower, status, counter = Processor.read_data_from_file(strFileName)
print(status)   # feedback to user regarding file contents
print('-' * 60)
IO.print_current_Entries_in_list(lstOfEmployeeHours)  # shows current data in the list
IO.print_current_Projects_in_list(lstOfProjects)      # shows current projects in the list

# Display a menu of choices to the user
while (True):
    # Show menu and ask user to choose a menu option
    IO.print_menu_options()  # Shows menu
    strChoice = IO.input_menu_choice()  # Get menu option


    # Process user's menu choice
    if strChoice == '1':  # Add a new entry
        objEntry, status, status_project = IO.input_new_entry()
        if objEntry != '':
            counter += 1   # entry has been validated and one added to counter in preparation for the next entry
            lstOfEmployeeHours, status = Processor.add_data_to_list(objEntry, lstOfEmployeeHours)
            print(status)   # message to user
        else:
            print(status_project)   # if project was not in list of projects, message informs the user
            print('Data rejected. Employee and process names should only contain letters.\n'
                  'Dates should be entered as 01/01/2021 and be valid.\n'
                  'Hours worked should be entered as decimals.')
        IO.input_press_to_continue()
        continue  # to show the menu


    elif strChoice == '2' and lstOfEmployeeHours != []:  # Remove an existing entry (enter the EntryNumber)
        strEntry = IO.input_entry_to_remove()
        lstOfEmployeeHours, dictEntryRow, status = Processor.remove_data_from_list(strEntry, lstOfEmployeeHours)
        print("The entry you chose to remove is: ")
        print(dictEntryRow['EntryNum'],'|', dictEntryRow['ProjectName'],'|',dictEntryRow['HoursWorked'],'|',
              dictEntryRow['FullDate'], '|',dictEntryRow['EmployeeName'])
        strChoice = IO.input_yes_no_choice("Are you sure you want to delete this entry? (y/n) -  ")
        if strChoice.lower() == 'y':
            print(status)
        else:
            lstOfEmployeeHours.append(dictEntryRow)
            x = print("Entry Was Not Removed!")
        IO.input_press_to_continue()
        continue  # to show the menu

    elif strChoice == '2' and lstOfEmployeeHours == []:  # Handles the situation when there are no entries to remove
        print("There are no entries to remove!")
        IO.input_press_to_continue()
        continue  # to show the menu

    elif strChoice == '3':  # Save Data to File
        strChoice = IO.input_yes_no_choice("Save this data to file? (y/n) - ")
        if strChoice.lower() == "y":
            status, counter = Processor.write_data_to_file(strFileName, lstOfEmployeeHours)
            print(status)
            IO.input_press_to_continue()
        else:
            IO.input_press_to_continue("Save Cancelled!")
        continue  # to show the menu

    elif strChoice == '4':  # Reload Data from File
        print("Warning: Unsaved Data Will Be Lost!")
        strChoice = IO.input_yes_no_choice("Are you sure you want to reload data from file? (y/n) -  ")
        if strChoice.lower() == 'y':
            lstOfEmployeeHours,lstOfProjects, lstOfProjects_lower, status, counter = Processor.read_data_from_file(strFileName)
            print(status)
            IO.print_current_Entries_in_list(lstOfEmployeeHours)
            IO.input_press_to_continue()
        else:
            IO.input_press_to_continue("File Reload Cancelled!")
        continue  # to show the menu

    elif strChoice == '5':  # Show current data in the list of dictionary rows
        IO.print_current_Entries_in_list(lstOfEmployeeHours)  # Show current data in the list of dictionary
        IO.input_press_to_continue()
        continue  # to show the menu

    elif strChoice == '6':   # Add a project to list of projects
        IO.print_current_Projects_in_list(lstOfProjects)
        strChoice = IO.input_yes_no_choice("Are you sure you want to add a new project name? (y/n) -  ")
        if strChoice.lower() == 'y':
            lstOfProjects,lstOfProjects_lower, status = IO.input_new_project(lstOfProjects,lstOfProjects_lower)
            print(status)
            IO.input_press_to_continue()
        else:
            IO.input_press_to_continue("Adding New Project Cancelled!")
        continue  # to show the menu

    elif strChoice == '7':  # Exit Program
        input("Press ENTER to exit.")
        break  # and Exit

    else:
        print("Please choose from menu options")

