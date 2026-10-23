import streamlit as st


_COMPONENT = st.components.v2.component(
    name="snap_presence_turnstile",
    html="""
        <div class="turnstile-container">
            <div id="turnstile-widget"></div>
            <div id="turnstile-status" role="status"></div>
        </div>
    """,
    css="""
        .turnstile-container {
            width: 100%;
            min-height: 65px;
            overflow: visible;
        }

        #turnstile-status {
            font-size: 0.85rem;
            margin-top: 4px;
        }
    """,
    js="""
        export default function(component) {
            const { parentElement, data, setStateValue } = component;

            const root = parentElement.querySelector(
                ".turnstile-container"
            );
            const status = parentElement.querySelector(
                "#turnstile-status"
            );
            const container = parentElement.querySelector(
                "#turnstile-widget"
            );

            if (!root || !status || !container) {
                return;
            }

            const sitekey = data?.sitekey;
            const action = data?.action;
            let widgetId = null;
            let disposed = false;

            if (!sitekey || !action) {
                status.textContent = "Turnstile configuration is missing.";
                return;
            }

            status.textContent = "Loading security verification...";

            function renderWidget() {
                if (
                    disposed ||
                    !window.turnstile ||
                    widgetId !== null
                ) {
                    return;
                }

                try {
                    widgetId = window.turnstile.render(container, {
                        sitekey: sitekey,
                        action: action,
                        theme: "auto",
                        callback: function(token) {
                            status.textContent =
                                "Verification completed.";

                            setStateValue("token", token);
                        },
                        "expired-callback": function() {
                            status.textContent =
                                "Verification expired. Please verify again.";

                            setStateValue("token", null);
                        },
                        "error-callback": function() {
                            status.textContent =
                                "Verification could not load. Please retry.";

                            setStateValue("token", null);
                        }
                    });
                } catch (error) {
                    status.textContent =
                        "Verification could not load. Please refresh and retry.";
                    setStateValue("token", null);
                }
            }

            if (window.turnstile) {
                renderWidget();
            } else {
                let script = document.querySelector(
                    'script[data-snap-turnstile="true"]'
                );

                if (!script) {
                    script = document.createElement("script");
                    script.src =
                        "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit";
                    script.async = true;
                    script.defer = true;
                    script.dataset.snapTurnstile = "true";
                    script.addEventListener("load", renderWidget);
                    script.addEventListener("error", function() {
                        status.textContent =
                            "Cloudflare verification failed to load.";
                        setStateValue("token", null);
                    });
                    document.head.appendChild(script);
                } else {
                    script.addEventListener("load", renderWidget, {
                        once: true
                    });
                }
            }

            return function cleanup() {
                disposed = true;

                if (
                    widgetId !== null &&
                    window.turnstile
                ) {
                    window.turnstile.remove(widgetId);
                }
            };
        }
    """,
)


def render_turnstile(action: str, key: str):
    """Render Turnstile and return its client token, if available."""
    site_key = st.secrets.get("TURNSTILE_SITE_KEY", "")

    if not isinstance(site_key, str) or not site_key.strip():
        st.error(
            "Security verification is not configured. "
            "Please contact the administrator."
        )
        return None

    result = _COMPONENT(
        data={
            "sitekey": site_key.strip(),
            "action": action,
        },
        default={"token": None},
        on_token_change=lambda: None,
        key=key,
        width="stretch",
        height=90,
    )

    token = getattr(result, "token", None)

    if isinstance(token, str) and 0 < len(token) <= 2048:
        return token

    return None