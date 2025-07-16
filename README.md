# Zeru_Project
# Aave Wallet Credit Scoring

This project analyzes DeFi wallet behaviors on Aave V2 using historical transactions and assigns a **credit score (0–1000)** to each wallet.

## 🚀 How It Works

- Input: JSON file with raw transaction-level data (deposit, borrow, repay, etc.)
- Feature Engineering:
  - Count and amount of each action type
  - Ratios (borrow/deposit, repay/borrow, etc.)
  - Liquidation frequency
  - Active period, activity recency, volatility
- Unsupervised scoring:
  - Weighted combination of features
  - Score normalized to 0–1000

## 🔧 Usage

```bash
pip install -r requirements.txt
python score_wallets.py --input user_transactions.json --output wallet_scores.csv
