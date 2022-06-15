"""
Author: Maris Koopmans
Project: YouTube statistics visualization

License for 3rd party use: Anyone can use this lol I don't mind
"""

import thumbnail_repr_stats as ts
import numpy as np
import json
import os

# TODO add some more functions to get other statistics from the json files?

def get_thumbnail_repr_stats(creator):
    """
    Function to retrieve the thumbnail latent representation statistics for a specific YouTuber.
    If the data does not yet exist, this function calls generate_repr_stats() to generate the latent's
    statistics.

    args:
        - creator: The name of the YouTuber whose statistics we're looking for
    
    returns:
        - latent_mean: The mean of all thumbnail latent vectors from this YouTuber
        - latent_std: The standard deviation of all dimensions of the latent thumbnail
                      vectors from the above mentioned mean, summed together.
    """
    thumbnail_stats_file = os.path.join("..", "data", "thumbnail-repr-stats.json")

    # Check if the thumbnail statistics data already exists
    if not os.path.exists(thumbnail_stats_file):
        ts.generate_repr_stats(thumbnail_stats_file)

    with open(thumbnail_stats_file) as f:
        creator_dict = json.load(f)

    # Check if the creator is in the data
    if creator in creator_dict.keys():
        creator_stats = creator_dict[creator]
    else:
        print(f"{creator} doesn't appear in the dataset. Try again with a different YouTuber.")

    latent_mean = np.array(creator_stats["mean_latent"]) 
    latent_std = creator_stats["stdev"]

    return latent_mean, latent_std

if __name__ == '__main__':
    # Just some testing code
    mean_pewds, std_pewds = get_thumbnail_repr_stats("pewdiepie")
    print(f"Pewdiepie's video latent standard deviation: {std_pewds}")
