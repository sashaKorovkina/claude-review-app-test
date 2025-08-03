# services/merchant_service.py
import logging

# Configure audit logger
audit_logger = logging.getLogger('audit')
audit_logger.setLevel(logging.INFO)

class NotFoundError(Exception):
    pass

class PermissionDeniedError(Exception):
    pass

class MockDB:
    users = {1: "Alice", 2: "Bob"}
    merchants = {101: {"name": "Merchant A", "group_id": None}, 102: {"name": "Merchant B", "group_id": 1}}
    groups = {1: "Group One", 2: "Group Two"}
    permissions = {1: [101, 102], 2: [102]}  # user_id: [merchant_ids]

    @classmethod
    def user_exists(cls, user_id):
        return user_id in cls.users

    @classmethod
    def merchant_exists(cls, merchant_id):
        return merchant_id in cls.merchants

    @classmethod
    def group_exists(cls, group_id):
        return group_id in cls.groups

    @classmethod
    def user_can_edit_merchant(cls, user_id, merchant_id):
        return merchant_id in cls.permissions.get(user_id, [])

    @classmethod
    def update_merchant_group(cls, merchant_id, group_id):
        cls.merchants[merchant_id]["group_id"] = group_id
        return cls.merchants[merchant_id]

def update_merchant_group(user_id, merchant_id, group_id):
    if not user_id:
        raise ValueError("user_id must be provided")
    if not merchant_id:
        raise ValueError("merchant_id must be provided")
    if not group_id:
        raise ValueError("group_id must be provided")

    if not MockDB.user_exists(user_id):
        raise NotFoundError(f"User {user_id} not found")
    if not MockDB.merchant_exists(merchant_id):
        raise NotFoundError(f"Merchant {merchant_id} not found")
    if not MockDB.group_exists(group_id):
        raise NotFoundError(f"Group {group_id} not found")
    if not MockDB.user_can_edit_merchant(user_id, merchant_id):
        raise PermissionDeniedError(f"User {user_id} cannot update merchant {merchant_id}")

    updated = MockDB.update_merchant_group(merchant_id, group_id)

    # Audit log
    audit_logger.info("User %s updated merchant %s to group %s", user_id, merchant_id, group_id)

    return {
        "status": "success",
        "updated_merchant": updated
    }
