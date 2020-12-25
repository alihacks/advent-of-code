package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strings"
)

func readInput() []string {
	var (
		lines []string
	)
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines
}

type planet struct {
	name string
	sun  *planet
}

func countOrbits(p planet) int {
	if p.sun == nil {
		return 0
	}
	return 1 + countOrbits(*p.sun)

}

var planets [5000]planet // this is a terrible idea for sake of perf
var pc int

func findOrCreatePlanet(name string, sunIx int) int {
	for i := 0; i < pc; i++ {
		if planets[i].name == name {
			if sunIx >= 0 {
				planets[i].sun = &planets[sunIx]
			}
			return i
		}
	}
	// insert at end, not found
	if sunIx >= 0 {
		planets[pc] = planet{name, &planets[sunIx]}
	} else {
		planets[pc] = planet{name, nil}
	}

	//	fmt.Printf("Added to index %s at %d\n", planets[pc], pc)
	pc++
	return pc - 1
}

func getAncestors(name string) []string {
	ix := findOrCreatePlanet(name, -1)
	if planets[ix].sun != nil {
		return append(getAncestors(planets[ix].sun.name), planets[ix].sun.name)
	}
	return nil

}

func main() {
	lines := readInput()

	pc = 0

	for _, line := range lines {
		parts := strings.Split(line, ")")
		sunName := parts[0]
		planetName := parts[1]
		sunIx := findOrCreatePlanet(sunName, -1)
		findOrCreatePlanet(planetName, sunIx)
	}
	fmt.Printf("%d planet(s) loaded\n", pc)
	orbits := 0
	for i := 0; i < pc; i++ {
		planet := planets[i]
		o := countOrbits(planet)
		orbits += o
		//fmt.Printf("%s %d\n", planet.name, o)
	}
	fmt.Printf("TOTAL orbits: %d\n", orbits)

	myAncestors := getAncestors("YOU")
	santaAncestors := getAncestors("SAN")
	myRelativeIx := 0
	santaRelativeIx := 0
	for i := 0; i < len(myAncestors); i++ {
		anc := myAncestors[i]
		for j := 0; j < len(santaAncestors); j++ {
			if anc == santaAncestors[j] {
				myRelativeIx = i
				santaRelativeIx = j
			}
		}
	}

	for _, a := range myAncestors {
		fmt.Printf("%s,", a)
	}
	fmt.Printf("\nSanta: ")
	for _, a := range santaAncestors {
		fmt.Printf("%s,", a)
	}
	fmt.Printf("\nClosest ancestor: %s\n", myAncestors[myRelativeIx])
	mydist := len(myAncestors) - myRelativeIx - 1 // subtract one because we both share the ancestor
	santadist := len(santaAncestors) - santaRelativeIx - 1
	fmt.Printf("\nDistances to ancestor: my: %d santa %d, TOT: %d\n", mydist, santadist, mydist+santadist)

}
