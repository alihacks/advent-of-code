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
func intCodeComputer(mem []int, chatty bool, inputs []int, ip int) (int, int) {
	var (
		op, rb              int
		mode1, mode2, mode3 int
		p1, p2, p3          int
		ret                 int
		inputIndex          int
	)
	for op != 99 {
		op = mem[ip]
		p1 = 0
		p2 = 0
		p3 = 0
		mode1 = op / 100 % 10
		mode2 = op / 1000 % 10
		mode3 = op / 10000 % 10
		op = op % 100
		if chatty {
			fmt.Printf("ip=%d mem=[ ", ip)
			for i := 0; ip+i < len(mem) && i <= 3; i++ {
				fmt.Printf("%d ", mem[ip+i])
			}
			fmt.Printf("]\tOp: %d Modes %d, %d, %d", op, mode1, mode2, mode3)
		}

		// Get param1 for ops that support it
		if op == 1 || op == 2 || op == 4 || op == 5 || op == 6 || op == 7 || op == 8 || op == 9 {
			if mode1 == 0 {
				p1 = mem[mem[ip+1]]
			} else if mode1 == 1 {
				p1 = mem[ip+1]
			} else if mode1 == 2 {
				p1 = mem[rb+mem[ip+1]]
			}
		}
		if op == 3 { // for 3, p1 is an index
			if mode1 == 0 {
				p1 = mem[ip+1]
			} else if mode1 == 2 {
				p1 = rb + mem[ip+1]
			}
		}
		// get param 2 for ops that support it
		if op == 1 || op == 2 || op == 5 || op == 6 || op == 7 || op == 8 {

			if mode2 == 0 {
				p2 = mem[mem[ip+2]]
			} else if mode2 == 1 {
				p2 = mem[ip+2]
			} else if mode2 == 2 {
				p2 = mem[rb+mem[ip+2]]
			}
		}

		if mode3 == 0 {
			p3 = mem[ip+3]
		} else if mode3 == 2 {
			p3 = rb + mem[ip+3]
		}

		if chatty {
			fmt.Printf("(params %d %d)\n", p1, p2)
		}

		if op == 1 { // add
			mem[p3] = p1 + p2
			if chatty {
				fmt.Printf("\tmem[%d] = %d + %d = %d\n", p3, p1, p2, p1+p2)
			}
			ip += 4
		} else if op == 2 { // mul
			mem[p3] = p1 * p2
			if chatty {
				fmt.Printf("\tmem[%d] = %d * %d = %d\n", p3, p1, p2, p1*p2)
			}
			ip += 4
		} else if op == 3 { // read input
			fmt.Printf("Reading input, hardcoded %d\n", inputs[inputIndex])
			mem[p1] = inputs[inputIndex]
			inputIndex++
			ip += 2
		} else if op == 4 { // print val
			ret = p1
			fmt.Printf("VALUE: %d\n", ret)
			ip += 2
			//return ip, ret

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
				mem[p3] = 1
			} else {
				mem[p3] = 0
			}
			ip += 4
		} else if op == 8 { // equals
			if p1 == p2 {
				mem[p3] = 1
			} else {
				mem[p3] = 0
			}
			ip += 4
		} else if op == 9 { // save base
			rb += p1
			if chatty {
				fmt.Printf("New RB:%d\n", rb)
			}
			ip += 2
		} else if op == 99 {
			if chatty {
				fmt.Printf("We are done here!!\n")
				return -1, ret
			}
			break
		} else {
			log.Fatal(fmt.Sprintf("Bad opcode %d", op))
		}
	}
	return -1, ret
}

func main() {
	originalCode := readInput()
	//originalCode = []int{109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99}  // self print
	//originalCode = []int{104, 1125899906842624, 99} // large test
	code := make([]int, len(originalCode)+65535)
	copy(code, originalCode)
	_, out := intCodeComputer(code, false, []int{1}, 0)
	fmt.Printf("Q1 %d\n", out)

	//copy(code, originalCode)
	_, out = intCodeComputer(code, false, []int{2}, 0)
	fmt.Printf("Q2 %d\n", out)
}
