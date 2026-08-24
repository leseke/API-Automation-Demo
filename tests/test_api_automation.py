from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from api_automation import fetch_json, transform, export_csv


SAMPLE = [
    {"id": 1, "name": " Alice Martin ", "email": "ALICE@EXAMPLE.COM ", "active": True},
    {"id": 2, "name": "Bob Durand", "email": "bob@example.com", "active": False},
]


def test_transform_normalizes_and_filters():
    rows = transform(SAMPLE)
    assert rows == [{"id": "1", "name": "Alice Martin", "email": "alice@example.com", "active": True}]


def test_export_csv(tmp_path: Path):
    path = export_csv(transform(SAMPLE), tmp_path / "customers.csv")
    assert path.exists()
    assert "alice@example.com" in path.read_text(encoding="utf-8")


def test_fetch_json_uses_http_layer():
    response = Mock()
    response.json.return_value = SAMPLE
    response.raise_for_status.return_value = None
    with patch("api_automation.requests.get", return_value=response) as get:
        payload = fetch_json("https://api.example.test/customers")
    assert payload == SAMPLE
    get.assert_called_once_with("https://api.example.test/customers", timeout=10)


def test_missing_field_is_rejected():
    with pytest.raises(ValueError):
        transform([{"id": 1, "name": "Alice", "active": True}])
