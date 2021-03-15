# Forced Choice Annotater for PHOSA

Code for running forced choice annotation for [PHOSA](https://jasonyzhang.com/phosa/).

### Setup

1. Install flask:
```
pip install flask
```

2. Start annotation server. Access the annotator at `localhost:29152`.
```
python app.py
```

### File Structure

The project directory should a directory called "ablations" with the following structure:
```
ablations
|__{category_name}
|  |__{ablation_name}
|__evaluation_ids.json
```
Where `category_name` is the name of the category (e.g. bat, bench, bicycle, etc) and
`ablation_name` is the name of the name of the loss being ablated (e.g. collision, depth,
mask, etc).

Each ablation directory should contain the rendered images where the beginning of the
file name is imageid.

The images corresponding independent composition should be placed in
`abalations/{category_name}/baseline`, and the images corresponding to PHOSA should be
placed in `ablations/{category_name}/ours`.

### Directions:
For each image, examine the two left and right image (presented in randomized order).

### Commands:
* w: prefer left
* r: prefer right
* e: equal/ no preference
* space: clear selection
* left: previous image
* right: next image
* enter: submit (left and right submit automatically)


### Credits:

Some parts of the code were borrowed from Achal Dave.
