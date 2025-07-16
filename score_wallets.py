import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_transactions(json_path):
    print(f"Loading data from {json_path} ...")
    with open(json_path, 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

def compute_features(df):
    print("Computing features per wallet...")
    # Basic counts and sums per action
    actions = ['deposit', 'borrow', 'repay', 'redeemunderlying', 'liquidationcall']
    
    # Create columns for each action count and amount (if amount exists)
    df['amount'] = df.get('amount', 0)  # fallback if amount key missing
    
    features = df.groupby('wallet').agg(
        total_txns = ('action', 'count'),
        deposits = ('action', lambda x: (x == 'deposit').sum()),
        borrows = ('action', lambda x: (x == 'borrow').sum()),
        repays = ('action', lambda x: (x == 'repay').sum()),
        liquidations = ('action', lambda x: (x == 'liquidationcall').sum()),
        total_deposit_amount = ('amount', lambda x: x[df.loc[x.index, 'action']=='deposit'].sum()),
        total_borrow_amount = ('amount', lambda x: x[df.loc[x.index, 'action']=='borrow'].sum()),
        total_repay_amount = ('amount', lambda x: x[df.loc[x.index, 'action']=='repay'].sum()),
    ).reset_index()
    
    # Derived features
    features['repay_borrow_ratio'] = features['total_repay_amount'] / (features['total_borrow_amount'] + 1e-6)
    features['liquidation_rate'] = features['liquidations'] / (features['total_txns'] + 1e-6)
    features['activity_level'] = features['total_txns']
    
    return features

def compute_score(features):
    print("Computing wallet credit scores...")
    # Example scoring heuristic (customize as needed)
    score = (
        300 * (features['repay_borrow_ratio'].clip(0,1)) +   # repay ratio max 1
        300 * (1 - features['liquidation_rate'].clip(0,1)) + # fewer liquidations better
        100 * (np.log1p(features['activity_level']))         # more activity better
    )
    # Normalize score to 0-1000
    score = np.clip(score, 0, 1000)
    return score

def plot_score_distribution(features):
    print("Plotting score distribution by buckets...")
    features["score_bucket"] = pd.cut(
        features["score"],
        bins=[0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        labels=["0-100", "100-200", "200-300", "300-400", "400-500",
                "500-600", "600-700", "700-800", "800-900", "900-1000"]
    )
    
    bucket_counts = features["score_bucket"].value_counts().sort_index()
    plt.figure(figsize=(10,6))
    bucket_counts.plot(kind="bar", color="skyblue")
    plt.title("Wallet Credit Score Distribution by Range")
    plt.xlabel("Score Range")
    plt.ylabel("Number of Wallets")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("sample_output/score_distribution.png")
    plt.show()

def main(input_path, output_path):
    df = load_transactions(input_path)
    features = compute_features(df)
    features['score'] = compute_score(features)
    features[['wallet', 'score']].to_csv(output_path, index=False)
    print(f"Saved wallet scores to {output_path}")
    plot_score_distribution(features)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aave Wallet Credit Scoring")
    parser.add_argument('--input', type=str, required=True, help='Input JSON file path')
    parser.add_argument('--output', type=str, required=True, help='Output CSV file path')
    args = parser.parse_args()
    main(args.input, args.output)
