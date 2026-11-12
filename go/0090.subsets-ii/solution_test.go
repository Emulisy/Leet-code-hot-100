package main

import (
	"fmt"
	"math/rand"
	"reflect"
	"sort"
	"testing"
)

func TestSubsetsWithDupAgainstPowerSet(t *testing.T) {
	rng := rand.New(rand.NewSource(90))
	cases := [][]int{{}, {0}, {2, 1, 2}, {2, 2, 2}, {-1, -1, 0}}
	for size := 1; size <= 8; size++ {
		for trial := 0; trial < 20; trial++ {
			values := make([]int, size)
			for i := range values {
				values[i] = rng.Intn(5) - 2
			}
			cases = append(cases, values)
		}
	}
	for _, values := range cases {
		original := append([]int{}, values...)
		expected := map[string]bool{}
		for mask := 0; mask < 1<<len(values); mask++ {
			subset := []int{}
			for i, value := range values {
				if mask&(1<<i) != 0 {
					subset = append(subset, value)
				}
			}
			sort.Ints(subset)
			expected[fmt.Sprint(subset)] = true
		}
		actual := subsetsWithDup(values)
		if !reflect.DeepEqual(values, original) {
			t.Fatalf("input mutated: %v became %v", original, values)
		}
		if len(actual) != len(expected) {
			t.Fatalf("input %v: expected %d unique subsets, got %v", values, len(expected), actual)
		}
		for _, subset := range actual {
			copyOfSubset := append([]int{}, subset...)
			sort.Ints(copyOfSubset)
			key := fmt.Sprint(copyOfSubset)
			if !expected[key] {
				t.Fatalf("input %v: unexpected or repeated subset %v", values, subset)
			}
			delete(expected, key)
		}
	}
}

func TestSubsetsWithDupResultsDoNotAlias(t *testing.T) {
	values := []int{2, 1, 2}
	result := subsetsWithDup(values)
	before := make([]string, len(result))
	for i, subset := range result {
		before[i] = fmt.Sprint(subset)
	}
	for i, subset := range result {
		if len(subset) == 0 {
			continue
		}
		subset[0] = 100
		for j, other := range result {
			if j != i && fmt.Sprint(other) != before[j] {
				t.Fatal("different output subsets share mutable storage")
			}
		}
		break
	}
	if !reflect.DeepEqual(values, []int{2, 1, 2}) {
		t.Fatal("output subsets share mutable storage with the input")
	}
}
