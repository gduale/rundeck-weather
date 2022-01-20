#!/usr/bin/env python3
# coding: utf-8

import requests
import json
from datetime import datetime
import sys
from jinja2 import Environment, FileSystemLoader

import params

# Vars
final = dict()

# Make request to the API (get all projects)
url = params.urlbase + "/projects" + params.token
r_projects = requests.get(url, headers=params.headers)

# Loop on projects name.
for element in r_projects.json():
  project = element["name"]
  project_url = params.url_rundeck + "project/" + project + "/jobs"

  # Get SCM export status for current project
  url_jobexecutions = params.urlbase + "/project/" + project + "/scm/export/status" + params.token
  r_jobs = requests.get(url_jobexecutions, headers=params.headers) # r_jobs is a dict
  d_jobs = r_jobs.json() # d_jobs is a dict

  if d_jobs["message"] == "No export plugin configured":
    final[project] = [project_url, d_jobs["message"]]
  else:
    if d_jobs["synchState"] == "EXPORT_NEEDED":
      final[project] = [project_url, d_jobs["message"]]

# Get the current date to display it on the html page
the_date = datetime.now().strftime('%Y-%m-%d at %H:%M:%S')

# HTML part with Jinja
# Load templates folder in env
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# Load the html template
template = env.get_template('jobs-to-commit.html')

# Render the html page
output = template.render(final=final,the_date=the_date,rundeck_weather_version=params.rundeck_weather_version,job_commit_active="active")

# Write the page to disk
file = open('html/jobs-to-commit.html','w')
file.write(output)
file.close()
