# PROTEIN FOLDING

We can begin with a simplified version of the 2D HP model in the square lattice.
- 2D: real proteins fold in 3D. Alternatives (3D):
    - simple cubic lattice
    - body centered cubic lattice
    - face centered cubic lattice

- Square lattice: real proteins also don't always fold in 90º angles. Alternatives:
    - Triangular lattice

This simplified model has only two types of aminoacids, H and P. H stands for 
hydrophobic and P for polar. As the name states it, the H is afraid of water. 
In our body, proteins are suspended in water (or mostly water), however, some 
of the aminoacids must not be in contact with it (they react), while others 
can. When the protein folds, the H aminoacids must be on the inside, that is
why the score is measured by the number of H molecules that are bonded. The
more H molecules are bonded, the more grouped are, and the less surface touching
the outside, where it can be the nasty water.


## Modelization
- Elements:
    - H: Hydrophobic
    - P: Hydrophili (polar)
    - H-H edge
    - H-P edge
    - H-H bond

- Score: Number of H-H bonds 


## Problem 
**Maximize the number of H-H bonds** . Technically, the H-H edge is also
a H-H bond, but they are not mutable, as we would be breaking the 
structure of the protein, so these are ignored.


## Notes and observations of the problem
- In this first 2D squared lattice, a typical node (except the first and 
the last) has 2 edge neighbors and 2 other neighbors. 
- The optimal folding has the maximum score
- Considdering the string of molecules, only even and odd H's can possibly
bond together, (because of the 2D squared lettuce).
- OPT <= 2·min{#even H's, #odd H's}. Explanation:
        + Every bond defines an even and an odd 
        + Every even and odd can only get hit up to twice
        + If there is more even than odds its not going to help, as there is 
        + way to use more even than odds (excludig first and last)


## Hardness
This problem is already NP-hard.
To find the optimal folding of a given HP string is NP-Hard. First it was proved
that 3D HP was NP-Hard, later was proved that 2D also.


<!-- We are going to work out the estimate combinatory. To make it easy we won't be speaking
in terms of aminoacids, but in terms of slots of each aminoacid. Each aminoacid has 2
slots, so there are 2·k blanks to fill. In each blank we can put any other bound 
(remember, there are 2·k of them) plus 1, because we can leave a empty bound. Adding up
the previous premises, we have 2·k blanks to fill with 2·k+1 possible fillings. That is
the same as saying (2·k+1)^(2·k). Now let's work out with that number:

   - having a protein string of length k, we consider that all aminoacids could be H,
      that's why whe have the last k, in (2k+1)^(2k)
   
   - One aminoacid can bound at maximum 2 times and at minimmum 0, thats why we have
      the 2 in (2k+1)^(2k)

   - If one aminoacid bounds, it can't be with itself, so the formula needs to be
      adjusted to (2k)^(2k) 
   
   - If one aminoacid bounds two times, it has to be with different aminoacids, the
      formula we have now is (k)^(2k)

   - If a[1] is the aminoacid in position 1, a[1][0] and a[1][1] are their 
      left and right bound space, respectively. Nevertheless this is indferent, so 
      combinatory speaking we don't diferenciate left and right.

   - The bounds are symetrical, so if the aminoacid 4 is chained with the 9th, the 9th
      is also chained to the 4th. Having said that, not all the H can be paired, so we 
      can't get by permutating half of the chain, as we would be able to do otherwise
-->
    


### Approximations 
- 1/3 - approximations: this approximation is based on the fact that the 
optimal number of H bonds is OPT <=2·min{#even H's, #odd H's}. The goal is to 
get 1/3 of OTP. To reach the 1/3, a set of stages are followed. Following them
the chance of finding relatively quickli a 1/3 of the OPT is high.


## Implementation schema
Basic, implementation schema idea storm.
- Iteration 0.1
    + A file stores a secuence of H and P letters and other parametters
    + Seed parametter, to be able to track random walks
    + Maximum number of steps, in order not to get stuck searching the optimum
    + The program will check for all the combinations, storing the one with better score 
    + We will think about representation later
    + First implementation will be in python
- Iteration 0.2
    + Iteration 0.1 almost completed. Jumping to 0.2
    + Fix different usages with arguments
    + It will have a benchmark mode, this mode will give the time that has taken to make
   a given number of folds. To make the bench more even, the number of folds and the protein
   will be given.

## Use
:


## Other stuff

- The hydrophobicity of a protein is a parametter heavily researched.
- The natural folding of proteins is a very unknown field, it is 
supposed that all information of how to fold a protein lies in its
aminoacids, so there is no such thing as an Ikea guide that the cell
has. So the combinatory problem is so large that it is already not 
know how it is thone for the cell to acquire the lowest energy
configuration for that protein, wich is what makes it functional, 
(otherwise is considered "dead").
- To know the folding configuration maded naturally by the cells it is 
needed a process that can take a lot of research, money and time. To
throw some light, it is needed to cristalise a proteine (wich can take
years of research). From that you get one 3D image that is collected in
a protein data bank. 
