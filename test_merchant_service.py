from unittest.mock import Mock


class TestUserMerchantGroupService:

    def test_edge_case_1(self):

        mock_service = Mock()
        mock_service.update_merchant_group.return_value = True

        result = mock_service.update_merchant_group(123)
        assert result
