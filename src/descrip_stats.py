import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import matplotlib as mpl

mpl.rcParams.update(
    {'text.usetex': True, 'font.family': 'serif', 'font.serif': 'cmr10',
        'font.weight': 'bold', 'mathtext.fontset': 'cm',
        'axes.unicode_minus': False}
        )

regions = pd.read_csv(os.path.join("output", "data.csv"))["region"].values

counter = Counter(regions)


print(counter)
y = list(counter.values())
names = counter.keys()

name_short = list()
for name in names:
    if " " in name:
        name = name.split()[-1]
    name_short.append(name)


x = np.arange(len(counter))

fig, ax = plt.subplots()
#ax.yaxis.set_major_formatter(formatter)
plt.bar(x, y, color="k")
plt.xticks(x, name_short, rotation=20)
plt.xlabel("Newspaper")
plt.ylabel("Frequency")
plt.title("News distribution of `Umbrella case'")
plt.tight_layout()
plt.savefig(os.path.join("fig", "region_hist.png"))


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct)


fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
wedges, texts, autotexts = ax.pie(
    y, autopct=lambda pct: func(pct, y), textprops=dict(color="w")
    )
ax.legend(wedges, names,
          title="Coverage",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
plt.setp(autotexts, size=8, weight="bold")
ax.set_title("News distribution of `Umbrella case'")
plt.tight_layout()
plt.savefig(os.path.join("fig", "region_pie.png"))
