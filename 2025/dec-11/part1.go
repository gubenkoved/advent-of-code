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

	var countPaths func(from, to string) int

	countPaths = func(from, to string) int {

		var inner func(target string) int

		memo := map[string]int{}

		inner = func(target string) int {
			if target == from {
				return 1
			}

			if m, ok := memo[target]; ok {
				return m
			}

			result := 0
			for _, parent := range parents[target] {
				result += inner(parent)
			}
			memo[target] = result
			return result
		}

		return inner(to)
	}

	fmt.Println(countPaths("you", "out"))
}
