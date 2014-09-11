Romeu
=====

Romeu aims to be a simple but powerful content management system for multilingual theatrical archives.
Romeu is built on Django, and is used to power the [Cuban Theater Digital Archive][] at the
University of Miami Libraries.

Requirements
------------

You will need the following installed on your server:

- Python (2.7. Python 3 is *not* supported.)
- Python packages:
	- Django==1.5.5
	- South==0.8.2
	- Unidecode==0.04.14
	- django-dajax==0.9.2
	- django-dajaxice==0.5.5
	- django-debug-toolbar==1.0.1
	- django-disqus==0.4.1
	- django-haystack==1.2.7
	- django-reversion==1.8.0
	- django-rosetta==0.7.3
	- django-smart-selects==1.0.9
	- django-taggit==0.11.2
	- django-taggit-autocomplete-modified==0.1.0b4
	- django-tinymce==1.5.2
	- psycopg2==2.5.2
	- pysolr==3.2.0
	- sorl-thumbnail==11.12

Preparing your environment

	Installing Python
		Most Linux distributions has python 2.6 already install,
		check your system documentation on how to have the original pyhton version 2.6 and 2.7 install at same time.
	
	Installing Django	
		Most Linux distributions can install Django through their package management tools, allowing for easy maintenance and upgrades.
		
		pip install django==1.5.5
		
	Installing third-party apps¶ 

		You can install any of the packages above using pip.
		
	Installing Romeu
		Get the source code
			Now that you have a Python/Django environment ready to go, it’s time to install and set up Romeu. If you have Git installed,
			installing Romeu is as easy as navigating to the parent directory you want to install it in and typing:

			git clone git://github.com/umdsp/romeu.git

			This will create a new directory, romeu, containing the Romeu source code.
			If you do not have Git installed, you can alternatively download a .zip or .tar.gz archive of the project’s source code
			by visiting https://github.com/umdsp/romeu/downloads.

	Configure Romeu
		After downloading Romeu, you will need to configure it for your server environment (this includes using Romeu on your development machine).
		All server-specific configuration for Romeu is contained in a local_settings.py file at the root Romeu directory.
		To begin configuring Romeu, rename the local_settings.py.example file to local_settings.py.
		
		Within local_settings.py, you will need to adjust the following entries to match your server environment:

			ADMINS: Enter your name and email address. This is where error reports, etc. will be sent.
			You may also enter more than one admin here; each admin will be notified when an error occurs.
			DEBUG / THUMBNAIL_DEBUG / TEMPLATE_DEBUG: DEBUG is set to True, and the rest are set to False, by default.
			Change these to True if you would like to see more detailed debug information when an error occurs.
			
			DATABASES: 	Under default, enter the connection details for your database.
						Django supports PostgreSQL, MySQL, SQLite and Oracle without additional plugins.
						The included local_settings.py.example sets up an SQLite database;
						just change the database listed under NAME to an absolute path.

	Syncing the database
		Before you can begin to use Romeu, you must perform an initial database sync.
		To do this, navigate to the main Romeu directory and type:

			python manage.py syncdb
		
[Cuban Theater Digital Archive]: http://cubantheater.org