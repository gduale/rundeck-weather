# Rundeck weather

This project generate web pages by requesting the Rundeck API.

## Description of scripts

 - jobs-digest.py : Generate a web page containing all the jobs's status for all projects present in your Rundeck instance.
 - jobs-running-and-scheduled.py : Generate a web page containing all jobs currently running and all jobs scheduled by a user.
 - jobs-to-commit.py : Generate a web page containing all jobs there are not commited in your SCM yet.

The html pages are generated in the "html" directory, present in the current directory.

They are named like the script, for example the script jobs-digest.py generate a web page here "html/jobs-digest.html".

## API Token

You need to export in an environment variable, the rundeck api token in a variable named "RD_TOKEN"

## Rundeck API endpoint

Adapt the variable "urlbase" in the params.py file, to match your rundeck api endpoint.

## LICENCE

 - This software is licensed under the GPL version 3.
 - You can find the license in LICENSE.txt in this repository.

## Thanks

 - Thanks to [Virtual-Expo](https://www.virtual-expo.com) for allowing me to release this code.
