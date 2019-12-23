Non-static variables:The variables which are declared by
using the name self are known as non-static variables or
instance variables.

properties of Non-static variable:
    1.If data is changing from one object to another
    object--->then we use non-static variable
    ex:-ename,eid,designation,salary.
    
    2.For all the non-static variables of a class,memory will
      be allocated whenever we create a object.
      
      -for static variable, memory is allocated only once, but
      -for non static variable, memory is allocated for 'n' no
       of times,depending on no of objects
      
    3. object is used to allocate memory for non-static
       variable,whenever object is created,that memorylocation
       address of the object is taken by python interpreter
       and creates indirect address and this indirect address
       is allocated to a variable called reference variable.
       
    4.with respect to every object creation,seperate copy of
      memory will be allocated to non-static variables of the
      class.
    5.Non-static variables of a class can be accessed by all
      the methods of the same class by using self.
    6. Non-static variables of one class can be accessed
       ouside of that class by using reference variable.
      
          


       
          
    
    

    
    
