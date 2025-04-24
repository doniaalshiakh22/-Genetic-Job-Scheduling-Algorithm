# Genetic Job Scheduling with a Genetic Algorithm

## Project Summary
This repository demonstrates how to optimize job-shop scheduling in a manufacturing environment using a Genetic Algorithm (GA). The goal is to minimize the overall makespan—the total time required to complete all jobs across multiple machines.

---

## Genetic Algorithm Workflow
The process consists of the following key stages:

1. **Population Initialization**  
   Generate an initial set of chromosomes, where each chromosome is a permutation of job identifiers.

2. **Fitness Assessment**  
   For every chromosome, simulate the schedule it encodes and compute the makespan. Shorter completion times correspond to higher fitness.

3. **Parent Selection**  
   Select candidates for reproduction based on their fitness values, typically using a tournament or roulette-wheel approach.

4. **Crossover**  
   Combine pairs of parent chromosomes to produce offspring, mixing job sequences to explore new scheduling orders.

5. **Mutation**  
   Introduce random swaps or inversions in offspring with a low probability, ensuring genetic diversity and preventing premature convergence.

6. **Population Update**  
   Form the next generation by replacing the old population with the newly produced children. Repeat the cycle for a predefined number of generations or until convergence.

---

## Scheduling Function
The core scheduling routine takes two inputs: a chromosome (ordering of jobs) and the job definitions. It then:

1. Iterates through the job sequence encoded by the chromosome.  
2. Assigns each operation to its designated machine, tracking both machine availability and job readiness.  
3. Calculates idle and waiting times when a job arrives before its machine is free.  
4. Records each task’s start and finish times, updating machine timelines accordingly.  
5. Returns the final completion time (makespan) once all operations are scheduled.

---

## Chromosome Representation
A chromosome is simply an ordered list of job indices. For example:  
```[2, 0, 1, 3]```  
means process job `2` first, followed by job `0`, then `1`, and finally `3`.  

By evolving these sequences over multiple generations, the genetic algorithm searches for the arrangement that yields the smallest makespan.

---

## Example Output
Below is a simplified illustration of how scheduled tasks might look across four machines for two jobs (Job_1 and Job_2). Numbers in brackets indicate job labels, and time markers show start and end times:

```
Best Chromosome: [1, 2]

M1 | 0-[Job_1]10-------37-[Job_2]45 |
M2 | 0-----10-[Job_1]15----22-[Job_2] |
M3 | 0-------------22-[Job_2]37 |
M4 | 0-----15-[Job_1]27 |

Total Makespan: 45
```

Adjust parameters such as population size, crossover rate, and mutation probability in `main.py` to explore different performance characteristics.

---

