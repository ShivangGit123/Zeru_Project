import pandas as pd

def compute_features(df):
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    grouped = df.groupby("user").agg({
        "amount": ["sum", "mean", "std"],
        "action": lambda x: x.value_counts().to_dict(),
        "timestamp": ["min", "max", "count"]
    })

    grouped.columns = ['_'.join(col) for col in grouped.columns]
    grouped = grouped.reset_index().rename(columns={"user_": "wallet"})

    grouped["lifetime_days"] = (
        pd.to_datetime(grouped["timestamp_max"]) -
        pd.to_datetime(grouped["timestamp_min"])
    ).dt.days + 1

    grouped["action_deposit"] = grouped["action_<lambda>"].apply(lambda x: x.get("deposit", 0))
    grouped["action_borrow"] = grouped["action_<lambda>"].apply(lambda x: x.get("borrow", 0))
    grouped["action_repay"] = grouped["action_<lambda>"].apply(lambda x: x.get("repay", 0))
    grouped["action_liquidation"] = grouped["action_<lambda>"].apply(lambda x: x.get("liquidationcall", 0))

    grouped["raw_score"] = (
        grouped["action_deposit"] * 1.0 +
        grouped["action_repay"] * 3.0 -
        grouped["action_borrow"] * 1.5 -
        grouped["action_liquidation"] * 10.0 +
        grouped["lifetime_days"] * 0.5
    )

    return grouped[["wallet", "raw_score"] + [col for col in grouped.columns if col.startswith("action_")]]
