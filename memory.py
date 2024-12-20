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
        "importance": "",
        "location": "",
    }
"""

import json

class memory:
    def __init__(self):
        self.tasks={}

    def add_task(self, name, time, importance, location):
        self.tasks[name]={"time":time,
                    "importance":importance,
                    "location":location}

    def remove_task(self, name):
        del self.tasks[name]
    def write(self):
        with open("memory.json","w") as file:
            json.dump(self.tasks,file, indent=4)
            file.close

    def read_json(self):
        with open("memory.json","r") as file:
            self.tasks.clear()
            self.tasks.update(json.load(file))
            return(self.tasks)
