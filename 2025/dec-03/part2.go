//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

// it seem like we can greedily solve this due to nature of numbers comparision
// each previous value has more effect than the next one
func solve(line string, k int) int64 {
	n := len(line)
	picked := []string{}

	// find the first biggest digit still leaving the place to pick other
	// 12-pos-1 digits
	var pick = func(startIdx int, pos int) int {
		bestDigit := -1
		bestIdx := startIdx
		for idx := startIdx; idx < n-(k-pos)+1; idx++ {
			digit := int(line[idx] - '0')
			if digit > bestDigit {
				bestDigit = digit
				bestIdx = idx
			}
		}
		return bestIdx
	}

	startIdx := 0
	for pos := 0; pos < k; pos++ {
		pickedIndex := pick(startIdx, pos)
		startIdx = pickedIndex
		picked = append(picked, string(line[pickedIndex]))
		startIdx = pickedIndex + 1
	}

	value, _ := strconv.ParseInt(strings.Join(picked, ""), 10, 64)
	return value
}

func main() {
	data, _ := os.ReadFile("data.txt")
	text := string(data)

	sum := int64(0)
	for _, line := range strings.Split(text, "\n") {
		if line == "" {
			continue
		}
		fmt.Printf("%s", line)
		best := solve(line, 12)
		fmt.Printf(" -> %d\n", best)
		sum += best
	}
	fmt.Println(sum)
}
