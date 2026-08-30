CC = gcc
CFLAGS = -Wall -Wextra -Werror -std=c23

SRC = src/main.c
OBJ = build/main.o
TARGET = build/cshell

run: $(TARGET)
	$(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET)

build/%.o: src/%.c
	mkdir -p build
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -rf build

.PHONY: run clean
