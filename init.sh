#!/bin/bash

function usage
{
    echo "Usage: $0 [newDjangoDir | -h]"
}

if [ $# -ne 1 -o $# -eq 0 -o "$1" == "-h" ]; then
  usage
  exit 1
fi

if [ ! -e $1 ]; then
  mkdir $1
  chmod 2750 $1
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

pyPath=`getPython2`

if [ "$pyPath" == "" ]; then
  echo "Error: python 2.x is required"
  exit 1
fi 

cp -R requirements $1
cd $1

wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
$pyPath virtualenv.py --no-site-packages .env

source .env/bin/activate

pip install -r requirements/default_install.txt
pip freeze > requirements/dev.txt
rm -f virtualenv.py virtualenv.pyc requirements/default_install.txt

deactivate

cd ..
