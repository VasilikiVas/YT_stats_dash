"""
Author: Maris Koopmans
Project: YouTube statistics visualization

License for 3rd party use: Anyone can use this lol I don't mind
"""

import thumbnail_repr_stats as ts
from util.constants import Topic
import numpy as np
import torch
import json
import os

# TODO add some more functions to get other statistics from the json files?

def get_thumbnail_repr(category, creator):
    """
    Function to retrieve the thumbnail latent representation statistics for a specific YouTuber.
    If the data does not yet exist, this function calls generate_repr_stats() to generate the latent's
    statistics.

    args:
        - category: the type of content we're looking for
        - creator: The name of the YouTuber whose statistics we're looking for
    
    returns:
        - latent_mean: The mean of all thumbnail latent vectors from this YouTuber
        - latent_std: The standard deviation of all dimensions of the latent thumbnail
                      vectors from the above mentioned mean, summed together.
    """
    out_dir = os.path.join("..", "data", "thumbnail_latents")
    thumbnail_stats_file = os.path.join(out_dir, category, creator + "_stats.json")

    # Check if the thumbnail statistics data already exists
    if not os.path.exists(thumbnail_stats_file):
        ts.generate_repr_stats(out_dir, category)

    try:
        with open(thumbnail_stats_file) as f:
            creator_dict = json.load(f)
    except FileNotFoundError:
        print(f"{creator} doesn't appear in the dataset. Try again with a different YouTuber.")    # Check if the creator is in the data    

    all_latents = torch.Tensor(creator_dict["all_latents"]) 

    return all_latents

if __name__ == '__main__':
    # Just some testing code
    category = Topic.gaming
    creator = 'pewdiepie'
    all_latents = get_thumbnail_repr(category, creator)