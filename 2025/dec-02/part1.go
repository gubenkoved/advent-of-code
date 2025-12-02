package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func dup(x int64) int64 {
	xx, err := strconv.ParseInt(fmt.Sprintf("%d%d", x, x), 10, 64)
	if err != nil {
		panic("bad")
	}
	return xx
}

// actually, no need to overcomplicate this one
func lowBound(x int64) int64 {
	return 1
}

func main() {
	data, _ := os.ReadFile("data.txt")
	text := string(data)

	sum := int64(0)
	for _, rangeRepr := range strings.Split(text, ",") {
		if rangeRepr == "" {
			continue
		}
		fmt.Println("handling", rangeRepr)
		components := strings.Split(rangeRepr, "-")
		from, _ := strconv.ParseInt(components[0], 10, 64)
		to, _ := strconv.ParseInt(components[1], 10, 64)
		x := lowBound(from)
		for {
			// fmt.Println("  x = ", x)
			if dup(x) < from {
				x += 1
				continue
			}
			if dup(x) > to {
				break
			}
			fmt.Println("  found: ", dup(x))
			sum += dup(x)
			x += 1
		}
	}
	fmt.Println(sum)
}
