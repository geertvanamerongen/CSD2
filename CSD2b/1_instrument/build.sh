#! /bin/bash

#compile
g++ -c hello.cpp
g++ -c world.cpp

#link and create exec
g++ -o hello hello.o world.o

#remove .o files
# rm hello.o world.o