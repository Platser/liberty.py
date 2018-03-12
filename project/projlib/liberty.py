import re
import logging
import pprint

class liberty_array:
    def __init__(
            self):
        self.keyword=None
        self.array=[]

    def from_string(
            self,
            string):
        logging.debug("String: "+string)
        m=re.match('^\s*([a-zA-Z0-9_]+)\s*\(\s*([a-zA-Z0-9_".,]+)\s*\)\s*;\s*$',string.replace('\\',''))
        if m:
            #logging.debug(re.split('\",',m.group(2)))
            self.keyword=m.group(1)
            array_string=m.group(2)
            logging.debug("    array_string: "+array_string)
            pos=0
            self.array=[]
            quotas_start=None
            i=0
            while pos < len(array_string):
                if i > 500:
                    logging.error("Infinit loop stop")
                    logging.error("i="+str(i)+", pos="+str(pos)+", len="+str(len(array_string)))
                    exit(1)
                i+=1
                if array_string[pos] in [ '"' ]:
                    if quotas_start is None:
                        pos+=1
                        quotas_start=pos
                        logging.debug("    Quotas_start found at: "+str(quotas_start))
                        continue
                    else:
                        logging.debug("    array_string: "+array_string)
                        sub_array_candidate=array_string[quotas_start:pos]
                        sub_array=sub_array_candidate.split(',')
                        logging.debug(    "    Sub array candidate: "+str(sub_array)+" at pos="+str(pos)+", quotas_start="+str(quotas_start))
                        self.array.append(sub_array)
                        pos+=1
                        quotas_start=None
                        continue
                pos+=1
            #logging.debug("    Array '%s' was resognized: %s" % ( self.keyword, pprint.pprint(self.array) ) )
            logging.debug("    Array '%s' was resognized: %s" % ( self.keyword, self.array ) )
            return(True)
        else:
            return(False)
        



class liberty_attribute:

    def __init__(
            self,
            name=None,
            value=None):
        self.name=name
        self.value=value
    
    def from_string(
            self,
            string):
        pass
    


class liberty_element:
    #child_elements=[]
    #attributes=[]
    #arrays=[]
    #keyword=""
    #name=""
    #level=0
    
    def __init__(
            self,
            keyword=None,
            name="",
            level=0):
        self.child_elements=[]
        self.attributes=[]
        self.arrays=[]
        self.keyword=keyword
        self.level=level
        self.name=name
        
    
    def add_child_element(
            self,
            element):
        #logging.debug("Adding child element %s ( %s ) to the element %s ( %s )" % (element.keyword, element.name,self.keyword,self.name))
        self.child_elements.append(element)
        
    def add_attribute(
            self,
            attribute_string):
        m = re.match('^\s*([a-zA-Z0-9_]+)\s*:\s*([a-zA-Z0-9_"]+)\s*;\s*$',attribute_string);
        if m:
            name=m.group(1)
            value=m.group(2)
            new_attribute=liberty_attribute(name=name,value=value)
            self.attributes.append(new_attribute)
            return(True)
        else:
            return(False)
            
    def add_array(
            self,
            array_string):
        new_array=liberty_array()
        if new_array.from_string(array_string):
            logging.debug("Appending new array %s to the %s ( %s )" % ( new_array.array, self.keyword, self.name ) )
            self.arrays.append(new_array)
            return(True)
        else:
            return(False)



class liberty:

    def __init__(
            self,
            filename=None):
        self.raw=None
        if filename is not None:
            self.read_from_file(filename)
        self.root=None

    def read_from_file(
            self,
            filename):
        logging.info("Reading "+ filename)
        with open(filename, 'r') as fh:
            self.raw=fh.read().replace('\n','').replace(' ', '')
            self.raw=re.sub('/\*.*\*/','',self.raw)
            #self.raw=re.sub('\\','',self.raw)
            self.pos=0
            

    def recursive_parse(
            self,
            current_element=None,
            start=0,
            end=None):
        if end is None:
            end=len(self.raw)-1
        pos=start
        buffer_start=start
        while pos <= end:
            buffer_end=pos
            if self.raw[pos] == ";":
                check=False
                check = check or current_element.add_attribute(self.raw[buffer_start:pos+1])
                check = check or current_element.add_array(self.raw[buffer_start:pos+1])
                if not check:
                    logging.warning("Unable to parse string: "+self.raw[buffer_start:pos+1])
                buffer_start=pos+1
                pos+=1
                continue
            if self.raw[pos] == "{":
                m=re.match('^\s*(\w+)\((\w*)\)',self.raw[buffer_start:pos+1])
                keyword=m.group(1)
                name=m.group(2)
                if current_element is None:
                    self.root=liberty_element(keyword=keyword,name=name)
                    pos=self.recursive_parse(start=pos+1,current_element=self.root)
                    buffer_start=pos
                else:
                    new_element=liberty_element(keyword=keyword,name=name,level=current_element.level+1)
                    pos=self.recursive_parse(start=pos+1,current_element=new_element)
                    buffer_start=pos
                    current_element.add_child_element(new_element)
                continue
            if self.raw[pos] == "}":
                return(pos+1)
            pos+=1
    
    def recursive_print(
            self,
            element):
        print("%s%s ( %s ) {" % ( '    '*element.level, element.keyword, element.name) )
        for attr in element.attributes:
            print("%s%s : %s ;" % ('    '*(element.level+1), attr.name, attr.value) )
        for child_element in element.child_elements:
            self.recursive_print(child_element)
        print("%s}" % ('    '*element.level) )
        
    
    def print_lib(self):
        self.recursive_print(self.root)
        
    
    def out(self):
        print(self.raw)
    