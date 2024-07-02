import pathlib
import sys

import matplotlib.pyplot as plt
import mplhep
import numpy as np
import yaml

plt.style.use(mplhep.style.ATLAS)


# parameters to include (TRExFitter names)
POI_NAMES = ["ttH_ptH_0_60", "ttH_ptH_60_120", "ttH_ptH_120_200", "ttH_ptH_200_300", "ttH_ptH_300_450", "ttH_ptH_gt450"]

LABEL_FONT_SIZE = 15
TICK_LINEWIDTH = 1.00

LABELS = [
    r"$\sigma_{t\bar{t}H}$ [0, 60] GeV",
    r"$\sigma_{t\bar{t}H}$ [60, 120] GeV",
    r"$\sigma_{t\bar{t}H}$ [120, 200] GeV",
    r"$\sigma_{t\bar{t}H}$ [200, 300] GeV",
    r"$\sigma_{t\bar{t}H}$ [300, 450] GeV",
    r"$\sigma_{t\bar{t}H}$ [450, $\infty$] GeV",

]  # latex labels

def set_yaxis_labels(ax, labels, fontsize):
    ax.set_yticklabels([])
    for i, label in enumerate(labels):
        ax.text(-0.02, i, label, va='center', ha='right', transform=ax.get_yaxis_transform(), fontsize=fontsize)

# point script to CorrelationMatrix.yaml file
corr_mat_info = yaml.safe_load(pathlib.Path(sys.argv[-1]).read_text())
par_names = corr_mat_info[0]["parameters"]
corr_mat = np.asarray(corr_mat_info[1]["correlation_rows"])

# reorder par_names and corr_mat based on the POI_NAMES via a list comprehension
indices = [par_names.index(name) for name in POI_NAMES if name in par_names]
par_names = [par_names[i] for i in indices]
corr_mat = corr_mat[np.ix_(indices, indices)]

n_labels = len(LABELS)
tick_locs = np.arange(n_labels) - 0.5

fig, ax = plt.subplots(layout="constrained")
im = ax.imshow(corr_mat, vmin=-1, vmax=1, cmap="RdBu", extent=(-0.5, n_labels - 0.5, n_labels - 0.5, -0.5))
mplhep.atlas.text(text="Internal", loc=0, ax=ax)

for spine in ax.spines.values():
    spine.set_linewidth(TICK_LINEWIDTH)

ax.set_xticks(tick_locs)
ax.set_yticks(tick_locs)
ax.set_xticklabels(LABELS, rotation=45, ha="center", fontsize=LABEL_FONT_SIZE)
set_yaxis_labels(ax, LABELS, LABEL_FONT_SIZE)

ax.tick_params(axis='both', which='major', length=8, width=TICK_LINEWIDTH, bottom=True, top=True, left=True, right=True)
ax.tick_params(axis='both', which='minor', length=0)
ax.tick_params(axis='x', which='major', pad=6)



ax.set_xticks(np.arange(n_labels), minor=True)
ax.set_yticks(np.arange(n_labels), minor=True)
fig.colorbar(im, ax=ax)
ax.set_aspect("auto")
ax.text(2.87, -0.58, r"$\sqrt{s}\, =\, 13\,\mathrm{TeV},\, 140\, \mathrm{fb}^{-1}$", fontsize=16, style="normal")

# add correlation as text
for (j, i), corr in np.ndenumerate(corr_mat):
    text_color = "white" if abs(corr_mat[j, i]) > 0.75 else "black"
    if abs(corr) > 0.005:
        ax.text(i, j, f"{corr:.2f}", ha="center", va="center", color=text_color)

fig.savefig("POI_correlations.pdf")
# fig.savefig("POI_correlations.png")


