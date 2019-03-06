from os import listdir
from os.path import isfile, join
import string
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import nltk
import re
from nltk.tokenize import RegexpTokenizer

#download latest stopwords
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))


################# Step 1 ##########################
original_path = "20_newsgroups"
#creating a list of folder names to make valid pathnames later
folders = [f for f in listdir(original_path)]

#creating a 2D list to store list of all files in different folders
files = []
for folder_name in folders:
    my_path = join(original_path, folder_name)
    files.append([f for f in listdir(my_path)])

#creating a list of pathnames of all the documents
#this would serve to split our dataset into train & test later without any bias
pathname_list = []
for fo in range(len(folders)):
    for fi in files[fo]:
        pathname_list.append(join(original_path, join(folders[fo], fi)))

#making an array containing the classes each of the documents belong to
Y = []
for folder_name in folders:
    folder_path = join(original_path, folder_name)
    num_of_files= len(listdir(folder_path))
    for i in range(num_of_files):
        Y.append(folder_name)

####### step-1 ends ###########


####### step 2 ########################
doc_train, doc_test, Y_train, Y_test = train_test_split(pathname_list, Y, random_state=0, test_size=0.5)

def flatten(list):
    new_list = []
    for i in list:
        for j in i:
            new_list.append(j)
    return new_list
	
#function to convert a document into list of words
def doc_tokenize(path):
    #load document as a list of lines
    f = open(path, 'r')
    text_lines = f.readlines()
    
    #initiazing an array to hold all the words in a document
    doc_words = []
    tokenizer = RegexpTokenizer(r'\w+')
    
    #traverse over all the lines and tokenize each one with the help of helper function: tokenize_sentence
    for line in text_lines:
        doc_words.append(tokenizer.tokenize(line))
        
    return doc_words
	
def hasNumbers(inputString):
    return bool(re.search(r'\d', inputString))

############## step 2 ends ##############
    
######## step 3 #########################

list_of_words = []

for document in doc_train:
    list_of_words.append(flatten(doc_tokenize(document)))
	
def preprocess_data(words_by_document):
    #remove stop words
    stp_removed_words = np.array([word for word in words_by_document if not word in stop_words])
    
    #remove any digits
    dig_removed_words = np.array([word for word in stp_removed_words if not word.isdigit()])
    
    #remove words of length 1
    len1_removed_words = np.array([word for word in dig_removed_words if not len(word) == 1])
    
    #remove words of length 2
    len2_removed_words = np.array([word for word in len1_removed_words if len(word) > 2])
    
    #remove words if it is not a string
    ntstr_removed_words = np.array([str for str in len2_removed_words if str])
    
    #remove words if it is alphanumeric
    alpnum_removed_words = np.array([word for word in ntstr_removed_words if word.isalnum()])
    
    #remove words if it has numbers in one of its characters
    charnum_removed_words = np.array([word for word in alpnum_removed_words if not hasNumbers(word)])
    
    #convert the preprocessed words to lowercase
    preprocessed_words = np.array([word.lower() for word in charnum_removed_words])
    
    return preprocessed_words
	
flatten_to1D_words = np.asarray(flatten(list_of_words))
list_of_words_train = preprocess_data(flatten_to1D_words)

Xtrain_by_each_doc = [list(preprocess_data(doc_arr)) for doc_arr in list_of_words]

def get_features(preprocessed_words, feature_count):
    #get the word frequency or value count
    word_counts = nltk.FreqDist(preprocessed_words)
    
    #get the least common words - words that were not repeated at all, were present only once
    least_repeated = []
    for keyVal in word_counts.keys():
        if(word_counts[keyVal] == 1):
            least_repeated.append(keyVal)
    
    #get the sorted most common words
    unique_words = np.array(list(dict(word_counts.most_common()).keys()))
    
    #remove the least common from unique words list
    most_repeated_words = np.array([word for word in unique_words if not word in least_repeated])
    
    #get the featured words based on feature selection count that is set
    featured_words = most_repeated_words[0:feature_count]
    
    return featured_words
	
#extract features from train data
feature_selection_count = 10000
features = get_features(list_of_words_train, feature_selection_count)

######## step 3 ends ##############################

#################### step 4 ##################
# get a dictionary of words for each document with respect to each word count in the document, in the whole train set of documents
train_dict = {}
doc_num = 1
for doc_words in Xtrain_by_each_doc:
    #print(doc_words)
    np_doc_words = np.asarray(doc_words)
    w, c = np.unique(np_doc_words, return_counts=True)
    train_dict[doc_num] = {}
    for i in range(len(w)):
        train_dict[doc_num][w[i]] = c[i]
    doc_num = doc_num + 1
	
#now we make a 2D array having the frequency of each word of our feature set in each individual documents
X_train = []
for k in train_dict.keys():
    row = []
    for f in features:
        if(f in train_dict[k].keys()):
            #if word f is present in the dictionary of the document as a key, its value is copied
            #this gives us no. of occurences
            row.append(train_dict[k][f]) 
        else:
            #if not present, the no. of occurences is zero
            row.append(0)
    X_train.append(row)
	
#we convert the X and Y into np array for concatenation and conversion into dataframe
X_train = np.asarray(X_train)
Y_train = np.asarray(Y_train)

#do the same to get test_x
test_tokenize = []
for document in doc_test:
        test_tokenize.append(flatten(doc_tokenize(document)))
		
Xtest_by_each_doc = [list(preprocess_data(doc_arr)) for doc_arr in test_tokenize]  

test_dict = {}
doc_num = 1
for doc_words in Xtest_by_each_doc:
    #print(doc_words)
    np_doc_words = np.asarray(doc_words)
    w, c = np.unique(np_doc_words, return_counts=True)
    test_dict[doc_num] = {}
    for i in range(len(w)):
        test_dict[doc_num][w[i]] = c[i]
    doc_num = doc_num + 1
	
#now we make a 2D array having the frequency of each word of our feature set in each individual documents
X_test = []
for k in test_dict.keys():
    row = []
    for f in features:
        if(f in test_dict[k].keys()):
            #if word f is present in the dictionary of the document as a key, its value is copied
            #this gives us no. of occurences
            row.append(test_dict[k][f]) 
        else:
            #if not present, the no. of occurences is zero
            row.append(0)
    X_test.append(row)
	
X_test = np.asarray(X_test)
Y_test = np.asarray(Y_test)


#################### step 4 ends ##################

############### step 5 ###################

#function to create a training dictionary out of the text files for training set, consisiting the frequency of
#words in our feature set (vocabulary) in each class or label of the 20 newsgroup
def fitTrainData(X_train, Y_train):
    result = {}
    classes, counts = np.unique(Y_train, return_counts=True)
    
    for i in range(len(classes)):
        curr_class = classes[i]
        
        result["TOTAL_DATA"] = len(Y_train)
        result[curr_class] = {}
        
        X_tr_curr = X_train[Y_train == curr_class]
        
        num_features = 10000
        
        for j in range(num_features):
            result[curr_class][features[j]] = X_tr_curr[:,j].sum() 
                
        result[curr_class]["TOTAL_COUNT"] = counts[i]
    
    return result
	
#function for calculating naive bayesian log probablity for each test document being in a particular class
def find_class_probablity(dictionary_train, x, curr_class):
    output = np.log(dictionary_train[curr_class]["TOTAL_COUNT"]) - np.log(dictionary_train["TOTAL_DATA"])
    num_words = len(x)
    for j in range(num_words):
        if(x[j] in dictionary_train[curr_class].keys()):
            xj = x[j]
            count_curr_class_equal_xj = dictionary_train[curr_class][xj] + 1
            count_curr_class = dictionary_train[curr_class]["TOTAL_COUNT"] + len(dictionary_train[curr_class].keys())
            curr_xj_prob = np.log(count_curr_class_equal_xj) - np.log(count_curr_class)
            output = output + curr_xj_prob
        else:
            continue
    
    return output
	
#helper function for the predict() function that predicts the class or label for one test document at a time
def predict_each_class(dictionary_train, x):
    classes = dictionary_train.keys()
    best_p = -10000
    best_class = -1
    for curr_class in classes:
        if(curr_class == "TOTAL_DATA"):
            continue
        p_curr_class = find_class_probablity(dictionary_train, x, curr_class)
        if(p_curr_class > best_p):
            best_p = p_curr_class
            best_class = curr_class
            
    return best_class
	
#predict function that predicts the class or label of test documents using train dictionary made using the fit() function
def predict(dictionary_train, X_test):
    Y_pred = []
    for x in X_test:
        y_predicted = predict_each_class(dictionary_train, x)
        Y_pred.append(y_predicted)
    
    #print(Y_pred)
    return Y_pred
	
trainData_dict = fitTrainData(X_train, Y_train)
X_test = []
for key in test_dict.keys():
    X_test.append(list(test_dict[key].keys()))
	
my_predictions = predict(trainData_dict, X_test)
my_predictions = np.asarray(my_predictions)
print(accuracy_score(Y_test, my_predictions))
print(classification_report(Y_test, my_predictions))

############## step 5 ends #######################
