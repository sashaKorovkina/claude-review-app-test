## Before vs After - Good Test Practices

1. **Autospec in mocks** 
    - `autospec` ensures your mock methods have the **same signature** as the real ones.
    - If the real `update_merchant_group()` requires two arguments, calling it with the wrong number will raise a `TypeError`.
    - This helps **catch bugs early** in your test code.

*Example:* https://github.com/heron-data/backend/pull/5181/files#diff-a68d9b02f2bbd8804d31acd42c0e1c864b738ea323a5d2657495044a7e7d91d4R1068

```python
mock_service = create_autospec(UserMerchantGroupService)
mock_service.update_merchant_group.return_value = user_merchant_group

DIContext.override_instance(
    DIContext.user_merchant_group_service,
    mock_service
)
```

1. **Using persistence session instead of mocking database calls** 
- The dummy session does nothing when commit() is called, so your service logic runs without actually persisting to the database.
- You can test your service's business logic (like the merchant grouping logic) without worrying
about database state or cleanup.
- No actual database transactions means faster test execution.

```python
saved_merchant_group = self.user_merchant_groups_repo.save(merchant_group)
self.persistence_session.commit()
```

1. **Service classes mean dependencies in tests have to be set once** 

Before:

```python
# Each test had to mock every function's dependencies separately
  def test_update_merchant_group(mocker):
      mock_repo = mocker.Mock()
      mock_db_session = mocker.patch('app.domain.user_merchant_groups.services.db.session')
```

After:

```python
After (Class):
  # Set up dependencies once, reuse across all tests
  def test_update_merchant_group():
      mock_repo = InMemoryUserMerchantGroupsRepository()
      persistence_session = DummyPersistenceSession()
      service = UserMerchantGroupService(mock_repo, persistence_session)

      # Clean method calls without dependency injection noise
      result = service.update_merchant_group(merchant_id=123, user_id=456, group_id="group1")
```

1. **Eliminated Import/Module Path Dependencies**

Before**:** 

Tests were brittle to module restructuring:

```python
mocker.patch('app.domain.user_merchant_groups.services.db.session')
  # Breaks if you move or rename the services module
```

After:

Only depends on interfaces:

```python
service = UserMerchantGroupService(repo, persistence_session)
```

1. **Direct Domain Focus Instead of Generic Containers**
    1. Do not use test classes because 

Before (with a test class):

```python
class TestUserMerchantGroupService:
			def test_default(self):
					# setup code...
					# test code...

      def test_get_merchants_by_group_id(self):
          # Setup code...

      def test_populate_user_merchant_group_table_when_empty(self):
          # Setup code...

      def test_populate_user_merchant_group_table_when_not_empty(self):
          # Setup code...
```

The class TestUserMerchantGroupService is just a container - it doesn't tell you anything about the business domain or what scenarios are being tested.

After:

```python
def test_get_merchants_by_group_id(user, mca_merchant, mca_merchant_not_use_name_as_alias, merchants):
      # Test categorizes merchants into pending/custom/rejected groups

def test_populate_user_merchant_group_table_when_empty(mca_merchant, user):
    # Test initializes merchant groups for new user

def test_populate_user_merchant_group_table_when_not_empty(mca_merchant, user):
    # Test skips initialization when user already has groups

def test_update_merchant_group_create_new(user, mca_merchant):
    # Test creates new merchant group assignment

def test_update_merchant_group_update_existing(user, mca_merchant):
    # Test modifies existing merchant group assignment
```

Each function name immediately tells you **what business scenario** is being tested. It also aligns with the bounded context

<aside>
💡

In case a **test gets too long,** we should put it into a **separate file** and not create classes to containerise the logic 

</aside>

1. **Clear edge case documentation** 

Makes it clear why a specific edge case is being tested and what issues are likely to occur 

Before (Unclear Edge Cases):

```python
class TestUserMerchantGroupService:
      def test_edge_case_1(self):
      def test_edge_case_2(self):
```

 

After adding comments on the edge case:

```python
def test_get_user_merchant_group_override_for_merchant(user, mca_merchant, merchants):
      # Test with different merchant ID / group ID
      different_merchant = merchants[0]
      result = service.get_user_merchant_group_override_for_merchant(user.id, different_merchant.id)
      assert result == {}  # No group set for this merchant regardless if it had a group
```