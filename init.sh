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

GROUP_PROJECT_DIR=`stat -c %G $PROJECT_PATH`;
APACHE_GROUP=`grep -E "(www-data|www|http|apache):" /etc/group|cut -d ':' -f 1`

if [ "$GROUP_PROJECT_DIR" != "$APACHE_GROUP" ]; then
  
  groups | grep -q "$APACHE_GROUP" # is user in the apache group ?
  
  if [ $? -eq 1 -a "`id -u -n`" != "root" ]; then
    echo "Directory's group is '$GROUP_PROJECT_DIR' and you don't seem to be in apache group '$APACHE_GROUP'. Files inside that directory will inherit his group, so it would be best to set it to the apache group (via \"sudo chgrp $APACHE_GROUP $PROJECT_DIR\"). "
    read -r -p "Do you want to exit now to correct the problem ? (y/n) " response
    case $response in
        [yY][eE][sS]|[yY]) 
            exit
            ;;
    esac
  
  else
    chgrp $APACHE_GROUP $PROJECT_PATH
  fi
fi


if [ "`stat -c %a $PROJECT_PATH`" != "2750" ]; then
    groups | grep -q `stat -c %G $PROJECT_PATH`
    if [ $? -eq 0 ]; then
      chmod 2750 $PROJECT_PATH
    else
      echo
      echo "Cannot set permissions on $PROJECT_PATH. Please manually run \"sudo chmod 2750 $PROJECT_PATH\""
      exit;

    fi
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
