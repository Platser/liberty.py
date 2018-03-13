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
    
    def echo(self):
        return('%s : %s ;' % ( self.name, self.value ) )
    


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
            
    def echo(
            self):
        return("%s ( %s )" % (self.keyword, self.name))
        
    def get_attribute(
            self,
            name):
        attribute=None
        for att in self.attributes:
            if att.name == name:
                attribute=att
        return(attribute)
        
    def get_children(
            self,
            keyword=None,
            name=None):
        result=[]
        for el in self.child_elements:
            if keyword is None or el.keyword == keyword:
                if name is None or el.name == name:
                    result.append(el)
        return(result)
        

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
        logger = logging.getLogger('main.liberty.read_from_file')
        logger.info("Reading "+ filename)
        logger1 = logging.getLogger()
        logger1.info("Reading "+ filename)
        with open(filename, 'r') as fh:
            self.raw=fh.read().replace('\n','').replace(' ', '')
            #self.raw=re.sub('/\*[ a-zA-Z0-9.,;%_;:-]*\*/','',self.raw)
            self.raw=re.sub('/\*.+?(?=\*/)\*/','',self.raw)
            #self.raw=re.sub('\\','',self.raw)
            self.pos=0
        with open('dump.lib', 'w') as fh:
            fh.write(self.raw)

    def recursive_parse(
            self,
            current_element=None,
            start=0,
            end=None):
        logger = logging.getLogger('main.liberty.recursive_parse')
        if end is None:
            end=len(self.raw)-1
        pos=start
        buffer_start=start
        #logger.debug('start = %s, end = %s' % (start, end))
        while pos <= end:
            buffer_end=pos
            #logger.debug('pos = ' + str(pos) )
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
                m=re.match('^\s*(\w+)\(([a-zA-Z_.,0-9"]*)\)',self.raw[buffer_start:pos+1])
                if not m:
                    logger.error("Unable to parse: %s" % ( self.raw[buffer_start:pos+1] ) )
                    exit(1)
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

    # def find_elements(
    #         self,
    #         keyword=None,
    #         name=None,
    #         parent_element=None,
    #         recursion=False, ### True means that function called by recursion, should be used only during recursion call inside this function
    #         ):
    #     if recursion is False:
    #         self.find_results =  []
    #     if parent_element is None:
    #         parent_element = self.root
    #     for el in parent_element.child_elements:
    #         flag = True
    #         if keyword is not None and el.keyword != keyword:
    #             flag=False
    #         elif name is not None and el.name != name:
    #             flag=False
    #         if flag:
    #             self.find_results.append(el)
    #         self.find_elements(keyword=keyword,name=name,parent_element=el, recursion=True)
    #     return(self.find_results)
    
    # def get_table(
    #         self,
    #         cell_name,
    #         pin_name,
    #         table_name):
    #     logger = logging.getLogger('main.liberty.get_table')
    #     result=[]
    #     cells = self.find_elements(keyword="cell", name=cell_name)
    #     if len(cells) > 1:
    #         logger.error("More than one cell with name \"%s\" was found in the library" % cell_name)
    #         exit(1)
    #     if len(cells) < 1:
    #         logger.error("Cell with name \"%s\" was not found in the library" % cell_name)
    #         exit(1)
    #     pins = self.find_elements(keyword="pin", name=pin_name,parent_element=cells[0])
    #     if len(pins) > 1:
    #         logger.error("More than one cell/pin with name \"%s/%s\" was found in the library" % ( cell_name, pin_name ) )
    #         exit(1)
    #     if len(pins) < 1:
    #         logger.error("Cell/pin with name \"%s/%s\" was not found in the library" % ( cell_name, pin_name ) )
    #         exit(1)
    #     for pin in pins:
    #         print(pin.echo())
    #         print(pin.get_attribute('direction').echo())
            
    def get_cell_pins(
            self,
            cell_name,
            direction=None):
        pass
        
        
    def get_cell_names(
            self):
        cell_names=[]
        cells = self.root.get_children(keyword="cell")
        for c in cells:
            cell_names.append(c.name)
        return(cell_names)
        
