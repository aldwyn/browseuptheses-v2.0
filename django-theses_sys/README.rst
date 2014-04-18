=======================
Browse UP Theses System
=======================

Browse UP Theses System is a Django-powered (i.e. server-side
Python scripting) systematic engine of theses data that is used
browse theses of student researchers from the University of the Philippines Cebu.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "theses_sys" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'theses_sys',
      )

2. Include the polls URLconf in your project urls.py like this::

      url(r'^theses_sys/', include('theses_sys.urls')),

3. Run `python manage.py syncdb` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to view initial data of authorized users (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/theses_sys/ to browse the search engine.