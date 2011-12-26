==========================
Semiautomatic django setup
==========================

::

  ./init.sh path/to/your/new/django/project

It's that simple!

You'll get a django project with a professional structure (see below) and 
permissions done right, multiple settings (by default for development and 
production, you can add as many as you need), a working filesystem based cache, 
logging, javascript/css grouping and minification, localization, an apache 
virtualhost configuration that will be quite ready, git ignore files 
pre-configured to just init your repository and start committing and a fabric 
file to automate the most repetitive tasks. Obviously in your virtualenv 
environment and without forgetting a barebone HTML5 layout.

With no magic. You can change everything.

You are expected to change the settings to match your needs, but be warned that 
the project will just work. The tedious and error prone tasks are done, so you 
can start to develop pretty soon (you'll still have to review the settings to 
change things like the timezone but it's a matter of minutes, and you want to 
know the settings anyway).

Why?
====

After the nth time that I started a Django project, created a 
devel/stage/production friendly structure, set the most basics things and be 
swarmed by little mistakes (logs nowhere to be found, permissions not really 
correct, cache inconsistencies) I decided to automatize the start of the 
project.

A project must start simple and start well, have a rational structure and a 
minimum set of working features (like cache and javascript 
grouping/minification). They don't need to be the top right at first, but they 
must work and be upgradeable later (like an initial file caching instead of 
memcache).

How to use it?
==============

::

  ./init.sh path/to/your/new/django/project

If the directory does not exist, it will create it. The script will try to set 
group and permissions on his own if your user has enough rights. If it can't it 
will propose you what to do.

Why the documentation is so long?
=================================

While simple, there are a lot of things done under the hood. You can either 
read the code (it's not that much, really) or read this manual to know exactly 
what has been configured. 

What does it do?
================

* create the project directory (chmod 2750) if not present, and enter it
* set umask to 0027 (others can't read the files and group can only read as 
  default)
* download *virtualenv* and install it along with *pip* in the .env directory
* activate virtual environment
* install the libraries listed in base_project/requirements/default_install.txt
* copy the content of base_project into the directory
* add group write permissions to some directories (e.g. /var/tmp and /var/log)
* create some empty log files so that you own them
* collect default locale strings and static files, compress what it can (to 
  prove it works)
* exit from virtualenv, restore original umask and enter the original directory

How will be the project structured?
===================================

* **apps/** # here stay your applications
* **configs/** # here stay server configurations. There are a couple defaults
  
  * **develop/**
  * **production/**
* **fabfile/** # fabric files goes here
* **locale/** # project level locale directory for generic internazionalization
  
  * **en/**
    
    * **LC_MESSAGES/**
* **requirements/** # whenever you pip freeze your dependencies, put them here
* **static/** # here are project level static files (e.g. favicon or global css)
  
  * **admin/**
  * **public/**
* **templates/** # project level templates
  
  * **layout/** # templates that give a whole page structure
  * **views/** # generic views not linked to an app
* **var/** # variable files
  
  * **log/** # logs, obviously
  * **media/** # user uploaded files
  * **static/** # collected static files of the whole project
  * **tmp/** # directory for temporary files


I ran the script. What now?
===========================

Start versioning your project
-----------------------------

If you use git all the details about ignoring settings and logs are yet done.

So just init your project

::

  git init .
  git add .
  git commit -m "First commit"

If you use another vcs as mercurial or bazaar, you'll have to do your homework.

Please ignore the content of 

* .env/
* var/media/
* var/static/
* var/log/
* var/tmp/
* local_settings.py # anywhere
* fabfile/*_settings.py
* any *.pyc *.pyo 


Check that it works
-------------------

Here and later, remember to enter the virtualenv environment first

::

   source .env/bin/activate

*Start the server with development settings*

::
  
  python manage.py runserver

Check on http://localhost:8000/ that you see a welcome page.
Read the HTML source, you'll notice multiple CSS files loaded (normalize.css 
and main.css).

Write an unexistent url to see the 404 django error page.

*Start the server with production settings*

::
  
  TARGET="production" python manage.py runserver

You'll see the same page as before but at refresh it will not update the time 
written on it (cache enabled). Check the page's source, you'll now find a 
single compressed file CSS (so CSS are being aggregated and compressed). If you 
try to load a random url the site's default 404 page is presented.

If something didn't work please submit a ticket.

Understand the settings structure
---------------------------------

Settings are stored in

configs/<confname>/settings.py

To create a configuration for your *stage* or *preproduction* server

configs/stage/settings.py

you'd be able to run it via

::
  
  TARGET="stage" python manage.py runserver

as you guessed, "develop" is the default target. 

Confidential informations are put inside a file named **local_settings.py** in 
the same directory where settings.py reside. Any local_settings.py file in the 
project is not versioned by default.

You will find an example inside. Typical data that go there are database 
passwords and api keys.

Review the settings
-------------------

Feel free now to read the content of develop and production settings.py.

Note: the production settings.py inherit the content of develop settings.py and 
rewrites or add rules. If you don't like such behaviour because you could 
enable in develop something and forget to mask it in production, you'll have to 
copy development settings in 

configs/production/

and change/add what you found in the original production settings.py

About the content of settings files, what you really need to check and 
evenctually change are:

* TIME_ZONE
* SITE_ID
* LANGUAGE_CODE and LANGUAGES

Also, in the local_settings.py (you can copy and change the 
local_settings.py.example)

* SECRET_KEY
* ADMINS
* DATABASES

A note about databases
----------------------

No database drivers have been installed because there are so many options. Here 
is an incomplete list of what you need to install to use the most classical 
databases

* PostgreSQL - pip install psycopg2
* MySQL - pip install MySQL-python
* SQLite - pip install pysqlite

Configuring Apache
------------------

If you want to use Apache as webserver for your Django project you can start 
with the configuration provided at webserver_example_confs/apache.conf. I used 
mod_macro because is so easier to administrate a configuration (you need to 
change just the last line !)

::

  Use VHost <hostname> /path/to/your/new/django/project <confname>

If you can't install mod_macro you'll have to remove the mod_macro loading rows 
and the macro tag that surround the whole configuration. And obviously change 
each variable with the corresponding value (and then you'll start to think if 
there is a way to install such a useful mod).

Once again, the configuration is made to just work, provided the three 
parameters. If it doesn't, ticket.

Logs
----

Logs are stored at var/logs. There are three logs initially

* apache-access.log - logs any request
* apache-error.log - logs any error that didn't let django to run
* django.log - logs any error in django with production configuration, or any 
debug or higher message in development configuration. The logger name is 
'django'

Example To log an error in django

::

  from django.utils.log import getLogger
  logger = getLogger('django')
  logger.debug('debug log test')

Remember to use your own logger name for your applications and to configure it 
in the LOGGING settings.

Logs are not rotated automatically. You'll have to add a cron job to do it.

Templates
---------

To simplify the design of the site I added two directories to a global template 
dir.

* templates/layout
* templates/views

Layouts are templates that give a structure to the whole page, while views 
contains inner content. Being the template directory at root of the project 
somewhat global, only particular views should go there (like an about page) and 
application related views should stay in that application template directory.

The default layouts are

* base.html
* content_only.html
* header_footer.html

All of them have a common block named "content", so that when you write a view 
you simply have to extend the layout and override the "content" block. Changing 
the layout becomes as easy as changing the name of the extended file.

e.g.

::
  
  {% extends "layout/base.html" %}
  {% block content%}Hello world{% endblock %}

::

  {% extends "layout/header_footer.html" %}
  {% block content%}Hello world{% endblock %}

*base.html* contains the most barebone page. Just <html><head> and <body> tags, 
with blocks to handle css and javascript (and compression handled). It 
shouldn't have particular css styles.

*content_only.html* simply put the "content" block inside a #main-content div 
container. Add some style to the main.css to have it serve pages like the about 
page.

*header_footer.html* unsurprisingly this layout add <header> and <footer> tags 
surrounding that same container written into "content_only" layout.

This are the most generic layouts I could think off, and adding one of them 
(e.g. a two column layout) is dead simple. Create the file in templates/layout/ 
and ensure it has a block named "content".

Fabric and deployment
---------------------

To deploy your site you can use Fabric. There is a not so simple fabric 
configuration at

fabfile/__init__.py

to connect to a remote host and run a batch of common tasks (collect static 
files, minify css/js, clear cache and more). There is a system in place that 
will let you write your configurations on separated files, as

<confname>_settings.py

They will have to stay in that same fabfile directory. This will let you avoid 
to store inside your scm informations that do not need to be versioned (if you 
are using git you'll be pleased to know that there is .gitignore file ready for 
that).

Note that <confname> must be one of the configuration directories you created 
inside 'configs/'.

Author
------
Riccardo Attilio Galli <riccardo@sideralis.org> [http://www.sideralis.org]

