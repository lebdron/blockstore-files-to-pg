#!/usr/bin/env python3

from reblockstorer.loader import BlockLoader
from binascii import hexlify
import psycopg2
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(
    description='Copy Hyperledger Iroha blockstore from files to PostgreSQL.')
parser.add_argument(
    '-b',
    '--blockstore',
    dest='blockstore',
    type=lambda p: Path(p).absolute(),
    help='Source blockstore directory path',
    required=True)
parser.add_argument(
    '-c',
    '--connectionstring',
    dest='connectionstring',
    type=str,
    help='PostgreSQL connection string',
    required=True)
parser.add_argument(
    '-f',
    '--force',
    dest='force',
    action='store_true',
    help='Force overwrite blocks table in PostgreSQL')
args = parser.parse_args()

block_loader = BlockLoader(args.blockstore)
conn = psycopg2.connect(args.connectionstring)

cur = conn.cursor()
if args.force:
    cur.execute('TRUNCATE blocks')
for block in block_loader.blocks():
    cur.execute('INSERT INTO blocks (height, block_data) VALUES(%s, %s)',
                (block.block_v1.payload.height,
                 hexlify(block.block_v1.SerializeToString()).decode('ascii')))
conn.commit()

cur.close()
conn.close()
