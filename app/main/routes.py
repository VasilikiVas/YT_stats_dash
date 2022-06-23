from flask import render_template, request, jsonify, send_from_directory
import os, json, sys

from decimal import Decimal

import pandas as pd
import numpy as np

from . import main

DATA_DIR = os.path.join("data")

@main.route('/', methods=['GET'])
@main.route('/category', methods=['GET'])
def category():
	cat = request.args.get("category")
	subview_mode = request.args.get("subview_mode")

	if not cat:
		cat = "gaming"
	if not subview_mode:
		subview_mode = "thumbnail"

	# Get channels info
	channels_info_path = os.path.join(DATA_DIR, f"channels-info_{cat}.json")
	with open(channels_info_path, "r") as f:
		channels_dict = json.load(f)

	# Get videos info
	videos_info_path = os.path.join(DATA_DIR, f"videos-info_{cat}.json")
	with open(videos_info_path, "r") as f:
		videos_dict = json.load(f)
	videos = []
	for name, videos in videos_dict.items():
		for vid in videos:
			videos.append({"channel": name, **vid})
		channels_dict[name]["avg_views"]	  = np.mean([vid["views"] for vid in videos])
		channels_dict[name]["vids_available"] = len(videos)

	channels = []
	for name, info in channels_dict.items():
		channels.append({
			"name": name,
			"thumbnail_std": None, # TODO
			"title_std": None, 	   # TODO
			**info
		})

	category = {
		"name": cat, 		  # str: name of category
		"avg_subs": 190000,   # int: avg subs per channel in cat TODO
		"avg_views": 1200000, # int: avg views per video in cat TODO
		# THUMBNAIL
		"avg_thumbnail": os.path.join(DATA_DIR, "thumbnail-averages-gaming", "1c63394b-91b6-4f7e-9e53-58c4318200da.png"), # str: path to avg thumbnail TODO
		"repr_thumbnail": os.path.join(DATA_DIR, "thumbnails", "___OSEsR5pk_high.jpg"), # str: path to most representative thumbnail TODO
		"dominant_colors": {"#ffaa99": 36.5, "#00ff00": 11.7}, # dict: keys are color clusters, values are percentage TODO
		"object_effectiveness": {"person": 11.3, "cat": 3.5, "tie": -5.3}, # dict: keys are objects, values are percentage (delta/avg_views_without) TODO
		# TITLE
		"repr_title": "This is a title", # str: most representative title TODO
		"token_count": {"token1": 13000, "token2": 5000}, # dict: keys are tokens, values are the count TODO
		"token_effectiveness": {"$10,000": 11.3, "best": 3.5, "books": -5.3}, # dict: keys are tokens, values are percentage (delta/avg_views_without) TODO
	}

	return render_template("category.html", 
		channels=channels, 			# list of dicts: all channels in the category, sorted by Subs
		category=category, 			# dict: info about the category
		subview_mode=subview_mode,	# "thumbnail" or "title"
		videos=videos,				# list of dicts: all videos (or maybe top-n if computation requires it) in the category, sorted by views
	)


@main.route('/video', methods=['GET'])
def video():
	vid_id = request.args.get("video")
	channel_name = request.args.get("channel")
	subview_mode = request.args.get("subview_mode")

	if not vid_id:
		pass # TODO show error message and redirect
	if not subview_mode:
		subview_mode = "thumbnail"

	video = {
		"id": vid_id, # str: video id
		"thumbnail_sim_videos": list(), # list of dicts: top-n videos sorted by thumbnail similarity
		"title_sim_videos": list(), # list of dicts: top-n videos sorted by title similarity
	}

	channel = {}

	return render_template("video.html", 
		video=video, 			    # dict: info about the video
		channel=channel,			# dict: info about the video's channel
		subview_mode=subview_mode,	# "thumbnail" or "title"
	)

