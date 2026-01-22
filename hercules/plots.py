# hercules/plots.py
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from typing import Optional

AA_ORDER = list("ACDEFGHIKLMNPQRSTVWY")

def plot_profile(profile, protein_id: Optional[str] = None, global_score: Optional[float] = None):
    """
    Plot a single HERCULES RNA-binding profile.
    
    Parameters
    ----------
    profile : array-like
        HERCULES profile values
    protein_id : str, optional
        Protein identifier (shown in title)
    global_score : float, optional
        Global fused score (shown in title)
    """
    plt.figure(figsize=(12, 4))
    plt.plot(profile, color="steelblue", lw=2)
    title = ""
    if protein_id:
        title += f"{protein_id} "
    if global_score is not None:
        title += f"(global score = {global_score:.3f})"
    if title:
        plt.title(title)
    plt.xlabel("Position")
    plt.ylabel("HERCULES profile")
    plt.tight_layout()
    plt.show()


def plot_mutagenesis_heatmap(df):
    """
    Plot a heatmap from a mutagenesis scan DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Columns: position, wt, mutant, delta_score
    """
    heatmap_df = df.pivot(index="mutant", columns="position", values="delta_score")
    heatmap_df = heatmap_df.reindex(AA_ORDER)
    mask = heatmap_df.isna()
    
    plt.figure(figsize=(12, 6))
    sns.heatmap(
        heatmap_df,
        mask=mask,
        cmap="coolwarm",
        center=0,
        xticklabels=25,
        cbar_kws={"label": "Mutation score"}
    )
    plt.xlabel("Sequence position")
    plt.ylabel("Amino acid substitution")
    plt.tight_layout()
    plt.show()
