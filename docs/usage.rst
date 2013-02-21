.. _usage:

Usage
=====

Using this application. Add the following to your URLS.py file::
This application is made up of three components: Main-Project, Main reusable-app, Other-reusable-apps

Main-Project
============
The main project will be your django-project (see demo_project in github repo)
This project will include one URL entry, which is called the "root-url" string
This will tell it that any regex caught after that URL prefix, will be processed
via the main reusable app's controller.


Main-reusable-app
=================
The main reusable app is the application that will handle the main crud events (add, write, edit, delete)
Any other reusable apps that are built can be used just for their model and their internal API urls. If you decide to use internal api urls for the "other" reusable apps (which will be utilzed by the main app) then you will need to add those url entries into your PROJECTS urls.py configuration. (api/other-reusable/show-users)


Other-reusable-apps
====================
Other reusable apps will be used for their model definitions, custom forms, or API views.
They will have to be coded into the main-reusable-app views, with a try/except import. 
If those imports are found, the data for the models and forms will then be added to the main ``data`` dictionary for the controller.


