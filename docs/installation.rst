.. _usage:

Installation
=====

- enable ``'django.template.loaders.eggs.Loader'`` in ``TEMPLATE_LOADERS`` in your ``settings.py`` file
- (Optional) Add ``url(r'^demo/', include('demo.foo.urls')),`` to your project urls.py file

<b>Installing instructions</b><br />
(Todo: script these steps into deployment...)
To set this application up the right way, you will need to do some things to your project configuration, and your app_folder configuration. You can use the demo_project or use your own if you have already started a main project<br />
- Pick a desired app-name
<b>Application implementation</b>
- update setup.py - replace "app_folder_name" with your desired app name
- change folder app_folder_name to the application name you would like
- replace "app_folder_name" in MANIFEST.in file with your app name
- modify conf.py as needed in your docs/ directory
- modify urls.py inside the app_folder, and replace app_folder_name with your app-name
- modify views.py file and change logger instance name
- modify views.py and change the class-table names and forms inside of data dictionary
- modify tests.py to change your models around to the actual table classes
<b>Project configuration </b><br />
- modify your PROJECTS (see demo_project folder) urls.py file to include this apps urls.py file 
with a root-url (See: reusable-main in demo_project/urls). E.g http://www.site.com/root-url-name/services/model-name/action/ID
- modify your projects settings.py file, replace "demo_project" with your project name in ROOT_URLCONF, and WSGI_APPLICATION variables, and update any other settings you would like here.
- modify wsgi.py and replace demo_project with your project name

