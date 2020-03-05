# Siifparser
Siifparser is a UWWTD (Urban Waste Water Treatment Directive) reporting file standalone tester and parser
  - Upload a UWWTD reporting file using the php client tester
  - wait for the Web Processing Service to answer
# How to run
  - excecute run.sh 
# What is where?
 - run.sh: main script to run the WPS as a daemon
 - siifparser.py: the main WPS script
 - ./processes/siifparser.py: the siifparser WPS process  handler
 - ./src/siifparser/: source code for the siifparser
    - data/schemas: UWWTD XSD reporting schema
    - testfiles: previous reported files for testing
    - tests: unit testing
    - test_siifparser.db: sqlite unit testing database
    - error_level.conf: configuration file for error levels
    - SiifParser.py: main class
- .src/siifparser/client_php: a php demo client to test WPS remotely

# To be continued...
