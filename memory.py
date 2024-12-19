"""
Program name: memory.py
Written By: Vladyslav Revutskyy


Tasks: 
    manipulates user input for the main program

High level pseudo code:
    1. create a way to create the file 
    2. create a function to clear the file
    3. create a function to append to the file
    4. create a function to feed the contet of the file to python dictionary
    5. remove individual pieces from the file]

This will be done using JSON files

Each task will look like this:

{
    "tasks_name":
    {
        "time": "",
        "improtance": "",
        "location": "",
    }
"""

import json

class memory:
    def __init__(self):
        with open('memory.json', 'w') as file: #creates an empty file
            file.close()

    def add_event(self, event, time, importance, location):
       task={ event: {
           "time": time,
           "importance": importance,
           "location" : location
           }
        }
       with open('memory.json', 'a') as file:
           json.dump(task, file, indent=4)
           file.close
