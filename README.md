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
- **MySQL client**

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
Once the containers are up and running, and we have all the requirements installed for running the python query we will execute the following command
```
python3 query.py
```

## Configuration

By default, the MaxScale container is configured to route SQL queries to two MariaDB shards using the `schemarouter` module.

MaxScale listens on port `4000` for incoming SQL connections. This port is exposed to the host in the `docker-compose.yml` file.

### Manual REST API Access (Optional)

MaxScale also provides a REST API on port `8989` by default. To use it, ensure port 8989 is exposed and then run:

```
curl -u admin:mariadb http://localhost:8989/v1/maxscale
```

## Maxscale Docker-Compose Setup

This project uses Docker Compose to bring up a MaxScale container and two MariaDB shard containers. The `docker-compose.yml` file defines the services, networks, ports, and volume mounts.

### Services

- `maxscale`: The MaxScale proxy that routes queries to the correct shard
- `zipcodes_one`: The first MariaDB shard containing part of the zipcode data
- `zipcodes_two`: The second MariaDB shard containing the other half

### Ports

- **4000**: Exposed by MaxScale for incoming SQL client connections
- **3306**: Used internally by the MariaDB shards

### Volumes

The MaxScale container mounts a configuration file from the repo:
```
   volumes:
            - ./maxscale.cnf.d:/etc/maxscale.cnf.d
```


Once complete, to remove the cluster and maxscale containers:

```
docker-compose down -v
```
