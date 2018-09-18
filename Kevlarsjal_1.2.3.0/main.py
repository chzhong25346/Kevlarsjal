#!/usr/bin/python3

import time
import sys,os
import argparse
import logging
import logging.config
logger = logging.getLogger('main')
import yaml
from core import *

start_time = time.time()

# Arguments Parser
parser = argparse.ArgumentParser(description="Kevlarsjal reads index and store data")
group = parser.add_mutually_exclusive_group()
group.add_argument("-a","--all",help="Update all",action="store_true")
group.add_argument("-i", "--industry",help="Update by Industry Code",action="store_true")
parser.add_argument("index", help="index, ej: tsxci")
parser.add_argument("ic", help="None if update all. Industry Code sigle word(first 3cha), multi-word(1st cha)")
parser.add_argument("type", help="query type, full or compact")
args = parser.parse_args()


# Logging setup
def setup_logging(default_path='config.yaml', default_level=logging.INFO):
    path = default_path
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == '__main__':
    yaml_path = 'log/config.yaml'
    setup_logging(yaml_path)

    index_name,indCode,type = args.index,args.ic,args.type

    if(args.all):
        logger.debug('updating all.. %s %s', index_name,type)
        update_all(index_name,type)
    elif(args.industry):
        logger.debug('updating by industry.. %s %s %s', index_name,indCode,type)
        update_by_industry(index_name,indCode,type)

    logger.info( "Program took %s minutes to run", ((time.time() - start_time)/60))
    # update_index('tsxci')
