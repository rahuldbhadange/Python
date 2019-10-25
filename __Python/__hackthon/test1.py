"""WIN or LOSE (100 Marks)
A new fighting game has become popular.
There are N number of villains with each having some strength.
There are N players in the game with each having some energy.
The energy is used to kill the villains.
The villain can be killed only if the energy of the player is greater than the strength of the villain.

Maxi is playing the game and at a particular time wants to know if it is possible
for him to win the game or not with the given set of energies and strengths of players and villains.
Maxi wins the game if his players can kill all the villains with the allotted energy.


Input Format
The first line of input consist of number of test cases, T.
The first line of each test case consist of number of villains and player, N.
The second line of each test case consist of the N space separated strengths of Villains.
The third line of each test case consist of N space separated energy of players.


Constraints
1<= T <=10
1<= N <=1000
1<= strength , energy <=100000

Output Format
For each test case, Print WIN if all villains can be killed else print LOSE in separate lines.

Sample TestCase 1
Input
1
6
112 243 512 343 90 478
500 789 234 400 452 150

Output
WIN
Explanation
For the given test case, If we shuffle the players and villains,
we can observe that all the villains can be killed by players.



Player

Villain

RESULT

500

478

WIN

789

512

WIN

234

112

WIN

400

243

WIN

452

343

WIN

150

90

WIN


As all the villains can be killed by the players, MAXI will WIN the game. Thus, the final output is WIN.
Sample TestCase 2
Input"""


Villains = [10, 20, 50, 100, 500, 400]
print(Villains, type(Villains))
Players = [30, 9, 40, 70, 90, 490]
print(Players, type(Players))


def main(Villains, Players):
    Villains.sort()
    print("Strength: ", Villains)
    Players.sort()
    print("Energy: ", Players)

    for strength in Villains:
        for energy in Players:
            if energy > strength:
                yield energy, strength, "LOOSE"
                # strength = strength + 1
                # energy = energy + 1
                # yield energy, strength, "WIN"
                break
            else:
                yield (energy, strength, "WIN")
                # strength = strength + 1
                # energy = energy + 1
                break


gen = main(Villains, Players)
print(gen)
for g in gen:
    print(g)
