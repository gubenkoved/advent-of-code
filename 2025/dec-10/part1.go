//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Switch []int

type LightsState []bool

type Machine struct {
	target   LightsState
	switches []Switch
}

func stateToInt(state LightsState) int {
	result := 0
	for idx := 0; idx < len(state); idx++ {
		if state[idx] {
			result |= 2 << idx
		}
	}
	return result
}

func solve(machine Machine) int {
	k := len(machine.target)

	targetInt := stateToInt(machine.target)

	// initial state -- all off
	initial := stateToInt(make(LightsState, k))

	queue := []int{initial}

	// key -- state as integer
	dist := map[int]int{}
	dist[initial] = 0

	visited := map[int]bool{}

	for len(queue) > 0 {
		state := queue[0]
		queue = queue[1:]

		if visited[state] {
			continue
		}

		visited[state] = true

		d := dist[state]

		if state == targetInt {
			break
		}

		// neighbor states
		for _, sw := range machine.switches {
			// apply the switches
			updated := state

			for _, flipIdx := range sw {
				updated ^= 2 << flipIdx
			}

			// skip if already in dist
			if _, ok2 := dist[updated]; ok2 {
				continue
			}

			dist[updated] = d + 1
			queue = append(queue, updated)
		}
	}

	return dist[targetInt]
}

func main() {
	data, _ := os.ReadFile("data.txt")

	lines := strings.Split(string(data), "\n")

	machines := []Machine{}

	for _, line := range lines {
		segments := strings.Split(line, " ")
		targetStr := segments[0]
		switchesSegments := segments[1 : len(segments)-1]

		target := LightsState{}
		for idx := 1; idx < len(targetStr)-1; idx++ {
			if targetStr[idx] == '#' {
				target = append(target, true)
			} else {
				target = append(target, false)
			}
		}

		switches := []Switch{}

		for _, switchStr := range switchesSegments {
			switchStr = switchStr[1 : len(switchStr)-1] // drop paranthesys
			nums := strings.Split(switchStr, ",")

			switchObj := Switch{}

			for _, num := range nums {
				x, _ := strconv.Atoi(num)
				switchObj = append(switchObj, x)

			}

			switches = append(switches, switchObj)
		}

		machine := Machine{
			target:   target,
			switches: switches,
		}

		machines = append(machines, machine)
	}

	result := 0

	for _, machine := range machines {
		cur := solve(machine)
		fmt.Printf("%v# -> %d\n", machine, cur)
		result += cur
	}

	fmt.Println(result)
}
