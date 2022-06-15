import json
import numpy as np
import nltk

def get_unique_terms_views(videos):
    title_views=[]; terms = []
    for user, info in videos.items():
        for entry in info: 
            title = entry["title"]
            views = entry["views"]
            title = nltk.word_tokenize(title)
            title_views.append([title, views])
            terms.extend(title)
    return np.unique(terms), title_views

def get_avg_term_views(title_views, uterms):
    terms_avg = {}
    for uterm in uterms:
        sum1 = 0; views1 = 0; sum2 = 0; views2 = 0

        for title, view in title_views:
            if uterm in title:
                sum1 += 1
                views1 += view
            else:
                sum2 += 1
                views2 += view
        terms_avg[uterm] = [views1/sum1, views2/sum2]
    return terms_avg


if __name__ == '__main__':

    with open('./data/videos_info.json', 'r') as infile:
        videos = json.load(infile)

    with open('./data/channels_info.json', 'r') as infile:
        channels = json.load(infile)

    uterms, title_views = get_unique_terms_views(videos)
    terms_avg = get_avg_term_views(title_views, uterms)

    with open('terms-avg.txt', 'w') as outfile:
        outfile.write("Term, Avg. (with), Avg. (without)\n")
        for term, views in terms_avg.items():
            output = term + " " + str(int(views[0])) + " " + str(int(views[1])) + '\n'
            outfile.write(output) 