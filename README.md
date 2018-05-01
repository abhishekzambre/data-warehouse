# Data Warehouse

Data warehousing using [Luigi](https://github.com/spotify/luigi), [PostgreSQL](https://www.postgresql.org/), and [Metabase](https://www.metabase.com/).

Luigi is used for Data Pipeline.

PostgreSQL is used as a Database.

Metabase is used for Data Analytics Dashboard.


## Environment Setup

The system is developed and tested on the environment with the below configurations.

- [Ubuntu 16.04.4](https://www.ubuntu.com/download/desktop)
- [Python 3.5.2](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/linux/ubuntu/)
```
sudo apt-get install postgresql postgresql-contrib
```
- [OpenJDK 1.8.0_162](http://openjdk.java.net/install/index.html)
```
sudo apt-get install openjdk-8-jdk
```
- [pip](https://pypi.org/project/pip/)
```
sudo apt install python3-pip
```
- [Luigi](https://github.com/spotify/luigi)
```
pip3 install luigi
```
```
luigid
```
- [psycopg2](http://initd.org/psycopg/)
```
pip3 install psycopg2
```
- [pandas](https://pandas.pydata.org/)
```
pip3 install pandas
```
- [mlxtend](https://github.com/rasbt/mlxtend)
```
pip3 install mlxtend
```
- [pycountry](https://pypi.org/project/pycountry/)
```
pip3 install pycountry
```
- [Metabase](https://www.metabase.com/)
Download the jar file (version: 0.28.6) from [here](https://www.metabase.com/start/jar.html).

- pgadmin4
```
pip3 install https://ftp.postgresql.org/pub/pgadmin/pgadmin4/v3.0/pip/pgadmin4-3.0-py2.py3-none-any.whl
```