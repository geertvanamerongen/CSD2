#include <iostream>
#include "figuur.h"

Figuur::Figuur(int x, int y)
{
	std::cout << "Figuur constructor" << std::endl;
	this->x=x;
	this->y=y;
}

Figuur::~Figuur()
{

}

void Figuur::teken()
{
	std::cout << "teken: " << x << "," << y << std::endl;
}

void Figuur::verplaats()
{

}

void Figuur::setSnelheid(int snelheid)
{

}