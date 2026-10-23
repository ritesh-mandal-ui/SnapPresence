import logging
import uuid

import httpx
import streamlit as st


logger = logging.getLogger(__name__)

SITEVERIFY_URL = (
    "https://challenges.cloudflare.com/turnstile/v0/siteverify"
)

DEFAULT_ALLOWED_HOSTNAMES = {
    "snappresence-yfxlcxdgu8vubz9ktrwmvz.streamlit.app",
}


def verify_turnstile_token(token: str, expected_action: str) -> bool:
    """
    Verify a Turnstile token on the server.

    Returns False for missing configuration, invalid tokens,
    unexpected actions/hostnames, or verification service errors.
    """
    if (
        not isinstance(token, str)
        or not token
        or len(token) > 2048
        or not isinstance(expected_action, str)
        or not expected_action
    ):
        return False

    secret_key = st.secrets.get("TURNSTILE_SECRET_KEY", "")

    if not isinstance(secret_key, str) or not secret_key.strip():
        logger.error("Turnstile secret key is not configured.")
        return False

    configured_hosts = st.secrets.get(
        "TURNSTILE_ALLOWED_HOSTNAMES",
        list(DEFAULT_ALLOWED_HOSTNAMES),
    )

    if not isinstance(configured_hosts, (list, tuple)):
        logger.error("Turnstile allowed-hostnames setting is invalid.")
        return False

    allowed_hostnames = {
        str(host).strip().lower()
        for host in configured_hosts
        if str(host).strip()
    }

    if not allowed_hostnames:
        logger.error("No allowed Turnstile hostnames are configured.")
        return False

    payload = {
        "secret": secret_key.strip(),
        "response": token,
        "idempotency_key": str(uuid.uuid4()),
    }

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.post(
                SITEVERIFY_URL,
                json=payload,
            )
            response.raise_for_status()
            result = response.json()

    except (httpx.HTTPError, ValueError):
        logger.warning("Turnstile server-side verification failed.")
        return False

    if not isinstance(result, dict) or result.get("success") is not True:
        return False

    verified_action = result.get("action")
    verified_hostname = str(
        result.get("hostname", "")
    ).strip().lower()

    if verified_action != expected_action:
        logger.warning("Turnstile action did not match the expected action.")
        return False

    if verified_hostname not in allowed_hostnames:
        logger.warning("Turnstile hostname was not allowlisted.")
        return False

    return True