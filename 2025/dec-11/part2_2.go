//go:build ignore

package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	data, _ := os.ReadFile("data.txt")

	parents := map[string][]string{}

	for _, line := range strings.Split(string(data), "\n") {
		s1 := strings.Split(line, ":")
		source := s1[0]
		destinations := strings.Split(s1[1][1:], " ")

		for _, dest := range destinations {
			if parents[dest] == nil {
				parents[dest] = []string{}
			}

			parents[dest] = append(parents[dest], source)
		}
	}

	countPaths := func(from, to string) int {

		// what is the [recursive] function call?
		// def f(x):
		//    # before
		//    f(y)
		//    # after
		// we have frame with x on our stack, and we add another frame with y
		// argument on the stack; notice however that as soon as we done with y
		// we still need to process x again performing "after" part; and in
		// this processing code we can use results of recursive calculation

		type Frame struct {
			target           string
			isPostProcessing bool
		}

		stack := []Frame{{to, false}}
		memo := map[string]int{}

		for len(stack) > 0 {
			frame := stack[len(stack)-1]
			stack = stack[:len(stack)-1]

			// this node is alrady fully calculated -> skip
			if _, processed := memo[frame.target]; processed {
				continue
			}

			if !frame.isPostProcessing {
				stack = append(stack, Frame{frame.target, true})

				// add and process all parents
				for _, parent := range parents[frame.target] {
					stack = append(stack, Frame{parent, false})
				}
			} else {
				// compute results
				result := 0
				for _, parent := range parents[frame.target] {
					result += memo[parent]
				}
				if frame.target == from {
					result += 1
				}
				memo[frame.target] = result
			}
		}

		return memo[to]
	}

	fmt.Println(
		countPaths("svr", "dac"),
		countPaths("dac", "fft"),
		countPaths("fft", "out"),
		"->",
		countPaths("svr", "dac")*countPaths("dac", "fft")*countPaths("fft", "out"),
		"::",
		countPaths("svr", "fft"),
		countPaths("fft", "dac"),
		countPaths("dac", "out"),
		"->",
		countPaths("svr", "fft")*countPaths("fft", "dac")*countPaths("dac", "out"),
	)
}
