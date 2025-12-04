//go:build ignore

package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	data, _ := os.ReadFile("data.txt")
	field := [][]int{}

	for _, line := range strings.Split(string(data), "\n") {
		if line == "" {
			continue
		}
		fieldLine := []int{}

		for _, rune := range line {
			chr := string(rune)
			if chr == "@" {
				fieldLine = append(fieldLine, 1)
			} else {
				fieldLine = append(fieldLine, 0)
			}
		}

		field = append(field, fieldLine)
	}

	rows := len(field)
	cols := len(field[0])
	reachable := map[[2]int]bool{}

	var processOnce func() map[[2]int]bool = func() map[[2]int]bool {
		harvested := map[[2]int]bool{}

		for row := 0; row < rows; row++ {
			for col := 0; col < cols; col++ {
				cell := field[row][col]

				if cell != 1 {
					continue
				}

				adjacentCount := 0
				adjacent := [][2]int{
					{row - 1, col - 1},
					{row - 1, col},
					{row - 1, col + 1},
					{row, col - 1},
					{row, col + 1},
					{row + 1, col - 1},
					{row + 1, col},
					{row + 1, col + 1},
				}

				for _, adj := range adjacent {
					arow := adj[0]
					acol := adj[1]
					if arow < 0 || arow >= rows || acol < 0 || acol >= cols {
						continue
					}
					acell := field[arow][acol]

					if acell == 1 {
						adjacentCount += 1
					}
				}

				if adjacentCount < 4 {
					harvested[[...]int{row, col}] = true
				}
			}
		}
		return harvested
	}

	roundIdx := 0
	for {
		roundIdx += 1
		fmt.Printf("Processing round #%d (currently reachable %d)\n", roundIdx, len(reachable))
		harvested := processOnce()

		// update the field
		for k, _ := range harvested {
			reachable[k] = true
			r, c := k[0], k[1]
			field[r][c] = 0
		}

		if len(harvested) == 0 {
			fmt.Printf("Nothing harvested, exit!\n")
			break
		}
	}

	// print result field
	out, _ := os.Create("data2.out")
	writer := bufio.NewWriter(out)

	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			cell := [2]int{row, col}
			if reachable[cell] {
				writer.WriteString("x")
			} else {
				if field[row][col] == 0 {
					writer.WriteString(" ")
				} else if field[row][col] == 1 {
					writer.WriteString("@")
				}
			}
		}
		writer.WriteString("\n")
	}
	writer.Flush()
	out.Close()

	fmt.Println(len(reachable))
}
