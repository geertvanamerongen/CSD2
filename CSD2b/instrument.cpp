#include <iostream>
#include "instrument.h"

Instrument::Instrument()
{
	sound = "ratata";
}
void Instrument::makeSound()
{
	std::cout << sound << std::endl;
}

void Instrument::makeMultipleSounds(int numTimes)
{
	for( int i = 0; i <numTimes; i++) {
		makeSound();
	}
}
