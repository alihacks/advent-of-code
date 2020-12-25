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
func intCodeComputer(mem []int, chatty bool, input int) {
	var (
		op, ip              int
		mode1, mode2, mode3 int
		p1, p2              int
	)
	for op != 99 {
		op = mem[ip]
		p1 = 0
		p2 = 0
		mode1 = op / 100 % 10
		mode2 = op / 1000 % 10
		mode3 = op / 10000 % 10
		op = op % 100
		if chatty {
			fmt.Printf("ip=%d mem=[ ", ip)
			for i := 0; ip+i < len(mem) && i < 3; i++ {
				fmt.Printf("%d ", mem[ip+i])
			}
			fmt.Printf("]\tOp: %d Modes %d, %d, %d", op, mode1, mode2, mode3)
		}

		// Get param1 for ops that support it
		if op == 1 || op == 2 || op == 5 || op == 6 || op == 7 || op == 8 {
			if mode1 == 0 {
				p1 = mem[mem[ip+1]]
			} else {
				p1 = mem[ip+1]
			}
		}
		// get param 2 for ops that support it
		if op == 1 || op == 2 || op == 5 || op == 6 || op == 7 || op == 8 {

			if mode2 == 0 {
				p2 = mem[mem[ip+2]]
			} else {
				p2 = mem[ip+2]
			}
		}

		if chatty {
			fmt.Printf("(params %d %d)\n", p1, p2)
		}

		if op == 1 { // add
			mem[mem[ip+3]] = p1 + p2
			ip += 4
		} else if op == 2 { // mul
			mem[mem[ip+3]] = p1 * p2
			ip += 4
		} else if op == 3 { // read input
			fmt.Printf("Reading input, hardcoded %d\n", input)
			mem[mem[ip+1]] = input
			ip += 2
		} else if op == 4 { // print val
			if mode1 == 1 { // imm
				fmt.Printf("VALUE: %d\n", mem[ip+1])
			} else {
				fmt.Printf("VALUE: %d\n", mem[mem[ip+1]])
			}
			ip += 2

		} else if op == 5 { // jump-if-true
			if p1 != 0 {
				ip = p2
			} else {
				ip += 3
			}
		} else if op == 6 { // jump-if-false
			if p1 == 0 {
				ip = p2
			} else {
				ip += 3
			}
		} else if op == 7 { // less than
			if p1 < p2 {
				mem[mem[ip+3]] = 1
			} else {
				mem[mem[ip+3]] = 0
			}
			ip += 4
		} else if op == 8 { // equals
			if p1 == p2 {
				mem[mem[ip+3]] = 1
			} else {
				mem[mem[ip+3]] = 0
			}
			ip += 4
		} else if op == 99 {
			fmt.Printf("We are done here!!\n")
			break
		} else {
			log.Fatal(fmt.Sprintf("Bad opcode %d", op))
		}
	}
}

func main() {
	originalCode := readInput()
	code := make([]int, len(originalCode))
	copy(code, originalCode)

	fmt.Printf("Input: %d\r\n", code)

	intCodeComputer(code, false, 1)

	// Q2
	copy(code, originalCode)
	intCodeComputer(code, false, 5)

}
