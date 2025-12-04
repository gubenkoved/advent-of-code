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
	field := []string{}

	for _, line := range strings.Split(string(data), "\n") {
		if line == "" {
			continue
		}
		field = append(field, line)
	}

	rows := len(field)
	cols := len(field[0])

	reachable := map[[2]int]bool{}
	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			cell := string(field[row][col])

			if cell != "@" {
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
				acell := string(field[arow][acol])

				if acell == "@" {
					adjacentCount += 1
				}
			}

			if adjacentCount < 4 {
				reachable[[...]int{row, col}] = true
			}
		}
	}

	// print result field
	out, _ := os.Create("data.out")
	writer := bufio.NewWriter(out)

	for row := 0; row < rows; row++ {
		for col := 0; col < cols; col++ {
			cell := [2]int{row, col}
			if reachable[cell] {
				writer.WriteString("x")
			} else {
				writer.WriteString(string(field[row][col]))
			}
		}
		writer.WriteString("\n")
	}
	writer.Flush()
	out.Close()

	fmt.Println(len(reachable))
}
