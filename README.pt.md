goworking-map
===

System for controlling the Go Working tables and rooms of the Fábrica do
Future.

Copyright (C) 2019-2020 Fábrica do Futuro

This program is free software: you can redistribute it and / or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

i18n
---

* [English] (./ README.md)
* [Brazilian Portuguese] (./ README.pt.md)

---

RGSoC 2020
---

** (Only in English) **

This project is part of Rails of Girls Summer of Code 2020. The offical
page for this project is at the
[RGSoC Teams App] (https://teams.railsgirlssummerofcode.org/projects/366-improve-the-desks-and-rooms-control-system-for-the-coworking).

Releases
---

### v 0.1

Delivery date: Friday, December 06, 2019

#### Scope

* Ethiele must be able to view the goworking tables;
* Ethiele should be able to see which chairs are occupied, for
who, from which company;
* Ethiele must be able to edit information about chairs, people,
companies;

### v 0.2

Delivery date: Friday, December 12, 2019

* All registrations working (inhabitants and companies, in addition to spaces,
tables and chairs);
* Update data is not working properly. To change
information is necessary to re-register;

### v 0.3

Delivery date: Wednesday, December 25, 2019

* Edit inhabitants and businesses is working correctly;
* Only relevant functions appear for Ethiele;
* UX changes specific to Ethiele:
* When clicking on an empty chair, an add new button is displayed
inhabitant with specific form for this purpose;

### v 0.4

Delivery date: Friday, January 10, 2020

* Correct display and recording of CPF and CNPJ;

Roadmap
---

TODO:

- [] Document how to use with pipenv
- [] Increase the skeleton from 4 to 5 columns, add the cabins
- [] Extend the scope of the system with new blueprints to contemplate
other features
- [] Migrate login out of the goworking blueprint
- [] Change file names to eg view_habitante.py,
model_habitante.py, etc.

Instructions
---

In the event that someone ever reads the installation instructions.

### git

Clone the repository with the source code.

git clone https://notabug.org/fabricadofuturo/goworking-mesas.git

### Prepare Python and Flask

I use * pipenv * . How to install pipenv is outside the scope of this guide.

    mkdir instance
    cp default_config.py instance / config.py
    cp default_env .env

Edit the `.env` and` instance / config.py` files with the configuration data
Flask, SQLAlchemy, WTForms, etc.

The minimum required is to define the data in the database. For example, in
* .env * file:

    DATABASE_URL = mysql + pymysql: // user: password @ localhost / goworking

    user @ server: goworking-tables $ pipenv install

### Database

You can use any type of database management system that
work with Flask SQL Alchemy. These instructions are for using MariaDB:

#### Install MariaDB Server

MariaDB is the GPL version of MySQL.
In debian: `sudo apt install mariadb-server`;

#### Change username and password

Change the database creation file located at * doc / mysql.sql * :

    CREATE DATABASE goworking DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin;
    GRANT ALL PRIVILEGES ON goworking. * To user @ 'localhost' IDENTIFIED BY 'password';

Change "user" to some username and "password" to any password.

#### Run creation script

Access mariadb-client, copy and paste the commands or run the script.

In debian: `sudo mysql`

    MariaDB [(none)]> SOURCE doc / mysql.sql;
    Query OK, 1 row affected (0.001 sec)

    Query OK, 0 rows affected (0.001 sec)

    MariaDB [(none)]> SHOW DATABASES;
    + -------------------- +
    | Database |
    + -------------------- +
    | goworking |
    | information_schema |
    | mysql |
    | performance_schema |
    + -------------------- +
    4 rows in set (0.001 sec)

If what you have available is a PHPMyAdmin or something, find out how it is
the hard way to paste these simple commands into this complicated system.

#### flask-migrate

    user@server:goworking-mesas$ pipenv run flask db init
    Loading .env environment variables...
    user@server:goworking-mesas$ pipenv run flask db upgrade
    Loading .env environment variables...
    INFO  [alembic.runtime.migration] Context impl MySQLImpl.
    INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
    INFO  [alembic.runtime.migration] Running upgrade  -> fead50b08d21, empty message
    INFO  [alembic.runtime.migration] Running upgrade fead50b08d21 -> dc7d560eee94, empty message

### gunicorn

I use systemd.

There is an example systemd file in * doc / gunicorn-goworking.service * .

    user@server:goworking-mesas$ sudo cp gunicorn-goworking.service /lib/systemd/system/
    user@server:goworking-mesas$ sudo systemctl enable gunicorn-goworking.service
    user@server:goworking-mesas$ sudo systemctl start gunicorn-goworking.service

### Nginx

Sample file in * doc / goworking.conf * .

    user@server:goworking-mesas$ sudo cp doc/goworking.conf /etc/nginx/sites-available/
    user@server:goworking-mesas$ pushd /etc/nginx/sites-enabled
    user@server:/etc/nginx/sites-enabled$ sudo ln -s ../sites-available/goworking.conf
    user@server:/etc/nginx/sites-enabled$ popd
    user@server:goworking-mesas$ sudo nginx -t
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    user@server:goworking-mesas$ sudo systemctl -l reload nginx.service
