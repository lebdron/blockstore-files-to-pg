# blockstore-files-to-pg
Copy Hyperledger Iroha blockstore from files to PostgreSQL

## Installation

Docker:
```sh
docker build -t blockstore-files-to-pg .
docker run --rm blockstore-files-to-pg --help
```

## Usage

```
usage: blockstore-files-to-pg.py [-h] -b BLOCKSTORE -c CONNECTIONSTRING [-f]

Copy Hyperledger Iroha blockstore from files to PostgreSQL.

optional arguments:
  -h, --help            show this help message and exit
  -b BLOCKSTORE, --blockstore BLOCKSTORE
                        Source blockstore directory path
  -c CONNECTIONSTRING, --connectionstring CONNECTIONSTRING
                        PostgreSQL connection string
  -f, --force           Force overwrite blocks table in PostgreSQL
```

Source blockstore is located in `/path/to/source/blockstore`, node is deployed in separate containers with a `iroha-default` network, config `pg_opt` value is `host=iroha-postgres port=5432 user=iroha password=hello` (default `dbname` hardcoded in `irohad` is `iroha_default`).

```sh
docker run \
    --rm \
    -v /path/to/source/blockstore:/in/blockstore \
    --network iroha-default \
    blockstore-files-to-pg \
    -b /in/blockstore \
    -c "host=iroha-postgres port=5432 user=iroha password=helloworld dbname=iroha_default"
```
