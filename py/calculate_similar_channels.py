"""
Author: Maris Koopmans
Project: YouTube statistics visualization

License for 3rd party use: Anyone can use this lol I don't mind
"""

from get_channel_stats import *
import numpy as np
import torch
import json
import os

from util.constants import Topic


def cosine_sim(vec1, vec2):
    """Helper function which calculates cosine similarity of two vectors"""

    return abs(np.dot(vec1, vec2)/np.linalg.norm(vec1)*np.linalg.norm(vec2))


def generate_most_similar(data_type):
    """
    Function that calculates for every channel the similarity score between that
    channel and all other channels. It does so for all categories and saves the 
    output to a single JSON file for each category.

    args:
        - data_type: the type of representation we're working on. Can be 'thumbnail' or 'title'
    """
    categories = Topic._member_names_
    
    out_dir = os.path.join(DATA_DIR, f"{data_type}_similars")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    for cat in categories:
        most_similar_dic = {}

        with open(os.path.join("..", "data", f"videos-info_{cat}.json"), "r") as f:
            channel_info = json.load(f)
            channel_names = channel_info.keys()

        # Load all mean latent vectors
        all_mean_latents = {chan: get_mean_latent(cat, chan, data_type) for chan in channel_names}

        # Calculate the cosine similarity for every combination
        for chan in channel_names:
            most_similar_dic[chan] = {chan2: cosine_sim(all_mean_latents[chan], all_mean_latents[chan2]) 
                                        for chan2 in channel_names}

        with open(os.path.join(out_dir, cat + "_similars.json"), 'w') as f:
            json.dump(most_similar_dic, f)

if __name__ == "__main__":
    DATA_DIR = os.path.join("..", "data")
    generate_most_similar('thumbnail')
    generate_most_similar('title')