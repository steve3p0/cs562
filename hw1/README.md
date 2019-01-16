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
 
#### Part 3: Counting and comparing ####

What to turn in:

1. How many unique types are present in this corpus?

    72,926

2. How about unigram tokens?

    16,966,821

3. Produce a rank-frequency plot (similar to those seen on the Wikipedia page for Zipf's Law) for this corpus.

![picture alt](https://raw.githubusercontent.com/steve3p0/cs562/master/hw1/test_results/zipfs.png "Title is optional")

4. What are the twenty most common words?

    THE, TO, OF, AND, IN, A, THAT, TAIWAN, SAID, FOR, ON, WILL, WITH, IS, AT, AS, BY, HE, BE, FROM

5. You may notice that the most common are words that occur very frequently in the English language (stopwords). What happens to your type/token counts if you remove stopwords using nltk.corpora's stopwords list?

    The counts drop significantly.  The most common non-stop word is TAIWAN.  It still appears over 200,000 times.  But after that the counts really drop.

6. After removing stopwords, what are the 20 most common words?
    
    TAIWAN, SAID, CHINA, PERCENT, GOVERNMENT, YEAR, CHEN, ALSO, PRESIDENT, TAIPEI, TWO, NT, US, MAINLAND, PEOPLE, NEW, CHINESE, PARTY, 1, ACCORDING

#### Word association metrics ####

There are many ways to identify collocated words, but one common one is to use Pointwise Mutual Information. This measure captures how much more likely it is that two events occur together than 
would be the case if the events were statistically independent.

* Recalling Emily Bender's sage advice- "Look at your data!"- examine the 30 highest-PMI word pairs, along with their unigram and bigram frequencies. What do you notice?
		
    With no threshold I see data that makes no sense.  There's a lot of numbers.  When start moving the threshold up higher, let's say from 5 - 100, I get a lot names that probably comes from that part of the world, Taiwan.  At a threshold of 40, I get SPONGIFORM ENCEPHALOPATHY, that was mentioned in class.  When I hit about 200-300, I see terms that start making sense to me.  I noticed the higher I go, I start getting into some very common and words like LAST-MINUTE CHANGES and METRIC TONS.
    
* Experiment with a few different threshold values, and report on what you observe.
    
    When start moving the threshold up higher, let's say from 5 - 100, I get a lot names that probably comes from that part of the world, Taiwan.  At a threshold of 40, I get SPONGIFORM ENCEPHALOPATHY, that was mentioned in class.  When I hit about 200-300, I see terms that start making sense to me.  I noticed the higher I go, I start getting into some very common and words like LAST-MINUTE CHANGES and METRIC TONS.
    
* With a threshold of 100, what are the 10 highest-PMI word pairs?

    Examine the PMI for "New York". Explain in your own words why it is not higher.

* With a threshold of 100, what are the 10 highest-PMI word pairs?

    [('SPONGIFORM', 'ENCEPHALOPATHY'), ('YING-', 'JEOU'), ('BOVINE', 'SPONGIFORM'), ('ALMA', 'MATER'), ('SRI', 'LANKA'), ('KUALA', 'LUMPUR'), ('SAO', 'TOME'), ('AU', 'OPTRONICS'), ('ERIC', 'LILUAN'), ('QIAN', 'QICHEN')]

* Examine the PMI for "New York". Explain in your own words why it is not higher.

    I don't think the way I did PMI was in the spirit of your assignment.  I used the NLTK library to calculate PMI and thus didn't compute unigram and b-gram probabilities.  If I may take a look at this after my class ends, I can get this done rather quickly.

