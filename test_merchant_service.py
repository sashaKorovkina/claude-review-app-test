# tests/test_merchant_service.py
import pytest
from merchant_service import (
    update_merchant_group,
    NotFoundError,
    PermissionDeniedError
)

def test_successful_update():
    result = update_merchant_group(user_id=1, merchant_id=101, group_id=2)
    assert result["status"] == "success"
    assert result["updated_merchant"]["group_id"] == 2

def test_missing_ids():
    with pytest.raises(ValueError):
        update_merchant_group(None, 101, 2)

def test_user_not_found():
    with pytest.raises(NotFoundError):
        update_merchant_group(999, 101, 2)

def test_merchant_not_found():
    with pytest.raises(NotFoundError):
        update_merchant_group(1, 999, 2)

def test_group_not_found():
    with pytest.raises(NotFoundError):
        update_merchant_group(1, 101, 999)

def test_permission_denied():
    with pytest.raises(PermissionDeniedError):
        update_merchant_group(2, 101, 2)
