import re

class liberty_array:
    pass



class liberty_attribute:
    name=""
    value=""
    
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
    child_elements=[]
    attributes=[]
    arrays=[]
    keyword=""
    name=""
    level=0
    
    def __init__(
            self,
            keyword=None,
            name="",
            level=0):
        self.keyword=keyword
        if self.keyword is not None:
            #print(self.keyword)
            pass
        self.level=level
        self.name=name
    
    def add_child_element(
            self,
            element):
        self.child_elements.append(element)



class liberty:
    root=None
    pos=0

    def __init__(
            self,
            filename=None):
        #print("Hellow World from Liberty class!")
        self.raw=None
        if filename is not None:
            self.read_from_file(filename)
        
    def read_from_file(
            self,
            filename):
        with open(filename, 'r') as fh:
            self.raw=fh.read().replace('\n','').replace(' ', '')
            self.raw=re.sub('/\*.*\*/','',self.raw)
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
        buffer_end=start
        while pos <= end:
            buffer_end=pos
            if self.raw[pos] == ";":
                #print(self.raw[buffer_start:pos+1])
                if self.is_attribute(self.raw[buffer_start:pos+1]):
                    print("%s%s" % ( '    '*(current_element.level+1), self.raw[buffer_start:pos+1] ) )

                # is_array to be here
                    
                buffer_start=pos+1
                pos+=1
                continue
            if self.raw[pos] == "{":
                #print(self.raw[buffer_start:pos+1])
                m=re.match('^\s*(\w+)\((\w*)\)',self.raw[buffer_start:pos+1])
                keyword=m.group(1)
                name=m.group(2)
                if current_element is None:
                    self.root=liberty_element(keyword=keyword,name=name)
                    print("<%s>" % keyword)
                    pos=self.recursive_parse(start=pos+1,current_element=self.root)
                    print("</%s>" % keyword)
                    buffer_start=pos
                else:
                    new_element=liberty_element(keyword=keyword,name=name,level=current_element.level+1)
                    print("%s<%s> %d" % ( '    '*new_element.level, keyword, pos))
                    pos=self.recursive_parse(start=pos+1,current_element=new_element)
                    print("%s</%s> %d" % ( '    '*new_element.level, keyword, pos))
                    buffer_start=pos
                    current_element.add_child_element(new_element)
                continue
            if self.raw[pos] == "}":
                return(pos+1)
            pos+=1
    
    def recursive_print(
            self,
            element):
        print("element: %s" % element)
        print("element.child_elements: %s" % element.child_elements )
        print("%s%s ( %s ) {" % ( '    '*element.level, element.keyword, element.name) )
        for child_element in element.child_elements:
            print(child_element)
            self.recursive_print(child_element)
        print("%s}" % '    '*element.level )
        
    
    def print_lib(self):
        self.recursive_print(self.root)
        
    
    def is_attribute(
            self,
            string):
        #print(string)
        m = re.match('^\s*[a-zA-Z0-9_]+\s*:\s*[a-zA-Z0-9_”"]+\s*;\s*$',string);
        if m:
            #print('+')
            return(True)
        return(False)

    def out(self):
        print(self.raw)
    