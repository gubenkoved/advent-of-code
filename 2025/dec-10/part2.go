//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Switch []int

type Machine struct {
	switches []Switch
	targets  []int
}

type Range struct {
	Min int
	Max int
}

var Empty Range = Range{
	Min: 0,
	Max: -1,
}

func (r Range) IsEmpty() bool {
	return r.Min > r.Max
}

func clone(r []Range) []Range {
	result := make([]Range, len(r))
	copy(result, r)
	return result
}

func intersect(r1, r2 Range) Range {
	// ensure r1 starts earlier
	if r1.Min > r2.Min {
		return intersect(r2, r1)
	}

	if r2.Min > r1.Max {
		return Empty
	}

	newMin := max(r1.Min, r2.Min)
	newMax := min(r1.Max, r2.Max)

	return Range{
		Min: newMin,
		Max: newMax,
	}
}

func solve(machine Machine) int {
	// search results by traversing whole search space fulfilling the
	// given conditions, each unknown will be associated with range (min, max)
	// on each iteration we pick a value for unknown, then see if we can infer
	// values for any other unknown

	// TODO: why reordering of switches changes the result?!
	// TODO: process switches that connected to MOST lights first
	// slices.SortFunc(machine.switches, func(a, b Switch) int {
	// 	return -1 * cmp.Compare(len(a), len(b))
	// })

	// amount of switches
	N := len(machine.switches)

	// targets count
	T := len(machine.targets)

	// variable index -> range of possible values
	initRanges := []Range{}

	// helper array -- for each target stores set of switch indexes it is influenced by
	targetToSwitchMap := make([]map[int]bool, T)

	// we start by identifying max times we can press each switch
	// it can be calculated as minimum of targets it switches as every time
	// switch is pressed all of the are incremented
	for swIdx, sw := range machine.switches {
		m := -1
		for _, targetIdx := range sw {
			if m == -1 {
				m = machine.targets[targetIdx]
			} else {
				m = min(m, machine.targets[targetIdx])
			}
			if targetToSwitchMap[targetIdx] == nil {
				targetToSwitchMap[targetIdx] = map[int]bool{}
			}
			targetToSwitchMap[targetIdx][swIdx] = true
		}

		initRanges = append(initRanges, Range{
			Min: 0,
			Max: m,
		})
	}

	fmt.Printf("solving for %v, %d switches, %d targets, initial ranges: %v\n", machine, N, T, initRanges)

	bestSolutionResult := -1

	// recursive function that solves for given switch index
	var search func(swIdx int, ranges []Range)

	search = func(swIdx int, ranges []Range) {

		// all switches resolved -> record solution
		if swIdx == N {
			sol := []int{}
			solResult := 0
			for idx := 0; idx < N; idx++ {
				sol = append(sol, ranges[idx].Min)
				if ranges[idx].Min != ranges[idx].Max {
					panic("unresolved range!")
				}
				solResult += ranges[idx].Min
			}
			// TODO: add cut if amount of switches already worse than current
			// 	(sum of mins)
			if bestSolutionResult == -1 || solResult < bestSolutionResult {
				bestSolutionResult = solResult
				fmt.Printf("  found beter solution %+v (%d)\n", sol, solResult)
			}
			return
		}

		r := ranges[swIdx]
		// fmt.Printf("Solving for switch #%d which is in range %#v", r)

		// try all the possible values, but update ranges for each case
		for value := r.Min; value <= r.Max; value++ {

			updatedRanges := clone(ranges)

			// set specific value for the given switch
			updatedRanges[swIdx] = Range{Min: value, Max: value}

			// for each switch after this one -> compute updated range given
			// new input AND then merge the range with existing one
			// if there is NO intersection -> stop processing this branch as
			// unsolvable

			for otherSwitchIdx := swIdx + 1; otherSwitchIdx < N; otherSwitchIdx++ {
				// for each equation it is part of range can be calculated as
				// follows, suppose
				// x1 + x2 + x3 = A
				// rewrite for x2:  x2 = A - x1 - x3
				// x2_min = A - x1_max - x3_max
				// x2_max = A - x1_min - x3_min

				for targetIdx := 0; targetIdx < T; targetIdx++ {
					// skip this target since it is NOT influenced by the switch in question
					if targetToSwitchMap[targetIdx][otherSwitchIdx] == false {
						continue
					}

					sum_of_min := 0
					sum_of_max := 0

					for swIdx3 := range targetToSwitchMap[targetIdx] {
						if swIdx3 == otherSwitchIdx {
							continue
						}
						sum_of_min += ranges[swIdx3].Min
						sum_of_max += ranges[swIdx3].Max
					}

					inferredRange := Range{
						Min: machine.targets[targetIdx] - sum_of_max,
						Max: machine.targets[targetIdx] - sum_of_min,
					}

					// range infer from this given equation
					updatedRanges[otherSwitchIdx] = intersect(
						updatedRanges[otherSwitchIdx],
						inferredRange,
					)

					// if ANY of the ranges becomes empty -> no solution, can exit
					// earlier from this branch
					if updatedRanges[otherSwitchIdx].IsEmpty() {
						return
					}
				}
			}

			search(swIdx+1, updatedRanges)
		}
	}

	// start the search
	search(0, initRanges)

	return bestSolutionResult
}

func main() {
	data, _ := os.ReadFile("data.txt")

	lines := strings.Split(string(data), "\n")

	machines := []Machine{}

	for _, line := range lines {
		segments := strings.Split(line, " ")
		switchesSegments := segments[1 : len(segments)-1]
		targetValuesStr := segments[len(segments)-1]
		targetValuesStr = targetValuesStr[1 : len(targetValuesStr)-1]

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

		targets := []int{}
		for _, targetValueStr := range strings.Split(targetValuesStr, ",") {
			val, err := strconv.Atoi(targetValueStr)
			if err != nil {
				panic(fmt.Sprintf("bad value: %s", targetValueStr))
			}
			targets = append(targets, val)
		}

		machine := Machine{
			switches: switches,
			targets:  targets,
		}

		machines = append(machines, machine)
	}

	result := 0

	for machineIdx, machine := range machines {
		cur := solve(machine)
		fmt.Printf("#%d: %v# -> %d\n", machineIdx, machine, cur)
		result += cur
	}

	fmt.Println(result)
}
