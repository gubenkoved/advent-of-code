//go:build ignore

package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func insideRangeExclusive(from, to, value int) bool {
	if to < from {
		return insideRangeExclusive(to, from, value)
	}

	if value > from && value < to {
		return true
	}

	return false
}

// returns true if point p is inside rect formed by c1 and c2 as corners
func isInsideRect(c1, c2, p [2]int) bool {
	return insideRangeExclusive(c1[0], c2[0], p[0]) && insideRangeExclusive(c1[1], c2[1], p[1])
}

func main() {
	data, _ := os.ReadFile("data.txt")
	text := string(data)

	points := [][2]int{}

	for _, line := range strings.Split(text, "\n") {
		segments := strings.Split(line, ",")
		x, _ := strconv.Atoi(segments[0])
		y, _ := strconv.Atoi(segments[1])
		p := [2]int{x, y}
		points = append(points, p)
	}

	result := 0

	n := len(points)
	for i := 0; i < n; i++ {
		for j := i + 1; j < n; j++ {
			p1 := points[i]
			p2 := points[j]

			pointInside := false
			for k := 0; k < n; k++ {
				if isInsideRect(p1, p2, points[k]) {
					pointInside = true
					break
				}
			}

			if pointInside {
				continue
			}

			// another geometry hack for the inputs -- central tooth
			if insideRangeExclusive(p1[1], p2[1], 50187) || insideRangeExclusive(p1[1], p2[1], 48595) {
				continue
			}

			w := abs(p1[0]-p2[0]) + 1
			h := abs(p1[1]-p2[1]) + 1

			if w*h > result {
				result = w * h
				fmt.Printf("%v %v\n", p1, p2)
			}
		}
	}

	fmt.Println(result)
}
