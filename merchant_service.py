def classify_merchant_risk(merchant_id, merchant_data):
    # Placeholder logic for risk classification
    name = merchant_data["name"].lower()
    group_id = merchant_data.get("group_id")

    if "crypto" in name:
        risk_level = "high"
    elif group_id == 1:
        risk_level = "medium"
    else:
        risk_level = "low"

    return {
        "merchant_id": merchant_id,
        "risk_level": risk_level
    }
