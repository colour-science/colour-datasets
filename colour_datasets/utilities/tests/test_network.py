"""Define offline regression tests for bounded JSON network requests."""

from unittest.mock import MagicMock, patch

import pytest

from colour_datasets.utilities import json_open


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
