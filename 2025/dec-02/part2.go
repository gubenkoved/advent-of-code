//go:build ignore

package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func dup(x int64, k int) int64 {
	result := ""
	for i := 0; i < k; i++ {
		result += fmt.Sprintf("%d", x)
	}
	xx, err := strconv.ParseInt(result, 10, 64)
	if err != nil {
		panic("bad!")
	}
	return xx
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
		digitCount := int(math.Ceil(math.Log10(float64(to))))
		seen := map[int64]bool{}
		for repCount := 2; repCount <= digitCount; repCount++ {
			x := int64(1)
			for {
				// fmt.Println("  x = ", x)
				xx := dup(x, repCount)
				if xx < from {
					x += 1
					continue
				}
				if xx > to {
					break
				}
				if !seen[xx] {
					seen[xx] = true
					fmt.Println("  found: ", xx)
					sum += xx
				}
				x += 1
			}
		}
	}
	fmt.Println(sum)
}
