#!/usr/bin/env python


#import re
import projlib.liberty

lib = projlib.liberty.liberty('example.lib')
#lib.out()
lib.recursive_parse()


#m=re.match('"+','""xxx"""')
#print(m)

print("%s - %s" % ( ' '*10, '*'*10 ) )