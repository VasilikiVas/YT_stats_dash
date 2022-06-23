"""
Author: Maris Koopmans
Project: YouTube statistics visualization

License for 3rd party use: Anyone can use this lol I don't mind
"""

from get_creator_stats import *
import numpy as np
import torch
import json
import os


def generate_most_repr(data_type):
    """
    Function that calculates the most representative thumbnails or titles for
    all categories and channels and saves the output to a single JSON file.

    args:
        - data_type: the type of representation we're working on. Can be 'thumbnail' or 'title'
    """

    categories = ["animals", "autos", "blogs", "comedy", "education", "entertainment"\
                    "gaming", "howto", "science"]
    
    out_dir = os.path.join(DATA_DIR, f"{data_type}_representatives")
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    
    for cat in categories:
        most_repr_dic = {}

        with open(os.path.join("..", "data", f"videos-info_{cat}.json"), "r") as f:
            creator_info = json.load(f)
            creator_names = creator_info.keys()

        # Already calculate the mean (yes I know this is an extra for loop, but else you have to
        # store all latent representations of all creators in memory)
        category_avg = torch.mean([get_mean_latent(cat, creator, data_type) for creator in creator_names],dim=0)
        all_vids = {}

        for creator in creator_names:
            all_creator_latents = get_all_latents(cat, creator, data_type)
            creator_avg = get_mean_latent(cat, creator, data_type)
            similarities = []

            for vid_id, latent in all_creator_latents.items():
                similarities.append(abs(np.dot(latent, creator_avg)/np.linalg.norm(latent)*np.linalg.norm(creator_avg)))
                all_vids[vid_id] = abs(np.dot(latent, category_avg)/np.linalg.norm(latent)*np.linalg.norm(category_avg))

            most_similar_vid_id = all_creator_latents.keys()[np.argmin(similarities)]
            most_repr_dic[creator] = most_similar_vid_id

        cat_most_similar_vid_id = all_vids.keys()[np.argmin(all_vids.values())]
        most_repr_dic[f"Category_{cat}"] = cat_most_similar_vid_id

        with open(os.path.join(out_dir, cat + "_representatives.json"), 'w') as f:
            json.dump(most_repr_dic, f)

if __name__ == "__main__":
    DATA_DIR = os.path.join("..", "data")
    generate_most_repr()