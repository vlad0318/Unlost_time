'''
* Name: Vladyslav Revutskyy
* Class Name: CSE223
* Date: 06/03/2025
* Program Name: unlost.py

* Program description:
* This program takes tasks stored in a memory.json file and organizes them using a local Ollama model.
* The resulting schedule is then added to Google Calendar.

* Functions:
* __init__: initializes the memory object
* read_tasks: loads tasks from memory
* schedule_tasks: sends tasks to Ollama for scheduling
* parse_schedule: parses the JSON schedule returned by Ollama
* authenticate_calendar: authenticates with Google Calendar API
* add_to_calendar: adds each task from the schedule to the calendar
* run: runs the entire process
'''

import json  # imports the JSON module
import datetime  # imports the datetime module
import ollama  # imports the ollama module
import os  # imports the os module
from google.oauth2.credentials import Credentials  # imports credentials handling
from google_auth_oauthlib.flow import InstalledAppFlow  # imports the installed app flow for authentication
from googleapiclient.discovery import build  # imports the calendar API builder
from google.auth.transport.requests import Request  # imports the request handler for refresh

SCOPES = ['https://www.googleapis.com/auth/calendar']  # defines the Google Calendar API scope

class unlosttime:
	def __init__(self, mem):  # constructor for unlosttime class
		self.mem = mem  # stores memory handler
		self.tasks = {}  # dictionary to store tasks
		self.schedule = {}  # dictionary to store scheduled tasks

	def read_tasks(self):  # reads tasks from the memory file
		self.tasks = self.mem.read_json()  # loads tasks from memory.json

	def schedule_tasks(self):  # sends prompt to local AI to schedule tasks
		prompt = (  # builds the prompt line by line
			"Organize the following tasks into a realistic schedule for today.\n"
			"Each task must start at the exact given time.\n"
			"Minimum duration per task: 30 minutes.\n"
            "If tasks are scheduled at the same time go with the most important one and reschedule the less important one for a different time\n"
			"Return JSON with a list named 'tasks'. Each task must include:\n"
			"- name: string\n- start_time: string in HH:MM 24-hour format\n- duration: integer (minutes)\n\nTasks:\n"
		)
		for name, details in self.tasks.items():  # adds each task to the prompt
			prompt = prompt +  f"- {name} (start_time: {details['time']}, importance: {details['importance']}, location: {details['location']}, duration: {details['duration']})\n"  # added duration here

		response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])  # sends prompt to Ollama
		self.schedule = self.parse_schedule(response['message']['content'])  # stores the parsed schedule

	def parse_schedule(self, response_str):  # parses JSON from Ollama's response
		try:
			start = response_str.find('{')  # find start of JSON
			brace_count = 0  # set counter for braces
			end = -1  # initialize end
			for i in range(start, len(response_str)):  # go through the response
				if response_str[i] == '{':
					brace_count = brace_count + 1  # increment for each opening brace
				elif response_str[i] == '}':
					brace_count = brace_count - 1  # decrement for each closing brace
				if brace_count == 0:  # if braces are balanced
					end = i + 1
					break
			if end == -1:
				return {}  # return empty if braces do not match
			json_str = response_str[start:end]  # extract JSON string
			return json.loads(json_str)  # parse and return
		except Exception:
			return {}  # return empty if parsing fails

	def authenticate_calendar(self):  # handles Google Calendar authentication
		creds = None  # initialize credentials
		if os.path.exists('token.json'):  # check for existing token
			creds = Credentials.from_authorized_user_file('token.json', SCOPES)
		if not creds or not creds.valid:  # if credentials not valid
			if creds and creds.expired and creds.refresh_token:  # try to refresh
				creds.refresh(Request())
			else:
				flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)  # start auth flow
				creds = flow.run_local_server(port=0)  # run local server
				with open('token.json', 'w') as token:  # save token
					token.write(creds.to_json())
		return build('calendar', 'v3', credentials=creds)  # return calendar service

	def add_to_calendar(self):  # adds scheduled tasks to Google Calendar
		today = datetime.date.today()  # gets today’s date
		if 'tasks' not in self.schedule:  # if no tasks, stop
			return
		service = self.authenticate_calendar()  # authenticate calendar
		for task in self.schedule['tasks']:  # go through each task
			name = task['name']  # get task name
			start_str = f"{today}T{task['start_time']}:00"  # build start time string
			start_dt = datetime.datetime.fromisoformat(start_str)  # convert to datetime
			end_dt = start_dt + datetime.timedelta(minutes=task['duration'])  # calculate end time
			event = {  # build event details
				'summary': name,
				'location': self.tasks[name]['location'],
				'start': {
					'dateTime': start_dt.isoformat(),
					'timeZone': 'America/Los_Angeles'
				},
				'end': {
					'dateTime': end_dt.isoformat(),
					'timeZone': 'America/Los_Angeles'
				}
			}
			service.events().insert(calendarId='primary', body=event).execute()  # insert into calendar

	def run(self):  # runs the whole process
		self.read_tasks()  # load tasks
		self.schedule_tasks()  # schedule them
		self.add_to_calendar()  # upload to calendar

