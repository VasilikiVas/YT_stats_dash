import numpy as np
from matplotlib import image
from sklearn.cluster import KMeans
from util.constants import Topic, THUMBNAIL_HEIGHT, THUMBNAIL_WIDTH
from tqdm import tqdm
from PIL import Image
import numpy as np
import json
import os

THUMBNAIL_PATH = os.path.join("..","..","thumbnails")

from crop_black_borders import crop_black_border_img

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def make_image_grid_1_row(imgs):
    w, h = imgs[0].size
    cols = len(imgs)

    grid = Image.new('RGB', size=(w * cols, h))
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i % cols*w, i//cols*h))
    return np.array(grid)


def make_image_grid(imgs, rows, cols):
    assert len(imgs) == rows*cols

    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return np.array(grid)


def extract_dom_colours(img, clusters):
    """
    Function to extract dominant colours of given image.
    """
    # print(img.shape)
    # remove dark colours from image
    filtered_img = img[img[:,:,0] + img[:,:,1] + img[:,:,2] > 100]
    if len(filtered_img) > 100:
        img = filtered_img

    flat_img = np.reshape(img,(-1,3))

    flat_img = np.resize(flat_img,(200*100, 3))

    kmeans = KMeans(n_clusters=clusters, random_state=0)
    kmeans.fit(flat_img)

    dominant_colors = np.array(kmeans.cluster_centers_, dtype='uint8')
    dominant_colors = tuple(map(tuple, dominant_colors))
    dominant_colors = [rgb_to_hex(dom_color) for dom_color in dominant_colors]

    percentages = (np.unique(kmeans.labels_, return_counts=True)[1]) / flat_img.shape[0]
    percentages = [round(perc, 3) for perc in percentages]

    c_and_p_dict = {"colours" : dominant_colors, "perc" : percentages}

    return c_and_p_dict


def extract_category_dom_colours(category: Topic, clusters):
    """
    Function to extract dominant colours per creator and category for the given category.

    args:
        - category: the given category
    """

    with open(os.path.join("..", "data", "info_videos", f"videos-info_{category}.json"), "r") as f:
        print("Loading creator's videos")
        videos_info = json.load(f)
    print("Finished loading creator's videos\n")

    print("Calculating dominant colours for all channels in category: " + category + "\n")
    all_category_thumbnails = []
    for creator in tqdm(list(videos_info.keys())):
        if os.path.isfile(os.path.join(CHANNELS_PATH, creator + ".json")):
            continue
        
        creator_thumbnails = []
        for vid_dict in videos_info[creator]:
            try:
                img = image.imread(os.path.join(THUMBNAIL_PATH, vid_dict['id'] + "_high.jpg"))
            except FileNotFoundError:
                continue
            img = crop_black_border_img(img)
            
            if type(img) == bool and not img:
                continue
                        
            # resize so kmeans is faster
            _, _, C = img.shape
            img = np.resize(img,(100, 200, C))

            creator_thumbnails.append(Image.fromarray(img))
        if len(creator_thumbnails) < 5:
            print(f"not enough thumbnails for {creator}")
            continue

        # all_category_thumbnails.extend(creator_thumbnails)

        img_grid = make_image_grid_1_row(creator_thumbnails)
        dom_colours = extract_dom_colours(img_grid, clusters)

        with open(os.path.join(CHANNELS_PATH, creator + ".json"), 'w') as f:
            json.dump(dom_colours, f)
        
    # print("Calculating dominant colours for category: " + category + "\n")

    # img_grid = make_image_grid_1_row(all_category_thumbnails)
    # dom_colours = extract_dom_colours(img_grid, clusters)

    # with open(os.path.join(CATEGORY_PATH, category + ".json"), 'w') as f:
        # json.dump(dom_colours, f)

    print("Finished calculating dominant colours per creator\n")


if __name__ == '__main__':

    CATEGORY_PATH = "../data/thumbnail-dom-colours/categories"
    CHANNELS_PATH = "../data/thumbnail-dom-colours/channels"

    if not os.path.exists(CATEGORY_PATH):
        os.makedirs(CATEGORY_PATH)

    if not os.path.exists(CHANNELS_PATH):
        os.makedirs(CHANNELS_PATH)

    # choose how many colours to extract
    clusters = 5

    for category in Topic._member_names_:
        extract_category_dom_colours(category, clusters)
