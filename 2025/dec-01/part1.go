package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func main() {
	data, err := os.ReadFile("data.txt")

	if err != nil {
		panic("unable to read")
	}

	text := string(data)
	lines := strings.Split(text, "\n")

	result := 0
	current := 50
	for _, line := range lines {
		line = strings.TrimSpace(line)

		if len(line) == 0 {
			continue
		}

		direction := line[:1]
		count, err := strconv.Atoi(line[1:])

		if err != nil {
			panic(fmt.Errorf("bad number at line \"%s\"", line))
		}

		if direction == "L" {
			current = (current + 100 - count) % 100
		} else {
			current = (current + count) % 100
		}

		if current == 0 {
			result += 1
		}
	}
	fmt.Println(result)
}
