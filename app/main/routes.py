from collections import defaultdict
from flask import render_template, request, jsonify, send_from_directory
import os, json, sys
import re
import requests
from PIL import Image

from decimal import Decimal

import pandas as pd
import numpy as np
import math

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

with open(os.path.join(DATA_DIR, "vid2channel.json"), "r") as f:
    VID2CHANNEL = json.load(f)
with open(os.path.join(DATA_DIR, "channel2category.json"), "r") as f:
    CHANNEL2CAT = json.load(f)
with open(os.path.join(DATA_DIR, "channel-name2id.json"), "r") as f:
    CHANNEL2ID = json.load(f)

def format_channel_name(name):
    return re.sub(r"-?([A-z0-9]){8}-([A-z0-9]){4}-([A-z0-9]){4}-([A-z0-9]){4}-([A-z0-9]){12}", "", name)

VID_DICT = {}
CHANNELS_INFO_BY_CAT = defaultdict(dict)
for cat in Topic._member_names_:
    with open(os.path.join(DATA_DIR, "info_videos", f"videos-info_{cat}.json"), "r") as f:
        VID_DICT.update({vid["id"]:{"channel":chan, **vid} for chan,vids in json.load(f).items() for vid in vids})
    with open(os.path.join(DATA_DIR, "info_channels", f"channels-info_{cat}.json"), "r") as f:
        CHANNELS_INFO_BY_CAT[cat] = {k:{
            "name_id": k,
            "name": format_channel_name(k),
            **v,
        } for k,v in sorted(json.load(f).items(), key=lambda x:x[1]["Subscribers"], reverse=True)}


@main.route('/', methods=['GET'])
def base():
    return redirect('/category/gaming?subview_mode=title')


@main.route('/category/<cat>', methods=['GET'])
def category(cat):
    subview_mode = request.args.get("subview_mode")

    if not cat:
        cat = "gaming"
    if not subview_mode:
        subview_mode = "title"

    channels_dict = CHANNELS_INFO_BY_CAT[cat]

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

    cat_avg_subs = int(np.mean([info["Subscribers"] for info in channels_dict.values()]))
    cat_avg_views = int(np.mean([info["avg_views"] for info in channels_dict.values() if "avg_views" in info]))
    cat_avg_vids = int(np.mean([info["Video count"] for info in channels_dict.values()]))

    category = {
        "name": cat, 		  # str: name of category
        "avg_subs": cat_avg_subs,   # int: avg subs per channel in cat
        "avg_views": cat_avg_views, # int: avg views per video in cat
        "avg_video_count": cat_avg_vids, # int: avg amount of videos per channel in cat
    }

    return render_template("category.html",
        view="category",
        categories=Topic._member_names_,
        channels=[c for c in channels_dict.values() if c["name_id"] in videos_dict], 	    # list of dicts: all channels in the category, sorted by Subs
        category=category, 			# dict: info about the category
        info_display={
            "Subs/Channel: ": category["avg_subs"],
            "Views/Video: ": category["avg_views"],
            "Videos/Channel: ": category["avg_video_count"],
        },
        subview_mode=subview_mode,	# "thumbnail" or "title"
        videos=videos[:30],			# list of dicts: all videos (or maybe top-n if computation requires it) in the category, sorted by views
    )


@main.route('/channel/<chan>', methods=['GET'])
def channel(chan):
    cat = CHANNEL2CAT[chan]
    subview_mode = request.args.get("subview_mode")

    if not subview_mode:
        subview_mode = "title"

    channels_dict = CHANNELS_INFO_BY_CAT[cat]

    # Get videos info
    videos_info_path = os.path.join(DATA_DIR, "info_videos", f"videos-info_{cat}.json")
    with open(videos_info_path, "r") as f:
        videos_dict = json.load(f)

    videos = videos_dict[chan] if chan in videos_dict else []
    videos.sort(key=lambda x: x["views"], reverse=True)

    channel_info = channels_dict[chan]
    channel_info["name"]           = format_channel_name(chan)
    channel_info["avg_views"]	   = np.mean([vid["views"] for vid in videos])
    channel_info["vids_available"] = len(videos)

    return render_template("category.html",
        view="channel",
        categories=Topic._member_names_,
        category={"name": cat},
        channel=channel_info,
        channels=[c for c in channels_dict.values() if c["name_id"] in videos_dict], 			# list of dicts: all channels in the category, sorted by Subs
        info_display={
            "Subscribers: ": channel_info["Subscribers"],
            "Views/Video: ": channel_info["avg_views"],
            "Num Videos: ": channel_info["Video count"],
        },
        subview_mode=subview_mode,	# "thumbnail" or "title"
        videos=videos,			# list of dicts: all videos (or maybe top-n if computation requires it) in the category, sorted by views
    )


###############################################################################
# APIs
###############################################################################


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
        for t,c in counts.items() if c > int(min_count)}
    eff = [{
            "group": t, 
            "value": e/avg_views,
            "count": counts[t],
            "avg_views": int(e),
        } for t,e in sorted(eff.items(), key=lambda x:x[1],reverse=True)]

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
@main.route('/get_title_tooltip_data', methods = ['GET'])
def get_token_tooltip_data():

    category = request.args.get("category")
    channel = request.args.get("channel")
    token = request.args.get("group")

    if category:
        token_data_path = os.path.join(DATA_DIR, "title-tokens", "categories_inv_index", f"{category}.json")
    elif channel:
        token_data_path = os.path.join(DATA_DIR, "title-tokens", "channels_inv_index", f"{channel}.json")

    with open(token_data_path, "r") as f:
        inv_idx = json.load(f)

    id_list = inv_idx[token] if token in inv_idx else []
    if not id_list:
        return "[]"

    vid_list = [VID_DICT[id] for id in id_list]
    vid_list = sorted(vid_list, key=lambda x:x["views"],reverse=True)[:5]
    return json.dumps(vid_list)


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
    object = request.args.get("group")

    if category:
        thumbnail_data_path = os.path.join(DATA_DIR, "thumbnail-objects", "categories_inv_index", f"{category}.json")
    elif channel:
        thumbnail_data_path = os.path.join(DATA_DIR, "thumbnail-objects", "channels_inv_index", f"{channel}.json")

    with open(thumbnail_data_path, "r") as f:
        inv_idx = json.load(f)

    id_list = inv_idx[object] if object in inv_idx else []
    if not id_list:
        return "[]"

    vid_list = [VID_DICT[id] for id in id_list]
    vid_list = sorted(vid_list, key=lambda x:x["views"],reverse=True)[:5]
    return json.dumps(vid_list)


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
        most_repr_thumbnail_path = os.path.join(DATA_DIR, "thumbnail-latents", "channels_best_repr.json")
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
        most_repr_title_path = os.path.join(DATA_DIR, "title-latents", "channels_best_repr.json")
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
        with open(std_data_path, "r") as f:
            std_data = json.load(f)
    elif channel:
        std_data_path = os.path.join(DATA_DIR, "title-latents", "video_deviation", f"{channel}.json")
        with open(std_data_path, "r") as f:
            std_data = json.load(f)
        std_data["datapoints"] = [{
            "thumbnail": f"https://i.ytimg.com/vi/{d['id']}/default.jpg",
            **VID_DICT[d["id"]],
            **d
        } for d in std_data["datapoints"]]

    if math.isnan(std_data["mean"]):
        std_data["datapoints"] = [d for d in std_data["datapoints"] if not math.isnan(d["x"])]
        std_data["mean"] = np.array([d["x"] for d in std_data["datapoints"] if not math.isnan(d["x"])]).mean()

    return json.dumps(std_data)


# API for getting data for the thumbnail std plot
@main.route('/get_thumbnail_std_plot_data', methods = ['GET'])
def get_thumbnail_std_plot_data():

    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        std_data_path = os.path.join(DATA_DIR, "thumbnail-latents", "categories_plot_data", f"{category}.json")
        with open(std_data_path, "r") as f:
            std_data = json.load(f)
    elif channel:
        std_data_path = os.path.join(DATA_DIR, "thumbnail-latents", "video_deviation", f"{channel}.json")
        with open(std_data_path, "r") as f:
            std_data = json.load(f)
        std_data["datapoints"] = [{
            "thumbnail": f"https://i.ytimg.com/vi/{d['id']}/default.jpg",
            **VID_DICT[d["id"]],
            **d
        } for d in std_data["datapoints"]]
        

    if math.isnan(std_data["mean"]):
        std_data["datapoints"] = [d for d in std_data["datapoints"] if not math.isnan(d["x"])]
        std_data["mean"] = np.array([d["x"] for d in std_data["datapoints"] if not math.isnan(d["x"])]).mean()

    return json.dumps(std_data)


# API for getting data for the word cloud
@main.route('/get_word_cloud_data', methods = ['GET'])
def get_word_cloud_data():

    category = request.args.get("category")
    channel = request.args.get("channel")

    if category:
        token_count_path = os.path.join(DATA_DIR, "title-tokens", "categories", f"{category}.json")
        token_tf_idf_path = os.path.join(DATA_DIR, "title-tokens", "categories_tf_idf", f"{category}.json")
    elif channel:
        token_count_path = os.path.join(DATA_DIR, "title-tokens", "channels", f"{channel}.json")
        token_tf_idf_path = os.path.join(DATA_DIR, "title-tokens", "channels_tf_idf", f"{channel}.json")

    with open(token_count_path, "r") as f:
        token_count = json.load(f)

    with open(token_tf_idf_path, "r") as f:
        token_tf_idf = json.load(f)

    counts = token_count["token_counts"]

    word_cloud_dict = {}

    count_array = np.array(list(counts.values()))
    tfidf_array = np.array(list(token_tf_idf.values()))
    avg_count = count_array.mean()
    median_tfidf = tfidf_array.mean()
    word_cloud_dict["count_range"] = [float(count_array.min()), float(count_array.max())]
    word_cloud_dict["tfidf_range"] = [float(tfidf_array.min()), float(tfidf_array.max())]

    multiplier = 1
    if channel:
        multiplier = 50

    print("INFO", avg_count, median_tfidf, file=sys.stderr)

    word2size = {}; word2color = {}
    for key in [token for token,_ in sorted(token_tf_idf.items(), key=lambda x:x[1], reverse=True) if len(token) > 1][:100]:
        word2size[key] = token_tf_idf[key] /median_tfidf/3 * multiplier
        word2color[key] = counts[key] /avg_count/7 * multiplier
    word_cloud_dict["size"] = word2size
    word_cloud_dict["color"] = word2color

    return json.dumps(word_cloud_dict)