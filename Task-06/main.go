package main

import (
	"fmt"
	"sort"
	"strings"
)

type Process struct {
	id      int
	arrival int
	burst   int
}

func sortByArrival(processes []Process) []Process {
	procs := make([]Process, len(processes))
	copy(procs, processes)

	sort.Slice(procs, func(i, j int) bool {
		if procs[i].arrival == procs[j].arrival {
			return procs[i].id < procs[j].id
		}

		return procs[i].arrival < procs[j].arrival
	})

	return procs
}

func sortByBurst(processes []Process) []Process {
	procs := make([]Process, len(processes))
	copy(procs, processes)

	sort.Slice(procs, func(i, j int) bool {
		if procs[i].burst == procs[j].burst {
			if procs[i].arrival == procs[j].arrival {
				return procs[i].id < procs[j].id
			}

			return procs[i].arrival < procs[j].arrival
		}

		return procs[i].burst < procs[j].burst
	})

	return procs
}

func Fcfs_sched(processes []Process) {
	procs := sortByArrival(processes)

	current_time := 0
	average_waiting := 0
	average_tat := 0
	for _, proc := range procs {
		if current_time < proc.arrival {
			current_time = proc.arrival
		}

		completion_time := current_time + proc.burst
		tat_time := completion_time - proc.arrival
		waiting_time := tat_time - proc.burst
		current_time = completion_time

		average_waiting += waiting_time
		average_tat += tat_time

		fmt.Printf("Arrived Process: %d\n", proc.id)
		fmt.Printf("Time for completion: %d\n", completion_time)
		fmt.Printf("Turnaround time: %d\n", tat_time)
		fmt.Printf("Time Waited: %d\n", waiting_time)
		fmt.Print(strings.Repeat("\t|\n", 2))
	}

	fmt.Printf("Average waiting time: %f\n", float64(average_waiting)/float64(len(processes)))
	fmt.Printf("Average turnaround time: %f\n\n", float64(average_tat)/float64(len(processes)))
	fmt.Println(strings.Repeat("-", 50))
}

func Sjf_sched(processes []Process) {
	procs := make([]Process, len(processes))
	copy(procs, processes)

	current_time := 0
	average_waiting := 0
	average_tat := 0

	for len(procs) > 0 {
		var arrived_procs []Process
		for _, proc := range procs {
			if proc.arrival <= current_time {
				arrived_procs = append(arrived_procs, proc)
			}
		}

		if len(arrived_procs) == 0 {
			current_time++
			continue
		}

		arrived_procs = sortByBurst(arrived_procs)

		for _, proc := range arrived_procs {
			if current_time < proc.arrival {
				current_time = proc.arrival
			}

			completion_time := current_time + proc.burst
			tat_time := completion_time - proc.arrival
			waiting_time := tat_time - proc.burst
			current_time = completion_time

			average_waiting += waiting_time
			average_tat += tat_time

			result := make([]Process, 0, len(procs))
			for _, v := range procs {
				if v != proc {
					result = append(result, v)
				}
			}

			procs = result

			fmt.Printf("Arrived Process: %d\n", proc.id)
			fmt.Printf("Time for completion: %d\n", completion_time)
			fmt.Printf("Turnaround time: %d\n", tat_time)
			fmt.Printf("Time Waited: %d\n", waiting_time)
			fmt.Print(strings.Repeat("\t|\n", 2))
		}
	}
	fmt.Printf("Average waiting time: %f\n", float64(average_waiting)/float64(len(processes)))
	fmt.Printf("Average turnaround time: %f\n\n", float64(average_tat)/float64(len(processes)))
	fmt.Println(strings.Repeat("-", 50))
}

func RR_sched(processes []Process, q int) {
	procs := sortByArrival(processes)

	current_time := 0
	average_waiting := 0
	average_tat := 0

	var rd_que []Process
	next := 0

	remaining := make(map[int]int)
	for _, p := range procs {
		remaining[p.id] = p.burst
	}

	for next < len(procs) && procs[next].arrival <= current_time {
		rd_que = append(rd_que, procs[next])
		next++
	}

	for len(rd_que) > 0 || next < len(procs) {
		if len(rd_que) == 0 {
			current_time = procs[next].arrival
			rd_que = append(rd_que, procs[next])
			next++
			continue
		}

		proc := rd_que[0]
		rd_que = rd_que[1:]

		runtime := min(q, remaining[proc.id])
		remaining[proc.id] -= runtime

		current_time += runtime

		for next < len(procs) && procs[next].arrival <= current_time {
			rd_que = append(rd_que, procs[next])
			next++
		}

		if remaining[proc.id] == 0 {
			completion_time := current_time
			tat_time := completion_time - proc.arrival
			waiting_time := tat_time - proc.burst

			average_waiting += waiting_time
			average_tat += tat_time

			fmt.Printf("Arrived Process: %d\n", proc.id)
			fmt.Printf("Time for completion: %d\n", completion_time)
			fmt.Printf("Turnaround time: %d\n", tat_time)
			fmt.Printf("Time Waited: %d\n", waiting_time)
			fmt.Print(strings.Repeat("\t|\n", 2))
		} else {
			rd_que = append(rd_que, proc)
		}
	}

	fmt.Printf("Average waiting time: %f\n", float64(average_waiting)/float64(len(processes)))
	fmt.Printf("Average turnaround time: %f\n\n", float64(average_tat)/float64(len(processes)))
	fmt.Println(strings.Repeat("-", 50))
}

func main() {
	process1 := []Process{
		{2, 2, 8},
		{3, 4, 3},
		{1, 0, 6},
	}
	Fcfs_sched(process1)
	Sjf_sched(process1)
	RR_sched(process1, 2)
}
