from util.constants import Topic, THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH
from tqdm import tqdm
from PIL import Image
import numpy as np
import json
import os
from matplotlib import pyplot as plt
from crop_black_borders import crop_black_border_img

THUMBNAIL_PATH = os.path.join("..","..","thumbnails")

def generate_thumbnail_averages(category: Topic):
    """
    Function to generate all thumbnail averages per creator and category for the given category.

    args:
        - category: the given category
    """

    with open(os.path.join("..", "data", "info_videos", f"videos-info_{category}.json"), "r") as f:
        print("Loading channel's videos")
        videos_info = json.load(f)
    print("Finished loading channel's videos\n")

    print("Calculating thumbnail averages for all channels in category: " + category + "\n")
    category_thumbnails = []
    category_views = []
    for channel in tqdm(list(videos_info.keys())):        
        channel_thumbnails = []
        channel_views = []
        for vid_dict in videos_info[channel]:
            try:
                img = np.array(Image.open(os.path.join(THUMBNAIL_PATH, vid_dict['id'] + "_high.jpg")))
            except FileNotFoundError:
                continue
            img = crop_black_border_img(img)
            if type(img) == bool and not img: # Exclude shorts and wrong shapes
                continue
            channel_thumbnails.append(img)
            channel_views.append(vid_dict["views"])
        if len(channel_thumbnails) < 5:
            continue
        category_thumbnails.extend(channel_thumbnails)
        category_views.extend(channel_views)

        channels_avg_thumbnail = np.average(np.array(channel_thumbnails), weights = channel_views, axis=0)

        im = Image.fromarray(channels_avg_thumbnail.astype('uint8'))
        im.save(os.path.join(CHANNELS_PATH, channel + '.png'))
    
    # print("Calculating thumbnail average for category: " + category + "\n")
    # category_avg_thumbnail = np.average(np.array(category_thumbnails), weights = category_views, axis=0)

    # im = Image.fromarray(category_avg_thumbnail.astype('uint8'))
    # im.save(os.path.join(CATEGORY_PATH, category + '.png'))

    print("Finished saving thumbnail averages per channel and for category\n")


if __name__ == '__main__':

    CATEGORY_PATH = "../data/thumbnail-averages/categories"
    CHANNELS_PATH = "../data/thumbnail-averages/channels"

    if not os.path.exists(CATEGORY_PATH):
        os.makedirs(CATEGORY_PATH)

    if not os.path.exists(CHANNELS_PATH):
        os.makedirs(CHANNELS_PATH)

    for cat in Topic._member_names_:
        generate_thumbnail_averages(cat)
