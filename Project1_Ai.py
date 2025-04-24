import random #  'random' module, which provides functions to generate random numbers.

from collections import defaultdict # Importing defaultdict from the collections module, which provides a dictionary-like object that initializes a default value if the key does not exist.


class Job: # this to create object from job , each object jub must has two valus index and taske
    def __init__(self, index, tasks):
        self.index = index
        self.tasks = tasks

class Task: # this to create object from Task , each object jub must has seven valus index and taske
    def __init__(self, task, job_index, duration, task_order, started_time=None, ended_time=None):
        # initialize the Task object with attributes:
        self.task = task  # reprecent machine on which the task will run
        self.job_index = job_index  # this  index of the job to which this task belongs
        self.duration = duration
        self.task_order = task_order  # The order of the task in the job sequence
        self.started_time = started_time  # (initialized as None)
        self.ended_time = ended_time  #  (initialized as None)
        self.waited_time = 0  # the amount of time the task has waited to be processed (initialized to 0)

class Machine:
    def __init__(self, tasks=None, available=True):
        # to initialize the Machine object with attributes:
        if tasks is None: # If no tasks are provided,
            tasks = []  #initialize an empty list of tasks
        self.tasks = tasks  # The list of tasks assigned to this machine
        self.available = available  # The availability status of the machine (initialized to True)

# Function to red jobs from input file (jobs.txt)
def read_file (name_file):
    jobs = [] # List of jobs
    with open(name_file, 'r') as file: # to pen the file for reading
        for line in file:# repeat over each line in the file

            if line.strip():# this check if the line is not empty
                print(line.strip()) # print the line without leading or trailing whitespaces
                job_operate , tasks_str = line.split(':')# to split the line into job index and task descriptions
                job_operate  = int(job_operate .split('_')[1])# Extract the job index and convert it to an integer
                tasks = []  # to start an empty list to store tasks
                task_descriptions = tasks_str.strip().split(' -> ')# split the task descriptions into individual tasks
                order = 1 # initialize the order of tasks from 1
                for task_desc in task_descriptions: #for loop Iterate over each task description
                    machine, duration = task_desc.strip().split('[')# this split the task description into machine and duration
                    machine = machine.strip()[1:] # this extract the machine name and remove leading whitespace
                    duration = duration.strip(']') # this remove trailing ']' from duration and convert it to an integer
                    tasks.append(Task(machine, job_operate, int(duration), order))# to create a Task object and append it to the tasks list
                    order += 1 # to increment the order for the next task
                jobs.append(Job(job_operate, tasks)) # to create a Job object with the extracted job index and tasks, then append it to the jobs list

    return jobs # this to return the list of jobs read from the file

# This function tn initialize population randomly by uses library from imprt rando
def Init_Population(pop_size, num_jobs): # pop_size : population size
    # this to reate an initial population of chromosomes, each representing a permutation of job indices
    return [[x + 1 for x in random.sample(range(num_jobs), num_jobs)] for _ in range(pop_size)]
 # ecch first job start from 1 not zero

 # This function take bast chromosomes with best fitness (lower total time) to order tasks on machines and evaluated fitness
 #for each chromosome
def Scheduling(chromosome, jobs):
    current_time = 0  # initialize the current time
    job_position = [0] * len(jobs)  # To track the current task index for each job
    temp_machine = defaultdict(Machine)  # Temporary storage for machines and their tasks
    temp_machine_ordered = defaultdict(Machine)  # this store ordered tasks based on the chromosome
    machines = defaultdict(Machine)  # final machines and their tasks
    total_waiting_time = 0  # this total waiting time across all tasks

    for job in jobs: # in each loop take one job from jobs
        for task in job.tasks:
            task.waited_time = 0 # initialize the waiting time for each task to 0

    # Populate temp_machine with tasks
    for job in jobs:
        for task in job.tasks:
            if task.task not in temp_machine:
                temp_machine[task.task] = Machine()
            temp_machine[task.task].tasks.append(task)

    while True:
        # check if tasks on machines are completed at the current time
        for machine in machines:
            for task in machines[machine].tasks:
                if task.ended_time == current_time:
                    if job_position[task.job_index - 1] < len(jobs[task.job_index - 1].tasks):
                        job_position[task.job_index - 1] += 1  # Move to the next task in the job
                    machines[machine].available = True  # Mark the machine as available

        # to order tasks on temporary machines based on the chromosome
        for machine in temp_machine:
            for i in chromosome:
                for task in temp_machine[machine].tasks:
                    if i == task.job_index and task not in temp_machine_ordered[task.task].tasks:
                        temp_machine_ordered[task.task].tasks.append(task)

        # assign tasks to machines if they are available and ready to start
        for machine_index in temp_machine_ordered:
            machine = machines[machine_index]
            if machine.available and temp_machine_ordered[machine_index].tasks:
                task = temp_machine_ordered[machine_index].tasks[0]
                if task.task_order - 1 == job_position[task.job_index - 1]:  # check if the task is the next in order
                    task.started_time = current_time  # set the start time for the task
                    task.ended_time = current_time + task.duration  # set the end time for the task
                    machine.tasks.append(task)  # assign the task to the machine
                    temp_machine_ordered[machine_index].tasks.remove(task)  # remove task from ordered list
                    temp_machine[machine_index].tasks.remove(task)  # remove task from temporary storage
                    machine.available = False  # mark the machine as busy

        current_time += 1  # increment the current time
        for machine in temp_machine:
            for task in temp_machine[machine].tasks:
                task.waited_time += 1  # increment the waiting time for each task

        # This check if all jobs are complete
        complete = all(job_position[i] >= len(job.tasks) for i, job in enumerate(jobs))
        if complete:
            break

    # calculate the total waiting time
    for machine in machines:
        for task in machines[machine].tasks:
            total_waiting_time += task.waited_time

    return current_time - 1, machines  # return the total time as fitness  and the final machine schedules

def Crossover(p1, p2): # p1 : perent1 ,, p2 : perent 2
    # Select a crossover point randomly
    crossover_point = random.randint(1, len(p1) - 1)
    # create children by combining genes from both parents at the crossover point
    ch1 = p1[:crossover_point] + [gene for gene in p2 if gene not in p1[:crossover_point]] # ch1 :child1
    ch2 = p2[:crossover_point] + [gene for gene in p1 if gene not in p2[:crossover_point]] # ch2 :child2
    return ch1, ch2

def Mutation (chro, mutate_rate): # chro : chromosome
    # this mutate the chromosome with a given mutation rate
    if random.random() < mutate_rate:
        in1, in2 = random.sample(range(len(chro)), 2)  #ind1 : index1 ,, in2 : index2
        # to swap two genes in the chromosome
        chro[in1], chro[in2] = chro[in2], chro[in1]
    return chro

def SelectParents(pop, competition_size): #pop = population
    select_parents = []  # list to store selected parents
    for _ in range(len(pop)):
        # randomly select nominates for the tournament
        nominates = random.sample(pop, competition_size)
        # to choose the nominates with the best fitness
        winner = min(nominates, key=lambda x: x[1])
        select_parents.append(winner[0])  # Add the winner to the list of selected parents
    return select_parents

def Main_Schedule(jobs, pop, num_generations, mutate_rate, competition_size): #pop = population
    for g in range(num_generations): #g :generations
        computation_pop = []  # List to store the evaluated population
        for chro in pop: #chro : chromosome
            # to evaluate each chromosome using the scheduling function
            fitness, _ = Scheduling(chro, jobs) # best fitness (lower total time)
            computation_pop.append((chro, fitness))

        # this to select parents for the next generation
        parents = SelectParents(computation_pop,competition_size)

        new_pop = []  # List to store the new population
        for i in range(0, len(parents), 2):
            p1, p2 = parents[i], parents[i + 1]  # Select two parents # p1 : perent1 ,, p2 : perent 2
            # Perform crossover to produce children
            ch1, ch2 = Crossover(p1, p2) # ch1 :child1  # ch2 :child2
            # Mutate the children
            ch1 = Mutation(ch1, mutate_rate)  # ch1 :child1
            ch2 = Mutation(ch2, mutate_rate)# ch2 :child2
            new_pop.extend([ch1, ch2])  # to add the children to the new population
        pop = new_pop  # to update the population

    # to find the best chromosome with better fitness (lower total time)  in the computation_pop
    best_chromosome = min(computation_pop, key=lambda x: x[1])[0]
    # to get the final schedule using the best chromosome
    _, final_schedule = Scheduling(best_chromosome, jobs)

    print("Best Chromosome:", best_chromosome)  # Print the best chromosome

    return final_schedule  # Return the final schedule

# Print jobs from file
print("Contents of 'jobs.txt':")
jobs = read_file("jobs.txt")

# Get number of machines from user input
while True:
    num_machines = input("Enter the number of machines: ")
    if num_machines.lower() == "exit":
        exit()
    try:
        num_machines = int(num_machines)
        break
    except ValueError:
        print("Please enter a valid number or 'exit' to quit.")

# Check if the number of machines in the file matches the entered number
max_machine_num = max(int(task.task) for job in jobs for task in job.tasks)
if num_machines < max_machine_num:
    print(f"Number of machines provided ({num_machines}) is less than the required ({max_machine_num})")
    print("Please enter a valid number of machines or type 'exit' to quit.")
    while True:
        num_machines = input("Enter the number of machines: ")
        if num_machines.lower() == "exit":
            exit()
        try:
            num_machines = int(num_machines)
            break
        except ValueError:
            print("Please enter a valid number or 'exit' to quit.")

# get population size based on the number of jobs
pop_size = len(jobs) * 10 if len(jobs) < 5 else len(jobs) * 100 # pop_size : population size
population = Init_Population(pop_size, len(jobs))
num_generations = 100
mutate_rate = 0.001
competition_size = 4
schedule = Main_Schedule(jobs, population, num_generations, mutate_rate, competition_size)

# Print the final schedule in the desired format
for machine_index, machine in schedule.items(): #loop through each machine and its scheduled tasks in the final schedule
    # print the machine index in the desired format
    print(f"M{machine_index} | ", end="")
    current_time = 0  # Initialize the current time to 0
    # Loop through each task assigned to the current machine
    for task in machine.tasks:
        # Check if there is an idle period before the task starts
        if task.started_time > current_time:
            # Print the idle period as dashes
            print(f"{current_time}{'-' * (task.started_time - current_time)}", end="")
        # Print the task's start and end times along with the job index
        print(f"{task.started_time}[Job_{task.job_index}]{task.ended_time}", end=" ")
        current_time = task.ended_time  # Update the current time to the task's end time
    print("|")
