import nltk
from nltk.corpus import state_union
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from pprint import pprint

################################ FUNCTIONS ################################

def tokenize_text(text):
    """applies sentence and word tokenization and returns a nested list of sentences and words"""
    s_tknzd = sent_tokenize(text)
    all_words = []
    for sentence in s_tknzd:
        try:
            wordset = word_tokenize(sentence)
            all_words.append(wordset)
        except Exception as e:
            print(str(e))
    return all_words

def tag_POS(nested_word_list):
    """tags each word in a nested list of words with the POS information"""
    tagged_text = []
    for sentence in nested_word_list:
        tagged = nltk.pos_tag(sentence)
        tagged_text.append(tagged)
    return tagged_text

def cloze_text(tagged_text, *args):
    """applies cloze deletion to all words in a text that have different POS than entered in the *args.

    takes a POS tagged text as input
    as well as an arbitrary number of POS abbreviations
    replaces each word that is a different POS with a blank
    returns a nested list of sentences and words that only keep the words
    that associate with the entered POS.
    """
    clozed_text = []
    for sen in tagged_text:
        clozed_sen = []
        for word_inf in sen:
            word = word_inf[0]
            POS = word_inf[1]
            if POS not in args:
                # change this to "_____" if you prefer a more standard cloze deletion
                # I changed this for compactness and better display in the HTML
                clozed_sen.append(".")
            else:
                clozed_sen.append(word)
        clozed_text.append(clozed_sen)
    return clozed_text

def create_speech(clozed_text):
    """creates a string from a nested list"""
    essentialized_text = ""
    for s in clozed_text:
        sentence = " ".join(s)
        essentialized_text += sentence + "\n"
    return essentialized_text

def create_speech_for_web(clozed_text, filename):
    """creates a simple HTML website from a nested list"""
    essentialized_text = """<!DOCTYPE html>
<html>
<head>
	<title>Essential Speeches</title>
	<link href="https://fonts.googleapis.com/css?family=Amatic+SC" rel="stylesheet">
	<style type="text/css">
		body {
			margin: auto;
			text-align: center;
			max-width: 800px;
			font-family: 'Amatic SC', cursive;
			font-size: 2.3em;
			background-image: url("http://www.publicdomainpictures.net/pictures/70000/velka/old-parchment.jpg");
		}
		p {
			padding: 20px;
		}
	</style>
</head>
<body>"""
    for s in clozed_text:
        sentence = " ".join(s)
        essentialized_text += "<p>" + sentence + "</p>"
    essentialized_text += """</body>
</html>"""
    with open(filename, "w") as f:
        f.write(essentialized_text)

def get_real(president_speech):
    """creates a cloze-deleted website of a president's speech.

    takes as input a string of a state union speech .txt file
    runs it through the pipeline of functions and creates a website.
    if the speech is not correctly specified, it returns a list with available options.
    """
    try:
        speech = state_union.raw(president_speech)
        tokenized_text = tokenize_text(speech)
        text_POS_tagged = tag_POS(tokenized_text)
        # change the POS *args here for different results
        # check this page for all options:
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        essentials = cloze_text(text_POS_tagged, "NNP", "NNPS", "NN", "NNS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ")
        create_speech_for_web(essentials, "index.html")
    except:
        speeches = state_union.fileids()
        print("Please try again. Enter a STRING.")
        print("These are your options:\n")
        print(speeches)

################################ RUNNING ################################

# you can pick a different speech from the results of running: state_union.fileids()
kennedy2_full = state_union.raw("1962-Kennedy.txt")
text_POS_tagged = tag_POS(tokenize_text(kennedy2_full))
# select which POS to keep
# https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
# the "essentials" selection keeps all nouns and verbs - nudging to that Unconditional Language Universal
essentials = cloze_text(text_POS_tagged, "NNP", "NNPS", "NN", "NNS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ")
# However, this amounts still to quite some words. Because I didn't want to read so much,
# I also tried a version with stripping the text down to only proper nouns. It's fun 😁
noun_speak = cloze_text(text_POS_tagged, "NNP", "NNPS")

# uncomment to call the function to make a noun-only website
#create_speech_for_web(noun_speak, "word.html") # <- I think this one is fun :)

################################ CHOOSE YOUR OWN ################################

# enter a president's speech file name to create a small website with the essential words
# here are the (many) choices
# '1945-Truman.txt'
# '1946-Truman.txt'
# '1947-Truman.txt'
# '1948-Truman.txt'
# '1949-Truman.txt'
# '1950-Truman.txt'
# '1951-Truman.txt'
# '1953-Eisenhower.txt'
# '1954-Eisenhower.txt'
# '1955-Eisenhower.txt'
# '1956-Eisenhower.txt'
# '1957-Eisenhower.txt'
# '1958-Eisenhower.txt'
# '1959-Eisenhower.txt'
# '1960-Eisenhower.txt'
# '1961-Kennedy.txt'
# '1962-Kennedy.txt'
# '1963-Johnson.txt'
# '1963-Kennedy.txt'
# '1964-Johnson.txt'
# '1965-Johnson-1.txt'
# '1965-Johnson-2.txt'
# '1966-Johnson.txt'
# '1967-Johnson.txt'
# '1968-Johnson.txt'
# '1969-Johnson.txt'
# '1970-Nixon.txt'
# '1971-Nixon.txt'
# '1972-Nixon.txt'
# '1973-Nixon.txt'
# '1974-Nixon.txt'
# '1975-Ford.txt'
# '1976-Ford.txt'
# '1977-Ford.txt'
# '1978-Carter.txt'
# '1979-Carter.txt'
# '1980-Carter.txt'
# '1981-Reagan.txt'
# '1982-Reagan.txt'
# '1983-Reagan.txt'
# '1984-Reagan.txt'
# '1985-Reagan.txt'
# '1986-Reagan.txt'
# '1987-Reagan.txt'
# '1988-Reagan.txt'
# '1989-Bush.txt'
# '1990-Bush.txt'
# '1991-Bush-1.txt'
# '1991-Bush-2.txt'
# '1992-Bush.txt'
# '1993-Clinton.txt'
# '1994-Clinton.txt'
# '1995-Clinton.txt'
# '1996-Clinton.txt'
# '1997-Clinton.txt'
# '1998-Clinton.txt'
# '1999-Clinton.txt'
# '2000-Clinton.txt'
# '2001-GWBush-1.txt'
# '2001-GWBush-2.txt'
# '2002-GWBush.txt'
# '2003-GWBush.txt'
# '2004-GWBush.txt'
# '2005-GWBush.txt'
# '2006-GWBush.txt'

get_real('1962-Kennedy.txt')
