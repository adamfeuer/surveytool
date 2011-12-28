Mac OS X Lion installation instructions. 
========================================

These may vary with other versions of Mac OS X or other operating systems.

1. Install brew

see https://github.com/mxcl/homebrew/wiki/installation

2. Install python 2.7

brew install python

3. Then change system defaults to brew's cellar:

I found this article helpful: http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/

4. Make it so pip will install things in the right place without needing to use sudo

    sudo chown -R adamf:admin /usr/local/
    sudo chmod -R ug+rw /usr/local/
    cd /System/Library/
    sudo rm -rf 2.7
    sudo ln -s /usr/local/Cellar/python/2.7.2/Frameworks/Python.framework/Versions/2.7 .
    cd /Library/Python/
    rm -rf 2.7
    sudo rm -rf 2.7
    sudo ln -s /usr/local/Cellar/python/2.7.2/Frameworks/Python.framework/Versions/2.7 .
    sudo ln -s /usr/local/Cellar/python/2.7.2/Frameworks/Python.framework/Versions/2.7 Current
    sudo mkdir  /Library/Python/build
    sudo chown adamf:admin /Library/Python/build/
    sudo chmod ug+rw /Library/Python/build

5. Now set up virtualenv

    pip install virtualenv
    pip install virtualenvwrapper

6. Set up virtualenvwrapper

See http://www.doughellmann.com/docs/virtualenvwrapper/

7. Make the Survey Tool virtualenv

    mkvirtualenv surveytool
    cd $WORKON_HOME/surveytool

8. Install the required software in the Survey Tool virtualenv

    easy_install pip
    pip install install -r requirements.pip
 
9. Clone the Survey Tool git repository - this is a read-only link

    git clone git://github.com/adamfeuer/surveytool.git
    cd surveytool    

10. Generate keyczar keys:

    bin/keyczart keys

11. Create the Survey Tool config file

    vim $HOME/.surveytoolrc
    export TWILIO_FROM_PHONE_NUMBER='+1XXXYYYY'
    export TWILIO_ACCOUNT='your-twilio-account-string'
    export TWILIO_TOKEN='your-twilio-token'

12. Set up the database

    python manage.py syncdb

13. create Admin user by following prompts

   cd $WORKON_HOME/surveytool/surveytool
   bin/runserver

14. Create a Profile object for the Admin user - necessary to log in

Now visit http://localhost:8000/admin

15. Log in!

Visit http://localhost:8000




