# Online Live Monitoring
This repository is intended for online live monitoring display. To make interactive plot from the online data:

1. copy cafe online .csv file to this directory
2. read simc input parameter file (which has stats. count goal, rates, time, etc.) to be used as a reference when plotting data 
3. `plot_live.py`: this is the main script that reads in the .csv file and simc parameter file and generates an `index.html` 