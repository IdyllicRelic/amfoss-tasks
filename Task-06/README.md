# Task-06: Pirate King's Scheduler
A simple cpu scheduling simulator written go. This implements the First Come First Serve, Shortest Job First, and Round Robin(incomplete) algorithms

## Approach
### First Come First Serve
This sorts all processes by their time of arrival and runs the first arrival to completion and then moves on to the next one that came after
For each process is run till completion and prints the calculated completion, turnaround, and waiting time

### Shortest Job First
This one checks which all processes have arrived and of those ones picks the one with the shortest burst time and executes it till completion.
After that is again checks the list of processes that have arrived and again picks the one with the shorted burst time and executes it till completion.

### Round Robin
For Round Robin it manages a ready queue and a map mapping the process id's to their remaining execution times. All arrived processes are loaded onto the queue and ran for the specified quantum.
After it has ran for the specified time, it checks if the process has completed if so, print its stats else push it back onto the queue and repeat till all processes have completed.

## Concepts Learned
- How a CPU scheduler works
- Common scheduling algorithms
- Basics of Go

## Resources:
[GeeksforGeeks](https://www.geeksforgeeks.org/operating-systems/cpu-scheduling-in-operating-systems/)
[Go Docs](https://go.dev/tour)
