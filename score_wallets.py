import argparse
import json
import pandas as pd
from features import compute_features
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def main(input_path, output_path):
    with open(input_path) as f:
        transactions = [json.loads(line) for line in f]

    df = pd.DataFrame(transactions)
    features_df = compute_features(df)

    scaler = MinMaxScaler(feature_range=(0, 1000))
    features_df["score"] = scaler.fit_transform(features_df[["raw_score"]])

    features_df[["wallet", "score"]].to_csv(output_path, index=False)

    # Score histogram
    plt.hist(features_df["score"], bins=10, range=(0, 1000))
    plt.xlabel("Score")
    plt.ylabel("Wallet Count")
    plt.title("Wallet Credit Score Distribution")
    plt.savefig("sample_output/score_distribution.png")
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="wallet_scores.csv")
    args = parser.parse_args()
    main(args.input, args.output)
