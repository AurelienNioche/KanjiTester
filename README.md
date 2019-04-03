Adapted from https://github.com/larsyencken/kanjitester


Install mysql

    brew install mysql
    brew unlink mysql
    brew install mysql-connector-c
    sed -i -e 's/libs="$libs -l "/libs="$libs -lmysqlclient -lssl -lcrypto"/g' /usr/local/bin/mysql_config
    pip install MySQL-python
    brew unlink mysql-connector-c
    brew link --overwrite mysql
    
Prepare mysql

    mysql -u root -p
    
    CREATE DATABASE KanjiTester;
    
    CREATE USER 'admin'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost';
    
    FLUSH PRIVILEGES;
    
    exit
    
   
Compile Cython module:

    cythonize -a -i yourmod.pyx
