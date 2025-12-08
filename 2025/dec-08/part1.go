//go:build ignore

package main

import (
	"cmp"
	"fmt"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

type Point struct {
	X int
	Y int
	Z int
}

type Line struct {
	A      Point
	B      Point
	AIndex int
	BIndex int
}

func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func Dist(a, b Point) float64 {
	dx := Abs(a.X - b.X)
	dy := Abs(a.Y - b.Y)
	dz := Abs(a.Z - b.Z)
	return math.Sqrt(float64(dx*dx + dy*dy + dz*dz))
}

func Len(line Line) float64 {
	return Dist(line.A, line.B)
}

func main() {
	data, _ := os.ReadFile("data.txt")

	points := []Point{}
	for _, line := range strings.Split(string(data), "\n") {
		components := strings.Split(line, ",")

		x, _ := strconv.Atoi(components[0])
		y, _ := strconv.Atoi(components[1])
		z, _ := strconv.Atoi(components[2])

		points = append(points, Point{
			X: x,
			Y: y,
			Z: z,
		})
	}

	lines := []Line{}

	for i := 0; i < len(points); i++ {
		for j := i + 1; j < len(points); j++ {
			lines = append(lines, Line{
				A:      points[i],
				B:      points[j],
				AIndex: i,
				BIndex: j,
			})
		}
	}

	// sort by the distance
	slices.SortFunc(lines, func(a, b Line) int {
		return cmp.Compare(Len(a), Len(b))
	})

	// disjoint set init
	parent := make([]int, len(points)) // point index -> parent point index
	for idx := 0; idx < len(points); idx++ {
		parent[idx] = idx
	}

	parentOf := func(x int) int {
		for x != parent[x] {
			x = parent[x]
		}
		return x
	}

	// connect first 1000
	for lineIdx := 0; lineIdx < 1000; lineIdx++ {
		// connect the points
		line := lines[lineIdx]
		aParent := parentOf(line.AIndex)
		bParent := parentOf(line.BIndex)

		parent[bParent] = aParent
	}

	// count connected components
	counts := map[int]int{}
	for pointIdx := 0; pointIdx < len(points); pointIdx++ {
		parentIdx := parentOf(pointIdx)
		counts[parentIdx] += 1
	}

	fmt.Println(counts)

	sizes := []int{}
	for _, v := range counts {
		sizes = append(sizes, v)
	}

	slices.Sort(sizes)

	fmt.Println(sizes)

	k := len(sizes)

	fmt.Println(sizes[k-1] * sizes[k-2] * sizes[k-3])
}
