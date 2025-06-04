"""
Program name: memory.py
Written By: Vladyslav Revutskyy


Tasks: 
    manipulates user input for the main program

High level pseudo code:
    1. create a way to create the file 
    2. create a function to clear the file
    3. create a function to append to the file
    4. create a function to feed the content of the file to python dictionary
    5. remove individual pieces from the file

This will be done using JSON files

Each task will look like this:

{
    "tasks_name":
    {
        "time": "",
        "importance": "",
        "location": "",
        "duration": ""
    }
}
"""

import json  # imports the json library 

class memory:  # create the memory class
	def __init__(self):  # initiates itself
		self.tasks = {}  # creates an empty dictionary

	def add_task(self, name, time, importance, location, duration):  # adds a task to the dictionary we need to pass the name of the task, time, importance, location and duration
		self.tasks[name] = {  # store task info as dictionary value
			"time": time,
			"importance": importance,
			"location": location,
			"duration": duration  # added duration field
		}

	def remove_task(self, name):  # removes a task from the dictionary
		del self.tasks[name]

	def write(self):  # writes the dictionary to memory.json
		with open("memory.json", "w") as file:  # opens the file 
			json.dump(self.tasks, file, indent=4)  # writes the dictionary to the file
			file.close()

	def read_json(self):  # reads everything from memory.json
		with open("memory.json", "r") as file:  # opens memory.json in read mode
			self.tasks.clear()  # clears the dictionary
			self.tasks.update(json.load(file))  # writes everything from the file into the dictionary
			return(self.tasks)  # will return the values of the dictionary if needed in a variable

