import pytest

import moneychanger


class FakeSuccessResponse:
    status_code = 200

    @staticmethod
    def json():
        return {"conversion_result": 123.456}


class FakeErrorResponse:
    status_code = 500
    text = "upstream failure"


def test_returns_rounded_conversion_tuple_for_successful_response(monkeypatch):
    requested_urls = []

    def fake_get(url):
        requested_urls.append(url)
        return FakeSuccessResponse()

    monkeypatch.setattr(
        moneychanger, "requests", type("RequestsStub", (), {"get": fake_get}), raising=False
    )
    monkeypatch.setattr(moneychanger, "EXCHANGERATE_API_KEY", "test-key")

    result = moneychanger.get_exchange_rate("USD", "EUR", "100")

    assert result == ("USD", "EUR", "100", 123.46)
    assert requested_urls == ["https://v6.exchangerate-api.com/v6/test-key/pair/USD/EUR/100"]


def test_raises_exception_with_status_and_body_for_failed_response(monkeypatch):
    def fake_get(_url):
        return FakeErrorResponse()

    monkeypatch.setattr(
        moneychanger, "requests", type("RequestsStub", (), {"get": fake_get}), raising=False
    )
    monkeypatch.setattr(moneychanger, "EXCHANGERATE_API_KEY", "test-key")

    with pytest.raises(Exception) as exc_info:
        moneychanger.get_exchange_rate("USD", "EUR", "100")

    assert str(exc_info.value) == "Error fetching exchange rate: 500 - upstream failure"