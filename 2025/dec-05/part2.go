//go:build ignore

package main

import (
	"cmp"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func main() {
	data, _ := os.ReadFile("data.txt")
	lines := strings.Split(string(data), "\n")

	type Event struct {
		Value     int64
		IsOpening bool
	}

	events := []Event{}

	for _, line := range lines {
		if line == "" {
			break
		}
		tmp := strings.Split(line, "-")
		a, _ := strconv.ParseInt(tmp[0], 10, 64)
		b, _ := strconv.ParseInt(tmp[1], 10, 64)

		events = append(events, Event{
			a, true,
		})
		events = append(events, Event{
			b, false,
		})
	}

	// process all the events; if there are segments that start and end
	// on the same value, we process starts of the segments first
	slices.SortFunc(events, func(a, b Event) int {
		valueResult := cmp.Compare(a.Value, b.Value)
		if valueResult != 0 {
			return valueResult
		}
		if a.IsOpening == b.IsOpening {
			return 0
		} else if a.IsOpening {
			return -1
		} else if b.IsOpening {
			return +1
		}
		panic("not possible here")
	})

	freshCount := int64(0)
	depth := 0
	start := int64(-1)
	for _, event := range events {
		if event.IsOpening {
			if depth == 0 {
				start = event.Value
			}
			depth += 1
		} else {
			if depth == 1 {
				freshCount += event.Value - start + 1
			}
			depth -= 1
		}
	}

	fmt.Println(freshCount)
}
