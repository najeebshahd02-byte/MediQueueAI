import base64
from pathlib import Path
import streamlit as st


st.set_page_config(
    page_title="MediQueue AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)


image_path = Path("assets/hospital_waiting_room.png")

if not image_path.exists():
    st.error("לא נמצאה תמונת הרקע של המרפאה.")
    st.stop()

image_base64 = base64.b64encode(
    image_path.read_bytes()
).decode("utf-8")

arrival_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxjaXJjbGUgY3g9IjI0IiBjeT0iMjQiIHI9IjE3IiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIvPgo8cGF0aCBkPSJNMjQgMTR2MTFsOCA1IiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+Cjwvc3ZnPg=="
treatment_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxwYXRoIGQ9Ik0xNCA4djEwYTEwIDEwIDAgMCAwIDIwIDBWOCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8Y2lyY2xlIGN4PSIxNCIgY3k9IjgiIHI9IjIuNSIgZmlsbD0iIzA3OGZhNSIvPgo8Y2lyY2xlIGN4PSIzNCIgY3k9IjgiIHI9IjIuNSIgZmlsbD0iIzA3OGZhNSIvPgo8cGF0aCBkPSJNMjQgMjh2NmE3IDcgMCAwIDAgMTQgMHYtNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8Y2lyY2xlIGN4PSIzOCIgY3k9IjI3IiByPSIzIiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIvPgo8L3N2Zz4="
waiting_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxwYXRoIGQ9Ik0xNCA3aDIwTTE0IDQxaDIwIiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xNyA4YzAgOCA0IDExIDcgMTQtMyAzLTcgNi03IDE4TTMxIDhjMCA4LTQgMTEtNyAxNCAzIDMgNyA2IDcgMTgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+"
patients_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxjaXJjbGUgY3g9IjE3IiBjeT0iMTYiIHI9IjYiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxjaXJjbGUgY3g9IjMyIiBjeT0iMTgiIHI9IjUiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxwYXRoIGQ9Ik02IDQwYzEtOSA1LTEzIDExLTEzczEwIDQgMTEgMTNNMjUgNDBjMS04IDQtMTIgOS0xMiA1IDAgOCA0IDkgMTEiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+"
doctors_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxjaXJjbGUgY3g9IjI0IiBjeT0iMTUiIHI9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxwYXRoIGQ9Ik0xMCA0MGMxLTkgNi0xMyAxNC0xM3MxMyA0IDE0IDEzIiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0yNCAzMXYxME0xOSAzNmgxMCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4="
urgency_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxwYXRoIGQ9Ik0yNCA2IDQyIDQwSDZMMjQgNloiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+CjxwYXRoIGQ9Ik0yNCAxN3YxMiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8Y2lyY2xlIGN4PSIyNCIgY3k9IjM0IiByPSIxLjgiIGZpbGw9IiMwNzhmYTUiLz4KPC9zdmc+"


st.html(
    f"""
<style>

#MainMenu,
footer,
header[data-testid="stHeader"],
section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}

html,
body {{
    margin: 0;
    padding: 0;
}}

* {{
    box-sizing: border-box;
}}

.stApp {{
    background: #eef5f9;
}}

[data-testid="stMainBlockContainer"],
.block-container {{
    width: 100% !important;
    max-width: 100% !important;
    padding: 14px 28px !important;
    margin: 0 !important;
}}

.page-shell {{
    width: 100%;
    max-width: 1500px;
    margin: 0 auto;
    background: #ffffff;
    border-radius: 20px;
    overflow: hidden;
    box-shadow: 0 18px 55px rgba(16, 56, 92, 0.10);
    font-family: Arial, "Helvetica Neue", sans-serif;
}}

.topbar {{
    width: 100%;
    height: 74px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    direction: ltr;
    padding: 0 36px;
    background: #ffffff;
    border-bottom: 1px solid #e3edf3;
}}

.logo-box {{
    display: flex;
    align-items: center;
    gap: 11px;
    flex-shrink: 0;
}}

.logo-icon {{
    width: 51px;
    height: 51px;
    color: #08a5b7;
}}

.logo-icon svg {{
    width: 100%;
    height: 100%;
}}

.logo-text {{
    display: flex;
    flex-direction: column;
}}

.logo-text strong {{
    color: #07265f;
    font-size: 24px;
    font-weight: 900;
    letter-spacing: -0.7px;
    line-height: 1;
}}

.logo-text span {{
    margin-top: 4px;
    direction: rtl;
    color: #667b8e;
    font-size: 9px;
}}

.navbar {{
    direction: rtl;
    height: 100%;
    display: flex;
    align-items: center;
}}

.navbar a {{
    position: relative;
    height: 100%;
    display: flex;
    align-items: center;
    padding: 0 17px;
    color: #173f69;
    text-decoration: none;
    font-size: 13px;
    font-weight: 700;
    white-space: nowrap;
}}

.navbar a:hover {{
    color: #078da3;
}}

.navbar a.active {{
    color: #078da3;
}}

.navbar a.active::after {{
    content: "";
    position: absolute;
    bottom: 0;
    right: 14px;
    left: 14px;
    height: 3px;
    border-radius: 4px;
    background: #08a4b2;
}}

.hero {{
    width: 100%;
    height: 430px;
    display: grid;
    grid-template-columns: 39% 61%;
    direction: ltr;
    overflow: hidden;
}}

.hero-copy {{
    position: relative;
    z-index: 10;
    direction: rtl;
    text-align: right;
    padding: 43px 48px 35px;
    background:
        linear-gradient(
            90deg,
            #ffffff 0%,
            #ffffff 82%,
            rgba(255,255,255,0.96) 90%,
            rgba(255,255,255,0.30) 100%
        );
}}

.hero-kicker {{
    margin-bottom: 13px;
    color: #078fa5;
    font-size: 13px;
    font-weight: 850;
}}

.hero-brand {{
    direction: ltr;
    text-align: left;
    color: #06245f;
    font-size: 62px;
    font-weight: 900;
    line-height: 0.98;
    letter-spacing: -2.5px;
    white-space: nowrap;
}}

.hero-copy h1 {{
    margin: 14px 0 17px;
    color: #087f9b;
    font-size: 25px;
    font-weight: 900;
    line-height: 1.43;
}}

.hero-copy p {{
    max-width: 540px;
    margin: 0;
    color: #486178;
    font-size: 13px;
    line-height: 1.9;
}}

.hero-actions {{
    margin-top: 25px;
    display: flex;
    gap: 18px;
}}

.hero-button {{
    min-width: 188px;
    height: 46px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    border-radius: 9px;
    text-decoration: none;
    font-size: 13px;
    font-weight: 850;
}}

.hero-button.primary {{
    color: white;
    background:
        linear-gradient(
            135deg,
            #084b9e,
            #061d64
        );
    box-shadow:
        0 10px 25px
        rgba(4, 49, 129, 0.25);
}}

.hero-button.secondary {{
    color: #074990;
    background: #ffffff;
    border: 1px solid #146bb9;
}}

.hero-button .arrow {{
    font-size: 23px;
    line-height: 1;
}}

.hero-image {{
    position: relative;
    height: 430px;
    background-image:
        url("data:image/png;base64,{image_base64}");
    background-size: cover;
    background-position: center center;
    overflow: hidden;
}}

.hero-image-overlay {{
    position: absolute;
    inset: 0;
    background:
        linear-gradient(
            90deg,
            rgba(255,255,255,0.22) 0%,
            rgba(255,255,255,0.02) 24%,
            rgba(1,28,67,0.03) 100%
        );
}}

.input-section {{
    direction: rtl;
    padding: 22px 34px 28px;
    background:
        radial-gradient(circle at 10% 0%, rgba(20, 180, 200, 0.05), transparent 26%),
        linear-gradient(180deg, #ffffff 0%, #f9fcfe 100%);
    border-top: 1px solid #e2edf3;
}}

.section-heading {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 14px;
    margin-bottom: 16px;
}}

.section-heading::before,
.section-heading::after {{
    content: "";
    height: 1px;
    flex: 1;
    max-width: 300px;
}}

.section-heading::before {{
    background: linear-gradient(90deg, transparent, #32afbf);
}}

.section-heading::after {{
    background: linear-gradient(90deg, #32afbf, transparent);
}}

.section-heading h2 {{
    margin: 0;
    color: #075e92;
    font-size: 20px;
    font-weight: 900;
    white-space: nowrap;
}}

.input-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
}}

.input-card {{
    min-height: 118px;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 16px 17px;
    border: 1px solid #dce9f1;
    border-radius: 14px;
    background: #ffffff;
    box-shadow: 0 6px 18px rgba(22, 70, 105, 0.06);
}}

.input-card-icon {{
    width: 54px;
    height: 54px;
    flex: 0 0 54px;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.input-card-icon img {{
    width: 44px;
    height: 44px;
    display: block;
}}

.input-card-text {{
    flex: 1;
}}

.input-card-text h3 {{
    margin: 0 0 5px;
    color: #075b94;
    font-size: 15px;
    font-weight: 900;
}}

.input-card-text p {{
    margin: 0;
    color: #536b80;
    font-size: 10.5px;
    line-height: 1.6;
}}

.dataset-note {{
    margin-top: 14px;
    padding: 11px 16px;
    border: 1px solid #d9eef3;
    border-radius: 11px;
    background: #eef9fc;
    color: #45677b;
    text-align: center;
    font-size: 10.5px;
    line-height: 1.6;
}}

.dataset-note strong {{
    color: #087f9b;
}}
@media (max-width: 1100px) {{

    .navbar {{
        display: none;
    }}

    .hero {{
        height: auto;
        grid-template-columns: 1fr;
    }}

    .hero-copy {{
        order: 1;
    }}

    .hero-image {{
        order: 2;
        height: 430px;
    }}

    .input-grid {{
        grid-template-columns: repeat(2, 1fr);
    }}
}}

@media (max-width: 680px) {{

    .input-grid {{
        grid-template-columns: 1fr;
    }}

    .input-section {{
        padding: 24px 18px 30px;
    }}
}}

</style>


<div class="page-shell">

    <header class="topbar">

        <div class="logo-box">

            <div class="logo-icon">

                <svg viewBox="0 0 70 70">

                    <path
                        d="
                        M35 59
                        C28 53 11 42 11 25
                        C11 15 18 9 27 9
                        C32 9 35 13 35 13
                        C35 13 39 9 44 9
                        C53 9 60 15 60 25
                        C60 42 42 53 35 59Z
                        "
                        fill="none"
                        stroke="currentColor"
                        stroke-width="4"
                    />

                    <path
                        d="
                        M21 33
                        H28
                        L32 25
                        L36 42
                        L41 33
                        H49
                        "
                        fill="none"
                        stroke="#0870c5"
                        stroke-width="4"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                    />

                </svg>

            </div>


            <div class="logo-text">

                <strong>
                    MediQueue AI
                </strong>

                <span>
                    מערכת חכמה לניהול תורים רפואיים
                </span>

            </div>

        </div>


        <nav class="navbar">

            <a
                class="active"
                href="/"
                target="_self"
            >
                דף הבית
            </a>

            <a
                href="/Patient_Data"
                target="_self"
            >
                נתוני מטופלים
            </a>

            <a
                href="/Queue_Management"
                target="_self"
            >
                ניהול התור
            </a>

            <a
                href="/Queue_Analysis"
                target="_self"
            >
                ניתוח התור
            </a>

            <a
                href="/Decision_Support"
                target="_self"
            >
                תמיכה בהחלטות
            </a>

            <a
                href="/System_Evaluation"
                target="_self"
            >
                הערכת המערכת
            </a>

            <a
                href="/About_System"
                target="_self"
            >
                אודות המערכת
            </a>

        </nav>

    </header>


    <section class="hero">

        <div class="hero-copy">

            <div class="hero-kicker">
                מערכת מידע לניהול תורים רפואיים
            </div>

            <div class="hero-brand">
                MediQueue AI
            </div>

            <h1>
                מערכת חכמה לניהול תורים רפואיים
                <br>
                ותמיכה בקבלת החלטות
                <br>
                במרפאות ובבתי חולים
            </h1>

            <p>
                המערכת מנתחת נתוני הגעה של מטופלים,
                זמני טיפול, זמני המתנה, רמת דחיפות
                ומספר הרופאים הזמינים.
                באמצעות תורת התורים ניתן להעריך את ביצועי המערכת,
                לצמצם זמני המתנה ולשפר את ניצול המשאבים הרפואיים.
            </p>

            <div class="hero-actions">

                <a
                    class="hero-button primary"
                    href="/Patient_Data"
                    target="_self"
                >
                    <span class="arrow">‹</span>
                    התחלת ניתוח התורים
                </a>

                <a
                    class="hero-button secondary"
                    href="/About_System"
                    target="_self"
                >
                    מידע על המערכת
                </a>

            </div>

        </div>


        <div class="hero-image">
            <div class="hero-image-overlay"></div>
        </div>

    </section>


    <section class="input-section">

        <div class="section-heading">
            <h2>נתוני הקלט של המערכת</h2>
        </div>

        <div class="input-grid">

            <div class="input-card">

                <div class="input-card-icon"><img src="data:image/svg+xml;base64,{arrival_icon}" alt=""></div>

                <div class="input-card-text">

                    <h3>זמני הגעה</h3>

                    <p>
                        זמני ההגעה של המטופלים למרפאה או לבית החולים
                        לצורך ניתוח קצב ההגעה והעומס במערכת.
                    </p>

                </div>

            </div>


            <div class="input-card">

                <div class="input-card-icon"><img src="data:image/svg+xml;base64,{treatment_icon}" alt=""></div>

                <div class="input-card-text">

                    <h3>זמני טיפול</h3>

                    <p>
                        משך הטיפול המשוער עבור כל מטופל
                        לצורך הערכת קצב השירות ועומס הרופאים.
                    </p>

                </div>

            </div>


            <div class="input-card">

                <div class="input-card-icon"><img src="data:image/svg+xml;base64,{waiting_icon}" alt=""></div>

                <div class="input-card-text">

                    <h3>זמני המתנה</h3>

                    <p>
                        משך הזמן מהגעת המטופל ועד תחילת הטיפול
                        לצורך הערכת ביצועי מערכת התורים.
                    </p>

                </div>

            </div>


            <div class="input-card">

                <div class="input-card-icon"><img src="data:image/svg+xml;base64,{patients_icon}" alt=""></div>

                <div class="input-card-text">

                    <h3>מספר המטופלים</h3>

                    <p>
                        מספר המטופלים הנכללים במערכת
                        ומהווים את הביקוש לשירות הרפואי.
                    </p>

                </div>

            </div>


            <div class="input-card">

                <div class="input-card-icon"><img src="data:image/svg+xml;base64,{doctors_icon}" alt=""></div>

                <div class="input-card-text">

                    <h3>מספר הרופאים</h3>

                    <p>
                        מספר הרופאים הזמינים במערכת
                        לצורך טיפול במטופלים והקצאת המשאבים.
                    </p>

                </div>

            </div>


            <div class="input-card">

                <div class="input-card-icon"><img src="data:image/svg+xml;base64,{urgency_icon}" alt=""></div>

                <div class="input-card-text">

                    <h3>רמת דחיפות</h3>

                    <p>
                        רמת הדחיפות של כל מטופל
                        לצורך תמיכה בקביעת סדר הטיפול.
                    </p>

                </div>

            </div>

        </div>


        <div class="dataset-note">
            <strong>מקור הנתונים:</strong>
            נתוני המטופלים ישמשו בהמשך לחישובי זמני ההמתנה,
            ניתוח התורים והערכת ניצול המשאבים.
        </div>

    </section>

</div>
"""
)