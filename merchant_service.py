def classify_merchant_risk(merchant_id, merchant_data):
    # Enhanced risk classification with granular levels
    name = merchant_data["name"].lower()
    group_id = merchant_data.get("group_id")
    transaction_volume = merchant_data.get("transaction_volume", 0)
    
    risk_score = 0
    
    # Name-based risk factors
    high_risk_keywords = ["crypto", "bitcoin", "gambling", "casino", "forex"]
    medium_risk_keywords = ["loan", "credit", "investment", "trading", "ecommerce"]
    
    if any(keyword in name for keyword in high_risk_keywords):
        risk_score += 40
    elif any(keyword in name for keyword in medium_risk_keywords):
        risk_score += 25
    
    # Group-based risk factors
    if group_id == 1:  # High-risk group
        risk_score += 30
    elif group_id == 2:  # Medium-risk group
        risk_score += 15
    elif group_id == 3:  # Regulated group
        risk_score += 10
    
    # Transaction volume risk factors
    if transaction_volume > 1000000:  # Over 1M
        risk_score += 20
    elif transaction_volume > 100000:  # Over 100K
        risk_score += 10
    elif transaction_volume > 10000:  # Over 10K
        risk_score += 5
    
    # Determine granular risk level based on score with more granular levels
    if risk_score >= 90:
        risk_level = "critical"
    elif risk_score >= 80:
        risk_level = "very_high"
    elif risk_score >= 65:
        risk_level = "high"
    elif risk_score >= 50:
        risk_level = "moderate_high"
    elif risk_score >= 35:
        risk_level = "medium"
    elif risk_score >= 25:
        risk_level = "moderate_low"
    elif risk_score >= 15:
        risk_level = "low"
    elif risk_score >= 5:
        risk_level = "very_low"
    else:
        risk_level = "minimal"
    
    return {
        "merchant_id": merchant_id,
        "risk_level": risk_level,
        "risk_score": risk_score
    }
