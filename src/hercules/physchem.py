# hercules/physchem.py
import ast
import csv
import numpy as np
from glob import glob
from importlib.resources import files
import json

def transformSecDict(seq,dicto):
    # takes in a sequence seq  and a dictionary 'char_to_number'  and build up the list of numbers
    seq=list(seq)

    # Transform the characters into consecutive numbers
    return  [dicto[char] for char in seq]

def transformSeqFromJson(seq,file_name, smth = 7):

    # take a json file where there is a dictiopnary of aminoacid substitution

    # Open the file for reading
    with open(file_name, "r") as file:
        # Load the JSON data from the file and parse it into a dictionary
        loaded_dict = json.load(file)

    # Now, 'loaded_dict' contains the dictionary loaded from the JSON file
    #print(loaded_dict)

    return smooth(np.array(transformSecDict(seq,loaded_dict)),smth)


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

def compute_chemphysProfiles(seq,listofscalesJSON, smth=1, chargeNorm=False):

    profiles=[]
    for i in listofscalesJSON:
        if chargeNorm:
            if 'charge' in i:

                profiles.append(smooth((trasformSeqFromJson(seq,i, smth=1)+1)/2,smth))
            else:
                profiles.append(trasformSeqFromJson(seq,i, smth=smth))
        else:
            profiles.append(trasformSeqFromJson(seq,i, smth=smth))

    return np.array(profiles)

def load_physchem():
    scale_dir = files("hercules.data") / "chemphys_scales"
    scales = glob(str(scale_dir / "*.json"))

    names = [s.split("/")[-1].replace(".json", "") for s in scales]

    en_path = files("hercules.data") / "elasticnet.csv"
    EN = {}
    with open(en_path) as f:
        for k, v in csv.reader(f):
            EN[k] = v

    selected = ast.literal_eval(EN["selected_features"])
    weights = np.array(
        [float(x) for x in EN["weights"].strip("[]").split()]
    )

    idx = {n: i for i, n in enumerate(names)}
    selected_idx = np.array([idx[f] for f in selected])

    return scales, selected_idx, weights
