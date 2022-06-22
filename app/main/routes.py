from flask import render_template, request, jsonify, send_from_directory
import os, json

from decimal import Decimal

import pandas as pd
import numpy as np

from . import main


@main.route('/', methods=['GET'])
def index():
	return render_template("index.html")
