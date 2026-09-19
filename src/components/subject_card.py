import streamlit as st


def subject_card(
    name,
    code,
    section,
    stats=None,
    footer_callback=None
):

    total = None
    attended = None

    if stats:

        for item in stats:

            if len(item) < 3:
                continue

            _, label, value = item

            if label == "Total":
                total = value

            elif label == "Attended":
                attended = value

    has_attendance = (
        total is not None
        and attended is not None
    )

    percentage = 0

    if has_attendance and total > 0:

        percentage = round(
            (attended / total) * 100
        )

    if percentage >= 75:
        status = "Good attendance"
    elif percentage >= 50:
        status = "Needs attention"
    else:
        status = "Low attendance"

    attendance_badge = ""

    if has_attendance:

        attendance_badge = f"""
            <div style="
                background:#f3f4ff;
                color:#5865F2;
                padding:6px 11px;
                border-radius:999px;
                font-size:0.8rem;
                font-weight:600;
                white-space:nowrap;
            ">
                {percentage}% Attendance
            </div>
        """

    html = f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:18px;
        padding:22px;
        margin-bottom:16px;
        box-shadow:0 6px 24px rgba(15,23,42,0.06);
        border-left:5px solid #5865F2;
    ">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            gap:16px;
        ">

            <div>

                <div style="
                    color:#111827;
                    font-size:1.25rem;
                    font-weight:700;
                    margin-bottom:6px;
                ">
                    {name}
                </div>

                <div style="
                    color:#6b7280;
                    font-size:0.9rem;
                ">
                    {code} &nbsp;•&nbsp; Section {section}
                </div>

            </div>

            {attendance_badge}

        </div>

        <div style="
            height:1px;
            background:#eef0f3;
            margin:18px 0;
        "></div>

        <div style="
            display:flex;
            gap:10px;
            flex-wrap:wrap;
        ">
    """

    if stats:

        for item in stats:

            if len(item) < 3:
                continue

            icon, label, value = item

            html += f"""
                <div style="
                    background:#f8fafc;
                    border:1px solid #eef0f3;
                    padding:9px 13px;
                    border-radius:12px;
                    color:#374151;
                    font-size:0.88rem;
                ">
                    {icon}
                    <span style="
                        color:#111827;
                        font-weight:700;
                        margin-left:4px;
                    ">
                        {value}
                    </span>
                    <span style="
                        color:#6b7280;
                        margin-left:3px;
                    ">
                        {label}
                    </span>
                </div>
            """

    status_html = ""

    if has_attendance:

        status_html = f"""
            <div style="
                margin-top:14px;
                color:#6b7280;
                font-size:0.82rem;
            ">
                {status}
            </div>
        """

    html += f"""
        </div>

        {status_html}

    </div>
    """

    st.html(html)

    if footer_callback:

        footer_callback()