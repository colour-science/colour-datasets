"""Define offline regression tests for bounded JSON network requests."""

from email.message import Message
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

import pytest

from colour_datasets.utilities import json_open, url_download


def test_json_open_retries_timeout() -> None:
    """Retry a timed out request and decode the successful response."""

    response = MagicMock()
    response.__enter__.return_value.read.return_value = b'{"record": 1}'
    with patch(
        "colour_datasets.utilities.common.urllib.request.urlopen",
        side_effect=[TimeoutError("connection timed out"), response],
    ) as open_url:
        assert json_open("https://example.com/retry-timeout") == {"record": 1}
    assert open_url.call_count == 2
    assert all(call.kwargs["timeout"] == 10 for call in open_url.call_args_list)


def test_json_open_exhausts_timeout_retries() -> None:
    """Propagate the timeout when every retry fails."""

    with (
        patch(
            "colour_datasets.utilities.common.urllib.request.urlopen",
            side_effect=TimeoutError("connection timed out"),
        ) as open_url,
        pytest.raises(TimeoutError),
    ):
        json_open("https://example.com/exhaust-timeout", retries=2)
    assert open_url.call_count == 2


@pytest.mark.parametrize(
    "retry_after, delay", [("7", 7), ("999", 120), ("invalid", 30)]
)
def test_url_download_rate_limit(retry_after: str, delay: int) -> None:
    """Respect server retry delays within the maximum allowed wait."""

    headers = Message()
    headers["Retry-After"] = retry_after
    error = HTTPError(
        "https://example.com/data", 429, "Too Many Requests", headers, None
    )
    with (
        patch(
            "colour_datasets.utilities.common.urllib.request.urlretrieve",
            side_effect=[error, None],
        ) as retrieve,
        patch("colour_datasets.utilities.common.time.sleep") as sleep,
    ):
        url_download("https://example.com/data", "unused-filename")
    sleep.assert_called_once_with(delay)
    assert retrieve.call_count == 2


def test_json_open_rate_limit() -> None:
    """Honor the retry delay when the metadata service is rate limited."""

    headers = Message()
    headers["Retry-After"] = "5"
    error = HTTPError(
        "https://example.com/metadata", 429, "Too Many Requests", headers, None
    )
    response = MagicMock()
    response.__enter__.return_value.read.return_value = b'{"record": 1}'
    with (
        patch(
            "colour_datasets.utilities.common.urllib.request.urlopen",
            side_effect=[error, response],
        ),
        patch("colour_datasets.utilities.common.time.sleep") as sleep,
    ):
        assert json_open("https://example.com/metadata") == {"record": 1}
    sleep.assert_called_once_with(5)
