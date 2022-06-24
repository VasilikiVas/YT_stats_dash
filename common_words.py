import json
import numpy as np
import nltk

def get_unique_terms_views(videos):
    title_views_tok=[]; terms_tok = []
    title_views_spc=[]; terms_spc = []
    for _, info in videos.items():
        for entry in info: 
            title = entry["title"]
            views = entry["views"]
            title_tok = nltk.word_tokenize(title)
            title_spc = title.split()
            title_views_tok.append([title_tok, views])
            title_views_spc.append([title_spc, views])
            terms_tok.extend(title_tok)
            terms_spc.extend(title_spc)
    return np.unique(terms_tok), title_views_tok, np.unique(terms_spc), title_views_spc

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

def get_avg_symbol_views(title_views, uterms):
    valid_symbols = "!@#$%^&*()_-+={}[]?"
    terms_avg = {}
    for uterm in uterms:
        if not uterm.isalnum(): #if the term contains symbols
            flag = True
            for ch in uterm:
                if ch not in valid_symbols:
                    flag = False
                    break
            if flag == True: # if the term contains only valid_symbols, we count the average video views with and without the term
                print(uterm)
                sum1 = 0; views1 = 0; sum2 = 0; views2 = 0
                for title, view in title_views:
                    if uterm in title:
                        sum1 += 1
                        views1 += view
                    else:
                        sum2 += 1
                        views2 += view
                try:
                    terms_avg[uterm] = [views1/sum1, views2/sum2]
                except:
                    import pdb; pdb.set_trace()
    return terms_avg


if __name__ == '__main__':

    with open('./data/videos_info.json', 'r') as infile:
        videos = json.load(infile)

    with open('./data/channels_info.json', 'r') as infile:
        channels = json.load(infile)

    uterms_tok, title_views_tok, uterms_spc, title_views_spc = get_unique_terms_views(videos)
    terms_avg = get_avg_term_views(title_views_tok, uterms_tok)

    symbols_avg = get_avg_symbol_views(title_views_spc, uterms_spc)


    with open('terms-avg.txt', 'w') as outfile:
        outfile.write("Term, Avg. (with), Avg. (without)\n")
        for term, views in terms_avg.items():
            output = term + " " + str(int(views[0])) + " " + str(int(views[1])) + '\n'
            outfile.write(output) 

    with open('symbols-avg.txt', 'w') as outfile:
        outfile.write("Term, Avg. (with), Avg. (without)\n")
        for term, views in symbols_avg.items():
            output = term + " " + str(int(views[0])) + " " + str(int(views[1])) + '\n'
            outfile.write(output) 