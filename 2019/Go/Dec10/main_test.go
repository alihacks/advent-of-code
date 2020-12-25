package main

import "testing"

func Test1(t *testing.T) {
	input := `......#.#.
	#..#.#....
	..#######.
	.#.#.###..
	.#..#.....
	..#....#.#
	#..#....#.
	.##.#..###
	##...#..#.
	.#....####`
	r, c, cnt := 5, 8, 33
	row, col, count := solveString(input)
	if r != row || c != col {
		t.Errorf("Incorrect r,c %d,%d (Expected %d, %d)", row, col, r, c)
	}
	if count != cnt {
		t.Errorf("Incorrect count %d (Expected %d)", count, cnt)
	}
}

func Test2(t *testing.T) {
	input := `#.#...#.#.
	.###....#.
	.#....#...
	##.#.#.#.#
	....#.#.#.
	.##..###.#
	..#...##..
	..##....##
	......#...
	.####.###.`
	r, c, cnt := 1, 2, 35
	row, col, count := solveString(input)
	if r != row || c != col {
		t.Errorf("Incorrect r,c %d,%d (Expected %d, %d)", row, col, r, c)
	}
	if count != cnt {
		t.Errorf("Incorrect count %d (Expected %d)", count, cnt)
	}

}

func Test3(t *testing.T) {
	input := `.#..#..###
	####.###.#
	....###.#.
	..###.##.#
	##.##.#.#.
	....###..#
	..#.#..#.#
	#..#.#.###
	.##...##.#
	.....#.#..`

	r, c, cnt := 6, 3, 41
	row, col, count := solveString(input)
	if r != row || c != col {
		t.Errorf("Incorrect r,c %d,%d (Expected %d, %d)", row, col, r, c)
	}
	if count != cnt {
		t.Errorf("Incorrect count %d (Expected %d)", count, cnt)
	}
}

func Test4(t *testing.T) {
	input := `.#..##.###...#######
	##.############..##.
	.#.######.########.#
	.###.#######.####.#.
	#####.##.#.##.###.##
	..#####..#.#########
	####################
	#.####....###.#.#.##
	##.#################
	#####.##.###..####..
	..######..##.#######
	####.##.####...##..#
	.#####..#.######.###
	##...#.##########...
	#.##########.#######
	.####.#.###.###.#.##
	....##.##.###..#####
	.#.#.###########.###
	#.#.#.#####.####.###
	###.##.####.##.#..##`

	r, c, cnt := 11, 13, 210
	row, col, count := solveString(input)
	if r != row || c != col {
		t.Errorf("Incorrect r,c %d,%d (Expected %d, %d)", row, col, r, c)
	}
	if count != cnt {
		t.Errorf("Incorrect count %d (Expected %d)", count, cnt)
	}
}
