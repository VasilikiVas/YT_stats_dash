from turtle import shape
from util.constants import Topic, THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH
from tqdm import tqdm
from PIL import Image
import numpy as np
import json
import os
from matplotlib import pyplot as plt

def generate_thumbnail_averages(category: Topic):
    """
    Function to generate all thumbnail averages per creator.

    args:
        - out_folder: path to the folder where the thumbnail averages will be saved
    """

    # Define thumbnail path
    thumbnail_dir = os.path.join("..", "data", "thumbnails")

    with open(os.path.join("..", "data", f"videos-info_{category}.json"), "r") as f:
        print("Loading creator's videos")
        videos_info = json.load(f)
    print("Finished loading creator's videos\n")

    print("Calculating thumbnail averages for all creators in category: " + category + "\n")
    category_thumbnails = []
    category_views = []
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
            category_thumbnails.extend(all_creator_thumbnails)
            category_views.extend(all_creator_views)

        except FileNotFoundError:
            continue

        creators_avg_thumbnail = np.average(np.array(all_creator_thumbnails), weights = all_creator_views, axis=0)

        im = Image.fromarray(creators_avg_thumbnail.astype('uint8'))
        im.save(os.path.join(CREATORS_PATH, creator + '.png'))
    
    print("Calculating thumbnail average for category: " + category + "\n")
    category_avg_thumbnail = np.average(np.array(category_thumbnails), weights = category_views, axis=0)

    im = Image.fromarray(category_avg_thumbnail.astype('uint8'))
    im.save(os.path.join(CATEGORY_PATH, category + '.png'))

    print("Finished saving thumbnail averages per creator and for category\n")


if __name__ == '__main__':

    CATEGORY_PATH = "../data/thumbnail-averages/categories"
    CREATORS_PATH = "../data/thumbnail-averages/creators"

    if not os.path.exists(CATEGORY_PATH):
        os.makedirs(CATEGORY_PATH)

    if not os.path.exists(CREATORS_PATH):
        os.makedirs(CREATORS_PATH)

    # category = Topic.gaming

    for category in Topic:
        generate_thumbnail_averages(category.value)
        # only do gaming for now
        break
