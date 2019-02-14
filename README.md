
# Project Abstract


The SEC maintains EDGAR weblogs showing which IP addresses have accessed which documents for what company, and at what day and time this occurred.

This project is to build a pipeline to ingest that stream of data and calculate how long a particular user spends on EDGAR during a visit and how many documents that user requests during the session.


The program  expect two input files (be sure to read the section, "Repo directory structure", for details on where these files should be located):

* `log.csv`: EDGAR weblog data
* `inactivity_period.txt`: Holds a single value denoting the period of inactivity that should be used to identify when a user session is over

As it process the EDGAR weblogs line by line, the moment the program detect a user session has ended, your program should write a line to an output file, `sessionization.txt`, listing the IP address, duration of the session and number of documents accessed.

#My Solution
Create a session object to manage the user, start time, last active time and documents accessing during the session

Keep all active sessions in a map data structure(user_sessions) with user(ip)  as key

While reading through the input log line by line , keep updating the sessions in map

Once the input time changed, check the session in user_sessions, pop up the expired
session and write the info into output_file

# Repository structure

├── README.md
├── run.sh
├── src
│   └── sessionization.py
├── input
│   └── inactivity_period.txt
│   └── log.csv
├── output
|   └── sessionization.txt
├── insight_testsuite
    └── run_tests.sh
    └── tests
        └── test_1
        |   ├── input
        |   │   └── inactivity_period.txt
        |   │   └── log.csv
        |   |__ output
        |   │   └── sessionization.txt
        ├── your-own-test_1
            ├── input
            │   └── my-initial-inputs
            |── output
                └── sessionization.txt

#Instruction to run the project
Just run the run.sh script in the project directory with desired input file in the input folder.
