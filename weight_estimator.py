"""
Estimate the regional weights for relative frequency of publictions
"""
import os
import glob
import json
import re
import numpy as np
from collections import Counter
import pandas as pd


def delete_pattern(s, pattern):
    pat = re.compile(r"{}".format(pattern))
    return re.sub(pat, "", s)


def extract_region(fnames):
    regions = list()
    for i, fname in enumerate(fnames):
        with open(fname) as f:
            content = json.load(f)
            region = content["meta"]["Regions"][0]
            region = delete_pattern(region, "Region ")
            if region != "Udenlandske":
                regions.append(region)
    return regions


flatten = lambda l: [item for sublist in l for item in sublist]


def sample_list(l, n=100, N=1000):
    samples = list()
    for i in range(N):
        samples.append(np.random.choice(l, n))
    return samples


def main():
    filenames = glob.glob(os.path.join("data", "*.json"))
    REGION = extract_region(filenames)
    samples = flatten(sample_list(REGION))
    counter = Counter(samples)
    counts = list(counter.values())
    names = list(counter.keys())
    w = len(samples)
    counts_relative = [val/w for val in counts]
    df = pd.DataFrame()
    df["region"] = names
    df["counts"] = counts
    df["counts-relative"] = counts_relative
    df.to_csv(os.path.join("output", "weights.csv"), index=False)


if __name__ == '__main__':
    main()
