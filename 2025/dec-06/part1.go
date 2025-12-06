//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func parseInt(str string) int {
	val, err := strconv.ParseInt(str, 10, 32)
	if err != nil {
		panic(fmt.Errorf("bad int: %s", str))
	}
	return int(val)
}

func reduce(segments [][]string, idx int, op func(prev, cur int) int, initial int) int {
	result := initial
	for row := 0; row < len(segments)-1; row++ {
		result = op(result, parseInt(segments[row][idx]))
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

func main() {
	data, _ := os.ReadFile("data.txt")
	segments := [][]string{}
	lines := strings.Split(string(data), "\n")
	for _, line := range lines {
		segments = append(segments, filterEmpty(strings.Split(line, " ")))
	}

	result := 0

	rows := len(segments)
	cols := len(segments[0])

	for idx := 0; idx < cols; idx++ {
		op := segments[rows-1][idx]
		cur := 0
		if op == "+" {
			cur = reduce(segments, idx, func(a, b int) int {
				return a + b
			}, 0)
		} else if op == "*" {
			cur = reduce(segments, idx, func(a, b int) int {
				return a * b
			}, 1)
		} else {
			panic("what?")
		}
		result += cur
		fmt.Printf("Column #%d, col result: %d, total %d\n", idx, cur, result)
	}

	fmt.Println(result)
}
