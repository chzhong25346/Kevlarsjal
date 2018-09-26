#!/usr/bin/python3

import time
import sys,os
import argparse
import logging
import logging.config
logger = logging.getLogger('main')
import yaml
import math
from core import *
from log.mail import sendMail


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
    sys.path.append(os.path.realpath('..'))
    start_time = time.time()

    # Arguments Parser
    parser = argparse.ArgumentParser(description="Kevlarsjal reads index and store data")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-a","--all",help="Update all",action="store_true")
    group.add_argument("-i", "--industry",help="Update by Industry Code",action="store_true")
    group.add_argument("-r", "--report",help="Reporting",action="store_true")
    parser.add_argument("index", help="index, ej: tsxci")
    parser.add_argument("ic", help="Industry Code, default=none")
    parser.add_argument("type", help="query type, full or compact")
    parser.add_argument("intraday", help="interval=30min, default=none")
    args = parser.parse_args()
    yaml_path = 'log/config.yaml'
    setup_logging(yaml_path)

    index_name,indCode,type,intraday = args.index,args.ic,args.type,args.intraday

    if(args.all):
        logger.debug('updating all.. %s %s %s', index_name,type,intraday)
        update_all(index_name,intraday,type)
    elif(args.industry):
        logger.debug('updating by industry.. %s %s %s %s', index_name,indCode,type,intraday)
        update_by_industry(index_name,indCode,intraday,type)
    elif(args.report):
        logger.debug('analysing entire index.. %s %s %s %s', index_name,indCode,type,intraday)
        reporting(index_name,indCode,intraday,type)

    spendTime = math.ceil((time.time() - start_time)/60)
    sub = 'Task Completed: .. %s %s %s %s' % (index_name,indCode,type,intraday)
    cont = 'Program took ' + str(spendTime) + ' minutes to run'
    # sendMail(sub,cont)
    logger.info(cont)
