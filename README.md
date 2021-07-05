# marmara-stats
Marmara stats db implementation for Marmara explorer

## Getting Started
-------------------------
This project accesses komodod's JSON-RPC interface using Python.


Development Environment for Developers:
- Ubuntu 18.04
- Python3 is required for execution
- virtual environment

Update libraries:

* `sudo apt-get update`
Install the module slick-bitcoinrpc and its dependencies:
* `sudo apt-get install python3.6 python3.6-dev python3-pip libgnutls28-dev libssl-dev`

Change directory to Project's working directory.

Creating a python 3.6 virtual environment:
```sh
python3 -m venv venv
```
Activate the virtual environment:
```sh
source venv/bin/activate
```
Install required libraries inside venv:
```sh
python3.6 -m pip install setuptools wheel slick-bitcoinrpc
```


### Installing mySQL Server 
First, update the apt package index by:
```sh
sudo apt update
```
Install the MySQL package with the following command:
```sh
sudo apt install mysql-server
```
Once the installation is completed, the MySQL service will start automatically. To check if the MySQL server is running:
```sh
sudo systemctl status mysql
```
Secure MySQL by running the following script:
```sh
sudo mysql_secure_installation
```
One may set up the validate password plugin or skip it by pressing ENTER.
Depending upon the needs, answer the questions that appear on the terminal.

To login as root:
```sh
sudo mysql
```
Check out the current authentication plugin that MySQL server is using:
```
SELECT plugin from mysql.user where User='root';
```
To be able to login to MySQL with password, one needs to change the plugin from auth_socket to mysql_native_password. The command below could be used for it:
```
UPDATE mysql.user SET plugin = 'mysql_native_password', authentication_string = PASSWORD('changeme') WHERE User = 'root';
FLUSH PRIVILEGES;
```

In case of a need to login to MySQL server from an external program, one may create a new admin user with access to all databases by using the following command: (Replace the string very_strong_password with the password of your choice)
```
GRANT ALL PRIVILEGES ON *.* TO 'admin'@'localhost' IDENTIFIED BY 'very_strong_password';
FLUSH PRIVILEGES;
```
If you wish to grant only access to the specific database use the command below instead:
```
GRANT ALL PRIVILEGES ON marmara.* TO 'admin'@'localhost';
FLUSH PRIVILEGES;
```
To exit MySQL server, the following commands are useful:
```
exit
/q
```
Restart MySQL server using the following command:
```sh
sudo service mysql restart
```

Enter MySQL server as root with password:
```
mysql -u root -p
```
Enter MySQL server as admin with password:
```
mysql -u admin -p
```

## Useful MySQL commands 
show databases;
create database marmara;
use marmara;
CREATE TABLE marmarastat (
    ID int NOT NULL AUTO_INCREMENT,
    BeginHeight int NOT NULL,
    EndHeight int NOT NULL,
    TotalNormals float,
    TotalActivated float,
    TotalLockedInLoops float,
    PRIMARY KEY (ID)
);
show tables;
SELECT user();
DESCRIBE <table_name>;
