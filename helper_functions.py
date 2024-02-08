import os
import time

def clear_screen():
    os.system("cls")

def title_crawl(text, text_speed):

    current_text = ""

    for character in text:
        current_text += character
        print(current_text)
        time.sleep(text_speed)
        clear_screen()

def text_crawl(text, line_length=60, text_speed=0.1):
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

def seperate_list(npc_list):

    list_start = "-- "

    for npc in npc_list:
        list_start += npc + " -- "

    return list_start

def add_adventurer(text):
    return "Adventurer: " + text