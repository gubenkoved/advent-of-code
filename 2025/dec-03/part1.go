//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	data, _ := os.ReadFile("data.txt")
	text := string(data)

	sum := 0
	for _, line := range strings.Split(text, "\n") {
		if line == "" {
			continue
		}
		fmt.Printf("%s", line)

		// given the lines are very small we can solve for O(n^2) np problem
		// however obviously better solution exists
		n := len(line)
		best := 0
		for i := 0; i < n-1; i++ {
			for j := i + 1; j < n; j++ {
				val, _ := strconv.ParseInt(string(line[i])+string(line[j]), 10, 32)
				best = max(best, int(val))
			}
		}
		fmt.Printf(" -> %d\n", best)
		sum += best
	}
	fmt.Println(sum)
}
