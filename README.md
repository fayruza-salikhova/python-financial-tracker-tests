# Python Financial Tracker — Test Automation - Unit Tests

Automated tests for a personal finance tracker application, focused on validating financial calculations, transaction management, currency conversion, and data persistence.

The project demonstrates practical QA automation skills using Python and pytest.

## 🧪 Testing Coverage

| Area | What's tested |
|---|---|
| Balance | Income, expenses, zero and negative balances |
| Transactions | Creation, deletion, sorting, validation |
| Categories | CRUD operations, duplicates, input validation |
| Currency conversion | Multiple currencies, rounding, lowercase codes |
| Persistence | Saving and restoring transactions, categories and budgets |

## ⚙️ QA Techniques

- **Parametrized testing** — multiple scenarios with descriptive test IDs.
- **Fixtures & test isolation** — reusable fixtures, `tmp_path` and temporary JSON storage.
- **Mocking** — `monkeypatch` to isolate currency conversion and environment variables.
- **Negative testing** — validation errors and exception handling.
- **Boundary Value Analysis** — zero, minimum currency units and large amounts.
- **Persistence testing** — verification of data after reopening the tracker.
- **Logging validation** — checking application logs with `caplog`.

## 🛠 Tech Stack

- Python
- pytest
- Decimal — precise financial calculations
- monkeypatch — mocking and isolation
- JSON — test data persistence

## ▶️ Run Tests

```bash
pip install -r requirements.txt
pytest -v
```

## 💡 QA Focus

The main focus is test reliability, independent test execution, edge-case coverage, and validation of business logic in financial operations.
