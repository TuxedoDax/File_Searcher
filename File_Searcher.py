#---------------
#Created by: TuxedoDax
#Started on: May 22nd 2024
#Finished on: May 24th 2024
#This program will search for any category of file (I.E: Photos, Documents, etc.) from a specified location, and copy them to a new location.
#---------------


import os
import binfiles
import shutil
from datetime import datetime

def Filetyper():
    #Take input from user about the filetype.
    print("The please select from the following list of categories:")
    print("text, image, development, spreadsheet, system, executable, archive, backup, audio, database, presentation, video, bookmark, pim, shortcut, unidentifiable.\n")
    filetype = input("\nWhat kind of file are you looking for?:\n")
    return (filetype)

def Pather():
    #Take input from the user about the path.
    path = input("\nWhere do you want to look for this file?:\n")
    return(path)

def choice_verification(filetype,path,verification):
    if verification == "False":
        print("\n")
        #Figuring out which option was incorrect.
        error_check_input = input("Which option is wrong? Press 1 for the filetype, or 2 for the path\n")
        print("The value from error check input was", error_check_input)
        
        #Confirming the Filetype
        if error_check_input == "1":
            print("\nWe will confirm the Filetype.")
            filetype = Filetyper()
        
        #Confirming the Path
        if error_check_input == "2":
            print("\nWe will confirm the Path.")
            path = Pather()

    #If the verification was correct
    else:
        print("\nLet me look for any matches.")
        return(filetype,path)
    #Returning with the corrected information.
    return(filetype,path)

def filetype_and_path():
    #Obtain the filetype we want to look for.
    filetype = Filetyper()
    #Obtain the path we are looking in.
    path = Pather()
    print("\n")
    print("You chose a filetype of:", filetype, "and a path of:", path)
    verification = input("Was this correct? (True/False)\n")

    #As long as there is something wrong with the filetype or path, keep iterating until it's correct.
    while verification == "False":
        #Re-run the selectiosn for Filetype or Path
        filetype, path = choice_verification(filetype,path,verification)
        print("\nDoes the following information look correct?","\nFiletype:", filetype, "\nPath: ", path)
        verification2 = input("(Y/N): ")
        if verification2 == "Y":
            verification = "True"
    return(filetype,path)

def File_Detective(filetype, path):
    search_filetype = filetype
    #list for files that match
    file_matches = []
    #comparing the specified category to the ones in the binfiles.
    bin_check = getattr(binfiles, filetype)
    for path, subdirs, files in os.walk(path):
        #for every file we can find in the specified path.
        for file in files:
            #Split up the files that are found, and leave just the file name and extension.
            file_split = os.path.splitext(file)
            file_name = file_split[0]
            file_extension = file_split[1]
            file_checker = file_extension.lstrip(".")
            #if the stripped extension is in the list we assigned to the category
            if file_checker in bin_check:
                print("\nI found a match, that file is:", file)
                file_path = path + "/" + file
                file_path = os.path.normpath(file_path)
                file_matches.append(file_path)
    return(file_matches)

def path_normalization(path):
    #This ensures that the file path is correct for using in os library modules.
    path = os.path.normpath(path)
    return(path)

def folder_creation(filetype):
    #present working directory information
    pwd = os.getcwd()
    #getting the current date
    current_date = datetime.today().strftime('%Y-%m-%d')
    #creating a path to check using the pwd, current date and filetype the user specified at the beginning of the script.
    path = (pwd + "\\" + current_date + "_" + filetype)
    destination_folder = path_normalization(path)
    #Check to see if the destination_folder already exists.
    folder_exists = os.path.exists(destination_folder)
    #Create it if it doesn't exist.
    if not folder_exists:
        os.makedirs(destination_folder)
        print("\nHad to make the destination folder: " + destination_folder)
    else:
        print("\nDestination folder already existed.")
    return(destination_folder)

def number_remover(filename):
    #removing the all characters BUT the last three characters on the file name
    check_for_number = filename[-3:]
    #check for a left brace.
    if "(" in check_for_number:
        #check for a right brace.
        if ")" in check_for_number:
            #check if any of the 3 characters are a number.
            if any(char.isdigit() for char in check_for_number):
                filename = filename[:-3]
    return(filename)

def duplicate_file_checker(dst):
    #splitting the path up to get just the file name.
    filename = dst.rsplit("\\")
    #putting the file name into a variable.
    name_of_file = str(filename[-1])
    #the filename broken down into two parts, name and extension.
    name_of_file_no_extension = name_of_file.rsplit(".")
    filename = name_of_file_no_extension[0]
    extension = name_of_file_no_extension[1]

    file_namer = os.path.exists(dst)

    filename = number_remover(filename)

    name_appender = 1
    while file_namer == True:
        #Remove the (number) if it appears in the file name.
        filename = number_remover(filename)
        #add the current value of name_appender within brackets to the filename "(1)".
        filename = filename + "(" + str(name_appender) + ")"
        #combine the new number, a "." and the previous extension onto the filename.
        full_file_name = filename + "." + extension
        ### --- This section appears because there was a problem error handling renaming the file from (1) to (2), instead of (1)(2).
        #I take the original destination we wanted to use, and break it down.
        output_raw = dst.rsplit("\\") #####
        #remove the original filename.
        output_raw = output_raw[:-1]  #####
        #get the length of the new list.
        output_size = len(output_raw)
        output_fixer = 0
        output_path = ""
        #while our fixer doesn't equal the same size as our output_size length
        while output_fixer != output_size:
            #keep adding the parts back together. This is to create a string with the original information minus the filename.
            output_path = output_path + (output_raw[output_fixer] + "/")
            output_fixer = output_fixer + 1
        #once we have the required path, add the "/" and the new name we want to use on the file name.
        file_and_path = (output_path + "/" + full_file_name)
        file_and_path = path_normalization(file_and_path)
        file_name_checker = os.path.exists(file_and_path)
        #if the number name already exists, add one to the number we are using.
        if file_name_checker == True:
            name_appender = name_appender + 1
        #if the number isn't in use, use that number for the path.
        if file_name_checker == False:
            file_namer = file_name_checker
            updated_path = file_and_path
            return(updated_path)
    #if there was no number problem to begin with, just use the path.
    else:
        updated_path = dst
        return(updated_path)

def file_copier(filetype,file_matches):
    #Counter for iterating over my list
    myCounter = 0
    #Create the folder we will store everything in.
    destination_folder = folder_creation(filetype)
    for file in file_matches:
        #Normalize the path
        path = file_matches[myCounter]
        filename = path_normalization(path)
        #We will be using this normalized src for the copying later.
        src = filename
        #Split the filename up by every \ (note that the "\\" is the only way to do this.)
        filename = filename.rsplit("\\")
        #Take the last entry from the list within filename, and set filename equal to that.
        filename = filename[-1]
        #Set this DST to wherever you want to save the files.
        path = (destination_folder + "/" + filename)
        dst = path_normalization(path)
        dst = duplicate_file_checker(dst)
        #Copying the file from src to dst.
        shutil.copyfile(src, dst)
        #Iterate the counter to move onto the next thing.
        myCounter = myCounter + 1
        print("\nI copied " + filename + "\nfrom " + src + "\nto " + dst)
        print("\n")

filetype, path = filetype_and_path()
file_matches = File_Detective(filetype,path)
file_copier(filetype,file_matches)