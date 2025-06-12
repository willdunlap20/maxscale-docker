# MaxScale Sharded MariaDB Demo

## Introduction

This Project sets up a basic sharded database enviroment using two MariaDB shards and managed through Maxscale. It includes:

- Two MariaDB containers (`zipcodes_one`, `zipcodes_two`) preloaded with zipcode data
- A MaxScale container that routes queries across the shards
- A Python script that connects to MaxScale and runs sample queries across both shards

## Running

### Prerequisites

Make sure you have the following installed:

- **Docker** and **Docker Compose**
- **Python 3**
- **MySQL client** (optional, for manual testing)

You can install them on Ubuntu with:

```
sudo apt update
sudo apt install docker.io docker-compose python3 python3-pip mysql-client
```
as well as
```
pip3 install mysql-connector-python
```

Once we have all prerequisites

To start the enviroment:
```
docker-compose build
docker-compose up -d
```
Once the containers are running we can check their condition with the following command
```
$ docker-compose exec maxscale maxctrl list servers
```
We should see a readout similar to below
```
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬──────────┬─────────────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID     │ Monitor         │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┼─────────────────┤
│ server1 │ shard1  │ 3306 │ 0           │ Master, Running │ 0-3000-4 │ MariaDB-Monitor │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼──────────┼─────────────────┤
│ server2 │ shard2  │ 3306 │ 0           │ Slave, Running  │ 0-3001-4 │ MariaDB-Monitor │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴──────────┴─────────────────┘
```
Once the containers are up and running we have all the requirements installed for running the python query we will execute the following command
```
python3 query.py
```

Once complete, to remove the cluster and maxscale containers:

```
docker-compose down -v
```
