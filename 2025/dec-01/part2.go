//go:build ignore

package main

import (
	"fmt"
	"math"
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
			previous := current
			current -= count

			if current > 0 {
				continue
			}

			full := int(math.Abs(float64(current / 100)))
			current = (current + (full+1)*100) % 100

			if previous > 0 {
				result += full + 1
			} else {
				result += full
			}

		} else {
			current += count
			result += current / 100
			current = current % 100
		}
	}
	fmt.Println(result)
}
