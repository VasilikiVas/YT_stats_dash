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


def get_all_latents(category, creator, latent_type):
    """
    Function to retrieve the thumbnail latent representation statistics for a specific YouTuber.
    If the data does not yet exist, this function calls generate_repr_stats() to generate the latent's
    statistics.

    args:
        - category: the type of content we're looking for
        - creator: The name of the YouTuber whose statistics we're looking for
        - latent_type: The type of data we're looking for. Can be either 'thumbnail' or 'title'
    
    returns:
        - all_latents: all latent representations of the video thumbnails
    """
    if std_type not in ['thumbnail', 'title']:
        print(f"Wrong type of data requested. Please request either 'thumbnail' or 'title'")
        return

    out_dir = os.path.join("..", "data", f"{latent_type}_latents")
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

    
def get_standard_dev(category, creator, std_type):
    """
    Helper function to retrieve the standard deviation of the latent representations
    of either the video thumbnails or the video titles.
    
    args:
        - category: the type of content we're looking for
        - creator: The name of the YouTuber whose statistics we're looking for
        - std_type: The type of data we're looking for. Can be either 'thumbnail' or 'title'
    
    returns:
        - stdev: float representing the standard deviation of the latent representations
    """

    if std_type not in ['thumbnail', 'title']:
        print(f"Wrong type of data requested. Please request either 'thumbnail' or 'title'")
        return

    out_dir = os.path.join("..", "data", f"{std_type}_latents")
    thumbnail_stats_file = os.path.join(out_dir, category, creator + "_stats.json")

    # Check if the thumbnail statistics data already exists
    # TODO: if you wanna use this, change category to be instance of Topic
    # if not os.path.exists(thumbnail_stats_file):
    #     ts.generate_repr_stats(out_dir, category)

    try:
        with open(thumbnail_stats_file) as f:
            creator_dict = json.load(f)
    except FileNotFoundError:
        print(f"{creator} doesn't appear in the dataset. Try again with a different YouTuber.")    # Check if the creator is in the data    

    stdev = torch.Tensor(creator_dict["stdev"]) 

    return stdev

def get_mean_latent(category, creator, mean_type):
    """
    Helper function to retrieve the mean vector of the latent representations
    of either the video thumbnails or the video titles.
    
    args:
        - category: the type of content we're looking for
        - creator: The name of the YouTuber whose statistics we're looking for
        - mean_type: The type of data we're looking for. Can be either 'thumbnail' or 'title'
    
    returns:
        - mean: mean tensor representing the mean of the latent representations
    """

    if std_type not in ['thumbnail', 'title']:
        print(f"Wrong type of data requested. Please request either 'thumbnail' or 'title'")
        return

    out_dir = os.path.join("..", "data", f"{std_type}_latents")
    thumbnail_stats_file = os.path.join(out_dir, category, creator + "_stats.json")

    # Check if the thumbnail statistics data already exists
    # TODO: if you wanna use this, change category to be instance of Topic
    # if not os.path.exists(thumbnail_stats_file):
    #     ts.generate_repr_stats(out_dir, category)

    try:
        with open(thumbnail_stats_file) as f:
            creator_dict = json.load(f)
    except FileNotFoundError:
        print(f"{creator} doesn't appear in the dataset. Try again with a different YouTuber.")    # Check if the creator is in the data    

    mean = torch.Tensor(creator_dict["mean_latent"]) 

    return mean

if __name__ == '__main__':
    # Just some testing code
    category = "gaming"
    creator = 'pewdiepie'
    all_latents = get_thumbnail_repr(category, creator)