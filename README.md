Requirements:
  - graphviz executable
    - install with `sudo apt-get install graphviz
  - graphviz python module:
    - install with `pip install graphviz`
  - lxml python module:
    - install with `pip install lxml`
Installation

$ sudo python setup.py install

Types of edges:

Dependency:
  - description: the source class has some sort of dependency on the target
    class. This is very general and should be only used when more specific
    alternatives do not fit.
  - style: dashed line, vee arrow

Association:
  - description: means that the source class contains and uses one instance 
    of the target class.
  - style: solid line, vee arrow

Aggregation:
  - description: a type of association where the source class contains a 
    reference to an instance of the target class as part of its state and the
    scope of the contained object is not the same as that of the container.
  - style: solid line, vee arrow, open diamond at tail
  
Composition:
  - description: Similar to aggregation except that the scopes of contained 
    object is the same as the scope of the container.
  - style: solid line, vee arrow, solid diamond at tail
  
Generalization:
  - description: shows that the source class inherits the target class
  - style: solid line, open triangle arrow
  
Realization:
  - description: the source class is the implementation of an interface 
    described by the target class
  - style: dashed line, open triangle arrow
  
Each of the above can optionally have labels added at the head or tail of the 
arrow to indicate "multiplicity". An example would be a mother cat can have 
multiple kittens, each kitten has one mother.
