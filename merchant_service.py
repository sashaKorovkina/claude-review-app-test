def update_merchant_group(user_id, merchant_id, group_id):
    # simplified business logic
    if not merchant_id or not user_id:
        raise ValueError("IDs must be provided")
    return {"user_id": user_id, "merchant_id": merchant_id, "group_id": group_id}
