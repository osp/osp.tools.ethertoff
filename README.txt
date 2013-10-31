RELEARN
=======

Simple collaborative web platform, initially developed for the OSP 2013 Summerschool
bearing this name.

<http://relearn.be/>

Relearn.be is structured as a wiki where each page constitutes an Etherpad.

The pad is available to logged in users (‘write-mode’). 
The text of the pad is available to everyone (‘read-mode’).

relearn.be is a shell for an Etherpad installation hosted on the same domain.
This integration is based on Sofian Benaissa’s bridge between Django and Etherpad,
originally created for THINK WE MUST/CON-VOCATION a performance during Promiscuous
Infrastructures entrelacées, an exhibition by the collective Artivistic at SKOL.

-  <https://github.com/sfyn/django-etherpad-lite>
-  <http://www.riotnrrd.info/tech/etherpad-lite-performances-ongoing-saga>
-  <http://www.thinkwemust.org/?page_id=6>

- - -

## Installation instructions

    # Requires Django 1.5
    # First create and install a virtual environment [1]. Then:
    pip install "django<1.6"
    pip install https://github.com/devjones/PyEtherpadLite/archive/master.zip

    cd /path/to/relearn.be/      # [2]
    cd relearn
    cp local_settings.py.example local_settings.py
    # Add database details to local_settings.py
    cd ..
    python manage.py syncdb
    
    # --> and then install etherpad
    
    mkdir -p ~/src
    cd ~/src
    git clone https://github.com/ether/etherpad-lite.git
    
    # --> install node js
    Linux Binaries (.tar.gz) from http://nodejs.org/download/

    # run it with:
    
    ~/src/etherpad-lite/bin/run.sh
    
    Your Etherpad is running at http://12.0.0.1:9001/
    
    in Etherpad’s folder, you will find a file called APIKEY.txt
    you need it’s contents later 
    
    Run the surver:
    python manage.py runserver
    visit the admin at: http://127.0.0.1:800/admin/
    you can login with the superuser 
    Etherpadlite > Servers > Add
    url: http://127.0.0.1:9001/
    api_key: the contents of APIKEY.txt
    Auth > Group > Add
    Add your superuser to group you just created
    Etherpadlite > Group > Add
    Create an Etherpad Group based upon the group you just created.
    
    Now relearn is served at http://127.0.0.1:8000/

    You can set the site name, that appears on the header, in the ‘sites’ app in the admin.

- - -

[1] Something like:

    mkdir -p ~/venvs/
    cd ~/venvs/
    virtualenv relearn
    source ~/venvs/relearn/bin/activate

[2] For those running the Virtual Machine from the relearn sessions:

    cd ~/relearn/relearn.be/relearn
