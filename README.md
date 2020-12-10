# IFTTT-backend

## Requirements

Python 3

## Installation

1. Download the IFTTT backend service from IFTTT website
2. Put the repository in a desired directory
3. Installing required packages by running 
   > python3 -m pip install -r requirements.txt
   
   in the project directory

## Invocation

1. To start the trigger checking process using command:
   > sudo python3 Orchestrator.py
   
    in the backend directory
   
2. Monitors will be updated when the backend is started.\
Monitors can also be added by running 
   >python3 UpdateMonitors

3. The backend should be terminated before modifying monitor variables within 
   a current monitor to avoid exceptions.
   
## Adding New Monitors

1. Create a python file in /Monitors
2. Initialize the monitor_var variable dictionary variable which indicates the types of variables to be tracked by the monitor  
3. Initialize the monitor_text string variable which contains a string that provides assistance in monitor usage  
4. Create class for monitors and make it extend Monitor, inside this class: 
5. Create mapper function which returns a dictionary that maps the variable names to the functions that retrieve and return the status of each respective variable 
6. Define the functions that retrieve and return the status of the variables, for each variable. These functions take in the parameters (self, func, val) and should return the a tuple containing the value returned by func(VARIABLE_VALUE, val) and VARIABLE_VALUE i.e.   
7. Outside the class write the start method, which initializes the monitor

### Please look at the monitor folder for examples of monitors
