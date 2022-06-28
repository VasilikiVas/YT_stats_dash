from flask import render_template, request, jsonify, send_from_directory
import os, json, sys
import re
import requests
from PIL import Image

from decimal import Decimal

import pandas as pd
import numpy as np

from . import main
from flask import redirect, send_file

try:
    from ...py.get_channel_stats import *
    from ...py.util.constants import Topic
    from ...py.crop_black_borders import crop_black_border_img

except:
    path = os.getcwd()
    sys.path.append(os.path.join(path ,"py/"))

    from get_channel_stats import *
    from util.constants import Topic
    from crop_black_borders import crop_black_border_img
    
    sys.path.remove(os.path.join(path ,"py/"))


DATA_DIR = os.path.join("data")

@main.route('/', methods=['GET'])
def base():
    return redirect('/category/gaming?subview_mode=thumbnail')


@main.route('/category/<cat>', methods=['GET'])
def category(cat):
    subview_mode = request.args.get("subview_mode")

    if not cat:
        cat = "gaming"
    if not subview_mode:
        subview_mode = "thumbnail"

    # Get channels info
    channels_info_path = os.path.join(DATA_DIR, "info_channels", f"channels-info_{cat}.json")
    with open(channels_info_path, "r") as f:
        channels_dict = json.load(f)

    # Get videos info
    videos_info_path = os.path.join(DATA_DIR, "info_videos", f"videos-info_{cat}.json")
    with open(videos_info_path, "r") as f:
        videos_dict = json.load(f)
    videos = []
    for name, vids in videos_dict.items():
        videos.extend([{"channel": name, **vid} for vid in vids])
        channels_dict[name]["avg_views"]	  = np.mean([vid["views"] for vid in vids])
        channels_dict[name]["vids_available"] = len(vids)
    videos.sort(key=lambda x: x["views"], reverse=True)

    # Get dictionary to translate video ids to channel names (useful for e.g. most representative title)
    # vid2channel_path = os.path.join(DATA_DIR, "vid2channel.json")
    # with open(vid2channel_path, "r") as f:
    #     vid2channel = json.load(f)

    channels = []
    for name, info in channels_dict.items():
        channels.append({
            "name": re.sub(r"-?([A-z0-9]){8}-([A-z0-9]){4}-([A-z0-9]){4}-([A-z0-9]){4}-([A-z0-9]){12}", "", name),
            **info
        })

    cat_avg_subs = int(np.mean([info["Subscribers"] for info in channels_dict.values()]))
    cat_avg_views = int(np.mean([info["avg_views"] for info in channels_dict.values() if "avg_views" in info]))
    cat_avg_vids = int(np.mean([info["Video count"] for info in channels_dict.values()]))

	# # # Load in the video id of the videos with the most representative thumbnails
	# most_repr_thumbnail_path = os.path.join(DATA_DIR, "thumbnail_representatives", f"{cat}_representatives.json")
	# with open(most_repr_thumbnail_path, "r") as f:
	# 	most_repr_thumbnail_data = json.load(f)

    # # Load in the video ids of the videos with the most representative titles
	# most_repr_title_path = os.path.join(DATA_DIR, "title_representatives", f"{cat}_representatives.json")
	# with open(most_repr_title_path, "r") as f:
	# 	most_repr_title_data = json.load(f)

    category = {
        # TODO Actual code (WIP)
        "name": cat, 		  # str: name of category
        "avg_subs": cat_avg_subs,   # int: avg subs per channel in cat
        "avg_views": cat_avg_views, # int: avg views per video in cat
        "avg_video_count": cat_avg_vids, # int: avg amount of videos per channel in cat
        # # TITLE
        # "repr_title": most_repr_title, # str: most representative title

        # Hardcoded examples
        # TITLE
        "repr_title": "This is a title", # str: most representative title TODO

    }

    return render_template("category.html",
        categories=Topic._member_names_,
        channels=channels, 	    # list of dicts: all channels in the category, sorted by Subs
        category=category, 			# dict: info about the category
        category_display={
            "Subs/Channel: ": category["avg_subs"],
            "Views/Video: ": category["avg_views"],
            "Videos/Channel: ": category["avg_video_count"],
        },
        subview_mode=subview_mode,	# "thumbnail" or "title"
        videos=videos[:30],			# list of dicts: all videos (or maybe top-n if computation requires it) in the category, sorted by views
    )


@main.route('/channel', methods=['GET'])
def channel():
    chan = request.args.get("channel")
    subview_mode = request.args.get("subview_mode")

    # I don't know if we need a default, but let's just for whatever sake
    if not chan:
        chan = "pewdiepie"
    if not subview_mode:
        subview_mode = "thumbnail"

    channel2cat_path = os.path.join(DATA_DIR, "channel2category.json")
    with open(channel2cat_path, "r") as f:
        channels2cat = json.load(f)
    cat = channels2cat[chan]

    # Get channels info
    channels_info_path = os.path.join(DATA_DIR, "info_channels", f"channels-info_{cat}.json")
    with open(channels_info_path, "r") as f:
        channels_dict = json.load(f)

    # Get videos info
    videos_info_path = os.path.join(DATA_DIR, "info_videos", f"videos-info_{cat}.json")
    with open(videos_info_path, "r") as f:
        videos_dict = json.load(f)

    # Get dictionary to translate video ids to channel names (useful for e.g. most representative title)
    vid2channel_path = os.path.join(DATA_DIR, "vid2channel.json")
    with open(vid2channel_path, "r") as f:
        vid2channel = json.load(f)

    videos = videos_dict[chan]
    videos.sort(key=lambda x: x["views"], reverse=True)

    channel_info = channels_dict[chan]
    channel_info["avg_views"]	   = np.mean([vid["views"] for vid in videos])
    channel_info["vids_available"] = len(videos)

    all_channels = []
    for name, info in channels_dict.items():
        all_channels.append({
            "name": name,
            **info
        })

    # TODO write code to calculate the most similar channels based on either thumbnail or title
    # Load the most similar channels
    similar_thumbnails_path = os.path.join(DATA_DIR, "thumbnail_similars", f"{cat}_similars.json")
    with open(most_repr_thumbnail_path, "r") as f:
        sim_chans_thumbnail = json.load(f)

    most_repr_title_path = os.path.join(DATA_DIR, "title_similars", f"{cat}_similars.json")
    with open(most_repr_title_path, "r") as f:
        sim_chans_title = json.load(f)

    most_sim_chans_thumbnail = sim_chans_thumbnail[chan]
    most_sim_chans_thumbnail = dict(sorted(most_sim_chans_thumbnail.items(), key=lambda item: item[1]))

    most_sim_chans_title = sim_chans_title[chan]
    most_sim_chans_title = dict(sorted(most_sim_chans_title.items(), key=lambda item: item[1]))

    # Load in the video id of the videos with the most representative thumbnails
    most_repr_thumbnail_path = os.path.join(DATA_DIR, "thumbnail_representatives", f"{cat}_representatives.json")
    with open(most_repr_thumbnail_path, "r") as f:
        most_repr_thumbnail_data = json.load(f)

    # Load in the video ids of the videos with the most representative titles
    most_repr_title_path = os.path.join(DATA_DIR, "title_representatives", f"{cat}_representatives.json")
    with open(most_repr_title_path, "r") as f:
        most_repr_title_data = json.load(f)

    # Get the most representative title and thumbnail for this category specifically
    title_repr_id = most_repr_title_data[chan]
    thumbnail_repr_id = most_repr_thumbnail_data[chan]

    most_repr_title = next(vid for vid in videos if vid["id"]==title_repr_id)["title"]
    most_repr_thumbnail_path = os.path.join(DATA_DIR, f"thumbnails/{thumbnail_repr_id}_high.jpg")

    # TODO Actual code (WIP)
    # # THUMBNAIL
    # channel_info["avg_thumbnail"]: os.path.join(DATA_DIR, f"thumbnail-averages/categories/{cat}_average.png") # str: path to avg thumbnail
    # channel_info["repr_thumbnail"]: most_repr_thumbnail_path # str: path to most representative thumbnail
    # channel_info["dominant_colors"]: {"#ffaa99": 36.5, "#00ff00": 11.7} # dict: keys are color clusters, values are percentage TODO
    # channel_info["object_effectiveness"]: {"person": 11.3, "cat": 3.5, "tie": -5.3} # dict: keys are objects, values are percentage (delta/avg_views_without) TODO
    # # TITLE
    # channel_info["repr_title"]: most_repr_title # str: most representative title
    # channel_info["token_count"]: {"token1": 13000, "token2": 5000} # dict: keys are tokens, values are the count TODO
    # channel_info["token_effectiveness"]: {"$10,000": 11.3, "best": 3.5, "books": -5.3} # dict: keys are tokens, values are percentage (delta/avg_views_without) TODO
    # MISC
    # channel_info["most_similar_channels_title"] = most_sim_chans_title
    # channel_info["most_similar_channels_thumbnail"] = most_sim_chans_thumbnail

    # Hardcoded examples
    # THUMBNAIL
    channel_info["avg_thumbnail"]: os.path.join("static", "data", "thumbnail-averages", "channels", "a4.png") # str: path to avg thumbnail TODO
    channel_info["repr_thumbnail"]: os.path.join("static", "data", "thumbnails", "___OSEsR5pk_high.jpg") # str: path to most representative thumbnail TODO
    # channel_info["dominant_colors"]: {"#ffaa99": 36.5, "#00ff00": 11.7} # dict: keys are color clusters, values are percentage TODO
    # channel_info["object_effectiveness"]: {"person": 11.3, "cat": 3.5, "tie": -5.3} # dict: keys are objects, values are percentage (delta/avg_views_without) TODO
    # TITLE
    # channel_info["repr_title"]: "This is a title" # str: most representative title TODO
    # channel_info["token_count"]: {"token1": 13000, "token2": 5000} # dict: keys are tokens, values are the count TODO
    # channel_info["token_effectiveness"]: {"$10,000": 11.3, "best": 3.5, "books": -5.3} # dict: keys are tokens, values are percentage (delta/avg_views_without) TODO
    # MISC
    # channel_info["most_similar_channels_title"] = ["pewdiepie", "penguinz0", "sssniperwolf"]
    # channel_info["most_similar_channels_thumbnail"] = ["pewdiepie", "penguinz0", "sssniperwolf"]

    return render_template("channel.html",
        categories=["gaming", "howto", "science", "autos", "blogs"],
        channel_info=channel_info,
        channels=all_channels[:20], 			# list of dicts: all channels in the category, sorted by Subs
        channel_display={
            "Subs/Channel: ": channel_info["Subscribers"],
            "Views/Video: ": channel_info["avg_views"],
            "Videos/Channel: ": channel_info["Video count"],
        },
        subview_mode=subview_mode,	# "thumbnail" or "title"
        videos=videos[:20],			# list of dicts: all videos (or maybe top-n if computation requires it) in the category, sorted by views
    )


# API for getting data for the dominant colour pie chart
@main.route('/get_dom_colour_data', methods = ['GET'])
def get_dom_colour_data():

    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        # Get category dom colours
        colour_data_path = os.path.join(DATA_DIR, "thumbnail-dom-colours", "categories", f"{category}.json")
    elif channel:
        # Get channel dom colours
        colour_data_path = os.path.join(DATA_DIR, "thumbnail-dom-colours", "channels", f"{channel}.json")

    with open(colour_data_path, "r") as f:
        colour_data = f.read()

    return colour_data


def calc_effectiveness(views, counts, min_count):
    avg_views = np.array(list(views.values())).mean()
    eff = {t:views[t]/c
        for t,c in counts.items() if c > min_count}
    eff = [{"group":t, "value":e/avg_views}
        for t,e in sorted(eff.items(), key=lambda x:x[1],reverse=True)]
    return eff


# API for getting data for the token effectiveness plot
@main.route('/get_title_effectiveness_data', methods = ['GET'])
def get_token_effectiveness_data():

    category = request.args.get("category")
    channel = request.args.get("channel")
    min_count = request.args.get("min_count")
    if not min_count:
        min_count = 1000

    if category:
        token_data_path = os.path.join(DATA_DIR, "title-tokens", "categories", f"{category}.json")
    elif channel:
        token_data_path = os.path.join(DATA_DIR, "title-tokens", "channels", f"{channel}.json")

    with open(token_data_path, "r") as f:
        token_data = json.load(f)

    views = token_data[f"token_views"]
    counts = token_data[f"token_counts"]

    return json.dumps(calc_effectiveness(views, counts, min_count))


# API for getting data for the tooltip in the token effectiveness plot
@main.route('/get_token_tooltip_data', methods = ['GET'])
def get_token_tooltip_data():

    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        token_data_path = os.path.join(DATA_DIR, "title-tokens", "categories_inv_index", f"{category}.json")
    elif channel:
        token_data_path = os.path.join(DATA_DIR, "title-tokens", "channels_inv_index", f"{channel}.json")

    with open(token_data_path, "r") as f:
        token_data = f.read()

    return token_data


# API for getting data for the thumbnail effectiveness plot
@main.route('/get_thumbnail_effectiveness_data', methods = ['GET'])
def get_thumbnail_effectiveness_data():

    category = request.args.get("category")
    channel = request.args.get("channel")
    min_count = request.args.get("min_count")
    if not min_count:
        min_count = 100

    if category:
        thumbnail_data_path = os.path.join(DATA_DIR, "thumbnail-objects", "categories", f"{category}.json")
    elif channel:
        thumbnail_data_path = os.path.join(DATA_DIR, "thumbnail-objects", "channels", f"{channel}.json")

    with open(thumbnail_data_path, "r") as f:
        thumbnail_data = json.load(f)

    views = thumbnail_data[f"object_views"]
    counts = thumbnail_data[f"object_counts"]

    return json.dumps(calc_effectiveness(views, counts, min_count))


# API for getting data for the tooltip in the thumbnail effectiveness plot
@main.route('/get_thumbnail_tooltip_data', methods = ['GET'])
def get_thumbnail_tooltip_data():
    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        thumbnail_data_path = os.path.join(DATA_DIR, "thumbnail-objects", "categories_inv_index", f"{category}.json")
    elif channel:
        thumbnail_data_path = os.path.join(DATA_DIR, "thumbnail-objects", "channels_inv_index", f"{channel}.json")

    with open(thumbnail_data_path, "r") as f:
        thumbnail_data = f.read()

    return thumbnail_data


# API for getting data for the thumbnail average image
@main.route('/get_thumbnail_average_img', methods = ['GET'])
def get_thumbnail_average_img():
    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        avg_img_data_path = os.path.join("..", "data", "thumbnail-averages", "categories", f"{category}.png")
    elif channel:
        avg_img_data_path = os.path.join("..", "data", "thumbnail-averages", "channels", f"{channel}.png")

    return send_file(avg_img_data_path, mimetype='image/png')



# API for getting data for the most representative thumbnail
@main.route('/get_most_repr_thumbnail', methods = ['GET'])
def get_most_repr_thumbnail():
    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        most_repr_thumbnail_path = os.path.join(DATA_DIR, "thumbnail-latents", "categories_best_repr.json")
        view = category
    elif channel:
        most_repr_thumbnail_path = os.path.join(DATA_DIR, "thumbnail-averages", "channels_best_repr.json")
        view = channel

    with open(most_repr_thumbnail_path, "r") as f:
        most_repr_thumbnail_file = json.load(f)
    
    most_repr_thumbnail = most_repr_thumbnail_file[view]["vid_id"]
    
    url = "https://i.ytimg.com/vi/" + most_repr_thumbnail + "/hqdefault.jpg"
    img = Image.open(requests.get(url, stream=True).raw)
    img = crop_black_border_img(np.array(img))
    img = Image.fromarray(img)
    img_path = os.path.join("app", "static", "data", "temp_repr_thumbnail.jpg")
    img.save(img_path)

    return send_file(os.path.join("static", "data", "temp_repr_thumbnail.jpg"), mimetype='image/jpg')


# API for getting data for the most representative title
@main.route('/get_most_repr_title', methods = ['GET'])
def get_most_repr_title():
    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        most_repr_title_path = os.path.join(DATA_DIR, "title-latents", "categories_best_repr.json")
        view = category
    elif channel:
        most_repr_title_path = os.path.join(DATA_DIR, "title-averages", "channels_best_repr.json")
        view = channel

    with open(most_repr_title_path, "r") as f:
        most_repr_thumbnail_file = json.load(f)
    
    most_repr_thumbnail = most_repr_thumbnail_file[view]

    return most_repr_thumbnail


# API for getting data for the title std plot
@main.route('/get_title_std_plot_data', methods = ['GET'])
def get_title_std_plot_data():

    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        std_data_path = os.path.join(DATA_DIR, "title-latents", "categories_plot_data", f"{category}.json")
    #TODO same json for channels
    elif channel:
        std_data_path = os.path.join(DATA_DIR, "title-latents", "channels_plot_data", f"{channel}.json")

    with open(std_data_path, "r") as f:
        std_data = f.read()

    return std_data


# API for getting data for the thumbnail std plot
@main.route('/get_thumbnail_std_plot_data', methods = ['GET'])
def get_thumbnail_std_plot_data():

    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        std_data_path = os.path.join(DATA_DIR, "thumbnail-latents", "categories_plot_data", f"{category}.json")
    #TODO same json for channels
    elif channel:
        std_data_path = os.path.join(DATA_DIR, "title-latents", "channels", f"{channel}.json")

    with open(std_data_path, "r") as f:
        std_data = f.read()

    return std_data