# Sharding with MongoDB
reference : Just me and Opensource

The Mongos are the interfaces to the shards. The application never interacts directly with the charts but with the gateway which are the mongos (lightweight) in this case. Then we have the config servers (as replica sets, needs to have at least two as if one is down, the mongos can still have the configuration information about the chards)  which store all the metadata and finally the shards which store the actual data. 

Best case for the configuration server is to have a replica sets of 3 servers, one primary and 2 secondary. Each replica set (server and the 2 shards) must have a different


## Set up Sharding using Docker Containers

### Config servers
Start config servers (3 member replica set)
```
docker-compose -f config-server/docker-compose.yaml up -d
```
Initiate replica set
```
mongo mongodb://<ip_address>:40001
```
It doesn't matter which config instance you log into (based on the port you choose above) but the one you choose to apply the following command to, will be the primary config server
```
rs.initiate(
  {
    _id: "cfgrs",
    configsvr: true,
    members: [
      { _id : 0, host : "<your_ip_address>:40001" },
      { _id : 1, host : "<your_ip_address>:40002" },
      { _id : 2, host : "<your_ip_address>:40003" }
    ]
  }
)

rs.status()
```

This result of the replica set will show us that indeed three members have been added to the replica set. One primary and two secondary. The two secondary servers will be syncing to the primary. 

### Shard 1 servers
Start shard 1 servers (3 member replicas set)
```
docker-compose -f shard1/docker-compose.yaml up -d
```
Initiate replica set
```
mongo mongodb://<your_ip_address>:50001
```
```
rs.initiate(
  {
    _id: "shard1rs",
    members: [
      { _id : 0, host : "<your_ip_address>:50001" },
      { _id : 1, host : "<your_ip_address>:50002" },
      { _id : 2, host : "<your_ip_address>:50003" }
    ]
  }
)

rs.status()
```

### Mongos Router
Start mongos query router
Before being able to run this command, you will need to change your ip address in the .env file in the sharding folder. example : IP_ADDRESS=192.168.1.12
```
docker-compose -f mongos/docker-compose.yaml up -d
```

### Add shard to the cluster
Connect to mongos
```
mongo mongodb://<your_ip_address>:60000
```
Add shard
```
mongos> sh.addShard("shard1rs/<your_ip_address>:50001,<your_ip_address>:50002,<your_ip_address>:50003")
mongos> sh.status()
```
## Adding another shard
### Shard 2 servers
Start shard 2 servers (3 member replicas set)
```
docker-compose -f shard2/docker-compose.yaml up -d
```
Initiate replica set
```
mongo mongodb://<your_ip_address>:50004
```
```
rs.initiate(
  {
    _id: "shard2rs",
    members: [
      { _id : 0, host : "<your_ip_address>:50004" },
      { _id : 1, host : "<your_ip_address>:50005" },
      { _id : 2, host : "<your_ip_address>:50006" }
    ]
  }
)

rs.status()
```
### Add shard to the cluster
Connect to mongos
```
mongo mongodb://<your_ip_address>:60000
```
Add shard
```
mongos> sh.addShard("shard2rs/<your_ip_address>:50004,<your_ip_address>:50005,<your_ip_address>:50006")
mongos> sh.status()
```
