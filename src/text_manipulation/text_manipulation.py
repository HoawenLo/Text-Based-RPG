import os
import time
import re

def combine_characters(front_input_string, back_input_string, line_length):
    """Combines two strings with variable number of space in middle.
    This is dependant on the line length. The line length is a set constant.
    More longer line length will lead to more spaces in the middle.
    
    Args:
        front_input_string: A string which will be at the front of the line.
        back_input_string: A string which will be at the back of the line.
        line_length: Default is 51. The length of line.
        
    Returns: Returns a combined string with the front input string at the 
    front, followed by some calculated spaces and finally the back input
    string."""

    spaces_amount = line_length - len(front_input_string) - len(back_input_string)

    for _ in range(spaces_amount):
        front_input_string += " "
    
    string_output = front_input_string + back_input_string

    return string_output

def clear_screen():
    """Clear the output screen. Useful in text crawl."""
    os.system("cls")

def character_crawl(text, text_speed=0.01):
    """Text crawl the title. Crawls single characters.
    
    Args:
        text: The title to be crawled.
        text_speed: The speed to the crawl the text."""
    current_text = ""

    for character in text:
        current_text += character
        print(current_text)
        time.sleep(text_speed)
        clear_screen()

def word_crawl(text, line_length=60, text_speed=0.1):
    """Used to crawl text. Crawls words instead of 
    single characters.
    
    Args:
        text: The sentence to be crawled.
        line_length: Sets the length of the line.
        If has a large body of text, will move 
        onto next line if line length reached."""

    words = text.split()
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= line_length:
            current_line += word + " "
        else:
            print(current_line)
            current_line = word + " "
            time.sleep(text_speed)

        print(current_line, end="\r")
        time.sleep(text_speed)

    print(current_line)

def remove_underscore(input_string):
    """Removes underscore and return string with space instead."""
    modified_string = re.sub("_", " ", input_string)
    return modified_string

def add_adventurer(text):
    """Add adventurer to the start of the next.
    
    Args:
        text: The text to add adventurer to."""
    return "Adventurer: " + text

def list_chat_options(chat_options):
    """Takes a dictionary of chat options and prints it.
    
    Args:
        chat_options: The chat options to print."""
    
    for num, text in chat_options.items():
        display_text = num + ": " + text
        print(display_text)


def seperate_list(input_list):

    list_start = ""

    for i, val in enumerate(input_list):
        list_start += f" -- {i} {val} "

    list_start += " --"

    return list_start



