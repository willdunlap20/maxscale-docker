# MaxScale Sharded MariaDB Demo

## Introduction

This Project sets up a basic sharded database enviroment using two MariaDB shards and managed through Maxscale. It includes:

- Two MariaDB containers (`zipcodes_one`, `zipcodes_two`) preloaded with zipcode data
- A MaxScale container that routes queries across the shards
- A Python script that connects to MaxScale and runs sample queries across both shards

## Running

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

The cluster is configured to utilize automatic failover. To illustrate this you can stop the master
container and watch for maxscale to failover to one of the original slaves and then show it rejoining
after recovery:
```
$ docker-compose stop master
Stopping maxscaledocker_master_1 ... done
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬─────────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID        │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server1 │ master  │ 3306 │ 0           │ Down            │ 0-3000-5    │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Master, Running │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴─────────────┘
$ docker-compose start master
Starting master ... done
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬─────────┬──────┬─────────────┬─────────────────┬─────────────┐
│ Server  │ Address │ Port │ Connections │ State           │ GTID        │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server1 │ master  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server2 │ slave1  │ 3306 │ 0           │ Master, Running │ 0-3001-7127 │
├─────────┼─────────┼──────┼─────────────┼─────────────────┼─────────────┤
│ server3 │ slave2  │ 3306 │ 0           │ Slave, Running  │ 0-3001-7127 │
└─────────┴─────────┴──────┴─────────────┴─────────────────┴─────────────┘

```

Once complete, to remove the cluster and maxscale containers:

```
docker-compose down -v
```
