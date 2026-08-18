import base64
from pathlib import Path
import streamlit as st

st.set_page_config(
    page_title="MediQueue AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ASSETS = Path("assets")
BG_IMAGE = ASSETS / "hospital_waiting_room.png"
CSS_FILE = ASSETS / "style.css"


@st.cache_data
def file_to_base64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("utf-8")


if not BG_IMAGE.exists():
    st.error("לא נמצאה תמונת הרקע של המרפאה.")
    st.stop()

if not CSS_FILE.exists():
    st.error("לא נמצא קובץ style.css.")
    st.stop()

image_base64 = file_to_base64(str(BG_IMAGE))
css = CSS_FILE.read_text(encoding="utf-8").replace(
    "{image_base64}",
    image_base64
)

arrival_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxjaXJjbGUgY3g9IjI0IiBjeT0iMjQiIHI9IjE3IiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIvPgo8cGF0aCBkPSJNMjQgMTR2MTFsOCA1IiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+Cjwvc3ZnPg=="
treatment_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxwYXRoIGQ9Ik0xNCA4djEwYTEwIDEwIDAgMCAwIDIwIDBWOCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8Y2lyY2xlIGN4PSIxNCIgY3k9IjgiIHI9IjIuNSIgZmlsbD0iIzA3OGZhNSIvPgo8Y2lyY2xlIGN4PSIzNCIgY3k9IjgiIHI9IjIuNSIgZmlsbD0iIzA3OGZhNSIvPgo8cGF0aCBkPSJNMjQgMjh2NmE3IDcgMCAwIDAgMTQgMHYtNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8Y2lyY2xlIGN4PSIzOCIgY3k9IjI3IiByPSIzIiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIvPgo8L3N2Zz4="
waiting_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxwYXRoIGQ9Ik0xNCA3aDIwTTE0IDQxaDIwIiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0xNyA4YzAgOCA0IDExIDcgMTQtMyAzLTcgNi03IDE4TTMxIDhjMCA4LTQgMTEtNyAxNCAzIDMgNyA2IDcgMTgiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+"
patients_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxjaXJjbGUgY3g9IjE3IiBjeT0iMTYiIHI9IjYiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxjaXJjbGUgY3g9IjMyIiBjeT0iMTgiIHI9IjUiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxwYXRoIGQ9Ik02IDQwYzEtOSA1LTEzIDExLTEzczEwIDQgMTEgMTNNMjUgNDBjMS04IDQtMTIgOS0xMiA1IDAgOCA0IDkgMTEiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiLz4KPC9zdmc+"
doctors_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxjaXJjbGUgY3g9IjI0IiBjeT0iMTUiIHI9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIi8+CjxwYXRoIGQ9Ik0xMCA0MGMxLTkgNi0xMyAxNC0xM3MxMyA0IDE0IDEzIiBmaWxsPSJub25lIiBzdHJva2U9IiMwNzhmYTUiIHN0cm9rZS13aWR0aD0iMyIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+CjxwYXRoIGQ9Ik0yNCAzMXYxME0xOSAzNmgxMCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8L3N2Zz4="
urgency_icon = "PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCI+CjxwYXRoIGQ9Ik0yNCA2IDQyIDQwSDZMMjQgNloiIGZpbGw9Im5vbmUiIHN0cm9rZT0iIzA3OGZhNSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+CjxwYXRoIGQ9Ik0yNCAxN3YxMiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMDc4ZmE1IiBzdHJva2Utd2lkdGg9IjMiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPgo8Y2lyY2xlIGN4PSIyNCIgY3k9IjM0IiByPSIxLjgiIGZpbGw9IiMwNzhmYTUiLz4KPC9zdmc+"

PAGE_HTML = f"""
<style>
{css}
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

st.html(PAGE_HTML)
