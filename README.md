# This is the implementation of an exercise
Exercise files are in the "exercise" directory, with README.pdf containing instructions and two csv files containing data
Content:
  - exercise - directory contains the test description and test data
  - requirements - contains the dependencies
  - src - sources
    - tele_io.py module for the OS handling
    - telemetry.py module for telemetry validation and processing
  - test - directory contains the unit tests

# How to install the package
clone the repositiory
`git clone https://github.com/viopl/exercise_energy`

change the directory
`cd exercise_energy`

create virtual environment 
`virtualenv .venv`

activate the virtual environment
`source .venv/bin/activate`

on windows, the activation command is
`.venv\Scripts\activate.bat`

install required libraries for production environment
`pip install -r requirements/base.txt`

in order to run tests, install the test requirements
`pip install -r requirements/tests.txt`

# How to use the package
`python -m src.telemetry -a <zeros|agg> -i <input file name> -o <output file name>`

example:
`python -m src.telemetry -a zeros -i exercise/zero_reads_data.csv -o exercise/zero_out.csv`

parameters:
  -a | --action [zeros | agg]
    The function to be called: 
	    "zeros" for invalidating 0-telemetry
		"agg" for aggregating telemetry data per hour
		
  -i | --input <FileName>
    The input file name, mandatory

  -o | --output <FileName>
    The output file name; when empty, the input file will be overridden

# Run the tests
call the pytest package, e.g.
`pytest`

or 'pytest test/test_io.py' for a specific test module
