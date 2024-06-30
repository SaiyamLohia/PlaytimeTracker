# Playtime Calculator

An App to calculate the total play time of games, or any program running on your computer.



## Run Locally

Clone the project.

Install the "psutil" library and Python.

```
  pip install psutil
```
Open terminal in the project directory and run main.py

```
  python main.py
```

## Adding Games
In the "data.csv" file add the path to the executable of your game in the first column, name of the executable/game in the second column, time it has already run for (In Minutes) (intially 0) in the third column.


### The Third column in data.csv will be automatically updated as you use the executables added in the file.
### The time used will be added and updated only if applications are used (and closed) while the script is running.
