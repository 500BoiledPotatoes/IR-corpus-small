import getopt
import json
import math
import os
import re
import sys

from files import porter

containNum = {}
path = []
def check_if_dir(file_path):
    '''
    This method is used to iterate over all files in a nested folder
    '''
    temp_list = os.listdir(file_path)
    # Put file name from file_path in temp_list
    for temp_list_each in temp_list:
        if os.path.isfile(file_path + '/' + temp_list_each):
            # Determines whether the file name is a file
            temp_path = file_path + '/' + temp_list_each
            # Splice file path
            if temp_list_each == ".DS_Store":
                # DS_Store files that don't need to be processed
                continue
            else:
                path.append(temp_path)
                # Add the file path to the list
        else:
            check_if_dir(file_path + '/' + temp_list_each)  # loop traversal
    return path


def read(input_str):
    path = "documents"  # Destination folder directory
    files = check_if_dir(path)  # Get the names of all the files in the folder
    s = {}
    collections = {}
    if (os.path.isfile("index.txt")) is False:
        '''
        When the program is run for the first time, 
        an appropriate index is created so that IR can use the BM25 method
        '''
        for file in files:  # Traverse file paths
            if not os.path.isdir(file):
                # Determine if it's a folder, open only if it's not
                f = open(file, encoding='UTF-8')  # Open file
                iter_f = iter(f)  # Creating Iterators
                str = ""
                for line in iter_f:
                    # Traversing a file, line by line, reading text
                    str = str + line
                s[file] = str
                # The text of each file is stored in the dictionary
                '''
                Dictionary keys: File path
                Dictionary values: File text
                '''
        for str in s.keys():
            did = str.split("/")
            # Fetch document name
            b = re.split(r'\W+', s[str])
            # Processing text with regular expressions and removing punctuation
            c = [word.lower() for word in b if len(word) > 0]
            # Removing spaces and making split strings lowercase
            collections[did[len(did) - 1]] = remove_stopword(c)
            # The remove_stopword method is called to perform further processing on the punctuated string:
            # 1) remove the stopword. 2) stemming 3) Calculate the frequency of occurrence of each term
            # Store the processed text in the dictionary
            '''
            Set up dictionary to store document frequencies:
            key: Document id
            value is a dictionary:
                key: Term
                value: Frequency within that document
            '''
        with open('index.txt', 'w', encoding='UTF-8') as f:
            f.write(json.dumps(collections, ensure_ascii=False))
            '''
            Store the dictionary in a txt file 
            so that the next calculation of BM25 can directly use the processed dictionary in the txt file,
            reducing the time complexity
            '''
    else:
        f = open('index.txt', encoding='UTF-8')
        '''
        When the program is run a second time, 
        if the index file exists, 
        it will use the stored dictionary directly
        '''
        for line in f:
            collections = json.loads(line)
        for frequency in collections.values():
            for term in frequency.keys():
                if term not in containNum:
                    # If this is the first occurrence of the word,
                    # the number of occurrences will be equal to 1
                    containNum[term] = 1
                elif term in containNum:
                    # For each subsequent occurrence of this word,
                    # add 1 to the number of occurrences
                    containNum[term] = containNum[term] + 1
        '''
        Set up dictionary to store the total number of documents in the collection that contain term:
        key: Term
        value: Number
        '''
    if input_str == "automatic":
        # Automatic mode
        calculate_BM25(read_queries_auto(), collections)
        # Calculate BM25
    elif input_str == "interactive":
        # Interaction mode
        while True:
            queries = read_queries_interactive()
            if queries == "QUIT":
                break
            calculate_BM25_interactive(queries, collections)
            # Calculate BM25

def remove_stopword(txt):
    stemmer = porter.PorterStemmer()
    frequency = {}
    stopwords = []
    f = open('files/stopwords.txt', encoding='UTF-8')
    for line in f:
        stopwords.append(line.rstrip())
        # Reading stop words
    for term in txt:
        if term not in stopwords:
            term = stemmer.stem(term)
            # Stemming
            if term not in frequency:
                frequency[term] = 1
                # If this is the first occurrence of the word in the current document,
                # the word frequency will be equal to 1
                if term not in containNum:
                    # If this is the first occurrence of the word,
                    # the number of occurrences will be equal to 1
                    containNum[term] = 1
                elif term in containNum:
                    # For each subsequent occurrence of this word,
                    # add 1 to the number of occurrences
                    containNum[term] = containNum[term] + 1
            else:
                frequency[term] = frequency[term] + 1
                # For each subsequent occurrence of the word in the current document,
                # add 1 to the number of occurrences
    return frequency

def queries_manage(txt):
    # This method involves the removal of stop words and stemming of queries
    stemmer = porter.PorterStemmer()
    words = []
    stopwords = []
    f = open('files/stopwords.txt', encoding='UTF-8')
    for line in f:
        stopwords.append(line.rstrip())
    for term in txt:
        if term not in stopwords:
            term = stemmer.stem(term)
            words.append(term)
    return words


def calculate_BM25(queries, dict):
    dlength = len(dict)
    # Number of documents
    total_len = 0
    result = {}
    queries_bm25 = {}
    k = 1
    b = 0.75
    for n in dict.keys():
        total_len = total_len + len(dict[n])
        # Calculate the total length of all documents
    avg_len = total_len / len(dict)
    # Calculate the average length of each document in the collection
    for i in queries.keys():
        # Iterate over the id of queries
        doc_bm25 = {}
        for j in dict.keys():
            # Iterate over the ids of all documents
            bm25 = 0
            for term in queries[i]:
                # Iterate over the terms of each query
                if term in dict[j]:
                    # If the term is in the current document
                    bm25 = bm25 + (((dict[j][term] * (1 + k)) / (
                            dict[j][term] + k * ((1 - b) + (b * len(dict[j]) / avg_len)))) * math.log2(
                        ((dlength - containNum[term] + 0.5) / (containNum[term] + 0.5))))
                    '''
                    bm25 = bm25 + fij * (1 + k) / fij + k * ((1-b) + b * len(dj) / avg_doclen) * ((N - ni + 0.5) / (ni + 0.5))
                    fij (dict[j][term]): frequency of term in doc
                    k, b: constants
                    len(dj) (len(dict[j])): length of dj (the number of terms in doc)
                    avg_doclen (avg_len): the average length of a document in the collection
                    N (dlength): total number of documents in the collection
                    n (containNum[term]): total number of documents in the collection that contain term
                    '''
            doc_bm25[j] = bm25
            '''
            Set up dictionary to store bm25:
            key: Document id
            value: Bm25
            '''
        result[i] = doc_bm25
        '''
        Set up dictionary to store bm25 of each query:
        key: Query id
        value is a dictionary:
            key: Document id
            value: Bm25
        '''
    for i, j in zip(result.values(), queries):
        query = sorted(i.items(), key=lambda x: x[1], reverse=True)
        # Sort the bm25 for each doc from largest to smallest
        queries_bm25[j] = query
        # Store sorted bm25 for each document queried
    with open('output.txt', 'w') as f:
        for i in queries_bm25.values():
            max_value = i[0][1]
            # Since the numerator cannot be 0 when normalising,
            # it is divided into the case where bm25 is 0 and the case where it is not 0
            for j in range(0, 15):
                if max_value != 0:
                    # The output file for the automatic runs should have 4 columns:
                    # Query ID, Document ID, Rank, Similarity Score.
                    f.write(
                        str(list(queries_bm25.keys())[list(queries_bm25.values()).index(i)]) + " " + str(
                            i[j][0]) + " " + str(
                            j + 1) + " " + str(round(i[j][1] / max_value, 4)) + " " + "\n")
                else:
                    f.write(
                        str(list(queries_bm25.keys())[list(queries_bm25.values()).index(i)]) + " " + str(
                            i[j][0]) + " " + str(
                            j + 1) + " " + str(0) + " " + "\n")

def calculate_BM25_interactive(queries, dict):
    dlength = len(dict)
    # Number of documents
    total_len = 0
    result = {}
    queries_bm25 = {}
    k = 1
    b = 0.75
    for n in dict.keys():
        total_len = total_len + len(dict[n])
        # Calculate the total length of all documents
    avg_len = total_len / len(dict)
    # Calculate the average length of each document in the collection
    for i in queries.keys():
        # Iterate over the id of queries
        doc_bm25 = {}
        for j in dict.keys():
            # Iterate over the ids of all documents
            bm25 = 0
            for term in queries[i]:
                # Iterate over the terms of each query
                if term in dict[j]:
                    # If the term is in the current document
                    bm25 = bm25 + (((dict[j][term] * (1 + k)) / (
                            dict[j][term] + k * ((1 - b) + (b * len(dict[j]) / avg_len)))) * math.log2(
                        ((dlength - containNum[term] + 0.5) / (containNum[term] + 0.5))))
                    '''
                    bm25 = bm25 + fij * (1 + k) / fij + k * ((1-b) + b * len(dj) / avg_doclen) * ((N - ni + 0.5) / (ni + 0.5))
                    fij (dict[j][term]): frequency of term in doc
                    k, b: constants
                    len(dj) (len(dict[j])): length of dj (the number of terms in doc)
                    avg_doclen (avg_len): the average length of a document in the collection
                    N (dlength): total number of documents in the collection
                    n (containNum[term]): total number of documents in the collection that contain term
                    '''
            doc_bm25[j] = bm25
            '''
            Set up dictionary to store bm25:
            key: Document id
            value: Bm25
            '''
        result[i] = doc_bm25
        '''
        Set up dictionary to store bm25 of each query:
        key: Query id
        value is a dictionary:
            key: Document id
            value: Bm25
        '''
    for i, j in zip(result.values(), queries):
        query = sorted(i.items(), key=lambda x: x[1], reverse=True)
        # Sort the bm25 for each doc from largest to smallest
        queries_bm25[j] = query
        # Store sorted bm25 for each document queried
    print("Results for query: ")
    for i in queries_bm25.values():
        max_value = i[0][1]
        # Since the numerator cannot be 0 when normalising,
        # it is divided into the case where bm25 is 0 and the case where it is not 0
        for j in range(0, 15):
            if max_value != 0:
                # The output for the interactive runs should have 4 columns:
                # Query ID, Document ID, Rank, Similarity Score.
                print(
                        str(list(queries_bm25.keys())[list(queries_bm25.values()).index(i)]) + " " + str(
                            i[j][0]) + " " + str(
                            j + 1) + " " + str(round(i[j][1] / max_value, 4)) + " " + "\n")
            else:
                print(
                        str(list(queries_bm25.keys())[list(queries_bm25.values()).index(i)]) + " " + str(
                            i[j][0]) + " " + str(
                            j + 1) + " " + str(0) + " " + "\n")


def read_queries_auto():
    # This method is used to read and process the query document
    queries = {}
    f = open('files/queries.txt', encoding='gbk')
    for line in f:
        str = ""
        str = str + line
        b = re.split(r'\W+', str)
        c = [word.lower() for word in b if len(word) > 0]
        queries[c[0]] = queries_manage(c[1:])
    return queries


def read_queries_interactive():
    # This method is used to read and process the query entered by the user
    queries = {}
    str = input("Enter query: ")
    if str == "QUIT":
        return str
    else:
        b = re.split(r'\W+', str)
        c = [word.lower() for word in b if len(word) > 0]
        queries[len(queries) + 1] = queries_manage(c[1:])
        return queries


def main(argv):
    # This method is used to read and parse the commands entered by the user in the terminal
    input_str = ""
    try:
        opts, args = getopt.getopt(argv[1:], "m:")
        # Get the command after m
    except getopt.GetoptError as e:
        print(e.msg)
        sys.exit(2)
        # Print command input error
    for opt, arg in opts:
        if opt in "-m":
            input_str = arg
    if input_str == "interactive":
        # Incoming interactive mode
        read(input_str)
    elif input_str == "automatic":
        # Incoming automatic mode
        read(input_str)

if __name__ == "__main__":
    main(sys.argv)
