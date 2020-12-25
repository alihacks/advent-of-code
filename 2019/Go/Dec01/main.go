package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

// Fuel required to launch a given module is based on its mass.
// Specifically, to find the fuel required for a module, take its mass,
// divide by three, round down, and subtract 2.
func Fuel(mass int64) int64 {
	return mass/3 - 2
}

// Fuel2 - Keep in mind that fuel has mass and fuel needs fuel
// treat the fuel amount you just calculated as the input
// mass and repeat the process, continuing until a fuel requirement is zero or negative
func Fuel2(mass int64) int64 {
	if mass <= 0 {
		return 0
	}
	fm := Fuel(mass)
	if fm < 0 {
		fm = 0
	}
	return fm + Fuel2(fm)
}

func main() {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var (
		total  int64
		total2 int64
	)
	for scanner.Scan() {
		mass, err := strconv.ParseInt(scanner.Text(), 0, 64)
		if err != nil {
			log.Fatal(err)
		}
		fuel := Fuel(mass)
		total2 += fuel + Fuel2(fuel)
		total += fuel
		fmt.Printf("Mass: %d, Fuel: %d\r\n", mass, fuel)
	}
	fmt.Printf("Total Fuel Needed: %d\r\n", total)
	fmt.Printf("Total Fuel Needed including fuel for fuel: %d\r\n", total2)

}
