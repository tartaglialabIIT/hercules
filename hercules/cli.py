# hercules/cli.py
import argparse
from pathlib import Path
import pandas as pd

from hercules.api import profiles, global_fused_score, mutagenesis

def main():
    parser = argparse.ArgumentParser(
        description="HERCULES: RNA-binding propensity prediction"
    )
    parser.add_argument(
        "--uniprot",
        type=str,
        nargs="+",
        help="UniProt ID(s) or sequence(s) in FASTA format"
    )
    parser.add_argument(
        "--profiles",
        action="store_true",
        help="Compute HERCULES RNA-binding profiles"
    )
    parser.add_argument(
        "--mutagenesis",
        action="store_true",
        help="Perform in silico mutagenesis on the input protein(s)"
    )
    parser.add_argument(
        "--fused",
        action="store_true",
        help="Compute fused HERCULES global scores"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save output CSV file"
    )

    args = parser.parse_args()

    if not args.uniprot:
        parser.error("Please provide --uniprot")

    results = []

    # profiles
    if args.profiles:
        df_profiles = profiles(uniprot_ids=args.uniprot)
        results.append(("profiles", df_profiles))
        print("\n--- Profiles ---")
        print(df_profiles.to_string(index=False))

    # fused global score
    if args.fused:
        df_fused = global_fused_score(uniprot_ids=args.uniprot)
        results.append(("fused", df_fused))
        print("\n--- Fused Global Scores ---")
        print(df_fused.to_string(index=False))

    # mutagenesis (only for single protein at a time)
    if args.mutagenesis:
        if len(args.uniprot) > 1:
            print("Mutagenesis can be performed only on one protein at a time. Using the first UniProt ID.")
        df_mut = mutagenesis(uniprot_id=args.uniprot[0])
        results.append(("mutagenesis", df_mut))
        print("\n--- Mutagenesis Scan ---")
        print(df_mut.to_string(index=False))

    # save to CSV if requested
    if args.output:
        output_path = Path(args.output)
        if len(results) == 1:
            # save single dataframe
            results[0][1].to_csv(output_path, index=False)
        else:
            # save multiple sheets in Excel
            with pd.ExcelWriter(output_path) as writer:
                for name, df in results:
                    sheet_name = name[:31]  # Excel sheet name limit
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    main()
