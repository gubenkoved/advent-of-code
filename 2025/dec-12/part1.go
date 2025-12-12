//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Block struct {
	Shape [][]bool
	Area  int
}

type Puzzle struct {
	Width  int
	Height int
	Counts [6]int
}

func area(shape [][]bool) int {
	result := 0
	for row := range len(shape) {
		for col := range len(shape[row]) {
			if shape[row][col] {
				result += 1
			}
		}
	}
	return result
}

func parseInt(s string) int {
	res, err := strconv.Atoi(s)
	if err != nil {
		panic(fmt.Sprintf("bad num: %s", s))
	}
	return res
}

func main() {
	data, _ := os.ReadFile("data.txt")

	blocks := [6]Block{}
	puzzles := []Puzzle{}

	lines := strings.Split(string(data), "\n")

	for blockIdx := range 6 {
		blockLines := lines[blockIdx*5+1 : blockIdx*5+4]
		shape := [][]bool{}
		for _, blockLine := range blockLines {
			shapeRow := []bool{}
			for c := range 3 {
				if blockLine[c] == '#' {
					shapeRow = append(shapeRow, true)
				} else {
					shapeRow = append(shapeRow, false)
				}
			}
			shape = append(shape, shapeRow)
		}
		blocks[blockIdx] = Block{
			Shape: shape,
			Area:  area(shape),
		}
	}

	for _, line := range lines[30:] {
		seg := strings.Split(line, ":")

		sizeTmp := strings.Split(seg[0], "x")
		countsTmp := strings.Split(seg[1], " ")

		counts := []int{}
		for _, countStr := range countsTmp {
			if countStr == "" {
				continue
			}
			counts = append(counts, parseInt(countStr))
		}

		puzzles = append(puzzles, Puzzle{
			Width:  parseInt(sizeTmp[0]),
			Height: parseInt(sizeTmp[1]),
			Counts: [6]int(counts),
		})
	}

	count := 0

	for _, puzzle := range puzzles {
		needed := 0
		totalBlockCount := 0
		for idx, count := range puzzle.Counts {
			needed += blocks[idx].Area * count
			totalBlockCount += count
		}
		fmt.Printf("%#v: needed: %d, available: %d, total blocks: %d, number of 3x3 free places: %d\n", puzzle, needed, puzzle.Width*puzzle.Height, totalBlockCount, (puzzle.Width/3)*(puzzle.Height/3))

		if needed <= puzzle.Width*puzzle.Height {
			count += 1
		}
	}

	fmt.Println(count)
}
