# CS 562: Natural  Language Processing #
Instructor: Dr. Steven Bedrick, OHSU

Student: Steve Braich 

### Homework 1: Getting our Feet Wet ###

#### Part 1: Reading some data ####

What to turn in:

1. Your Program:

   * deserialize.py
   * deserialize_test.py
   * test_results/deserialize_100.txt
   * test_results/Test_Results_deserialize_test_py.html
  
2. Sample terminal output, showing perhaps the first 100 lines of its output

		[OUTPUT PANE OF PYCHARM TEST RUNNER]
        Testing started at 3:21 AM ...
        C:\Users\steve\AppData\Local\Programs\Python\Python37-32\python.exe "C:\Program Files\JetBrains\PyCharm 2018.3.3\helpers\pycharm\_jb_unittest_runner.py" --path C:/workspace_courses/cs562/hw1/deserialize_test.py
        Launching unittests with arguments python -m unittest C:/workspace_courses/cs562/hw1/deserialize_test.py in C:\workspace_courses\cs562\hw1
        
        Ran 4 tests in 7.736s
        OK

		[TERMINAL OUTPUT FROM PYCHARM]
		C:\Users\steve\AppData\Local\Programs\Python\Python37-32\python.exe C:/workspace_courses/cs562/hw1/deserialize.py data\GW-cna_eng\*.xml.gz -o data\GW-cna_eng\testMAIN_deserialize_all.txt
		Process finished with exit code 0
		
		[FIRST ONE HUNDRED LINES OF OUTPUT]
		steve@vboxUbuntu18:~/workspace_courses/cs562/hw1/data/GW-cna_eng$ head -100 testMAIN_deserialize_all.txt > ../../test_results/deserialize_100.txt
		
    You can find the first 100 lines of output in test_results/deserialize_100.txt
		
3. A sentence or two describing your approach and any bugs you encountered.

    I created a Deserialization class and unit tests.  The unit tests include some integration tests.  I added an optional argument "-o" to write the output to a file.  
            
        python deserialize.py cna_eng/*.xml.gz -o deserialized.txt
            
    I did this because I wanted to be able to run integration tests and specify an outfile (in the test) so that I could easily count the number lines and add other tests against the output data.  You can still redirect output to a file exactly as specified in the instructions:
            
        python deserialize.py cna_eng/*.xml.gz > deserialized.txt
    
    Bugs that I encountered:
    
    - Getting the xpath query just right.
    - Remembering how to do command line args in Python
    - Adjusting to Python 3
	- Reacquainting myself with PyCharm
	
#### Part 2: Structuring the data ####

What to turn in:
  
1. How many sentences are there in the CNA-GW corpus?
    
    585,065
    