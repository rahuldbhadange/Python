poly (many) + morph (form) + -ism.


Polymorphism literally means "many shapes", and that's pretty good at explaining its purpose. 
The idea behind polymorphism is that one can use the same calls on different types and have them behave appropriately.

It is important to distinguish this from the typing system - strongly typed languages require that objects be related through an inheritance chain to be polymorphic, but with weakly typed languages, this is not necessary.

In Java (et al.), this is why interfaces are useful - they define the set of functions that can be called on objects without specifying the exact object - the objects that implement that interface are polymorphic with respect to that interface.

In Python, since things are dynamically typed, the interface is less formal, but the idea is the same - calling foo() will succeed on two objects that know how to properly implement foo(), but we don't care about what type they really are

Polymorphism is where you have two classes that inherit from a main class but each implement a method differently.

Polymorphism is the concept that there can be many different implementations of an executable unit and the difference happen all behind the scene without the caller awareness.

For example, Bird and Plane are FlyingObject. So FlyingObject has a method call fly() and both Bird and Plane implement fly() method. Bird and Plan flies differently so the implementations are different. To the clients point of view, it does not matter how Bird or Plane fly, they can just call fly() method to a FlyingObject object does not matter if that object is Plan or Bird.


One particular kind of polymorphism, usually called parametric polymorphism in the functional community and generic programming in the OOP community, is the ability to perform certain operations on an object without caring about its precise type.
For example, to reverse a list, you don't need to care about the type of the elements of the list, you just need to know that it's a list.
So you can write generic (in this sense) list reversal code: it'll work identically on lists of integers, strings, widgets, arbitrary objects, whatever.
But you can't write code that adds the elements of a list in a generic way, because the way the elements are interpreted as numbers depends on what type they are.


Another kind of polymorphism, usually called ad-hoc polymorphism or (at least for some forms of it) generic programming in the functional community, 
and often subtyping polymorphism (though this somewhat restricts the concept) in the OOP community, it the ability to have a single method or function that behaves differently depending on the precise type of its arguments (or, for methods, the type of the object whose method is being invoked).
The add example above is ad-hoc polymorphism.
In dynamically typed languages this ability goes without saying; statically-typed languages tend to (but don't have to) have restrictions such as requiring that the argument be a subclass of some particular class (Addable).

Polymorphism is not about having to specify types when you define a function. That's more related to static vs. dynamic typing, though it's not an intrinsic part of the issue. Dynamically typed languages have no need for type declarations, while statically typed languages usually need some type declarations (going from quite a lot in Java to almost none in ML).


In some languages that lack polymorphism you find yourself in situations where you want to perform what is conceptually the same operation on different types of objects, in cases where that operation has to be implemented differently for each type. For instance, in a python-like syntax:


def dosomething(thing):

   if type(thing)==suchandsuch:
   
      #do some stuff
        
   elif type(thing)==somesuch: 
   
      #do some other stuff
      
   elif type(thing)==nonesuch:
   
      #yet more stuff
      
      
There are some problems with this. The biggest is that it causes very tight coupling and a lot of repetition. You are likely to have this same set of tests in a lot of places in your code. What happens if you add a new type that has to support this operation? You have to go find every place you have this sort of conditional and add a new branch. And of course you have to have access to all the source code involved to be able to make those changes. On top of that conditional logic like this is wordy, and hard to understand in real cases.

It's nicer to be able to just write:

thing.dosomething()

On top of being a lot shorter this leads to much looser coupling. This example/explanation is geared to traditional OO languages like Python. The details are a bit different in, say, functional languages. But a lot of the general utility of polymorphism remains the same.