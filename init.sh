#!/bin/bash

function usage
{
    echo "Usage: $0 [newDjangoDir | -h]"
}

if [ $# -ne 1 -o $# -eq 0 -o "$1" == "-h" ]; then
  usage
  exit 1
fi

ORIG_DIR=`pwd`
PROJECT_PATH=$1
PROJECT_NAME=`basename $PROJECT_PATH`

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

cp -R requirements $PROJECT_PATH
cd $PROJECT_PATH

wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
$pythonBinPath virtualenv.py --no-site-packages .env

source .env/bin/activate

pip install -r requirements/default_install.txt
pip freeze > requirements/dev.txt

django-admin startproject $PROJECT_NAME
find $PROJECT_NAME -maxdepth 1 -mindepth 1 -exec cp -R '{}' .  \;
rm -fr $PROJECT_NAME

mkdir apps
touch apps/__init__.py

rm -f virtualenv.py virtualenv.pyc requirements/default_install.txt

deactivate

cd $ORIG_DIR
