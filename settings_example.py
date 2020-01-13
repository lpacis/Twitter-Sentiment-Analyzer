#settings.py example file - config settings.py file with env vars - fill out with twitter API creds.
TWITTER_API_KEY = ''
TWITTER_API_SECRET = ''
BASE_URL = 'https://api.twitter.com/'
AUTH_URL = '{}oauth2/token'.format(BASE_URL)
SEARCH_URL = '{}1.1/search/tweets.json'.format(BASE_URL)