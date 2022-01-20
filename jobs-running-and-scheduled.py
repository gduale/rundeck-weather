#!/usr/bin/env python3
# coding: utf-8

import requests
import json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

import params

# Make request to the API (get all projects)
url = params.urlbase + "/projects" + params.token
r_projects = requests.get(url, headers=params.headers)

# Vars
running_jobs = []
current_project_jobs = {}

# Loop on projects name.
for element in r_projects.json():
  project = element["name"]

  # Get jobs for current project
  url_jobexecutions = params.urlbase + "/project/" + project + "/executions/running" + params.token
  r_jobs = requests.get(url_jobexecutions, headers=params.headers) # r_jobs is a dict
  d_jobs_list = r_jobs.json() # d_jobs_list is a dict (key : paging and executions)

  # Loop on jobs
  if d_jobs_list["executions"] != "":
    for values in d_jobs_list["executions"]: # 'values' is a dict
      if values["permalink"] != '': # if the job is running or scheduled
        running_jobs.append({"url":values["permalink"],"project":project,"job":values["job"]["name"],"status":values["status"],"user":values["user"]})

    # Save the data in current_project_jobs
    if running_jobs:
      current_project_jobs[project] = running_jobs

  # Empty vars for the next project loop
  running_jobs = []
  d_jobs_list = {}

# Get the current date to display it on the html page
the_date = datetime.now().strftime('%Y-%m-%d at %H:%M:%S')

# HTML part with Jinja
# Load templates folder in env
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# Load the html template
template = env.get_template('jobs-running-and-scheduled.html')

# Render the html page
output = template.render(running_jobs=current_project_jobs,the_date=the_date,rundeck_weather_version=params.rundeck_weather_version,job_running_active="active")

# Write the page to disk
file = open('html/jobs-running-and-scheduled.html','w')
file.write(output)
file.close()
