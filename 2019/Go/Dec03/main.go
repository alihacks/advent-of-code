package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"
)

// Coord represends coordinates
type Coord struct {
	x, y int
}

// Command to move in a given direction
type Command struct {
	xIncrement, yIncrement int
}

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

func splitCommandString(cmd string) Command {
	var xMove, yMove int
	runes := []rune(cmd)
	dir := string(runes[0:1])
	num, _ := strconv.Atoi(string(runes[1:len(runes)]))
	switch dir[0] {
	case 'U':
		yMove = 1
	case 'D':
		yMove = -1
	case 'R':
		xMove = 1
	case 'L':
		xMove = -1
	}
	return Command{xMove * num, yMove * num}
}

func getCommands(line string) []Command {
	var (
		res []Command
	)
	for _, cmd := range strings.Split(line, ",") {
		command := splitCommandString(cmd)
		res = append(res, command)
		//fmt.Printf("%s %+v\r\n", cmd, command)
	}
	return res
}
func abs(i int) int {
	if i >= 0 {
		return i
	}
	return -1 * i
}

func getCommandAdders(cmd Command) (int, int) {
	var xAdd, yAdd int
	if cmd.xIncrement > 0 {
		xAdd = 1
	} else if cmd.xIncrement < 0 {
		xAdd = -1
	}
	if cmd.yIncrement > 0 {
		yAdd = 1
	} else if cmd.yIncrement < 0 {
		yAdd = -1
	}
	return xAdd, yAdd
}

func manhattanDist(c Coord) int {
	return abs(c.x) + abs(c.y)
}
func main() {
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

}
