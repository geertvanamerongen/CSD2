//#pragma once
#ifndef _FIGUUR_H_
#define _FIGUUR_H_

class Figuur
{
public:
	Figuur(int x, int y);
	~Figuur(); //destructor

	void teken();
	void verplaats();
	void setSnelheid(int snelheid);

private:
	int x,y;
	int snelheid;
};

#endif // _FIGUUR_H_