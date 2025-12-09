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

func main() {
	data, _ := os.ReadFile("data.txt")
	text := string(data)

	points := [][2]int{}

	for _, line := range strings.Split(text, "\n") {
		segments := strings.Split(line, ",")
		x, _ := strconv.Atoi(segments[0])
		y, _ := strconv.Atoi(segments[1])

		points = append(points, [2]int{x, y})
	}

	largest := 0
	for i := 0; i < len(points); i++ {
		for j := i + 1; j < len(points); j++ {
			w := abs(points[i][0]-points[j][0]) + 1
			h := abs(points[i][1]-points[j][1]) + 1
			largest = max(largest, w*h)
		}
	}

	fmt.Println(largest)
}
