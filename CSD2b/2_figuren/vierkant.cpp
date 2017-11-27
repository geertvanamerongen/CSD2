#include <iostream>
#include "vierkant.h"

Vierkant::Vierkant(int x, int y) : Figuur(x,y)
{
	std::cout << "Vierkant constructor" << std::endl;
}

Vierkant::~Vierkant()
{

}

void Vierkant::teken()
{
	std::cout << "Teken vierkant " << std::endl;
}