# Task-13: Custom Shell
## Introduction
This is a very basic shell implemented in C. It currently has the following features implemented
- Can print the current working directory with `pwd`
- Can change the current working directory with `cd`
- Can print text to the output with `echo`
- Can execute any linux executable provided it is found in the path

## Installation
### Requirements
- C23 capable compiler(GCC 15+ or Clang 18+)
- GNU Make
### Building and Running
```bash
make    # can be skipped
make run
```

## Usage
- `pwd`: Prints the current working directory
- `cd`: Changes the current working directory
- `echo`: Prints provided text to the terminal
- `exit`: Exits the shell
- Type the name of any linux program found in path to run it
