from turtle import shape
from util.constants import Topic, THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH
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
        videos_info = json.load(f)
    print("Finished loading creator's videos\n")

    print("Calculating thumbnail averages for all creators in category: " + category.name + "\n")
    for creator in tqdm(list(videos_info.keys())):
        all_creator_thumbnails = []
        all_creator_views = []
        
        try:
            creator_thumbnails = []
            creator_views = []
            for vid_dict in videos_info[creator]:
                img = np.array(Image.open(os.path.join(thumbnail_dir, vid_dict['id'] + "_high.jpg")))
                h, w, _ = img.shape
                if h == THUMBNAIL_HEIGHT and w == THUMBNAIL_WIDTH:
                    # we exclude shorts by skipping the videos that were not cropped
                    continue
                creator_thumbnails.append(img)
                creator_views.append(vid_dict["views"])
            if len(creator_thumbnails) < 5:
                continue
            all_creator_thumbnails.extend(creator_thumbnails)
            all_creator_views.extend(creator_views)

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