package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
)

func main() {
	pwd, _ := os.Getwd()
	fmt.Println(pwd)
	// Open input file
	file, err := os.Open("~/code/advent_of_code_2021/day4/input.txt")
	defer file.Close()
	if err != nil {
		log.Fatalf("could not find file")
	}
	// Use scanner to parse file line by line and storein []string
	scanner := bufio.NewScanner(file)
	scanner.Split(bufio.ScanLines)
	var text []string
	for scanner.Scan() {
		text = append(text, scanner.Text())
	}
	// Print each line in text one by one
	for _, line := range text {
		fmt.Println(line)
	}
}
