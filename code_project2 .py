class Node:
    def __init__(self, value = None, next = None):
        self.value = value
        self.next = next


class LinkedList:

    def __init__(self, index=0, mode="simple"):
        self.start_node = None # Head pointer
        self.end_node = None # Tail pointer
        # Additional attributes
        self.index = index
        self.mode = "simple"

    # Method to traverse a created linked list
    def traverse_list(self):
        traversal = []
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            # Start traversal from head, and go on till you reach None
            while n is not None:
                traversal.append(n.value)
                n = n.next
            return traversal

    # Method to insert elements in the linked list
    def insert_at_end(self, value):
        # determine data type of the value
        if 'list' in str(type(value)):
            self.mode = "list"

        # Initialze a linked list element of type "Node"
        new_node = Node(value)
        n = self.start_node # Head pointer

        # If linked list is empty, insert element at head
        if self.start_node is None:
            self.start_node = new_node
            self.end_node = new_node
            return "Inserted"

        elif self.mode == "list":
            if self.start_node.value[self.index] >= value[self.index]:
                self.start_node = new_node
                self.start_node.next = n
                return "Inserted"

            elif self.end_node.value[self.index] <= value[self.index]:
                self.end_node.next = new_node
                self.end_node = new_node
                return "Inserted"

            else:
                while value[self.index] > n.value[self.index] and value[self.index] < self.end_node.value[self.index] and n.next is not None:
                    n = n.next

                m = self.start_node
                while m.next != n and m.next is not None:
                    m = m.next
                m.next = new_node
                new_node.next = n
                return "Inserted"
        else:
            # If element to be inserted has lower value than head, insert new element at head
            if self.start_node.value >= value:
                self.start_node = new_node
                self.start_node.next = n
                return "Inserted"

            # If element to be inserted has higher value than tail, insert new element at tail
            elif self.end_node.value <= value:
                self.end_node.next = new_node
                self.end_node = new_node
                return "Inserted"

            # If element to be inserted lies between head & tail, find the appropriate position to insert it
            else:
                while value > n.value and value < self.end_node.value and n.next is not None:
                    n = n.next

                m = self.start_node
                while m.next != n and m.next is not None:
                    m = m.next
                m.next = new_node
                new_node.next = n
                return "Inserted"


import sys
import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()


def preprocess_query(query):
    query = query.lower()  # 2a
    query = re.sub(r"[^a-z0-9]+", ' ', query)  # 2b #post processing
    query = query.strip()  # 2c
    return query


def get_tokens_from_query(query):
    token_list = set(query.split(' ')) - stop_words
    final_tokens = set([stemmer.stem(token) for token in token_list])
    #print(token_list)
    return final_tokens


def add_to_inverted_index(doc_id, document):
    doc_tokens = get_tokens_from_query(preprocess_query(document))
    for token in doc_tokens:
        if token not in inverted_index:
            inverted_index[token] = LinkedList()
        inverted_index[token].insert_at_end(doc_id)
        


def get_posting_lists(query_token):
    posting_map = {}
    #print(query_token)
    for token in query_token:
        posting_map[token] = inverted_index[token].traverse_list()
    
    return posting_map


def daatAnd(tokens):
    num_comparisons = 0
    daat_and_list = []
    #print(tokens)

    if len(tokens) is 0:
        return daat_and_list, num_comparisons

    tokens = sorted(tokens, key=lambda x: len(inverted_index[x].traverse_list()))
    
    daat_and_list = inverted_index[tokens[0]].traverse_list()
    #print(daat_and_list)
    if len(tokens) is 1:
        return daat_and_list, num_comparisons
    
    for token in tokens[1:]:
        doc_list_new = inverted_index[token].traverse_list()
        if len(daat_and_list) is 0 or len(doc_list_new) is 0:
            return [], num_comparisons

        doc_list_old = daat_and_list
        daat_and_list = []

        min_last_value = min(doc_list_new[-1], doc_list_old[-1])
        num_comparisons += 1

        old_index = 0
        new_index = 0
        try:
            while doc_list_old[old_index] is not min_last_value or doc_list_new[new_index] is not min_last_value:
                sub = doc_list_old[old_index] - doc_list_new[new_index]
                num_comparisons += 1
                if sub is 0:
                    daat_and_list.append(doc_list_old[old_index])
                    old_index += 1
                    new_index += 1
                elif sub > 0:
                    new_index += 1
                else:
                    old_index += 1

            if doc_list_old[old_index] is doc_list_new[new_index]:
                daat_and_list.append(doc_list_old[old_index])
                num_comparisons += 1
        except:
            continue
    #print(daat_and_list)

    return daat_and_list, num_comparisons-1


corpus_file_path = sys.argv[1]


# Construct Inverted Index
inverted_index = {}
total_no_docs = 0
with open(corpus_file_path, "r", encoding='utf-8') as corpus_file:
    for line in corpus_file.readlines():
        total_no_docs += 1  # getting total number of docs for idf
        line = line.split('\t')
        add_to_inverted_index(int(line[0]), line[1])


query_file_path = sys.argv[3]
outfile2 = sys.argv[2]              #output file
final_output_file_path = open(outfile2, 'w')
final_dict={}

# Prepare posting_output
with open(query_file_path, "r", encoding='utf-8') as query_file:
    query_tokens = set([])
    for line in query_file.readlines():
        query_tokens = query_tokens.union(get_tokens_from_query(preprocess_query(line)))
        output = get_posting_lists(query_tokens)
        final_dict["postingsList"]=output
    


# Prepare daat ouput
with open(query_file_path, "r", encoding='utf-8') as query_file:
    daat_json = {}
    query_tokens = set([])
    for line in query_file:
        #steps
        original_query=line
        original_query=original_query.strip()
        #print(original_query)
        query = preprocess_query(line)
        tokens = list(get_tokens_from_query(query))
        ans = daatAnd(tokens)
        daat_json[original_query]  = {"results": ans[0], "num_docs": len(ans[0]), "num_comparisons": ans[1]}
        final_dict['daatAnd']=daat_json
        
    json.dump(final_dict, final_output_file_path)
