Semiautomatic django setup
==========================

How to start
------------

::

  ./init.sh newDjangoDir

will

* create newDjangoDir (chmod 2750) if not present
* download *virtualenv* and install it along with *pip* in the .env directory
* enter virtual environment
* install it will download and install *virtualenv* (by default in the .env directory).

Caveat
------

For best results, newDjangoDir should be yet present and with correct permissions

e.g. 2750 with apache standard group (usually 'apache' or 'http')

Riccardo Attilio Galli <riccardo@sideralis.org> [http://www.sideralis.org]
