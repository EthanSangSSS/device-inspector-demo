import json
import time
import urllib.request


def test_steamdt_broad_anonymous_probe():
    url = (
        "https://api.steamdt.com/user/statistics/v2/chart"
        "?timestamp=%d&type=2&dateType=2"
        % int(time.time() * 1000)
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read(20000).decode("utf-8", "replace")
            status = resp.status
    except Exception as exc:
        raise AssertionError(f"SteamDT anonymous request failed: {exc}") from exc

    assert status == 200, f"unexpected HTTP status: {status}"
    try:
        payload = json.loads(body)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"non JSON response: {body[:500]}") from exc

    assert isinstance(payload, dict), f"unexpected payload type: {type(payload)}"
    assert "data" in payload, f"missing data field: {list(payload.keys())}"
