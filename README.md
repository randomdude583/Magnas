# Magnas
Python application to scrape tweets of a user and get all responses. Data can be used as training sets for machine learning

DEPENDANCIES:
Tweepy: pip install tweepy

STEPS:
1) Download the .py files.
2) Change the "user" field to the username that you want to scrape.
3) Input your Consumer Key, Consumer Secret, Access Token, and Access Secret.
4) Run using "python Magnas.py"
5) After the program finishes, a file will be created in the same directory titled data.txt that contains the output.
6) Run MagnasAnalyzer using "python MagnasAnalyzer.py" to search data for the largest dataset, and export as a LSV file titled trainingSet.txt
