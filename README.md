# Kanji Tester

Adapted from https://github.com/larsyencken/kanjitester

## Dependencies


* Homebrew

    
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

* Python3
    
    
    brew install python3

* Mysql
    
    
    brew install mysql
      
## Configuration

Install mysql and configure interaction with Python

    brew unlink mysql
    brew install mysql-connector-c
    sed -i -e 's/libs="$libs -l "/libs="$libs -lmysqlclient -lssl -lcrypto"/g' /usr/local/bin/mysql_config
    pip install MySQL-python
    brew unlink mysql-connector-c
    brew link --overwrite mysql
    

Create virtual env


* Install virtual env


    pip3 install virtualenv





* Create and activate virtual environment
    
    
    # Move inside project folder
    cd KanjiTester    
    # Create virtual env
    virtualenv -p python3 env 
    # Active it
    source env/bin/activate
        

Compile Cython module

* Install Cython for the virtualenv Python
    
    
    pip install cython
    

* Compile the module


    python setup.py build_ext --inplace



Prepare mysql


* Ensure a server is running (indications for Homebrew)

    
    mysql.sever start

* Connect to mysql
    
    
    mysql -u root -p

* Create the database 
   
    
    CREATE DATABASE KanjiTester;

* Create the user and give him the privileges


    CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
    ALTER USER 'admin'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
    FLUSH PRIVILEGES;
    
* Disconnect


    exit
    
    
Install python librairies


    pip install django numpy nltk

### Other info

Location of mysql for Homebrew mysql: /usr/local/var/mysql/