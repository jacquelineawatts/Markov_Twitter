from random import choice
from os import environ
import twitter
from sys import argv

def open_and_read_file(first_text, *argv):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file_text = open(first_text).read()

    for arg in argv:
        file_text += open(arg).read()

    return file_text


def make_chains(text_string):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """

    chains = {}

    words = text_string.split()

    key_item1 = 0
    key_item2 = 1
    key_item3 = 2
    value_item = 3

    while key_item3 < (len(words) - 1):

        key = (words[key_item1], words[key_item2], words[key_item3])

        if key not in chains:
            chains[key] = []

        chains[key].append(words[value_item])

        # if key in chains:
        #     chains[key].append(words[value_item])
        # else:
        #     chains[key] = [words[value_item]]
        
        key_item1 += 1
        key_item2 += 1
        key_item3 += 1
        value_item += 1


    return chains


def find_upper_case(chains):
    """Takes chains dictionary and finds all instances where first letter of the 0th index of a key is upper case."""

    upper_case_keys = []
    for key in chains: 
        if key[0][0].isupper():
            upper_case_keys.append(key)

    return upper_case_keys


def find_punctuated_keys(chains):
    """Takes chains dictionary and finds all instances of punctuation on the last index of the last key element."""

    punctuated_keys = []
    for key in chains:
        if key[2][-1] in ['.', '?', '!']:
            punctuated_keys.append(key)    

    return punctuated_keys


def establish_starter_key(chains):
    """Selects random starter key from chains dictionary. """

    return choice(find_upper_case(chains))  


def make_text(chains):
    """Takes dictionary of markov chains; returns random text."""
    # 1. Pick a random key from our dictionary
    # 2. Put randomly generated key into our string
    # 3. Select at random a word from our values list thats associated with our key 
    # 4. Add that word to the string
    # 5. Shift frame to new key set which is second word from previous key + new word from value list
    # 6. Start over from step2
    
    # Punctuation:
    # 1. Have huge text string
    # 2. Start filtering through from the back, begin from -1 index, moving backwards by 1
    # 3. Compare to various end characters (?, ., !)
    # 4. If it is not one of those characters, delete
    # 5. If it is, break and return our text

    text = ""

    # Grabs a random starter key and adds it to text string
    current_key = establish_starter_key(chains)
    for word in current_key:
        text += word + " "

    # Runs loop to: 1)Grab random value, append to text string, and reassign new key
    # Limits text string to 1000 char 
    while len(text) < 120:
        value = choice(chains[current_key])
        text += value + " "
        current_key = (current_key[1], current_key[2], value)

    # Ensures that text string will end in punctuation
    if current_key not in find_punctuated_keys(chains):
        for index in range(len(text) -1, 0, -1):
            if text[index] in [".", "!", "?"]:
                break
            else:
                text = text[:index]
           
    return text + "#hbgracefall16"

def post_to_twitter(tweet):

    api = twitter.Api(
    consumer_key = environ['TWITTER_CONSUMER_KEY'],
    consumer_secret = environ['TWITTER_CONSUMER_SECRET'],
    access_token_key = environ['TWITTER_ACCESS_TOKEN_KEY'],
    access_token_secret = environ['TWITTER_ACCESS_TOKEN_SECRET']
    )

    print api.VerifyCredentials()

    status = api.PostUpdate(tweet)
    print status.text


input_path = argv[1:]   

# Open the file and turn it into one long string
input_text = open_and_read_file(input_path[0], *argv)

# Get a Markov chain
chains = make_chains(input_text)

# Produce random text
random_text = make_text(chains)

# Posts random text string to twitter
post_to_twitter(random_text)
