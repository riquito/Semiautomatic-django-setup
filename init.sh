#!/bin/sh

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

cp -R requirements $1
cd $1

curl -O https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python2 virtualenv.py --no-site-packages .env

source .env/bin/activate

pip install -r requirements/default_install.txt
pip freeze > requirements/dev.txt
rm -f virtualenv.py virtualenv.pyc requirements/default_install.txt

deactivate

cd ..
