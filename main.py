"""
Program name: main.py
Written By: Vladyslav Revutskyy

Tasks:
    get user input for tasks
    write to memory
    run unlosttime schedule and calendar add
"""

from memory import memory
from unlost import unlosttime

mem = memory()

while True:
	name = input("Task name (or leave blank to finish): ")  # get task name from user
	if name == "":
		break

	time = input("Task time (HH:MM): ")  # get time from user
	if time == "":
		time = ""

	importance = input("Task importance (1-5): ")  # get importance
	if importance == "":
		importance = "1"

	location = input("Task location: ")  # get location
	if location == "":
		location = ""

	duration = input("Task duration (minutes): ")  # get duration
	if duration == "":
		duration = "30"  # default duration if blank

	mem.add_task(name, time, importance, location, duration)  # add task with all details

mem.write()  # write tasks to memory.json

ut = unlosttime(mem)  # create unlosttime object
ut.run()  # run the scheduling and calendar adding
