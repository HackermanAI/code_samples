
# Makefile for a simple C project

CC      := gcc
CFLAGS  := -Wall -Wextra -std=c11
SRC     := main.c utils.c
OBJ     := $(SRC:.c=.o)
TARGET  := myapp

.PHONY: all clean debug

all: $(TARGET)

$(TARGET): $(OBJ)
    $(CC) $(OBJ) -o $@

%.o: %.c
    $(CC) $(CFLAGS) -c $< -o $@

debug: CFLAGS += -g -O0
debug: clean all

clean:
    rm -f $(OBJ) $(TARGET)
