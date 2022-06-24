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
    Function to generate all thumbnail averages per channel.

    args:
        - out_folder: path to the folder where the thumbnail averages will be saved
    """

    # Define thumbnail path
    thumbnail_dir = os.path.join("..", "data", "thumbnails")

    with open(os.path.join("..", "data", f"videos-info_{category}.json"), "r") as f:
        print("Loading channel's videos")
        videos_info = json.load(f)
    print("Finished loading channel's videos\n")

    print("Calculating thumbnail averages for all channels in category: " + category + "\n")
    category_thumbnails = []
    category_views = []
    for channel in tqdm(list(videos_info.keys())):
        all_channel_thumbnails = []
        all_channel_views = []
        
        try:
            channel_thumbnails = []
            channel_views = []
            for vid_dict in videos_info[channel]:
                img = np.array(Image.open(os.path.join(thumbnail_dir, vid_dict['id'] + "_high.jpg")))
                h, w, _ = img.shape
                if h == THUMBNAIL_HEIGHT and w == THUMBNAIL_WIDTH:
                    # we exclude shorts by skipping the videos that were not cropped
                    continue
                channel_thumbnails.append(img)
                channel_views.append(vid_dict["views"])
            if len(channel_thumbnails) < 5:
                continue
            all_channel_thumbnails.extend(channel_thumbnails)
            all_channel_views.extend(channel_views)
            category_thumbnails.extend(all_channel_thumbnails)
            category_views.extend(all_channel_views)

        except FileNotFoundError:
            continue

        channels_avg_thumbnail = np.average(np.array(all_channel_thumbnails), weights = all_channel_views, axis=0)

        im = Image.fromarray(channels_avg_thumbnail.astype('uint8'))
        im.save(os.path.join(CHANNELS_PATH, channel + '.png'))
    
    print("Calculating thumbnail average for category: " + category + "\n")
    category_avg_thumbnail = np.average(np.array(category_thumbnails), weights = category_views, axis=0)

    im = Image.fromarray(category_avg_thumbnail.astype('uint8'))
    im.save(os.path.join(CATEGORY_PATH, category + '.png'))

    print("Finished saving thumbnail averages per channel and for category\n")


if __name__ == '__main__':

    CATEGORY_PATH = "../data/thumbnail-averages/categories"
    CHANNELS_PATH = "../data/thumbnail-averages/channels"

    if not os.path.exists(CATEGORY_PATH):
        os.makedirs(CATEGORY_PATH)

    if not os.path.exists(CHANNELS_PATH):
        os.makedirs(CHANNELS_PATH)

    # category = Topic.gaming

    for category in Topic:
        generate_thumbnail_averages(category.value)
        # only do gaming for now
        break
