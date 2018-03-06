#!/usr/bin/env python


#import re
import projlib.liberty

def lb():
    print("\n%s\n" % ( '*'*80 ) )


lib = projlib.liberty.liberty('example.lib')
#lib.out()
lib.recursive_parse()


#m=re.match('"+','""xxx"""')
#print(m)

lb()

print(lib.root.keyword)
for el in lib.root.child_elements:
    print(el.keyword)

lb()

lib.print_lib()
