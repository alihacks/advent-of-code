package main

import "testing"

func TestFuel(t *testing.T) {

	tables := []struct {
		mass int64
		fuel int64
	}{
		{12, 2},
		{14, 2},
		{1969, 654},
		{100756, 33583},
	}
	for _, table := range tables {
		calcFuel := Fuel(table.mass)
		if calcFuel != table.fuel {
			t.Errorf("Fuel for mass %d was incorrect, got: %d, want: %d.", table.mass, calcFuel, table.fuel)
		}
	}
}

func TestFuel2(t *testing.T) {

	tables := []struct {
		mass int64
		fuel int64
	}{
		{14, 2},
		{1969, 966},
		{100756, 50346},
	}
	for _, table := range tables {
		calcFuel := Fuel2(table.mass)
		if calcFuel != table.fuel {
			t.Errorf("Fuel2 for mass %d was incorrect, got: %d, want: %d.", table.mass, calcFuel, table.fuel)
		}
	}
}
