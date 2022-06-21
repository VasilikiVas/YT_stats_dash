from util.constants import Topic
from tqdm import tqdm
from PIL import Image
import numpy as np
import json
import os
from matplotlib import pyplot as plt

def generate_thumbnail_averages(out_folder, category: Topic):
    """
    Function to generate all thumbnail averages per creator.

    args:
        - out_folder: path to the folder where the thumbnail averages will be saved
    """

    # Define thumbnail path
    thumbnail_dir = os.path.join("..", "data", "thumbnails")

    with open(os.path.join("..", "data", f"videos-info_{category.name}.json"), "r") as f:
        print("Loading creator's videos")
        creator_info = json.load(f)
    print("Finished loading creator's videos\n")

    print("Calculating thumbnail averages for all creators in category: " + category.name + "\n")
    for creator in tqdm(list(creator_info.keys())):
        all_creator_thumbnails = []
        all_creator_views = []
        
        try:
            all_creator_thumbnails.extend([np.array(Image.open(os.path.join(thumbnail_dir, vid_dict['id'] + "_high.jpg")))
                                  for vid_dict in creator_info[creator]])

            all_creator_views.extend([vid_dict["views"] for vid_dict in creator_info[creator]])
        except FileNotFoundError:
            continue

        creators_palette = np.average(np.array(all_creator_thumbnails), weights = all_creator_views, axis=0)

        im = Image.fromarray(creators_palette.astype('uint8'))
        im.save(os.path.join("..", "data", out_folder, creator + '.png'))

    print("Finished saving thumbnail averages per creator\n")


if __name__ == '__main__':
    category = Topic.gaming

    out_folder = "thumbnail-averages-" + category.name
    if not os.path.exists(os.path.join("..", "data", out_folder)):
        os.makedirs(os.path.join("..", "data", out_folder))

    generate_thumbnail_averages(out_folder, category)