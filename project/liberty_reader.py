#!/usr/bin/env python


#import re
import logging
import argparse
import os
import pprint
import sys

import projlib.liberty

def lb():
    print("\n%s\n" % ( '*'*80 ) )

def main():

    parser=argparse.ArgumentParser()
    
    parser.add_argument("lib_file",help="Liberty file name")
    parser.add_argument("-debug", help="Debug messages logging", action="store_true")
    args=parser.parse_args()

    logFormat="%(asctime)s [%(threadName)-12.12s] [%(levelname)-8.8s]  %(message)s"
    logging.basicConfig(format=logFormat, level=logging.ERROR, filename='/dev/null', filemode='w')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    fileHandler = logging.FileHandler('liberty.log',mode='w')
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.INFO)
    if args.debug:
        fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setLevel(logging.WARNING)
    consoleHandler.setFormatter(logFormatter)
    logger.addHandler(consoleHandler)

    if not os.path.isfile(args.lib_file):
        logger.error('File not found: %s' % args.lib_file)
        exit(1)
    
    lib = projlib.liberty.liberty(os.path.abspath(args.lib_file))
    lib.recursive_parse()

    for cn in lib.list_cells():
        print(cn)

    lib.get_table("xor3v1x1","d","rise_constraint")
    

if __name__ == "__main__":
    main()




