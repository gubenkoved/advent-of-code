//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parseInt(str string) (int, bool) {
	val, err := strconv.ParseInt(str, 10, 32)
	if err != nil {
		return -1, false
	}
	return int(val), true
}

func reduce(numbers []int, op func(prev, cur int) int, initial int) int {
	result := initial
	for idx := 0; idx < len(numbers); idx++ {
		result = op(result, numbers[idx])
	}
	return result
}

func filterEmpty(arr []string) []string {
	result := []string{}
	for _, x := range arr {
		if x == "" {
			continue
		}
		result = append(result, x)
	}
	return result
}

func readNum(lines []string, colIdx int) (int, bool) {
	bytes := []byte{}
	for row := 0; row < len(lines)-1; row++ {
		bytes = append(bytes, lines[row][colIdx])
	}
	numString := strings.Trim(string(bytes), " ")
	return parseInt(numString)
}

func fill(str string, width int, filler string) string {
	if len(filler) != 1 {
		panic("bad filled")
	}
	k := width - len(str)
	toBeAdded := []string{}
	for range k {
		toBeAdded = append(toBeAdded, filler)
	}
	return str + strings.Join(toBeAdded, "")
}

func main() {
	data, _ := os.ReadFile("data.txt")
	lines := strings.Split(string(data), "\n")

	maxLen := 0
	for _, line := range lines {
		maxLen = max(len(line), maxLen)
	}

	// normalize the lines
	normalizedLines := []string{}
	for _, line := range lines {
		normalizedLines = append(normalizedLines, fill(line, maxLen, " "))
	}
	lines = normalizedLines

	colCount := len(lines[0])

	groups := [][]int{}
	group := []int{}

	for colIdx := 0; colIdx < colCount; colIdx++ {
		num, found := readNum(lines, colIdx)
		if !found {
			groups = append(groups, group)
			group = []int{}
		} else {
			group = append(group, num)
		}
	}

	// last group
	groups = append(groups, group)

	operators := filterEmpty(strings.Split(lines[len(lines)-1], " "))

	if len(operators) != len(groups) {
		panic("bad")
	}

	result := 0

	for gIdx := 0; gIdx < len(groups); gIdx++ {
		op := operators[gIdx]
		cur := 0
		if op == "+" {
			cur = reduce(groups[gIdx], func(a, b int) int {
				return a + b
			}, 0)
		} else if op == "*" {
			cur = reduce(groups[gIdx], func(a, b int) int {
				return a * b
			}, 1)
		}

		result += cur
		fmt.Printf("Group #%d, result: %d, total: %d\n", gIdx, cur, result)
	}

	fmt.Println(result)
}
