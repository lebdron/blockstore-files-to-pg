#!/usr/bin/env python3

from reblockstorer.loader import BlockLoader
from binascii import hexlify
import psycopg2
import argparse
from pathlib import Path
from tqdm import tqdm
import logging

NAME = 'BlockstoreFilesToPostgres'
LOGGER = logging.getLogger(NAME)

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
parser.add_argument(
    '-v',
    '--verbosity',
    choices=logging._nameToLevel,
    default='info',
    help='logging verbosity')
args = parser.parse_args()

logging.basicConfig(level=args.verbosity)

LOGGER.info('loading blockstore...')
block_loader = BlockLoader(args.blockstore)

LOGGER.info('connecting to database...')
conn = psycopg2.connect(args.connectionstring)

cur = conn.cursor()
if args.force:
    LOGGER.info('removing old blocks from database...')
    cur.execute('TRUNCATE blocks')

LOGGER.info('uploading blocks to database...')
for block in tqdm(block_loader.blocks(), desc='uploaded', unit=' blocks'):
    cur.execute('INSERT INTO blocks (height, block_data) VALUES(%s, %s)',
                (block.block_v1.payload.height,
                 hexlify(block.block_v1.SerializeToString()).decode('ascii')))
LOGGER.info('committing changes...')
conn.commit()

LOGGER.info('done.')
cur.close()
conn.close()
