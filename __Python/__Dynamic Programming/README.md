The image above says a lot about Dynamic Programming. So, is repeating the things for which you already have the answer, a good thing ? A programmer would disagree. That's what Dynamic Programming is about. To always remember answers to the sub-problems you've already solved.

Let us say that we have a machine, and to determine its state at time t, we have certain quantities called state variables. There will be certain times when we have to make a decision which affects the state of the system, which may or may not be known to us in advance. These decisions or changes are equivalent to transformations of state variables. The results of the previous decisions help us in choosing the future ones.

What do we conclude from this? We need to break up a problem into a series of overlapping sub-problems, and build up solutions to larger and larger sub-problems. If you are given a problem, which can be broken down into smaller sub-problems, and these smaller sub-problems can still be broken into smaller ones - and if you manage to find out that there are some over-lappping sub-problems, then you've encountered a DP problem.

Some famous Dynamic Programming algorithms are:

Unix diff for comparing two files
Bellman-Ford for shortest path routing in networks
TeX the ancestor of LaTeX
WASP - Winning and Score Predictor
The core idea of Dynamic Programming is to avoid repeated work by remembering partial results and this concept finds it application in a lot of real life situations.

In programming, Dynamic Programming is a powerful technique that allows one to solve different types of problems in time O(n2) or O(n3) for which a naive approach would take exponential time.

Jonathan Paulson explains Dynamic Programming in his amazing Quora answer here.

Writes down "1+1+1+1+1+1+1+1 =" on a sheet of paper. 
"What's that equal to?"
Counting "Eight!"
Writes down another "1+" on the left. 
"What about that?"
"Nine!" " How'd you know it was nine so fast?"
"You just added one more!" 
"So you didn't need to recount because you remembered there were eight! Dynamic Programming is just a fancy way to say remembering stuff to save time later!"