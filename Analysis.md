# 📊 Aave Wallet Credit Score Analysis

This document provides insights and interpretation of the scoring results produced from analyzing historical transaction behavior of Aave V2 users.

---

## 🎯 Score Distribution

| Score Range | % of Wallets | Behavior Characteristics                    |
|-------------|--------------|----------------------------------------------|
| 0–100       | ~5%          | Bot-like or exploitative behavior, heavy liquidation |
| 100–300     | ~15%         | Risky borrowers, low repayment activity      |
| 300–600     | ~50%         | Average users with mixed patterns            |
| 600–800     | ~20%         | Good repayment behavior, consistent usage    |
| 800–1000    | ~10%         | Long-term users, regular deposits, no liquidation |

![Score Distribution](sample_output/score_distribution.png)

---

## 🔍 Low-Scoring Wallets (0–300)

- **High liquidation frequency** (≥1 liquidationcall per 10 transactions)
- **Few or no repay actions** relative to borrow volume
- Many accounts show **short-lived activity** (1–2 days)
- Large spikes in borrow with minimal follow-up behavior
- Patterns suggest automated or risky strategies

---

## 🟡 Mid-Range Wallets (300–600)

- Mixed deposit/borrow behaviors
- Some wallets have repayments, but irregular or partial
- Activity spans a few days to weeks
- Lower standard deviation in transaction size
- Moderate lifetime but often low engagement depth

---

## 🟢 High-Scoring Wallets (600–1000)

- Consistently **deposit and repay** without triggering liquidation
- Lifetime spans **weeks or months**
- Show **low risk exposure** with responsible borrowing
- Higher number of smaller, stable transactions
- Typically no liquidationcalls recorded

---

## 🧠 Insights

- Liquidation behavior is a **strong predictor** of score drop
- Time in protocol (wallet lifetime) positively correlates with score
- Wallets with bot-like spike patterns or 1-time high-value interactions score poorly
- Consistent, low-risk behavior over time is rewarded

---

## 📎 Next Steps

- Add token-specific context (e.g. stablecoins vs volatile assets)
- Train a supervised classifier using liquidation as the target
- Cluster behavior types (e.g. farmers, borrowers, suppliers)

