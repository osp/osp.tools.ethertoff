RELEARN
=======

Web platform, initially for the OSP 2013 Summerschool bearing this name.

<http://relearn.be/>

Relearn.be is structured as a wiki where each page constitutes an Etherpad.

The pad is available to logged in users (‘write-mode’). 
The text of the pad is available to everyone (‘read-mode’).

The integration between Django and Etherpad is based on <https://github.com/sfyn/django-etherpad-lite>

- - -

## Installation instructions

    # First create and install a virtual environment. Then:
    mkdir -p ~/venvs/
    cd ~/venvs/
    virtualenv relearn
    source ~/venvs/relearn/bin/activate
    pip install django
    pip install https://github.com/rassie/PyEtherpadLite/zipball/master
    pip install https://github.com/codingisacopingstrategy/django-etherpad-lite/zipball/master
    cd ~/relearn/relearn.be/relearn
    cp local_settings.py.example local_settings.py
    # Add database details to local_settings.py
    cd ..
    python manage.py syncdb
    
    # --> and then install etherpad
    
    mkdir -p ~/src
    cd ~/src
    git clone https://github.com/ether/etherpad-lite.git
    
    # --> install npm
    Linux Binaries (.tar.gz) from http://nodejs.org/download/

    # run it with:
    
    ~/src/etherpad-lite/bin/run.sh
    
    Your Etherpad is running at http://12.0.0.1:9001/
    
    in Etherpad’s folder, you will find a file called APIKEY.txt
    you need it’s contents later 
    
    (check context-processor)
    
    Run the surver:
    python manage.py runserver
    visit the admin at: http://127.0.0.1:800/admin/
    you can login with the superuser 
    Etherpadlite > Servers > Add
    url: http://127.0.0.1:9001/
    api_key:
    Auth > Group > Add
    Add your superuser to group you just created
    Etherpadlite > Group > Add
    Create an Etherpad Group based upon the group you just created.
    
    Now relearn is served at http://127.0.0.1:8000/
