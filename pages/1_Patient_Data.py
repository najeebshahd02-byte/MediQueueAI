from pathlib import Path
import pandas as pd
import streamlit as st

# =========================================================
# הגדרות העמוד
# =========================================================
st.set_page_config(
    page_title="MediQueue AI | נתוני מטופלים",
    layout="wide",
    initial_sidebar_state="collapsed"
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

URGENCY_OPTIONS = ["גבוהה", "בינונית", "נמוכה"]


# =========================================================
# פונקציות עזר
# =========================================================
def time_to_minutes(value):
    """
    מקבל שעה בפורמט HH:MM ומחזיר דקות מתחילת היום.
    """
    parts = str(value).strip().split(":")
    hour = int(parts[0])
    minute = int(parts[1])

    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        raise ValueError

    return hour * 60 + minute


def generate_default_patients(number_of_patients):
    """
    יוצר תרחיש התחלתי מציאותי לדוגמה עבור מרפאה.
    הנתונים אינם Dataset חיצוני וכל הערכים ניתנים לשינוי.
    המטרה היא להדגים עומס אמיתי, זמני טיפול שונים ורמות
    דחיפות שונות כך שניהול התור ייצור גם זמני המתנה.
    """

    # דפוסי ברירת מחדל מציאותיים יחסית למרפאה:
    # הגעות לא אחידות, זמני טיפול שונים ודחיפויות מגוונות.
    arrival_gaps = [0, 4, 3, 8, 3, 6, 4, 7, 5, 6, 3, 9, 4, 5, 7]
    service_times = [18, 25, 12, 30, 15, 22, 35, 10, 28, 20, 16, 32, 14, 24, 19]
    urgency_pattern = [
        "בינונית", "גבוהה", "נמוכה", "בינונית", "גבוהה",
        "בינונית", "נמוכה", "גבוהה", "בינונית", "נמוכה",
        "בינונית", "גבוהה", "נמוכה", "בינונית", "גבוהה"
    ]

    current_minutes = 8 * 60
    rows = []

    for i in range(number_of_patients):
        if i == 0:
            gap = 0
        else:
            gap = arrival_gaps[i % len(arrival_gaps)]
        current_minutes += gap

        hour = (current_minutes // 60) % 24
        minute = current_minutes % 60

        rows.append({
            "מטופל": f"P{i + 1}",
            "זמן הגעה": f"{hour:02d}:{minute:02d}",
            "זמן טיפול משוער (דקות)": service_times[i % len(service_times)],
            "רמת דחיפות": urgency_pattern[i % len(urgency_pattern)],
        })

    return pd.DataFrame(rows)


# =========================================================
# עיצוב
# =========================================================
st.html("""
<style>
#MainMenu,
footer,
header[data-testid="stHeader"],
section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.stApp {
    background: #eef5f9;
}

[data-testid="stMainBlockContainer"],
.block-container {
    width: 100% !important;
    max-width: 1450px !important;
    padding: 20px 30px 45px !important;
    margin: 0 auto !important;
}

.hero {
    direction: rtl;
    padding: 28px 32px;
    border: 1px solid #dceaf2;
    border-radius: 20px;
    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #f7fbfd 70%,
        #eaf7fb 100%
    );
}

.kicker {
    color: #0797aa;
    font-size: 12px;
    font-weight: 800;
}

.title {
    color: #07265f;
    font-size: 36px;
    font-weight: 900;
    margin: 7px 0 0;
}

.subtitle {
    color: #5c7186;
    font-size: 13px;
    line-height: 1.8;
    margin-top: 9px;
}

.section-title {
    direction: rtl;
    color: #075e92;
    font-size: 21px;
    font-weight: 900;
    margin: 26px 0 12px;
}

.note {
    direction: rtl;
    margin-top: 15px;
    padding: 13px 16px;
    border: 1px solid #d7edf3;
    border-radius: 12px;
    background: #eef9fc;
    color: #49687d;
    font-size: 12px;
    line-height: 1.75;
}

.note strong {
    color: #078fa5;
}

div.stButton > button[kind="primary"] {
    background: #0b4a92 !important;
    border: 1px solid #0b4a92 !important;
    color: white !important;
    min-height: 48px !important;
    font-weight: 800 !important;
}
</style>
""")


# =========================================================
# כותרת
# =========================================================
st.html("""
<div class="hero">

    <div class="kicker">
        MediQueue AI
    </div>

    <h1 class="title">
        נתוני מטופלים
    </h1>

    <div class="subtitle">
        בעמוד זה מוגדר תרחיש העבודה של MediQueue AI בהתאם
        לדרישות הפרויקט: מספר מטופלים, מספר רופאים,
        זמן הגעה, זמן טיפול משוער ורמת דחיפות.

        המערכת היא מערכת גנרית ולכן כל הנתונים ניתנים
        לשינוי על-ידי המשתמש ואינם תלויים ב-Dataset חיצוני.

        זמן ההמתנה אינו מוגדר כקלט בעמוד זה.
        הוא יחושב בעמוד ניהול התור לפי זמן ההגעה,
        זמינות הרופאים וסדר הטיפול שנקבע על-ידי המערכת.
    </div>

</div>
""")


# =========================================================
# הגדרת התרחיש
# =========================================================
st.markdown(
    '<div class="section-title">הגדרת התרחיש</div>',
    unsafe_allow_html=True
)

c1, c2 = st.columns(2)

with c1:
    number_of_patients = st.number_input(
        "מספר מטופלים",
        min_value=2,
        max_value=100,
        value=10,
        step=1
    )

with c2:
    number_of_doctors = st.number_input(
        "מספר רופאים זמינים",
        min_value=1,
        max_value=max(
            1,
            int(number_of_patients)
        ),
        value=min(
            3,
            int(number_of_patients)
        ),
        step=1
    )


# =========================================================
# יצירת טבלת קלט כאשר מספר המטופלים משתנה
# =========================================================
scenario_key = int(number_of_patients)

if (
    "patient_input_key"
    not in st.session_state
    or
    st.session_state[
        "patient_input_key"
    ] != scenario_key
):

    st.session_state[
        "patient_input_key"
    ] = scenario_key

    st.session_state[
        "patient_input_table"
    ] = generate_default_patients(
        int(number_of_patients)
    )

    # שינוי קלט מבטל תוצאות ישנות
    st.session_state.pop(
        "mediqueue_scenario",
        None
    )

    st.session_state.pop(
        "mediqueue_queue_results",
        None
    )

    st.session_state.pop(
        "mediqueue_analysis",
        None
    )

    st.session_state.pop(
        "mediqueue_decision_support",
        None
    )


# =========================================================
# נתוני המטופלים
# =========================================================
st.markdown(
    '<div class="section-title">נתוני המטופלים בתרחיש</div>',
    unsafe_allow_html=True
)

st.caption(
    "הזן עבור כל מטופל זמן הגעה, זמן טיפול משוער ורמת דחיפות. "
    "הערכים ההתחלתיים הם נתוני דוגמה בלבד וניתנים לשינוי."
)

edited_df = st.data_editor(
    st.session_state[
        "patient_input_table"
    ].copy(),
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",

    column_config={

        "מטופל":
            st.column_config.TextColumn(
                "מטופל",
                disabled=True
            ),

        "זמן הגעה":
            st.column_config.TextColumn(
                "זמן הגעה",
                help=(
                    "שעת הגעת המטופל למרפאה בפורמט HH:MM."
                )
            ),

        "זמן טיפול משוער (דקות)":
            st.column_config.NumberColumn(
                "זמן טיפול משוער (דקות)",
                min_value=1,
                max_value=240,
                step=1,
                help=(
                    "משך הטיפול המשוער עבור המטופל."
                )
            ),

        "רמת דחיפות":
            st.column_config.SelectboxColumn(
                "רמת דחיפות",
                options=URGENCY_OPTIONS,
                required=True,
                help=(
                    "רמת הדחיפות משמשת בקביעת סדר הטיפול. "
                    "כאשר מספר מטופלים כבר ממתינים, "
                    "מטופל בדחיפות גבוהה יקבל קדימות. "
                    "כאשר הדחיפות זהה, נשמר סדר ההגעה."
                )
            ),
    },

    key="patient_scenario_editor"
)


# =========================================================
# בדיקות תקינות
# =========================================================
validation_errors = []

for idx, row in edited_df.iterrows():

    try:
        time_to_minutes(
            row["זמן הגעה"]
        )
    except Exception:
        validation_errors.append(
            f"זמן ההגעה של {row['מטופל']} אינו תקין."
        )

    try:
        service_time = float(
            row[
                "זמן טיפול משוער (דקות)"
            ]
        )

        if service_time <= 0:
            raise ValueError

    except Exception:
        validation_errors.append(
            f"זמן הטיפול של {row['מטופל']} אינו תקין."
        )

    if (
        row["רמת דחיפות"]
        not in URGENCY_OPTIONS
    ):
        validation_errors.append(
            f"רמת הדחיפות של {row['מטופל']} אינה תקינה."
        )


# =========================================================
# סיכום רמות הדחיפות
# =========================================================
urgency_counts = (
    edited_df[
        "רמת דחיפות"
    ]
    .value_counts()
    .reindex(
        URGENCY_OPTIONS,
        fill_value=0
    )
)

u1, u2, u3 = st.columns(3)

with u1:
    st.metric(
        "דחיפות גבוהה",
        int(
            urgency_counts[
                "גבוהה"
            ]
        )
    )

with u2:
    st.metric(
        "דחיפות בינונית",
        int(
            urgency_counts[
                "בינונית"
            ]
        )
    )

with u3:
    st.metric(
        "דחיפות נמוכה",
        int(
            urgency_counts[
                "נמוכה"
            ]
        )
    )

if len(
    edited_df[
        "רמת דחיפות"
    ].unique()
) == 1:
    st.warning(
        "כל המטופלים מוגדרים כרגע באותה רמת דחיפות. "
        "המערכת עדיין תפעל, אך כדי להדגים את השפעת "
        "רמת הדחיפות על סדר הטיפול מומלץ להגדיר "
        "לפחות שתי רמות דחיפות שונות."
    )

if validation_errors:
    for error in validation_errors:
        st.error(error)


# =========================================================
# הסבר לגבי זמן ההמתנה
# =========================================================
st.info(
    "זמן ההמתנה יתקבל כתוצאה של ניהול התור ולא כקלט. "
    "לכל מטופל תחושב ההמתנה לפי: "
    "תחילת טיפול פחות זמן הגעה."
)


# =========================================================
# שמירת התרחיש והמשך
# =========================================================
st.markdown(
    '<div class="section-title">המשך לניהול התור</div>',
    unsafe_allow_html=True
)

if st.button(
    "שמור תרחיש והמשך לניהול התור",
    type="primary",
    use_container_width=True,
    disabled=bool(validation_errors)
):

    final_scenario = (
        edited_df.copy()
    )

    final_scenario[
        "urgency_score"
    ] = (
        final_scenario[
            "רמת דחיפות"
        ]
        .map({
            "גבוהה": 3,
            "בינונית": 2,
            "נמוכה": 1,
        })
        .astype(int)
    )

    final_scenario[
        "_arrival_minutes"
    ] = (
        final_scenario[
            "זמן הגעה"
        ]
        .apply(time_to_minutes)
    )

    final_scenario = (
        final_scenario
        .sort_values(
            [
                "_arrival_minutes",
                "מטופל"
            ]
        )
        .reset_index(drop=True)
    )

    # שמירת אותו תרחיש לכל שלבי המערכת
    st.session_state[
        "mediqueue_scenario"
    ] = {

        "number_of_patients":
            int(number_of_patients),

        "number_of_doctors":
            int(number_of_doctors),

        "patients":
            final_scenario.copy(),

        "data_source":
            "user_defined_scenario",

        "waiting_time_definition":
            "treatment_start_minus_arrival_time"
    }

    # שמירת טבלת הקלט המעודכנת
    st.session_state[
        "patient_input_table"
    ] = (
        edited_df.copy()
    )

    # כל תוצאות ישנות מהשלבים הבאים מבוטלות
    st.session_state.pop(
        "mediqueue_queue_results",
        None
    )

    st.session_state.pop(
        "mediqueue_analysis",
        None
    )

    st.session_state.pop(
        "mediqueue_decision_support",
        None
    )

    st.success(
        f"התרחיש נשמר בהצלחה: "
        f"{int(number_of_patients)} מטופלים ו-"
        f"{int(number_of_doctors)} רופאים."
    )

    queue_pages = [
        "pages/2_Queue_Management.py",
        "pages/Queue_Management.py",
    ]

    moved = False

    for page in queue_pages:
        if (
            PROJECT_ROOT
            / page
        ).exists():

            st.switch_page(page)
            moved = True
            break

    if not moved:
        st.info(
            "התרחיש נשמר בהצלחה. "
            "לא נמצא קובץ עמוד ניהול התור בתיקיית pages."
        )


# =========================================================
# הקשר לפרויקט
# =========================================================
st.html("""
<div class="note">

    <strong>הקשר לדרישות הפרויקט:</strong><br>

    MediQueue AI היא מערכת גנרית לניהול תורים.
    המשתמש מגדיר את מספר המטופלים, מספר הרופאים,
    זמן ההגעה, זמן הטיפול המשוער ורמת הדחיפות
    עבור כל מטופל.

    <br><br>

    בהתאם להערת המרצה, זמני ההגעה וזמני ההמתנה
    הם חלק מרכזי במודל.
    זמן ההגעה מוזן ישירות כנתון תרחיש,
    ואילו זמן ההמתנה מחושב על-ידי המערכת לאחר
    הפעלת מנגנון ניהול התור.

    <br><br>

    בעמוד הבא המערכת תשתמש באותו תרחיש בדיוק
    כדי לחשב:
    סדר טיפול,
    זמן המתנה לכל מטופל,
    חלוקת המטופלים בין הרופאים
    וניצול המשאבים.

</div>
""")