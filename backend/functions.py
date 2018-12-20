import re
import math
import string
import codecs
import os
import nltk
import json
import pymongo
import operator
from nltk.stem import WordNetLemmatizer
from bs4 import BeautifulSoup
from pymongo import MongoClient, InsertOne, DeleteMany


# Opens a file based on the docIDs from the bookkeeping.json
# and returns a list of files in the structure
# (./WEBPAGES_RAW/"##/##", "##/##")
# ----------------------------------------------------
def open_read_file() -> (str,str):
    """
    Opens a file based on the docIDs from the bookkeeping.json
    and returns a list of files and it designated docID
    """
    # bookkeeping.json contains all the folder numbers and docId
    path = "./WEBPAGES_RAW/bookkeeping.json"

    # sub_path is needed to concatenate with the folder number and docID
    sub_path = "./WEBPAGES_RAW/"

    document_list = list()

    my_file = open(path, 'r')
    json_data = json.load(my_file)

    # Looping through the bookkeeping.json
    for key, value in json_data.items():
        # concatenating the sub_path with the folder number and docID
        sub_path = sub_path + key

        document_list.append((sub_path, key))

        # This is needed to reset the sub_path variable
        sub_path = "./WEBPAGES_RAW/"

    print("Done creating document list")

    return document_list


# Receives a file and tokenize the content of the file.
# This function also removes stopwords and numbers(digits)
#  and lowercases each token
# It returns a list of tokens
# ----------------------------------------------------
def tokenize_and_clean(file:str) -> [str]:
    """
    Receives a file and tokenize the content of the file.
    This function also removes stopwords and lowercases each token
    It returns a list of tokens
    """
    # with codecs.open(sub_path, 'r') as sub_file:
    sub_file = open(file, 'r', encoding="utf8")

    # Get text from html file. It will only get text and not html tags
    soup = BeautifulSoup(sub_file, "html.parser")
    text = soup.get_text()

    # Keeps all alpha characters
    alpha_tokens = re.findall(r"[a-zA-Z]+", text)

    # Create a string based on the alphanumberic words
    joined_tokens = ' '.join(alpha_tokens)

    # Turn the text into tokens
    tokens = nltk.word_tokenize(joined_tokens)

    # Lowercase each token
    index = 0
    for token in tokens:
        tokens[index] = token.lower()
        index += 1

    return tokens

# Receives a string and tokenize the content of the file.
# This function also removes stopwords and lowercases each token
# It returns a list of tokens
# If the string recieved is None
# ----------------------------------------------------
def tokenize_string(meta_data: str) -> [str]:
    # Keeps all alphanumberic characters
    if meta_data == None:
        return []

    # Keeps all alpha characters
    alpha_tokens = re.findall(r"[a-zA-Z]+", meta_data)

    # Create a string based on the alphanumberic words
    joined_tokens = ' '.join(alpha_tokens)

    # Turn the text into tokens
    tokens = nltk.word_tokenize(joined_tokens)

    # Lowercase each token
    index = 0
    for token in tokens:
        tokens[index] = token.lower()
        index += 1

    return tokens


# Receives a file and tokenize the content of the file.
# This function also removes stopwords and lowercases each token
# It returns a dictionary with
# Key: docID
# Value: list of meta tokens
# ----------------------------------------------------
def get_metadata(document_list:list) -> dict:
    # initializes the dictionary
    meta_data_dict = dict()

    for location_info in document_list:
        # initializes list which will be inserted into dictionary
        meta_list = list()
        path_to_file = location_info[0]
        sub_file = open(path_to_file, encoding="utf8")
        soup = BeautifulSoup(sub_file, "html.parser")
        if soup.title is None:
            meta_data_dict[location_info[1]] = meta_list
            continue
        else:
            # adds the title information to the list
            title = tokenize_string(soup.title.string)
            meta_list = meta_list + title

        meta_data_dict[location_info[1]] = meta_list

    print('Done creating meta deta dictionary')

    return meta_data_dict


# This function creates a dictionary. Each Doc ID will have its designated lemmatize tokens
# Key - doc_id
# Value - lemmatize tokens
# ----------------------------------------------------
def create_lemma_dictionary(document_list:[str]) -> dict:
    """
    This function creates a dictionary. Each Doc ID will have its designated lemmatize tokens
    - Key: doc_id
    - Value: lemmatize tokens
    """
    lemma_dictionary = dict()
    for location_info in document_list:
        path_to_file = location_info[0]
        tokens = tokenize_and_clean(path_to_file)
        lemmatize_tokens = lemmatizer(tokens)
        lemma_dictionary[location_info[1]] = lemmatize_tokens

    print("Done creating lemma dictionary")
    return lemma_dictionary


# This function creates a set that contains all tokens from all documents
# ----------------------------------------------------
def create_all_tokens_set(lemma_dictionary:dict) -> set:
    """
    This function creates a set that contains all tokens from all documents
    """
    all_tokens_set = set()

    for doc_id, lemmatize_tokens in lemma_dictionary.items():
        for token in lemmatize_tokens:
            all_tokens_set.add(token)

    print("Done creating all tokens set\n")

    return all_tokens_set


# Apply linguistic methods to the tokens of each document
# For now we are using a lemmatizer
# ----------------------------------------------------
def lemmatizer(tokens:[str]) -> None:
    """
    Apply linguistic methods to the tokens of each document
    For now we are using a lemmatizer
    """
    # This variable will contain all the possible tokens from all documents
    global all_tokens_set
    all_tokens_set = set()

    # Initializing a lemmatizer.
    lemmatizer = WordNetLemmatizer()

    # List to store lemmatize tokens
    lemma_tokens = list()

    # Gets Part of Speech (POS) tags for each token
    tp_pair = nltk.pos_tag(tokens)

    for t in range(len(tp_pair)):
        word = tp_pair[t][0].lower()
        pos_tag = tp_pair[t][1]

        # Check for verbs
        if pos_tag[0] == "V":
            token = lemmatizer.lemmatize(word, "v")
            lemma_tokens.append(token)

        # Check for adjective
        elif pos_tag[0] == "J":
            token = lemmatizer.lemmatize(word, "a")
            lemma_tokens.append(token)

        # Check for Adverbs
        elif pos_tag[0] == "R":
            token = lemmatizer.lemmatize(word, "r")
            lemma_tokens.append(token)

        # Default is Nouns
        else:
            token = lemmatizer.lemmatize(word)
            lemma_tokens.append(token)

        all_tokens_set.add(token)

    return lemma_tokens


# Measures how frequently a term occurs in a document
# ----------------------------------------------------
def term_frequency(term:str, content_list:[str]) -> int:
    """
    Measures how frequently a term occurs in a document
    Parameters:
    - term: This is a word that we are looking for
    - content_list: this is a list containing all the words found in the document
    """
    tf = content_list.count(term) / len(content_list)
    return tf


# measures how common a word is among all documents in bloblist.
# The more common a word is, the lower its idf.
# The least common the word appears in the corpus the higher its idf value.
# Add 1 to the divisor to prevent division by zero.
# ----------------------------------------------------
def inverse_document_frequency(term:str, amount_of_documents:int, postings_list_length: int) -> float:
    """
    Measures how important a term is
    The more common a word is, the lower its idf.
    The least common a word appears in the corpus the higher its idf value.
    Parameters:
    - term: This is a word that we are looking for
    - amount_of_documents: Amount of total documents
    - postings_list_length: this is a integer representing the amount of docIDs where the token appears
    """
    idf = 1 + (math.log(postings_list_length) / amount_of_documents)
    return idf


# computes the TF-IDF score. It's the product of tf and idf.
# tfidf says how important that word is to that document with respect to the corpus
# IDF(t) = log_e(Total number of documents / Number of documents with term t in it).
# Good Example Here - https://www.quora.com/How-does-TfidfVectorizer-work-in-laymans-terms
# ----------------------------------------------------
def term_frequency_idf(term:str, tokens:[str], postings_list_length:int, amount_of_documents:int) -> int:
    """
    computes the TF-IDF score. It's the product of tf and idf.
    Parameters:
    - term: This is a word that we are looking for
    - postings_list_length: this is a integer representing the amount of docIDs where the token appears
    - tokens: this is a list containing all the words found in the document
    - amount_of_documents: Amount of total documents
    """
    tf_idf = term_frequency(term, tokens) * inverse_document_frequency(term, amount_of_documents, postings_list_length)
    return tf_idf


# Calls open_read_file()
# ------------------------
def create_document_list() -> list:
    document_list = open_read_file()
    return document_list

# This function creates the inverted_index that has been discussed in class
# The inverted_index is a dictionary with:
# Key - a token
# Value - a list of docID where that token appears
# ----------------------------------------------------
def create_inverted_index(lemma_dictionary:dict, all_tokens_set:set) -> dict:
    """
    This function creates the inverted_index that has been discussed in class
    The inverted_index is a dictionary with:
    - Key: a token
    - Value: a list of docID where that token appears
    """
    # This represents the inverted_index
    global inverted_index
    inverted_index = dict()

    # This will a list containing all the docIDs
    postings_list = list()
    # amount_of_documents = len(lemma_dictionary)

    # Opens one document and creates lemmatize_tokens for that doc
    for token in all_tokens_set:
        for doc_id, lemmatize_tokens in lemma_dictionary.items():
            if token in lemmatize_tokens:
                postings_list.append(doc_id)
                inverted_index[token] = postings_list
        print("Token\t{}".format(token))

         # We need to reset the list so it can append new docIDs with the a new token
        postings_list = list()

    print("Done creating inverted index ")

    return inverted_index


# This functions create inverted index from the project description
# Key: token
# Value: is a dictionary called dictionary_info_dict
#
# dictionary_info_dict contains
# Key: doc_id
# Value: Tf-Idf score.
# ----------------------------------------------------
def create_complete_inverted_index(lemma_dictionary:dict, inverted_index:dict, meta_data_dict:dict) -> dict:
    """
    This functions create inverted index from the project description
    - Key: token
    - Value: is a dictionary called dictionary_info_dict
    dictionary_info_dict contains
    - Key: doc_id
    - Value: Tf-Idf score
    """
    complete_inverted_index = dict()
    tfidf_additional = .0001

    for token, postings_list in inverted_index.items():
        # We put the dictionary_info_dict here so it resets on every token
        dictionary_info_dict = dict()
        position_dict = dict()

        for doc_id in postings_list:
            lemmatize_tokens = lemma_dictionary[doc_id]
            tfidf = term_frequency_idf(token, lemmatize_tokens, len(postings_list), len(lemma_dictionary))
            dictionary_info_dict[doc_id] = tfidf

            # Acceses the meta_data_list for the specific doc_id
            meta_data_list = meta_data_dict[doc_id]

            # Checks that the meta_data_list is not empty and that token is within this list
            if (meta_data_list != None) and (len(meta_data_list) != 0) and (token in meta_data_list):
                # increases the tfidf based on a weight
                dictionary_info_dict[doc_id] += tfidf_additional

            # Creating position dictionary, shows index in which token is found
            if token in lemmatize_tokens:
                token_position_list = [index for index, word in enumerate(lemmatize_tokens) if word==token]
                position_dict[doc_id] = token_position_list

        complete_inverted_index[token] = dictionary_info_dict, position_dict
        print("Token\t{}".format(token))

    print("Done creating complete inverted index \n")

    return complete_inverted_index


# This functions create the inserts the complete_inverted_index into the database
# ----------------------------------------------------
def insert_complete_inverted_index_to_database(complete_inverted_index:dict, lemma_dictionary: dict) -> None:
    """
    This functions create the inserts the complete_inverted_index into the database
    """

    data_list = [DeleteMany({})]
    for token, info_tuple in complete_inverted_index.items():
        doc_id_and_tfidf = info_tuple[0]
        position_dict = info_tuple[1]
        post_data = {
            "token": token,
            "doc_id_and_tfidf": doc_id_and_tfidf,
            "position_dict": position_dict
        }
        # data_list.append(InsertOne(post_data))
        InsertOne(post_data)

    # Inserts lemma_dictionary into the collection
    lemma_post_data = {
        "token": "lemma_dict",
        "lemma_dictionary" : lemma_dictionary
    }

    # data_list.append(InsertOne(lemma_post_data))
    InsertOne(lemma_post_data)

    print("Ready to bulk write into collection ")
    # ics_collection.bulk_write(data_list)

    print("Inserted info into collection \n")


# This functions create the database content.
# ----------------------------------------------------
def create_database_content(document_list: list) -> None:
    """
    This functions create the database content.
    """
    lemma_dictionary = create_lemma_dictionary(document_list)

    meta_data_dict = get_metadata(document_list)
    all_tokens_set = create_all_tokens_set(lemma_dictionary)

    inverted_index = create_inverted_index(lemma_dictionary, all_tokens_set)

    complete_inverted_index = create_complete_inverted_index(lemma_dictionary, inverted_index, meta_data_dict)

    insert_complete_inverted_index_to_database(complete_inverted_index, lemma_dictionary)

    get_search_results_and_display(lemma_dictionary)


# This function checks if the collection in the database
# holds the desired information
# If it does it asks the user for a query
# If it does not it creates the inverted index then asks
# the user for their query
# ----------------------------------------------------
def check_database_content() -> bool:
    """
    This function checks if the database has content in it. If it has content, then it
    will let the user make a query. If it does not, then it will
    create database content for it.
    """

    initalize_mongodb_client()

    document_list = create_document_list()

    if ics_collection.find_one({'token': 'data'}) != None:
        # If there is content in the collection, then it will display the results
        result = ics_collection.find_one({ "token":"lemma_dict"})
        lemma_dictionary = result['lemma_dictionary']
        get_search_results_and_display(lemma_dictionary)

    else:
        # If there is no content in the colection, then it will create content in the collection
        print(" There is no content in collection... creating content now ")
        create_database_content(document_list)


# This function asks the user for their query until
# they decide to end the program
# ----------------------------------------------------
def get_search_results_and_display(lemma_dictionary:dict) -> None:
    is_database = True
    intersection_and_matching = dict()

    while is_database:
        print("To end the program enter: 'end run'")
        query = ask_for_query()

        if query == ['end', 'run']:
            is_database = False
        else:
            search_results = search_it(query)
            if len(search_results) != 0:
                intersection_dict = create_intersection_dict(search_results)
                intersection_and_matching = calculate_exact_match(lemma_dictionary, intersection_dict, query)
                display_result_query(intersection_and_matching)


# This function asks the user to search for something
# ----------------------------------------------------
def ask_for_query() -> list:
    """
    This function asks the user to search for something
    """
    the_search = input("What are you searching for?: ").strip().lower().split()
    return the_search


# This function initializes a Mongodb client
# ----------------------------------------------------
def initalize_mongodb_client():
    """
    This function initializes a Mongodb client
    """
    print("Creating client... ")
    # Assigns localhost:27017 to be the host for the Mongodb client
    local_db_client = pymongo.MongoClient("mongodb://localhost:27017/")

    # creates search database
    print("Creating database")
    db = local_db_client.search_db

    # The database that will be used to search
    # It was made global because the search function is seperate see search_it()
    global ics_collection
    ics_collection = db.ics_collection

    print("Creating collection  ics_collection:: ", ics_collection)



# This function uses the globally creates 'posts' database to search for the search term
# ----------------------------------------------------
def search_it(search_terms: list) -> [list]:
    """
    This function uses the globally created 'ics_collection' to search for the search term
    """
    print("Searching... \n")
    # number of results you want to see

    result_list = list()

    # Returns one (find_one) item where token is found
    for search_term in search_terms:
        result = ics_collection.find_one({'token': search_term})

        if result == None:
            print("Word not found in the UCI ICS Domain\n")
        else:
            result_list.append(sort_dictionary(result['doc_id_and_tfidf']))
            result_list.append(result['position_dict'])

    return result_list


# This function creates an intersection dictionary where
# Key: doc_id
# Value: tfidf (cumulative tfidf)
# --------------------------------------------------------------
def create_intersection_dict(search_results: [list]) -> dict:
    doc_id_list = list()
    intersection_dict = dict()

    for result in search_results:
        if type(result) == list:
            doc_set = set()
            for doc_id, tfidf in result:
                doc_set.add(doc_id)
            doc_id_list.append(doc_set)

    intersection_set = set.intersection(*doc_id_list)

    for result in search_results:
        if type(result) == list:
            for doc_id, tfidf in result:
                if doc_id in intersection_set and doc_id in intersection_dict.keys():
                    intersection_dict[doc_id] += tfidf
                elif doc_id in intersection_set:
                    intersection_dict[doc_id] = tfidf

    return intersection_dict


# This function checks if the exact query string is within the doc id and updates the tfidf
# Key: doc_id
# Value: tfidf (cumulative tfidf)
# --------------------------------------------------------------
def calculate_exact_match(lemma_dictionary:dict, intersection_dict:dict, query:list) -> dict:
    query_string = ' '.join(query)
    combo_counter = 0
    tfidf_additional = .0001 # Change to whatever we want

    for doc_id, tfidf in intersection_dict.items():
        token_string = ' '.join(lemma_dictionary[doc_id])
        combo_counter = token_string.count(query_string)
        if combo_counter > 0:
            intersection_dict[doc_id] += combo_counter * tfidf_additional
        combo_counter = 0

    return intersection_dict


# This function uses result list [list] and displays the results
# --------------------------------------------------------------
def display_result_query(result_dict: dict) -> None:

    desired_result_number = 10

    print("Total number of search results: {}".format(len(result_dict)))
    print("Search result:\n {} \n".format(result_dict))
    print("Showing up to {} results.".format(desired_result_number))

    path = "./WEBPAGES_RAW/bookkeeping.json"
    my_file = open(path, 'r')
    json_data = json.load(my_file)

    # Starts at 1 to give exact desired_result_number
    index = 1

    for doc_id, tfidf in result_dict.items():
        if index <= desired_result_number:
            result_url = json_data.get(doc_id)
            print(index, "." , "{} \n".format(result_url))
            index += 1


# This function sorted the dictionary by value
# ----------------------------------------------------
def sort_dictionary(result_dictionary:dict) -> list:
    """
    This function sorted the dictionary by value
    """
    sorted_tuple_list = sorted(result_dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_tuple_list


# This function runs the program
# ----------------------------------------------------
def run_program() -> None:
    """
    This function runs the program
    """
    check_database_content()
