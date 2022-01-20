#!/bin/bash

okfail() {
  if [ $? -eq 0 ]; then
    echo -e "[\033[32m OK \033[00m] $1"
  else
    echo -e "[\033[31mFAIL\033[00m] $1"
    codeglobal=1
    [ -n "$2" ] && exit 1
  fi
}
codeglobal=0

DSTAPP="/opt/rundeck-weather"
DSTHTTP="/srv/http/rundeck-weather"
mkdir -p $DSTAPP
mkdir -p $DSTHTTP

#Ensure requests is installed
r=$(pip3 show requests)
if [ $? -ne 0 ];then
  pip3 install requests || echo "Install requests via pip3 failed, exit script."; exit 1
fi

#Run python
cd $DSTAPP
./jobs-digest.py
okfail "jobs-digest.py"

./jobs-running-and-scheduled.py
okfail "jobs-running-and-scheduled.py"

./jobs-to-commit.py
okfail "jobs-to-commit.py"

if [ $codeglobal -eq 0 ];then
  mkdir -p $DSTHTTP
  cp -a html/* $DSTHTTP/
  cd $DSTHTTP/
  ln -fs jobs-digest.html index.html
else
  echo "Python exec error."
fi

exit $codeglobal
