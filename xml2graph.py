#!/usr/bin/env python
from __future__ import print_function
import optparse as op
from lxml import etree
import os
import graphviz as gv

class Method(object):
  def __init__(self,xmlMethod):
    
    #get name
    self.name=xmlMethod.find("name").text
    print(self.name)
    
    #get visibility
    xmlVisilibity=xmlMethod.find("visibility")
    self.visibility=""
    if xmlVisilibity!=None:
      self.visibility=xmlVisilibity.text
    
class Attribute(object):
  def __init__(self,xmlAttribute):
    
    #get name
    self.name=xmlAttribute.find("name").text
    print(self.name)
    
    #get visibility
    xmlVisilibity=xmlAttribute.find("visibility")
    self.visibility=""
    if xmlVisilibity!=None:
      self.visibility=xmlVisilibity.text
      
    #get type
    xmlType=xmlAttribute.find("type")
    self.type=""
    if xmlType!=None:
      self.type=xmlType.text
      
    #get value
    xmlValue=xmlAttribute.find("value")
    self.value=""
    if xmlValue!=None:
      self.value=xmlValue.text
class Class(object):
  def __init__(self,xmlClass):
    
    #get name
    self.name=xmlClass.find("name").text
    print(self.name)
    
    #get attributes
    xmlAttributes=xmlClass.find("attributes")
    self.attributes=[]
    for xmlAttribute in xmlAttributes:
      attributeTemp=Attribute(xmlAttribute)
      self.attributes.append(attributeTemp)
    
    #get methods
    xmlMethods=xmlClass.find("methods")
    self.methods=[]
    for xmlMethod in xmlMethods:
      methodTemp=Method(xmlMethod)
      self.methods.append(methodTemp)
  def getNodeLabel(self):
    
    #add class name
    label="{"+self.name+"|"
    
    #add attributes
    for attribute in self.attributes:
    
      label+=attribute.visibility+" "+attribute.name
      if attribute.type!="":
        label+=" : "+attribute.type
      if attribute.value!="":
        label+=" = "+attribute.value
      label+="\l"
    
    label+="|"
    
    #add methods
    for method in self.methods:
      label+=method.visibility+" "+method.name+"\l"
    label+="}"
    return label
  def addToGraph(self,graph):
    graph.node(name=self.name,label=self.getNodeLabel(),shape="record")
class Package(object):
  def __init__(self,xmlPackage):
    
    #get name
    self.name=xmlPackage.find("name").text
    print(self.name)
    
    #get classes
    xmlClasses=xmlPackage.find("classes")
    self.classes=[]
    for xmlClass in xmlClasses:
      classTemp=Class(xmlClass)
      self.classes.append(classTemp)
  def getGraph(self):
    graph=gv.Digraph(self.name)
    
    #add classes to graph
    for classTemp in self.classes:
      classTemp.addToGraph(graph)
    return graph
class PackageManager(object):
  def __init__(self,xmlPackages):
    """
    """
    
    self.packages=[]
    for xmlPackage in xmlPackages:
      
      #create a packages
      package=Package(xmlPackage)
      self.packages.append(package)
  def getGraph(self):
    graph=gv.Digraph(format="pdf")
    for package in self.packages:
      graph.subgraph(package.getGraph())
    return graph
  def drawGraph(self):
    
    #get the graph to draw
    graph=self.getGraph()
    
    #save as "test" dot file and render to pdf as "test.pdf"
    filename=graph.render(filename="test")
def parseOptions():
  """Parses command line options
  
  """
  
  parser=op.OptionParser(usage="Usage: %prog [options] XMLINPUT"
    ,version="%prog 1.0"
    ,description="Draws a graph from the given XMLINPUT file")
  
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
  packageManager.drawGraph()
  
if __name__ == "__main__":
 main()