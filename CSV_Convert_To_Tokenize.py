import pandas as pd
import numpy as np
import scipy
import nltk
import re

def convert_CSV_TO_Dataframe(csv):
    read_csv = pd.read_csv(csv)
    return read_csv

def get_label_of_children(data, columns):
    df1 = pd.DataFrame(data, columns=columns)
    #newdf = data[data.columns[0,4,6]]
    return df1

def convert_children(children):
    children2 = children.replace("[", "").replace("]", "")
    list_of_children_comments = re.findall('"([^"]*)"', children2)
    return list_of_children_comments

def get_children_to_parent(data):
    Row_List = []
    for index, rows in data.iterrows():
        children_list = []
        children_list = convert_children(rows.children_body)
        my_list = [rows.comment_body, children_list, rows.score]
        Row_List.append(my_list)
    return Row_List


# THis is the main function
# You can alter what gets parsed by knowing 2 variables:
# The path to your csv and the names of the columns
def CSV_TO_TOKENIZE(csv_path, columns):
    data = convert_CSV_TO_Dataframe(csv_path)

    labels = get_label_of_children(data, columns)

    rows = get_children_to_parent(labels)
    return rows

# Test code ###########################################
#csv_path = "output/art0_posts.csv"
# data = convert_CSV_TO_Dataframe(csv_path)
# 
#
# columns = ['comment_body', 'children_body', 'score']
# labels = get_label_of_children(data , columns)
#
# rows = get_children_to_parent(labels)
# i=1




