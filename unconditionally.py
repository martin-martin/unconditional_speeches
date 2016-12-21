
# coding: utf-8

# # Unconditionally Universal Speeches
#
# People speak a lot.
#
# For example: politicians when they hold a speech.
#
# Playing with the linguistic concept of Language Universals, I wrote some code that weeds through words, and allows the reader a maybe pensive, maybe revealing, but most probably just ten-seconds-fun-amusing, digest of some past US president's mumblings.
#
# Hope you'll enjoy : )
#
# And choose your words wisely 😜

# ## Unconditional Language Universals
#
# Linguistics defines two types of **Language Universals** for natural human languages: _unconditional_ ones and _conditional_ ones.
#
# And actually their difference is smartly explained in the derivation and semantics of the two words. (Oh, those linguists... 😉 )
#
# While _conditional_ Language Universals rely on some conditions to hold up (e.g. "if a language has _inflection_, it usually also has _derivation_"), **unconditional Language Universals** are true without further prerequisites.
#
# ### Here I will focus on one of the unconditional LUs, namely:
#
# > Every language has nouns and verbs.
#
# Easy.
#
# ---
#
# >**DISCLAIMER:** THE REST OF THESE MUSINGS FROM HERE DOWNWARDS ARE NOTHING BUT SELF-MADE MIND-GAMES FOR FUN AND PROGRAMMING PRACTICE.
# Just keep that in mind.
#
# So, nouns and verbs are the **essential** Parts-of-speech in every language.
#
# I wanted to see what happens to my text understanding when stripping a written text from all but those essential POS.
#
# Ready for some code? Here we go!

# In[85]:

import nltk
from nltk.corpus import state_union
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from pprint import pprint


# Next I choose one speech for analysis (you can take a different one. there are many other possibilities!)
#
# Just choose from the wealth of the corpus.
# You can check which speeches exists with:
#
# >`state_union.fileids()`

# In[86]:

kennedy2_full = state_union.raw("1962-Kennedy.txt")


# Time for some functions. I hope they are well explained in docstrings and descriptive naming. Feedback welcome.

# In[87]:

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


# In[88]:

text_POS_tagged = tag_POS(tokenize_text(kennedy2_full))


# In[89]:

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


# In[90]:

essentials = cloze_text(text_POS_tagged, "NNP", "NNPS", "NN", "NNS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ")


# When using all of the different versions of nouns and verbs that have their [POS in NLTK](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html), this amounts to quite some words. Because I didn't want to read so much, I also tried a version with stripping the text down to **only proper nouns**. It's fun 😁

# In[91]:

noun_speak = cloze_text(text_POS_tagged, "NNP", "NNPS")


# In[92]:

def create_speech(clozed_text):
    """creates a string from a nested list"""
    essentialized_text = ""
    for s in clozed_text:
        sentence = " ".join(s)
        essentialized_text += sentence + "\n"
    return essentialized_text


# So below follows the "proper-noun version" of Kennedy's State Union Speech. Each dot represents a deleted word.
#
# Of course all those words were utterly unimportant. Or... are they?
#
# Hm, let's make a little experiment:
# > I think you are really an extremely nice person! That is because
#
# _(lots and lots of words, let's continue this in "essentials")_
#
# > . are . . . . . . .
#
# Ah, yep! I see why someone would care for adjectives! 😉
#
# Anyways, uncomment to read the beginning of the speech after rigorous cloze deletion.

# In[93]:

#print(create_speech(noun_speak)[:3000])


# Okay, so that's fun for me. Let's get it into a format that is easier to digest!
#
# For that aim I'll rewrite the functions to create a simple HTML page for viewing and joyful reading and contemplation.

# In[94]:

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
			background-image: url("https://cdn.pixabay.com/photo/2015/09/22/12/18/paper-951489_960_720.jpg");
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


# In[95]:

# calling the function to make some websites
#create_speech_for_web(essentials, "uncondLU-ized_speech.html")
#create_speech_for_web(noun_speak, "word.html") # <- I think this one is fun :)


# In[96]:

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


# ---
#
# After wrapping and adapting the code some more, it can output a HTML page (with some fun font and background 😜 )
#
# # Tldr;: just do the following for VISUAL RESULTS:
#
# ### Choose your favorite (or least favorite) president, run the code below on his speech, and see what he was really* saying!
#
# >*_"really"_ = unconditionally-language-universally

# In[97]:

get_real('1962-Kennedy.txt')

