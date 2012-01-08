>Survey Tool has been tested on Mac and Linux. Linux installation
instructions are after the Mac instructions.

Mac OS X Lion installation instructions. 
========================================

These may vary with other versions of Mac OS X or other operating systems.

1. Install brew

    See https://github.com/mxcl/homebrew/wiki/installation

2. Install python 2.7

    ```bash
    brew install python --framework --universal
    ```

3. Then change system defaults to brew's cellar:

    I found this article helpful: http://www.thisisthegreenroom.com/2011/installing-python-numpy-scipy-matplotlib-and-ipython-on-lion/

4. Make it so pip will install things in the right place without needing to use sudo

    ```bash
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
    ```

5. Now set up virtualenv

    ```bash
    pip install virtualenv
    pip install virtualenvwrapper
   ```

6. Set up virtualenvwrapper

    See http://www.doughellmann.com/docs/virtualenvwrapper/

7. Make the Survey Tool virtualenv

    ```bash
    mkvirtualenv surveytool
    cd $WORKON_HOME/surveytool
    ```

8. Install the required software in the Survey Tool virtualenv

    ```bash
    easy_install pip
    pip install pip --upgrade
    ```
 
9. Clone the Survey Tool git repository - this is a read-only link

    ```bash
    git clone git://github.com/adamfeuer/surveytool.git
    cd surveytool   
   ```

10. Install the required software in the Survey Tool virtualenv
    ```bash
    pip install -r requirements.pip
    ```

11. Generate keyczar keys:

    ```bash 
    cd $WORKON_HOME/surveytool/surveytool
    bin/keyczart keys
    ```

12. Create the Survey Tool config file

    ```bash
    vim $WORKON_HOME/surveytool/surveytool.config
    
    [Twilio]
    TWILIO_FROM_PHONE_NUMBER = +1XXXYYYY
    TWILIO_ACCOUNT = your-twilio-account-string
    TWILIO_TOKEN = your-twilio-token

    [Database]
    database = surveytool
    user = surveytool
    password = your-password
    ```

13. Install Postgres database

    ```bash
    brew install postgresql
    ```

    (MysSQL is known to not work.) Follow the installation
    instructions that are printed after the install succeeds.

14. Set up the database

    Create database, user, password
    ```bash
    createuser -D -A -P surveytool
    createdb -O surveytool surveytool
    ```

15. Set up the database

    ```bash
    python manage.py syncdb --settings=conf.dev.settings
    ```

16. Set up static resources

    ```bash
    python manage.py collectstatic --settings=conf.dev.settings
    ```

17. Start the server

   ```bash  
   cd $WORKON_HOME/surveytool/surveytool
   bin/runserver.sh
   ```

18. Create a Profile object for the Admin user - necessary to log in

    Now visit http://localhost:8000/admin

19. Log in!

    Visit http://localhost:8000


Ubuntu Linux installation instructions
======================================

Note that this may work for other Linux distributions, but I have not tested them.

These have been tested on Ubuntu 11.10 Server, Oneiric Ocelot.

(not done yet)


