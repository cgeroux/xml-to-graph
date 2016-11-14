#!/usr/bin/env python
from __future__ import print_function
import optparse as op
from lxml import etree
import os
import subprocess

__version__="1.0.0"

class Parameter(object):
  """Holds data pertaining to a method parameter and generates a label for that
  parameter.
  """
  
  def __init__(self,xmlParamter):
    """Save parameter attributes from xml node
    """
    
    #get name
    self.name=xmlParamter.find("name").text
    
    #get type
    xmlType=xmlParamter.find("type")
    self.type=None
    if xmlType!=None:
      self.type=xmlType.text
      
    #get direction
    xmlDirection=xmlParamter.find("direction")
    self.direction=None
    if xmlDirection!=None:
      self.direction=xmlDirection.text
  def getLabel(self):
    """Returns a string to use in a dot diagram to describe this parameter.
    """
    
    label=""
    
    #add visibility if we have it
    if self.direction!=None:
      label+=self.direction+" "
    
    #add name
    label+=self.name
    
    #add type if we have it
    if self.type!=None:
      label+=" : "+self.type
    return label
class Attribute(object):
  """Holds data pertaining to a class attributes and generates a label for that
  attribute.
  """
  
  def __init__(self,xmlAttribute):
    """Save attribute attributes from xml node
    """
    
    #get name
    self.name=xmlAttribute.find("name").text
    
    #get visibility
    xmlVisilibity=xmlAttribute.find("visibility")
    self.visibility=None
    if xmlVisilibity!=None:
      self.visibility=xmlVisilibity.text
      
    #get type
    xmlType=xmlAttribute.find("type")
    self.type=None
    if xmlType!=None:
      self.type=xmlType.text
    
    #get scope
    xmlScope=xmlAttribute.find("scope")
    self.scope="inside"
    if xmlScope!=None:
      self.scope=xmlScope.text
    
    #get value
    xmlValue=xmlAttribute.find("value")
    self.value=None
    if xmlValue!=None:
      self.value=xmlValue.text
  def getLabel(self):
    """Returns a string to use in a dot diagram to describe this class 
    attribute.
    """
    
    label=""
    
    #add visibility if we have it
    if self.visibility!=None:
      label+=self.visibility+" "
    
    #add name
    label+=self.name
    
    #add type if we have it
    if self.type!=None:
      label+=" : "+self.type
    
    #add value if we have it
    if self.value!=None:
      label+=" = "+self.value
    return label
class Method(object):
  """
  """
  
  def __init__(self,xmlMethod):
    """
    """
    
    #get name
    self.name=xmlMethod.find("name").text
    
    #get visibility
    xmlVisilibity=xmlMethod.find("visibility")
    self.visibility=None
    if xmlVisilibity!=None:
      self.visibility=xmlVisilibity.text
    
    #get return type
    xmlReturnType=xmlMethod.find("return-type")
    self.returnType=None
    if xmlReturnType!=None:
      self.returnType=xmlReturnType.text
    
    #get parameters
    self.parameters=[]
    xmlParameters=xmlMethod.find("parameters")
    if xmlParameters!=None:
      for xmlParameter in xmlParameters:
        self.parameters.append(Parameter(xmlParameter))
  def getLabel(self):
    """
    """
    
    label=""
    
    #add visibility if we have it
    if self.visibility!=None:
      label+=self.visibility+" "
    
    #add name
    label+=self.name
    
    #add parameters if we have then
    label+="("
    if len(self.parameters)>0:
      count=0
      for parameter in self.parameters:
        if count==0:
          label+=parameter.getLabel()
          count+=1
        else:
          label+=", "+parameter.getLabel()
          count+=1
    label+=")"
    
    #add return type
    if self.returnType!=None:
      label+=" : "+self.returnType
    return label
  def getTypes(self):
    
    #add return type
    types=set()
    if self.returnType!=None:
      types.add(self.returnType)
    
    #add parameter types
    for parameter in self.parameters:
      if parameter.type!=None:
        types.add(parameter.type)
    
    return types
class Dependency(object):
  """
  """
  
  def __init__(self,source,xml=None,target=None,type=None):
    """
    """
    
    self.source=source
    
    #set from xml
    if xml!=None:
    
      #get target
      self.target=xml.find("target").text
      
      #get type
      xmlType=xml.find("type")
      self.type="dependency"
      if xmlType!=None:
        self.type=xmlType.text
    
    #override from keywords
    if target!=None:
      self.target=target
    if type!=None:
      self.type=type
  def __eq__(self,other):
    return self.__dict__==other.__dict__
  def __ne__(self,other):
    return not self==other
class Class(object):
  """
  """
  
  def __init__(self,xmlClass):
    """
    """
    
    #get name
    self.name=xmlClass.find("name").text
    
    #get stereotype
    xmlStereotype=xmlClass.find("stereotype")
    self.stereotype=None
    if xmlStereotype!=None:
      self.stereotype=xmlStereotype.text
    
    #get attributes
    xmlAttributes=xmlClass.find("attributes")
    self.attributes=[]
    if xmlAttributes!=None:
      for xmlAttribute in xmlAttributes:
        attributeTemp=Attribute(xmlAttribute)
        self.attributes.append(attributeTemp)
    
    #get methods
    xmlMethods=xmlClass.find("methods")
    self.methods=[]
    if xmlMethods!=None:
      for xmlMethod in xmlMethods:
        methodTemp=Method(xmlMethod)
        self.methods.append(methodTemp)
    
    #get parents
    xmlParents=xmlClass.find("parents")
    self.parents=[]
    if xmlParents!=None:
      for xmlParent in xmlParents:
        self.parents.append(xmlParent.text)
    
    #add implicit dependencies
    tempDep=[]
    
    #add attribute types
    for attribute in self.attributes:
      if attribute.type!=None:
        
        #remove "*" to match types directly
        typeTmp=attribute.type.replace("*","")
        dependencyType="composition"
        if attribute.scope=="outside":
          dependencyType="aggregation"
        tempDep.append(Dependency(self.name,target=typeTmp
          ,type=dependencyType))
    
    #add types from methods
    for method in self.methods:
      methodTypes=method.getTypes()
      for type in methodTypes:
        typeTmp=type.replace("*","")
        tempDep.append(Dependency(self.name,target=typeTmp
            ,type="dependency"))
    
    #add parents
    for parent in self.parents:
      tempDep.append(Dependency(self.name,target=parent
        ,type="inheritance"))
      
    #get dependencies
    xmlDependencies=xmlClass.find("dependencies")
    if xmlDependencies!=None:
      for xmlDependency in xmlDependencies:
        dependencyTemp=Dependency(self.name,xmlDependency)
        tempDep.append(dependencyTemp)
    
    #finally filter out duplicates
    self.dependencies=[]
    for dep in tempDep:
      if dep not in self.dependencies:
        self.dependencies.append(dep)
  def getLabel(self):
    """
    """
    
    label="{"
    
    #add stereotype if we have one
    if self.stereotype!=None:
      #label+=self.stereotype+"\l"
      label+="\<\<"+self.stereotype+"\>\> \\n"
      
    #add class name
    label+=self.name
    
    if len(self.attributes)>0 or len(self.methods)>0:
      label+="|"
    
    #add attributes
    for attribute in self.attributes:
      label+=attribute.getLabel()+"\l"
    
    #add attribute method seperator if we have methods
    if len(self.methods)>0:
      label+="|"
    
    #add methods
    for method in self.methods:
      label+=method.getLabel()+"\l"
    
    label+="}"
    return label
  def addToGraph(self,file):
    """
    """
    
    file.write("\t\t\""+self.name+"\" [label=\""+self.getLabel()
      +"\" color=black fillcolor=white fontname=\"courier new\""
      +" shape=record style=filled]\n")
  def getDependencies(self):
    """Returns a list of dependencies
    """
    
    return self.dependencies
class Package(object):
  """
  """
  
  def __init__(self,xmlPackage):
    """
    """
    
    #get name
    self.name=xmlPackage.find("name").text
    
    #get classes
    xmlClasses=xmlPackage.find("classes")
    self.classes=[]
    for xmlClass in xmlClasses:
      classTemp=Class(xmlClass)
      self.classes.append(classTemp)
  def addGraph(self,file):
    """
    """
    
    file.write("\tsubgraph cluster_"+self.name+" {\n")
    
    #add classes to graph
    for classTemp in self.classes:
      classTemp.addToGraph(file)
    
    file.write("\t\tlabel="+self.name+"\n")
    file.write("\t\tstyle=filled\n")
    file.write("\t\tcolor=black\n")
    file.write("\t\tfillcolor=gray94\n")
    file.write("\t}\n")
  def getClasses(self):
    classes=[]
    
    for classTemp in self.classes:
      classes.append(classTemp.name)
    return classes
class PackageManager(object):
  """
  """
  
  def __init__(self,xmlPackages):
    """
    """
    
    self.packages=[]
    for xmlPackage in xmlPackages:
      
      #create a packages
      package=Package(xmlPackage)
      self.packages.append(package)
  def addEdges(self,file):
    """Adds edges to given graph
    """
    
    #get list of all classes
    classes=[]#assume no duplicated class names
    for package in self.packages:
      classes+=package.getClasses()
    
    #add edges
    for package in self.packages:
      for classTmp in package.classes:
        dependencies=classTmp.getDependencies()
        for dependency in dependencies:
          if dependency.target in classes:
            
            #add edge from classTmp to type
            if dependency.type=="dependency":
              dir="forward"
              arrowhead="vee"
              arrowtail="none"
              style="dashed"
            elif dependency.type=="association":
              dir="forward"
              arrowhead="vee"
              arrowtail="none"
              style="solid"
            elif dependency.type=="aggregation":
              dir="both"
              arrowhead="vee"
              arrowtail="odiamond"
              style="solid"
            elif dependency.type=="composition":
              dir="both"
              arrowhead="vee"
              arrowtail="diamond"
              style="solid"
            elif dependency.type=="inheritance":
              
              #Find the target class
              classTarget=None
              for pacakgeInner in self.packages:
                for classTmp in pacakgeInner.classes:
                  
                  #if we found the target
                  if classTmp.name==dependency.target:
                    classTarget=classTmp
                    break
              if classTarget==None:
                raise Exception("the target class\""+dependency.target
                  +"\" should have been found, something has gone wrong")
              
              #set style depending on target's stero type
              if classTarget.stereotype==None:
                dir="forward"
                arrowhead="onormal"
                arrowtail="none"
                style="solid"
              elif classTarget.stereotype=="interface":
                dir="forward"
                arrowhead="onormal"
                arrowtail="none"
                style="dashed"
            
            file.write("\t\""+dependency.source+"\" -> \""+dependency.target
              +"\" [arrowhead="+arrowhead+" arrowtail="+arrowtail+" dir="
              +dir+" style="+style+"]\n")
  def writeGraph(self,fileName):
    """
    """
    
    file=open(fileName+".dot",'w')
    
    file.write("digraph {\n")
    for package in self.packages:
      package.addGraph(file)
    
    graph=self.addEdges(file)
    
    file.write("}\n")
    file.close()
    
    #create image
    format="pdf"
    subprocess.call(["dot","-T"+format,fileName+".dot","-o",fileName+"."+format])
def parseOptions():
  """Parses command line options
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] XMLINPUT"
    ,version="%prog 1.0"
    ,description="Draws a graph from the given XMLINPUT file")
  
  parser.add_option("-o",action="store"
    ,dest="outputFileName"
    ,help="Sets the output file name. File extension added automatically "
    +"[default: XMLINPUT with pdf extension].",default=None)
  
  #parse command line options
  return parser.parse_args()
def main():
  
  #parse command line options
  (options,args)=parseOptions()
  
  #check we got the expected number of arguments
  if (len(args)!=1):
    raise Exception("Expected an xml settings file.")
  
  #load schema to validate against
  schemaFileName=os.path.join(os.path.dirname(__file__),"xmlSchema/packages.xsd")
  schema=etree.XMLSchema(file=schemaFileName)
  
  #parse xml file
  tree=etree.parse(args[0])
  
  #strip out any comments in xml
  comments=tree.xpath('//comment()')
  for c in comments:
    p=c.getparent()
    p.remove(c)
  
  #validate against schema
  schema.assertValid(tree)
  
  #Parse XML Packages
  xmlPackages=tree.getroot()
  packageManager=PackageManager(xmlPackages)
  
  #if no output file set, use the input xml file without extension
  if options.outputFileName==None:
    options.outputFileName=os.path.splitext(args[0])[0]
  
  #draw graph
  packageManager.writeGraph(options.outputFileName)
if __name__ == "__main__":
 main()