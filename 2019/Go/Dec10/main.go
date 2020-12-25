package main

import (
	"bufio"
	"log"
	"os"
	"strings"
)

// Coord represends coordinates
type Coord struct {
	x, y int
}

func readInput() [][]string {
	var (
		cells [][]string
	)
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		cells = append(cells, strings.Split(scanner.Text(), ""))
	}
	return cells
}
func solveString(puzzle string) (int, int, int) {
	var cells [][]string
	for _, c := range strings.Split(puzzle, "\n") {
		cells = append(cells, strings.Split(c, ""))

	}
	return solve(cells)
}

func solve(puzzle [][]string) (int, int, int) {

	return 0, 0, 0
}

func main() {
	/*
		var (
			coords [2][]Coord
		)
		lines := readInput()
		for i := 0; i < len(lines); i++ {
			coords[i] = append(coords[i], Coord{0, 0})
			for _, cmd := range getCommands(lines[i]) {
				xAdd, yAdd := getCommandAdders(cmd)
				for x := 0; x < abs(cmd.xIncrement); x++ {
					lastCoord := coords[i][len(coords[i])-1]
					coords[i] = append(coords[i], Coord{lastCoord.x + xAdd, lastCoord.y})
				}
				for y := 0; y < abs(cmd.yIncrement); y++ {
					lastCoord := coords[i][len(coords[i])-1]
					coords[i] = append(coords[i], Coord{lastCoord.x, lastCoord.y + yAdd})
				}
			}
			//fmt.Printf("line %d: %+v\n", i, coords[i])
		}
		var matches []int  // q1
		var matches2 []int // question 2 keeps track of len

		// Find duplicates, don't count start point
		for i := 1; i < len(coords[0]); i++ {
			for j := 1; j < len(coords[1]); j++ {
				if coords[0][i] == coords[1][j] {
					dist := manhattanDist(coords[0][i])
					fmt.Printf("Match %+v %+v %d,%d\r\n", coords[0][i], coords[1][j], dist, i+j)
					matches = append(matches, dist)
					matches2 = append(matches2, i+j)
				}
			}
		}
		sort.Sort(sort.IntSlice(matches))
		fmt.Printf("Q1 got %d matches, in order %+v\r\n", len(matches), matches)

		sort.Sort(sort.IntSlice(matches2))
		fmt.Printf("Q2 got %d matches in order %+v\r\n", len(matches2), matches2)
	*/
}
