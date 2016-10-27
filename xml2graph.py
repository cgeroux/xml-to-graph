#!/usr/bin/env python
from __future__ import print_function
import optparse as op
from lxml import etree
import os
import graphviz as gv

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
    if len(self.parameters)>0:
      label+="("
      count=0
      for parameter in self.parameters:
        if count==0:
          label+=parameter.getLabel()
          count+=1
        else:
          label+=", "+parameter.getLabel()
          count+=1
      label+=")"
    label+="\l"
    return label
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
  def addToGraph(self,graph):
    """
    """
    
    graph.node(name=self.name,label=self.getLabel(),shape="record"
    ,fontname="courier new")
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
  def getGraph(self):
    """
    """
    
    graph=gv.Digraph(self.name)
    
    #add classes to graph
    for classTemp in self.classes:
      classTemp.addToGraph(graph)
    return graph
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
  def getGraph(self,format="pdf"):
    """
    """
    
    graph=gv.Digraph(format=format)
    graph
    for package in self.packages:
      graph.subgraph(package.getGraph())
    return graph
  def drawGraph(self,fileName):
    """
    """
    
    #get the graph to draw
    graph=self.getGraph()
    
    #save as fileName dot file and render to pdf as fileName+".pdf"
    filename=graph.render(filename=fileName)
def parseOptions():
  """Parses command line options
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] XMLINPUT"
    ,version="%prog 1.0"
    ,description="Draws a graph from the given XMLINPUT file")
  
  parser.add_option("-o",action="store"
    ,dest="outputFileName"
    ,help="Sets the output file name. File extension added automatically "
    +"[default: %default].",default="graph")
  
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
  
  #draw graph
  packageManager.drawGraph(options.outputFileName)
if __name__ == "__main__":
 main()