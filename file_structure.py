"""
Export json content to dataframe

"""
import os
import glob
import json
import re
import pandas as pd


def clean_html(raw_html):
    """ removing html tags
    """
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)

    return cleantext


def json2csv(fnames, cutoff=2016):
    DF = pd.DataFrame()
    REGION, SOURCE, LANG, TITLE, DATE, BODY = [], [], [], [], [], []
    for i, fname in enumerate(fnames):
        with open(fname) as f:
            content = json.load(f)
            date = fname.split(" - ")[0].split("/")[1]
            if int(date.split("-")[0]) >= cutoff:
                main = content["content"]
                meta = content["meta"]
                # feature extraction
                REGION.append(meta["Regions"][0])
                # region = meta["Regions"][0]
                SOURCE.append(meta["Source"]["Name"])
                # source = meta["Source"]["Name"]
                LANG.append(meta["Language"])
                # lang = meta["Language"]
                TITLE.append(meta["Title"])
                # title = meta["Title"]
                DATE.append(date)
                # date = fname.split(" - ")[0].split("/")[1]
                BODY.append(clean_html(main["BodyText"]))
                # body = clean_html(main["BodyText"])
    DF["date"] = DATE
    DF["language"] = LANG
    DF["media"] = SOURCE
    DF["region"] = REGION
    DF["title"] = TITLE
    DF["content"] = BODY

    return DF


def main():
    filenames = glob.glob(os.path.join("data", "*.json"))
    df = json2csv(filenames)
    df.to_csv(os.path.join("output", "data.csv"), index=False, header=True)


if __name__ == '__main__':
    main()
