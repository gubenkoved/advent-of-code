//go:build ignore

package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	data, _ := os.ReadFile("data.txt")

	adjacency := map[string][]string{}

	for _, line := range strings.Split(string(data), "\n") {
		s1 := strings.Split(line, ":")
		source := s1[0]
		destinations := strings.Split(s1[1], " ")

		if adjacency[source] == nil {
			adjacency[source] = []string{}
		}

		for _, dest := range destinations {
			adjacency[source] = append(adjacency[source], dest)
		}
	}

	queue := []string{"you"}
	counts := map[string]int{}
	counts["you"] = 1

	visited := map[string]bool{}

	for len(queue) > 0 {
		cur := queue[0]
		queue = queue[1:]

		if visited[cur] {
			continue
		}
		visited[cur] = true

		for _, neigh := range adjacency[cur] {
			counts[neigh] += counts[cur]
			queue = append(queue, neigh)
		}
	}

	fmt.Println(counts["out"])
}
