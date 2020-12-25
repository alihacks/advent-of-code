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
		op                  int
		mode1, mode2, mode3 int
		p1, p2              int
		ret                 int
		inputIndex          int
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
			fmt.Printf("Reading input, hardcoded %d\n", inputs[inputIndex])
			mem[mem[ip+1]] = inputs[inputIndex]
			inputIndex++
			ip += 2
		} else if op == 4 { // print val
			if mode1 == 1 { // imm
				ret = mem[ip+1]

			} else {
				ret = mem[mem[ip+1]]
			}
			fmt.Printf("VALUE: %d\n", ret)
			ip += 2
			return ip, ret

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
	//originalCode = []int{3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0}
	code := make([]int, len(originalCode))

	codeA := make([]int, len(originalCode))
	codeB := make([]int, len(originalCode))
	codeC := make([]int, len(originalCode))
	codeD := make([]int, len(originalCode))
	codeE := make([]int, len(originalCode))

	phases := []int{0, 1, 2, 3, 4}
	//copy(code, originalCode)

	fmt.Printf("Input: %d\r\n", code)
	max := 0
	for _, a := range phases {
		for _, b := range phases {
			if b == a {
				continue
			}
			for _, c := range phases {
				if c == a || c == b {
					continue
				}
				for _, d := range phases {
					if d == a || d == b || d == c {
						continue
					}
					for _, e := range phases {
						if e == a || e == b || e == c || e == d {
							continue
						}
						copy(codeA, originalCode)
						copy(codeB, originalCode)
						copy(codeC, originalCode)
						copy(codeD, originalCode)
						copy(codeE, originalCode)

						_, out := intCodeComputer(codeA, false, []int{a, 0}, 0)
						_, out = intCodeComputer(codeB, false, []int{b, out}, 0)
						_, out = intCodeComputer(codeC, false, []int{c, out}, 0)
						_, out = intCodeComputer(codeD, false, []int{d, out}, 0)
						_, out = intCodeComputer(codeE, false, []int{e, out}, 0)

						if out > max {
							max = out
						}
						fmt.Printf("Ultimate answer for phases (%d,%d,%d,%d,%d): %d\n", a, b, c, d, e, out)
					}
				}
			}
		}
	}
	fmt.Printf("Q1 Max: %d\n", max)
	fmt.Println("Q2")
	phases = []int{5, 6, 7, 8, 9}
	max = 0
	for _, a := range phases {
		for _, b := range phases {
			if b == a {
				continue
			}
			for _, c := range phases {
				if c == a || c == b {
					continue
				}
				for _, d := range phases {
					if d == a || d == b || d == c {
						continue
					}
					for _, e := range phases {
						if e == a || e == b || e == c || e == d {
							continue
						}
						copy(codeA, originalCode)
						copy(codeB, originalCode)
						copy(codeC, originalCode)
						copy(codeD, originalCode)
						copy(codeE, originalCode)
						fmt.Printf("Start for phases (%d,%d,%d,%d,%d)\n", a, b, c, d, e)

						ipA, out := intCodeComputer(codeA, false, []int{a, 0}, 0)
						ipB, out := intCodeComputer(codeB, false, []int{b, out}, 0)
						ipC, out := intCodeComputer(codeC, false, []int{c, out}, 0)
						ipD, out := intCodeComputer(codeD, false, []int{d, out}, 0)
						ipE, out := intCodeComputer(codeE, false, []int{e, out}, 0)

						// Feedback loop
						for ipA >= 0 {
							ipA, out = intCodeComputer(codeA, false, []int{out}, ipA)
							ipB, out = intCodeComputer(codeB, false, []int{out}, ipB)
							ipC, out = intCodeComputer(codeC, false, []int{out}, ipC)
							ipD, out = intCodeComputer(codeD, false, []int{out}, ipD)
							ipE, out = intCodeComputer(codeE, false, []int{out}, ipE)
							if out > max {
								max = out
							}
						}

						fmt.Printf("Ultimate answer for phases (%d,%d,%d,%d,%d): %d\n", a, b, c, d, e, out)
					}
				}
			}
		}
	}
	fmt.Printf("Q2: %d\n", max)
}
