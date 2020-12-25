package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

// numbers takes a comma delimited strings and returns an int slice
func numbers(s string) []int {
	var n []int
	for _, f := range strings.Split(s, "") {
		i, err := strconv.Atoi(f)
		if err == nil {
			n = append(n, i)
		}
	}
	return n
}

// readInput reads the input.txt and returns an int slice
func readInput() []int {
	file, err := os.Open("input.txt")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	var (
		codes []int
		line  string
	)
	for scanner.Scan() {
		line = scanner.Text()
		if err != nil {
			log.Fatal(err)
		}
		codes = append(codes, numbers(line)...)
	}
	return codes
}

func main() {
	nums := readInput()
	var layers [][]int
	cols, rows := 25, 6

	for i := 0; i < len(nums); i += cols * rows {
		end := i + cols*rows
		if end > len(nums) {
			end = len(nums)
		}
		layers = append(layers, nums[i:end])
	}

	// Create a black image
	img := make([][]int, rows)
	for i := 0; i < rows; i++ {
		img[i] = make([]int, cols)
	}

	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			img[r][c] = 2
		}
	}

	for i := len(layers) - 1; i >= 0; i-- {
		r, c := 0, 0
		for _, pix := range layers[i] {
			if pix != 2 { // trasparent
				img[r][c] = pix
			}
			c++
			if c >= cols {
				c = 0
				r++
			}
		}

	}
	for r := 0; r < rows; r++ {
		for c := 0; c < cols; c++ {
			if img[r][c] == 1 {
				fmt.Printf("X")
			} else if img[r][c] == 0 {
				fmt.Printf(" ")
			}

		}
		fmt.Printf("\n")
	}
	//fmt.Printf("%+v", img)
	/*


		for _, v := range nums {
			img[r][c] = v

			// New layer
			if r >= rows {
				r, c = 0, 0
			}

		}
		fmt.Printf("%+v\n", img)

		//
	*/

}
