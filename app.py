import json
import os
import os.path as osp
import random
from glob import glob

import flask
import numpy as np

app = flask.Flask(__name__)
DATA_DIR = "ablations"
OUTPUT_DIR = "outputs"

ABLATIONS_LIST = ["baseline", "collision", "depth", "interaction", "mask", "scale"]
CATEGORIES_LIST = ["bat", "bench", "bicycle", "laptop",
                   "motorcycle", "skateboard", "surboard", "tennis"]

with open(osp.join(DATA_DIR, "evaluation_ids.json")) as f:
    EVALUATION_IDS = json.load(f)


def get_anno_path(ablation, category):
    return osp.join(OUTPUT_DIR, f"{ablation}-{category}.json")


def get_anno_data(ablation, category):
    path = get_anno_path(ablation, category)
    if osp.exists(path):
        with open(path) as f:
            return json.load(f)
    else:
        return [-1] * 50


@app.route('/submit', methods=['POST'])
def submit():
    data = flask.request.json
    ablation = data["ablation"]
    category = data["category"]
    index = data["index"]
    annotation = data["annotation"]
    path = get_anno_path(ablation, category)
    data = get_anno_data(ablation, category)
    data[index] = annotation
    with open(path, "w") as f:
        json.dump(data, f)
    return flask.jsonify({}), 200


@app.route('/image/<ablation>/<category>/<index>')
def image(ablation, category, index):
    dirname = osp.join(DATA_DIR, category, ablation)
    index = int(index)
    fname = EVALUATION_IDS[category][index]
    path = glob(osp.join(dirname, f"{fname}*"))[0]
    return flask.send_from_directory(dirname, osp.basename(path))


@app.route('/<ablation>')
def available_categories(ablation):
    ready = {}
    for cat in CATEGORIES_LIST:
        if len(glob(osp.join(DATA_DIR, cat, ablation, "*.jpg"))) >= 50:
            annotations = get_anno_data(ablation, cat)
            if -1 in annotations:
                first_index = annotations.index(-1)
            else:
                first_index = 0
            num_unfinished = 50 - annotations.count(-1)
            ready[cat] = (first_index, num_unfinished)
    return flask.render_template("ablation_list.html",
                                 ablation=ablation,
                                 available_categories=ready)


@app.route("/<ablation>/<category>/<index>")
def evaluate(ablation, category, index):
    index = int(index)
    if index < 0 or index >= 50:
        return

    annotations = get_anno_data(ablation, category)
    num_unfinished = annotations.count(-1)
    current_annotation = annotations[index]
    ours = f"/image/ours/{category}/{index}"
    not_ours = f"/image/{ablation}/{category}/{index}"

    if random.random() < 0.5:
        left_image = ours
        right_image = not_ours
        left_is_ours = "is_ours"
        right_is_ours = ""
    else:
        left_image = not_ours
        right_image = ours
        left_is_ours = ""
        right_is_ours = "is_ours"

    if current_annotation == -1:  # not annotated yet
        left_highlight, right_highlight = "", ""
    elif current_annotation == 1:  # both
        left_highlight, right_highlight = "highlight", "highlight"
    elif current_annotation == 0:  # not ours better
        if left_is_ours:
            left_highlight, right_highlight = "", "highlight"
        else:
            left_highlight, right_highlight = "highlight", ""
    elif current_annotation == 2:  # ours better
        if left_is_ours:
            left_highlight, right_highlight = "highlight", ""
        else:
            left_highlight, right_highlight = "", "highlight"
    else:
        raise Exception(f"Unexpected annotation: {current_annotation}. [-1, 0, 1, 2]")

    image_metadata = {
        "ablation": ablation,
        "category": category,
        "index": index,
        "left_is_ours": bool(left_is_ours),
        "annotation": current_annotation,
    }

    return flask.render_template(
        "evaluate.html",
        left_image=left_image,
        right_image=right_image,
        left_highlight=left_highlight,
        right_highlight=right_highlight,
        left_is_ours=left_is_ours,
        right_is_ours=right_is_ours,
        image_metadata=image_metadata,
        num_unfinished=num_unfinished,
    )

@app.route("/")
def show_image():

    return flask.render_template(
        "index.html", ablations_list=ABLATIONS_LIST, len=len(ABLATIONS_LIST),
    )


if __name__ == "__main__":
    if not osp.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    app.run(host='0.0.0.0', port=29152)
