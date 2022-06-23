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
	title_view = request.args.get("title_view")

	if not cat:
		cat = "gaming"

	channels_info_path = os.path.join(DATA_DIR, f"channels-info_{cat}.json")
	with open(channels_info_path, "r") as f:
		channels_dict = json.load(f)
	channels = [{"name": name, **info} for name,info in channels_dict.items()]

	return render_template("category.html", channels=channels[:5], category={"name": cat, "subs": 190000})


