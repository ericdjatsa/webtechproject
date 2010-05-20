#!/bin/bash

if [ $# -lt 2 ]
then
	echo "Missin parameter!Syntax : ranker.sh python_script search_string,  (python_script = actors.py,writers.py,directors.py...) ,(search_string= Freeman,Nicole Kidman,Georges Clooney,..."
	exit -1
fi
#$1 is the python scrypt
#$2 is the search_string

export DJANGO_SETTINGS_MODULE=settings
python -i $1 $2 #the i option is to open an interactive shell when the script finishes its execution
