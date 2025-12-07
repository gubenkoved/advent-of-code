//go:build ignore

package main

import (
	"fmt"
	"os"
	"strings"
)

type Pos [2]int

func main() {
	data, _ := os.ReadFile("data.txt")
	lines := strings.Split(string(data), "\n")

	// count of ways to reach a given point
	counter := map[Pos]int{}

	// simulate the beam downwards
	rows := len(lines)
	cols := len(lines[0])
	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			pos := Pos{row, col}
			char := lines[row][col]

			if char == 'S' {
				counter[Pos{row + 1, col}] += 1
			}

			if counter[pos] > 0 {
				// there is a beam from previous line here
				if char == '^' {
					counter[Pos{row + 1, col - 1}] += counter[pos]
					counter[Pos{row + 1, col + 1}] += counter[pos]
				} else if char == '.' {
					counter[Pos{row + 1, col}] += counter[pos]
				}
			}
		}
	}

	// sum the ways for the last row
	sum := 0
	for col := 0; col < cols; col++ {
		sum += counter[Pos{rows - 1, col}]
	}
	fmt.Println(sum)
}
