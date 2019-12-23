Garbage collector:
Garbage collector is a pre-defined program or application or background
thread which is invoked by the python interpreter whenever any object
reference count becomes zero at the time of execution of the program.

Garbage collector removes the unused or unreferenced objects from the
memory location
If any object reference count becomes  as a zero,then we call that object
as a unused or unreferenced object.

Reference count is equal to the number of Reference variables pointing to
that object.

ex:
    t1=test()
    t2=t1
    t3=t1
    here all 3 ref variables are storing address(pointing) of
    same object,so R.C=3 which is equal to no of ref variables(3)


whenever any object is removed from the memory location,then
Destructor of that class will be executed.
