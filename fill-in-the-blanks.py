# IPND Stage 2 Final Project

# For this project, I'll be building a Fill-in-the-Blanks quiz.
# The quiz will prompt a user with a paragraph containing several blanks.
# The user should then be asked to fill in each blank appropriately to complete the paragraph.
# This can be used as a study tool to help you remember important vocabulary!

import random
import time

# A list of replacement words to be passed in to the play game function. 
the_blanks  = ["___1___", "___2___", "___3___", "___4___", "___5___"]

# The following are some test strings to pass in to the play_game function. 
# These serve as questions and answers for the quiz based on difficulty level chosen.
easy_ques = '''A "Hello, World!" program is a computer program that ___1___ "Hello, World!" on a display device, 
often standard output. Being a very simple program in most ___2___ languages, it is often used to illustrate 
the basic ___3___ of a programming language for a working program. In Python this is particularly easy; all you 
have to do is type in: print "Hello, World!". This simple command uses the in-built function ___4___ to display 
"Hello, World!" on our computer screen.'''
easy_ans = ["prints", "programming", "syntax", "print"]

medium_ques = '''A function is created with the ___1___ keyword. You specify the inputs a ___2___ takes by 
adding ___3___ separated by commas between the parentheses. Functions by default return ___4___ if you don't 
specify the value to return. Arguments can be standard data types such as string, number, dictionary, tuple, 
and ___5___ or can be more complicated such as objects and lambda functions.'''
medium_ans = ["def", "function", "arguments", "None", "list"]

hard_ques = '''A ___1___ allows us to execute a statement or group of statements multiple times. These are 
of 3 types: ___2___ (checks condition first), ___3___ (executes atleast once and then checks condition) 
and ___4___ (guess!!!). To break out of a ___1___, we use ___5___.'''
hard_ans = ["loop", "for", "while", "nested", "break"]

""" Implemeted the logic of showing progress to the player after he guesses a blank correctly.
    Below is the implementation case where player guesses a blank correctly and gets new prompt that
    shows the correct answer and new prompt for the next blank.
    This function basically updates ml_string after each correct user input AND does take into account
    if or not we are updating, for example, ___2___ or ___2___, """
def player_progress(ml_string, replacement, user_input_case):
    i = 0 # counter to loop through entire ml_string and update as appropriate.
    while i < len(ml_string):
        if replacement == ml_string[i]:
            ml_string[i] = user_input_case
            i += 1 
        else:
            if replacement in ml_string[i]:
                ml_string[i] = ml_string[i].replace(replacement, user_input_case)
                i += 1
        i += 1
    return ml_string

""" Check and/or correct the case (upper/lower) of user input.
    Some special inputs (like None, etc. where ideally case must be taken into account) are handled."""
def correct_case_user_input(user_input):
    if user_input in ["None", "True", "False"]: # To handle some specific keywords of python.
                                                # Note: This list is not exhaustive. 
                                                # We have included only the words we have come across thus far.
                                                # For these words to serve as correct answer, they must be 
                                                # entered the same way, i.e., "None", "True", etc.
                                                # This means the user is expected to know that Python
                                                # considers "True" valid not "true" for a Boolean expr.
        user_input_case = user_input
    else:
        user_input_case = user_input.lower()
    return user_input_case

""" Determine position of an input in the correct answer list.
    The index from this is used to check ith user input with ith correct answer."""
def ans_pos(parts_of_speech, word):
    for i in [i for i,x in enumerate(parts_of_speech) if x in word]:
        index = i # index variable denotes the position of the answer in correct answer list
                  # index is used to strictly check ith user input with ith correct answer
    return index

""" This function updates the blank after checking the correctness of user input."""
def update_blank(parts_of_speech, word, replacement, correct_ans, replaced, temp_string, ml_string):
    i = 0
    while i < 5: # This loop is inserted to limit number of attampts for a particular answer to 5
        index = ans_pos(parts_of_speech, word)
        user_input = raw_input("\n" + "Type in the answer for " + replacement + ": ")
        user_input_case = correct_case_user_input(user_input) 
        if user_input_case == correct_ans[index]: # Compare user input with the correct answer
                                                  # correct_ans variable denotes the right answer to the blank
            word = word.replace(replacement, user_input_case)
            replaced.append(word)
            i, temp_string, ml_string = 5, temp_string.replace(replacement, user_input_case), player_progress(ml_string, replacement, user_input_case)
            print "Look, what you got - " + "\n" + temp_string
        else:
            print "Wrong answer!!! You have " + str(4-i) + " attempts left."
            i = i + 1
            if i == 5:
                print "\n" + "\n" + "You have lost the Quiz. Try again later." + "\n"
                replaced = "Fail"
    return replaced, temp_string, ml_string

""" Checks if a word in parts_of_speech is a substring of the word passed in."""
def word_in_pos(word, parts_of_speech):
    for pos in parts_of_speech:
        if pos in word:
            return pos
    return None
        
""" Plays a full game of mad_libs. A player is prompted to replace words in ml_string, 
    which appear in parts_of_speech with their own words.
    The logic was taken from Udacity's INPD Worsession 5 - def play_game(ml_string, parts_of_speech)."""
def play_game(ml_string, parts_of_speech, correct_ans):    
    replaced = []
    temp_string = ml_string # variable used for re-printing the question after each correct answer.
    ml_string = ml_string.split()
    for word in ml_string:
        replacement = word_in_pos(word, parts_of_speech)
        if replacement != None:
            replaced, temp_string, ml_string = update_blank(parts_of_speech, word, replacement, correct_ans, replaced, temp_string, ml_string)
            if replaced == "Fail":
                break
        else:
            replaced.append(word)
    if replaced != "Fail": #
        print "\n" + "\n" + "Congratulations! You have won the Python Programming Quiz." "\n"
    replaced = " ".join(replaced)
    return replaced

""" Depending on the choice of the player, this function presents question to the player."""
def assign_ques(choice):
    print "Here is your question:" + "\n"
    time.sleep(1)
    if choice == "easy":
        ques, ans = easy_ques, easy_ans
    elif choice == "medium":
        ques, ans = medium_ques, medium_ans
        ans = medium_ans
    elif choice == "hard":
        ques, ans = hard_ques, hard_ans
    print ques
    return ques, ans

""" The game starts from this function.
    This function gets player input for the difficulty level he wants to play. 
    Determines if the choise is valid."""
def main():
    print "\n" + "\n" + "\n" + "Python Programming Quiz" + "\n" + "\n"
    madlibs = ["easy", "medium", "hard"]
    while True:
        level = raw_input("Please select a game difficulty level (easy, medium, hard) by typing it in OR hit Enter to exit >> ")
        print "\n" + "\n"
        if not level:
            break
        else:
            choice = level.lower()
            if choice in madlibs:
                ques, ans = assign_ques(choice)
                play_game(ques, the_blanks, ans)
            else:
                print "Sorry, that was not a valid option." + "\n" + "\n"

main()

# DO NOT TOUCH THE ABOVE CODE

