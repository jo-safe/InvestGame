# InvestGame
In future it should be a cross-platform game about investing, trading or something, but now this repository has only a script for windows (using wx for python) to edit game data about some plot things for the game like exchanges information, news that should be happened by the plot, choosen by player. Besides, there is an .exe file and an example data file that is only a utf-8 text file but it can by viewed correctly by the program.
Some information about data files:
  - each news structure collects id, force with which it acts to the game situation, influence that defines stocks and commodities to apply the force to, duration and some descriptions
  - stocks have common information such as ticker from the exchange (that is kind of id), country, company, industry and commodities which the stock has influence to
  - commodities also have a ticker and name, sector, influence.
There are not any news in example file, there are 50 stocks and 24 commodities with an almost completed description.
