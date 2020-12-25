package main

import (
	"bufio"
	"fmt"
	"log"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

// numbers takes a comma delimited strings and returns an int slice
func numbers(s string) []int {
	var n []int
	for _, f := range strings.Split(s, ",") {
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

// intCodeComputer designed for AoC
func intCodeComputer(mem []int) {
	var (
		op int
		ip int
	)
	for op != 99 {
		op = mem[ip]
		if op == 1 {
			mem[mem[ip+3]] = mem[mem[ip+1]] + mem[mem[ip+2]]
			ip += 4
		} else if op == 2 {
			mem[mem[ip+3]] = mem[mem[ip+1]] * mem[mem[ip+2]]
			ip += 4
		}
	}
}

func main() {
	originalCode := readInput()
	code := make([]int, len(originalCode))
	// Overrides
	copy(code, originalCode)
	code[1] = 12
	code[2] = 2
	fmt.Printf("Input: %d\r\n", code)

	intCodeComputer(code)

	fmt.Printf("Q1: %d\r\n", code[0])

	//Q2
	magic := 19690720

	for code[0] != magic {
		copy(code, originalCode)
		code[1] = rand.Int() % (len(code) - 1)
		code[2] = rand.Int() % (len(code) - 1)
		intCodeComputer(code)

	}
	fmt.Printf("Q2: noun: %d verb: %d result: %d\r\n", code[1], code[2], 100*code[1]+code[2])
}
