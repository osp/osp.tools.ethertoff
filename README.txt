RELEARN
=======

Web platform, initially for the OSP 2013 Summerschool bearing this name.

<http://relearn.be/>

    # First create and install a virtual environment. Then:
    pip install django
    pip install https://github.com/rassie/PyEtherpadLite/zipball/master
    pip install https://github.com/codingisacopingstrategy/django-etherpad-lite/zipball/master
    cd relearn
    cp local_settings.py.example local_settings.py
    # Add database details to local_settings.py
    cd ..
    python manage.py syncdb
    # --> and then install etherpad
