import praw
from os.path import isfile
import praw
import pandas as pd
from time import sleep
from fstring import fstring



#sub = 'music'

subreddit_list = ['mbti', 'funny', 'news', 'worldnews', 'art','FoodPorn', 'EarthPorn','teenagers', 'trashy' ,'gaming', 'UpliftingNews',
                  'mildlyinteresting']

reddit = praw.Reddit()
for sub in subreddit_list:
    till_unique_flag = True
    i = 0
    while till_unique_flag:
        csv = ('output/' +str(sub) + str(i) +'_posts.csv')
        df, csv_loaded = (pd.read_csv(csv), 1) if isfile(csv) else ('', 0)
        if csv_loaded == 0:
            till_unique_flag = False
        i = i + 1

    sub_dict = {
                'comment_body': [], 'title': [], 'id': [], 'sorted_by': [],
                'score': [], 'children': [[]], 'children_body': [[]]}

    hot_posts = reddit.subreddit(str(sub)).hot(limit=10)
    sort = 'hot'

    # List of Replies refers to the dictioanary that stores the parent and the replies
    # List of kids refers to the list of unique comment ids

    def get_children(replies):
        list_of_kids = []
        total_list_of_kids = []
        list_of_replies = {}
        replies_to_add_to_total = []
        list_of_kids_body = []
        replies1 = {}
        for object1 in replies:
            if type(object1).__name__ == "Comment":
                list_of_replies[str(object1.id)] = []
                replies1, replies_to_add_to_total,add_to_total_list_of_kids,list_of_kids_body = get_children(object1.replies)  # Get replies of comment
                #list_of_kids_body.append(object1.body)
                list_of_kids.append(object1)
                total_list_of_kids.append(object1)
                list_of_replies[str(object1.id)] = list_of_kids_body
                list_of_replies = dict(list_of_replies, **replies1)
                total_list_of_kids = total_list_of_kids + add_to_total_list_of_kids
                for item in replies_to_add_to_total:
                    total_list_of_kids.append(item)
        list_of_kids_body = []
        #for reply in replies_to_add_to_total:
        #    add_to_total_list_of_kids.append(reply)
        for reply in list_of_kids:
            list_of_kids_body.append(reply.body)
        return list_of_replies, list_of_kids, total_list_of_kids, list_of_kids_body
        pass

    def process_comments(objects):
        list_of_comments = []
        list_of_replies = {}
        total_list_of_kids = []
        replies_to_add = []
        list_of_kids_body = []
        true_list_of_replies = {}
        for object1 in objects:
            if type(object1).__name__ == "Comment":
                replies,replies_to_add,total_list_of_kids, list_of_kids_body = get_children(object1.replies) # Get replies of comment
                list_of_replies[str(object1.id)] = list_of_kids_body
                total_list_of_kids = list(set(total_list_of_kids))
                list_of_comments.append(object1)
                list_of_comments = list_of_comments + total_list_of_kids
                for reply in replies_to_add:
                    list_of_comments.append(reply)
                list_of_replies = dict(list_of_replies, **replies)
                list_of_comments = list(set(list_of_comments))

                # Do stuff with comment (object)


            #elif type(object1).__name__ == "MoreComments":
            #    other_comments =  process_comments(object1.comments())  # commetns at smae level
            #    list_of_comments.append(object1) # object.body is where the meat is
        return list_of_comments, list_of_replies




    for post in hot_posts:
        print(post.title)
        unique_id = post.id not in tuple(df.id) if csv_loaded else True

        # Save any unique posts to sub_dict.
        if unique_id:
            submission = reddit.submission(id = post.id)
            comments, replies = process_comments(submission.comments)

            for comment in comments:
                try:
                    sub_dict['comment_body'].append(comment.body)
                    sub_dict['title'].append(post.title)
                    sub_dict['id'].append(post.id)
                    sub_dict['sorted_by'].append(sort)
                    sub_dict['score'].append(comment.score)
                    body = comment.body
                    id = comment.id
                    reply = comment.replies
                    # now use the items in comment that represent one item, do a look up in replies
                    lookup_replies = replies.get(comment.id, [])
                    children_body = []
                    children_fullname = []
                    for children in lookup_replies:
                        children_body.append(children)
                    sub_dict['children_body'].append(children_body)
                    #sub_dict['children'].append(comment.replies._comments)
                except:
                    pass
        sleep(0.1)
    #import numpy as np
    #np.save('data_floated_np.npy', sub_dict)
    #new_df = pd.DataFrame(sub_dict)
    new_df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in sub_dict.items() ]))

    mode = 'w'
    # Add new_df to df if df exists then save it to a csv.
    if 'DataFrame' in str(type(df)) and mode == 'w':
        pd.concat([df, new_df], axis=0, sort=0).to_csv(csv, index=False)
        print(('{len(new_df)} new posts collected and added to {csv}'))
    elif mode == 'w':
        new_df.to_csv(csv, index=False)
        print(str(len(new_df)) + 'posts collected and saved to ' + str(csv))
    else:
        print((' posts were collected but they were not '))
        mode = mode















