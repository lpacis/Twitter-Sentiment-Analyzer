# Twitter-Sentiment-Analyzer

Quick and easy way to do sentiment analysis for a given twitter handle. 

1. Apply for a developer account on twitter get consumer key and secret.

2. Create a settings.py file from the example file, and add your key and secret.

3. You will likely need to add the following packages to the environment.
  TextBlob, WordCloud, and tweepy
  If you get an import error for any other modules - check that you have them and if not install them.
  
4. Running this app is pretty simple, simply run the twitter.py file and you will see a few prompts.
  `Do you want to gather twitter data for an hour? (Y or N)` - This will kick off a loop to hit the twitter API every minute and build the sentiment for each tweet using TextBlob.
  Responding yes will prompt - `What is the twitter handle you want to gather data for? (include the @)` 
  
  This will create a CSV for that handle such as `@handle.csv`.
  
  After gathering data for an hour, it will ask - `Which file do you want to run analysis on? - `
  
  This will output some basic statistics for the number of neutral, positive, and negative sentiment percentages of tweets.
  
  Negative tweet percentage: 33.3%
  Positive teet percentage: 33.3%
  Neutral tweet percentage: 33.3%
  
  Then there is a prompt to display a word cloud of the most used words throughout all of the tweets.
  
  
