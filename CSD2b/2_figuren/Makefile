app: app.o figuur.o vierkant.o
	g++ -o app app.o figuur.o vierkant.o
	
app.o: app.cpp
	g++ -c app.cpp

figuur.o: figuur.cpp
	g++ -c figuur.cpp

vierkant.o: vierkant.cpp
	g++ -c vierkant.cpp

clean:
	rm -f *.o app