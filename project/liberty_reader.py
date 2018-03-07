#!/usr/bin/env python


#import re
import logging
import argparse
import os

import projlib.liberty

def lb():
    print("\n%s\n" % ( '*'*80 ) )

def main():
    parser=argparse.ArgumentParser()
    
    parser.add_argument("lib_file",help="Liberty file name")
    parser.add_argument("-debug", help="More detailed logging", action="store_true")
    
    args=parser.parse_args()

    if args.debug:
        logging.basicConfig(filename='liberty.log',filemode='w',level=logging.DEBUG)
    else:
        logging.basicConfig(filename='liberty.log',filemode='w',level=logging.INFO)

    lib = projlib.liberty.liberty(os.path.abspath('example.lib'))
    lib.recursive_parse()

    #lb()

    lib.print_lib()
    

if __name__ == "__main__":
    main()




