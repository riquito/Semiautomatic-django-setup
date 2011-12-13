#!/bin/bash

function usage
{
    echo "Usage: $0 [newDjangoDir | -h]"
}

if [ $# -ne 1 -o $# -eq 0 -o "$1" == "-h" ]; then
  usage
  exit 1
fi

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_PATH=$1
PROJECT_NAME=`basename $PROJECT_PATH`

ORIG_UMASK=`umask`
umask 0027 # -rw-r----- # files or directories needing group write
           # drwxr-x--- # will get it later

if [ ! -e $PROJECT_PATH ]; then
  mkdir $PROJECT_PATH
  chmod 2750 $PROJECT_PATH
fi

getPython2 ()
{
  local mostRecent=""
  local res=""
  for i in /usr/bin/python*; do
    echo $i | grep -q "python2\(\.[5-7]\)$";
    res=$?
    if [ $res -eq 0 ]; then
      mostRecent=$i
    fi
  done

  echo $mostRecent;
}

pythonBinPath=`getPython2`

if [ "$pythonBinPath" == "" ]; then
  echo "Error: python 2.x is required"
  exit 1
fi 

cd $PROJECT_PATH

wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
$pythonBinPath virtualenv.py .env # by default ignore system packages

source .env/bin/activate # enter virtual environment

find "$SCRIPT_DIR/base_project/" -maxdepth 1 -mindepth 1 -exec cp -R '{}' .  \;

# Install needed libraries
mv requirements/default_install.txt requirements/dev.txt
pip install -r requirements/dev.txt
#pip freeze > requirements/dev.txt # at present is missing dependencies

# Some directories must be writable by webserver group
chmod g+w var/log/ var/media var/tmp

# Give logs friendly permissions (current user will be the owner, group will be able to modify them)
touch var/log/apache-access.log
touch var/log/apache-error.log
touch var/log/django.log
chmod g+w var/log/*.log

# Do a default round of django calls to have all up and running
# (will work for both develop and production settings)
python manage.py makemessages -a
python manage.py compilemessages
python manage.py collectstatic --noinput
python manage.py compress --force

# Remove unneeded files
find . -name "*.pyc" -exec rm '{}' \;
rm virtualenv.py
rm -fr build

deactivate # exit virtual environment

umask $ORIG_UMASK

cd $SCRIPT_DIR
