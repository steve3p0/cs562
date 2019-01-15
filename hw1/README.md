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

    Two real challenges I had were the following:
    
    1. It took me forever to get PyCharm 2018.3 (the latest update) to push to github. I cried when I realized hours later I was clicking on the shortcut to PyCharm 2017.3.  When I installed the update, I had no idea it didn't remove the previous version :(
    2. I decided I would try to use my faster Windows machine rather than my Ubuntu VM.  Bad choice.
    
    Bugs that I encountered:
    
    - Getting the xpath query just right.
    - Remembering how parse command line args in Python
    - Adjusting to Python 3
	
#### Part 2: Structuring the data ####

What to turn in:
  
1. How many sentences are there in the CNA-GW corpus?
    
    585,065
    