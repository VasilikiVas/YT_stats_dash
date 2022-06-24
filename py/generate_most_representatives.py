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


def generate_most_repr(data_type):
    """
    Function that calculates the most representative thumbnails or titles for
    all categories and channels and saves the output to a single JSON file.

    args:
        - data_type: the type of representation we're working on. Can be 'thumbnail' or 'title'
    """

    categories = Topic._member_names_
    
    out_dir = os.path.join(DATA_DIR, f"{data_type}_representatives")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    for cat in categories:
        most_repr_dic = {}

        with open(os.path.join("..", "data", f"videos-info_{cat}.json"), "r") as f:
            channel_info = json.load(f)
            channel_names = channel_info.keys()

        # Already calculate the mean (yes I know this is an extra for loop, but else you have to
        # store all latent representations of all channels in memory)
        category_avg = torch.mean([get_mean_latent(cat, channel, data_type) for channel in channel_names],dim=0)
        all_vids = {}

        for channel in channel_names:
            all_channel_latents = get_all_latents(cat, channel, data_type)
            channel_avg = get_mean_latent(cat, channel, data_type)
            similarities = []

            for vid_id, latent in all_channel_latents.items():
                similarities.append(abs(np.dot(latent, channel_avg)/np.linalg.norm(latent)*np.linalg.norm(channel_avg)))
                all_vids[vid_id] = abs(np.dot(latent, category_avg)/np.linalg.norm(latent)*np.linalg.norm(category_avg))

            most_similar_vid_id = all_channel_latents.keys()[np.argmin(similarities)]
            most_repr_dic[channel] = most_similar_vid_id

        cat_most_similar_vid_id = all_vids.keys()[np.argmin(all_vids.values())]
        most_repr_dic[f"Category_{cat}"] = cat_most_similar_vid_id

        with open(os.path.join(out_dir, cat + "_representatives.json"), 'w') as f:
            json.dump(most_repr_dic, f)

if __name__ == "__main__":
    DATA_DIR = os.path.join("..", "data")
    generate_most_repr()