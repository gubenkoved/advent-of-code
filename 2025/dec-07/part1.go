//go:build ignore

package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	data, _ := os.ReadFile("data.txt")
	lines := strings.Split(string(data), "\n")

	counter := 0

	// columns where the beam is for the next row
	beamColums := map[int]bool{}
	nextBeamColumns := map[int]bool{}

	// simulate the beam downwards
	rows := len(lines)
	cols := len(lines[0])
	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			char := lines[row][col]

			if char == 'S' {
				nextBeamColumns[col] = true
			}

			if beamColums[col] {
				// there is a beam from previous line here
				if char == '^' {
					nextBeamColumns[col-1] = true
					nextBeamColumns[col+1] = true

					counter += 1
				} else if char == '.' {
					nextBeamColumns[col] = true
				}
			}
		}
		beamColums = nextBeamColumns
		nextBeamColumns = map[int]bool{}
	}

	fmt.Println(counter)
}
