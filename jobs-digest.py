#!/usr/bin/env python3
# coding: utf-8

import requests
import json
from datetime import datetime
import params
from jinja2 import Environment, FileSystemLoader


# Make request to the API (get all projects)
url = params.urlbase + "/projects" + params.token
r_projects = requests.get(url, headers=params.headers)

# Init vars
d_job = dict()
final = dict()
final_html = ""

#Loop on project's name.
for element in r_projects.json():
  project = element["name"]

  # Get jobs list for current project
  url_joblist = params.urlbase + "/project/" + project + "/jobs" + params.token
  r_joblist = requests.get(url_joblist, headers=params.headers)
  job_list = r_joblist.json()

  # Loop on jobs list
  for job in job_list:
    job_name = job["name"]
    url_job_executions = params.urlbase + "/job/" + job["id"] + "/executions" + params.token + "&max=1"
    r_job_executions = requests.get(url_job_executions, headers=params.headers)
    d_executions = r_job_executions.json() #d_executions is a dict (keys : paging and executions)

    # If the job has at least one execution
    if d_executions["executions"] != "":
      for values in d_executions["executions"]: #here "values" is a dict
        # Get successful and failed nodes
        if "successfulNodes" in values:
          node_succes = values["successfulNodes"]
        else:
          node_succes = "None"
        if "failedNodes" in values:
          node_fail = values["failedNodes"]
        else:
          node_fail = "None"

        # Get the job end date
        try:
          end_date = values["date-ended"]["date"].split('T')
          end_hour = end_date[1][:-1]
        except KeyError:
          end_date = "No end date."
          end_hour = "No end hour."

        start_date = values["date-started"]["date"].split('T')
        start_hour = start_date[1][:-1]

    # Construct a dict with the data for the current job
    d_job[job_name] = { "status":values["status"],
                        "nodeS":node_succes,
                        "nodeF":node_fail,
                        "start_date":start_date,
                        "start_hour":start_hour,
                        "end_date":end_date,
                        "end_hour":end_hour,
                        "url":values["permalink"]}

  # End of "for job in job_list:"
  final[project] = d_job
  d_job = {}

# Get the current date to display it on the html page
the_date = datetime.now().strftime('%Y-%m-%d at %H:%M:%S')

# HTML part with Jinja
# Load templates folder in env
file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# Load the html template
template = env.get_template('jobs-digest.html')

# Render the html page
output = template.render(final=final,the_date=the_date,rundeck_weather_version=params.rundeck_weather_version,job_digest_active="active")

# Write the page to disk
file = open('html/jobs-digest.html','w')
file.write(output)
file.close()
