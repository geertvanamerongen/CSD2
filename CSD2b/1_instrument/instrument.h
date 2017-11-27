class Instrument
{
public:
	Instrument();
	void makeSound();
	void makeMultipleSounds(int numTimes);
private:
	std::string sound;
};