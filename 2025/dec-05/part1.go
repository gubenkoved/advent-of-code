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
	lines := strings.Split(string(data), "\n")
	queries := []string{}
	ranges := [][2]int64{}

	for idx, line := range lines {
		if line == "" {
			queries = lines[idx+1:]
			break
		}
		tmp := strings.Split(line, "-")
		a, _ := strconv.ParseInt(tmp[0], 10, 64)
		b, _ := strconv.ParseInt(tmp[1], 10, 64)
		ranges = append(ranges, [2]int64{a, b})
	}

	freshCount := 0
	for _, query := range queries {
		num, _ := strconv.ParseInt(query, 10, 64)

		// find the range
		matched := false
		for _, freshRange := range ranges {
			if num >= freshRange[0] && num <= freshRange[1] {
				matched = true
				break
			}
		}
		if matched {
			freshCount += 1
		}
	}
	fmt.Println(freshCount)
}
