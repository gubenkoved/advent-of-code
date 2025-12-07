//go:build ignore

package main

import (
	"encoding/csv"
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

	outFile, err := os.OpenFile("data.out.csv", os.O_EXCL|os.O_WRONLY, 0644)

	if err != nil {
		panic(err)
	}

	writer := csv.NewWriter(outFile)
	writer.Write([]string{"row", "col", "count"})
	for k, v := range counter {
		writeErr := writer.Write([]string{fmt.Sprintf("%d", k[0]), fmt.Sprintf("%d", k[1]), fmt.Sprintf("%d", v)})
		if writeErr != nil {
			panic(writeErr)
		}
	}
	writer.Flush()
	outFile.Close()
}
