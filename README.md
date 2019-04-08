# Kanji Tester

Adapted from https://github.com/larsyencken/kanjitester


Install mysql and configure interaction with Python

    brew install mysql
    brew unlink mysql
    brew install mysql-connector-c
    sed -i -e 's/libs="$libs -l "/libs="$libs -lmysqlclient -lssl -lcrypto"/g' /usr/local/bin/mysql_config
    pip install MySQL-python
    brew unlink mysql-connector-c
    brew link --overwrite mysql
    
Prepare mysql


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
    
   
Compile Cython module:
       
    cd kanji_tester/plugins/visual_similarity/metrics
    cythonize -a -i stroke.pyx


### Other info

Location of mysql for homebrew mysql: /usr/local/var/mysql/