import pathlib
import sys
import matplotlib.pyplot as plt
import mplhep
import numpy as np
import yaml

# parameters to include (TRExFitter names)
POI_NAMES = [
    "ttH_ptH_0_60",
    "ttH_ptH_60_120",
    "ttH_ptH_120_200",
    "ttH_ptH_200_300",
    "ttH_ptH_300_450",
    "ttH_ptH_gt450",
]

LABELS = [
    r"$\sigma_{t\bar{t}H}$ [0, 60] GeV",
    r"$\sigma_{t\bar{t}H}$ [60, 120] GeV",
    r"$\sigma_{t\bar{t}H}$ [120, 200] GeV",
    r"$\sigma_{t\bar{t}H}$ [200, 300] GeV",
    r"$\sigma_{t\bar{t}H}$ [300, 450] GeV",
    r"$\sigma_{t\bar{t}H}$ [450, $\infty$] GeV",
]

LABEL_FONT_SIZE = 15

TICK_LINEWIDTH = 1.0


def set_plot_style():
    """Set the plot style using mplhep."""
    plt.style.use(mplhep.style.ATLAS)


def load_correlation_matrix(filepath):
    """Load the correlation matrix from YAML file."""
    try:
        corr_mat_info = yaml.safe_load(pathlib.Path(filepath).read_text())
        return corr_mat_info
    except Exception as e:
        print(f"Error loading correlation matrix file: {e}")
        sys.exit(1)


def reorder_parameters(par_names, corr_mat, poi_names):
    """Reorder parameters and correlation matrix based on POI_NAMES.

    Ensures we only use parameters that are in the list of POI_NAMES
    and in that same specified order.
    """
    indices = [par_names.index(name) for name in poi_names if name in par_names]
    par_names = [par_names[i] for i in indices]
    corr_mat = corr_mat[np.ix_(indices, indices)]
    return par_names, corr_mat


def set_yaxis_labels(ax, labels, fontsize):
    """Set y-axis labels."""
    ax.set_yticklabels([])
    for i, label in enumerate(labels):
        ax.text(
            -0.02,
            i,
            label,
            va="center",
            ha="right",
            transform=ax.get_yaxis_transform(),
            fontsize=fontsize,
        )


def plot_correlation_matrix(corr_mat, labels, output_file):
    """Plot corr. matrix and save fig."""
    n_labels = len(labels)
    tick_locs = np.arange(n_labels) - 0.5

    fig, ax = plt.subplots(layout="constrained")
    im = ax.imshow(
        corr_mat,
        vmin=-1,
        vmax=1,
        cmap="RdBu",
        extent=(-0.5, n_labels - 0.5, n_labels - 0.5, -0.5),
    )
    mplhep.atlas.text(text="Internal", loc=0, ax=ax)

    for spine in ax.spines.values():
        spine.set_linewidth(TICK_LINEWIDTH)

    ax.set_xticks(tick_locs)
    ax.set_yticks(tick_locs)
    ax.set_xticklabels(labels, rotation=45, ha="center", fontsize=LABEL_FONT_SIZE)
    set_yaxis_labels(ax, labels, LABEL_FONT_SIZE)

    ax.tick_params(
        axis="both",
        which="major",
        length=8,
        width=TICK_LINEWIDTH,
        bottom=True,
        top=True,
        left=True,
        right=True,
    )
    ax.tick_params(axis="both", which="minor", length=0)
    ax.tick_params(axis="x", which="major", pad=6)

    ax.set_xticks(np.arange(n_labels), minor=True)
    ax.set_yticks(np.arange(n_labels), minor=True)
    fig.colorbar(im, ax=ax)
    ax.set_aspect("auto")
    ax.text(
        2.87,
        -0.58,
        r"$\sqrt{s}\, =\, 13\,\mathrm{TeV},\, 140\, \mathrm{fb}^{-1}$",
        fontsize=16,
        style="normal",
    )

    for (j, i), corr in np.ndenumerate(corr_mat):
        text_color = "white" if abs(corr) > 0.75 else "black"
        if abs(corr) > 0.005:
            ax.text(i, j, f"{corr:.2f}", ha="center", va="center", color=text_color)

    fig.savefig(output_file)


def main():
    set_plot_style()
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_CorrelationMatrix.yaml>")
        sys.exit(1)

    filepath = sys.argv[1]
    corr_mat_info = load_correlation_matrix(filepath)
    par_names = corr_mat_info[0]["parameters"]
    corr_mat = np.asarray(corr_mat_info[1]["correlation_rows"])

    par_names, corr_mat = reorder_parameters(par_names, corr_mat, POI_NAMES)

    plot_correlation_matrix(corr_mat, LABELS, "POI_correlations.pdf")


if __name__ == "__main__":
    main()
