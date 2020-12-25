package main

import (
	"fmt"
	"strconv"
)

func isValid(num int) bool {
	bytes := []byte(strconv.Itoa(num))
	adjacent := false

	for i := 1; i < len(bytes); i++ {
		if bytes[i-1] > bytes[i] {
			return false
		}
		if bytes[i-1] == bytes[i] {
			adjacent = true
		}
	}
	return adjacent
}

func isValid2(num int) bool {
	bytes := []byte(strconv.Itoa(num))
	adjacent := false
	//var adjDigit byte = 0

	for i := 1; i < len(bytes); i++ {
		if bytes[i-1] > bytes[i] {
			return false
		}
		if bytes[i-1] == bytes[i] {
			if i == len(bytes)-1 {
				return true
			}

			if bytes[i+1] == bytes[i] { // triple
				for i < len(bytes)-1 && bytes[i+1] == bytes[i] {
					i++
				}
			} else {
				adjacent = true
			}

		}
	}
	return adjacent
}

func main() {
	from := 353096
	to := 843212
	var cnt, cnt2 int
	for i := from; i <= to; i++ {
		if isValid(i) {
			cnt++
		}
		if isValid2(i) {
			cnt2++
		}
	}
	fmt.Printf("Q1: Valid passwords: %d\n", cnt)
	fmt.Printf("Q2: Valid passwords: %d\n", cnt2)

}
