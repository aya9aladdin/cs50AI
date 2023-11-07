import nltk
import sys
import os
import string
import math
nltk.download('stopwords')
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    # get the seperator of the operating system
    sep = os.sep
    
    # path to the corpus directory
    path = os.path.join(directory + sep)
    txt_files = os.listdir(path)

    mapping_dict = {}

    for filename in txt_files:
        with open(path+filename, 'r') as f:
            mapping_dict[filename] = f.read()
    
    return mapping_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.tokenize.word_tokenize(document)
    tokenizations = []
    
    for w in words:
        if w not in string.punctuation and w not in nltk.corpus.stopwords.words("english"):
            tokenizations.append(w.lower())
            
    return tokenizations


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # used in idf calculations
    totaldocs = len(documents.keys())
    total_words = set()
    
    # remove words duplications in all documents
    for words in documents.values():
       total_words.update(set(words))
        
    words_idfs = {}
    for word in total_words:
         appears = 0
         for doc in documents.values():
             if word in doc:
                 appears = appears + 1
         words_idfs[word] = math.log10(totaldocs/appears)

    return words_idfs




def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    
    
    idf_tf = dict.fromkeys(files.keys(), 0)
    for q in query:
        for f in files:
            try:
                idf_tf[f] = idf_tf[f] + (idfs[q] * files[f].count(q))
            except:
                pass
     
        
    # sorting files according to td-idf value
    sorted_doc = sorted(idf_tf, reverse=True, key=idf_tf.get)

    return sorted_doc[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    idf_tf = dict.fromkeys(sentences.keys(), 0)

    for q in query:
        for s in sentences:
            
            try:
                idf_tf[s] = idf_tf[s] + (idfs[q] * sentences[s].count(q))
            except:
                pass
    
    
    # sorting sentences according to td-idf value
    sorted_sentences = sorted(idf_tf, reverse=True, key=idf_tf.get)

    return sorted_sentences[:n]

if __name__ == "__main__":
    main()
