from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="MediQueue AI | נתוני מטופלים",
    layout="wide",
    initial_sidebar_state="collapsed",
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
URGENCY_OPTIONS = ["גבוהה", "בינונית", "נמוכה"]
URGENCY_SCORES = {"גבוהה": 3, "בינונית": 2, "נמוכה": 1}
RESULT_KEYS = [
    "mediqueue_queue_results",
    "mediqueue_analysis",
    "mediqueue_decision_support",
]


def time_to_minutes(value):
    parts = str(value).strip().split(":")
    if len(parts) != 2:
        raise ValueError
    hour, minute = map(int, parts)
    if not (0 <= hour <= 23 and 0 <= minute <= 59):
        raise ValueError
    return hour * 60 + minute


@st.cache_data
def generate_default_patients(number_of_patients):
    arrival_gaps = [0, 4, 3, 8, 3, 6, 4, 7, 5, 6, 3, 9, 4, 5, 7]
    service_times = [18, 25, 12, 30, 15, 22, 35, 10, 28, 20, 16, 32, 14, 24, 19]
    urgency_pattern = [
        "בינונית", "גבוהה", "נמוכה", "בינונית", "גבוהה",
        "בינונית", "נמוכה", "גבוהה", "בינונית", "נמוכה",
        "בינונית", "גבוהה", "נמוכה", "בינונית", "גבוהה",
    ]

    current_minutes = 8 * 60
    rows = []

    for i in range(number_of_patients):
        if i:
            current_minutes += arrival_gaps[i % len(arrival_gaps)]

        rows.append({
            "מטופל": f"P{i + 1}",
            "זמן הגעה": f"{(current_minutes // 60) % 24:02d}:{current_minutes % 60:02d}",
            "זמן טיפול משוער (דקות)": service_times[i % len(service_times)],
            "רמת דחיפות": urgency_pattern[i % len(urgency_pattern)],
        })

    return pd.DataFrame(rows)


def clear_results():
    for key in RESULT_KEYS:
        st.session_state.pop(key, None)


def validate_patients(df):
    errors = []

    for _, row in df.iterrows():
        patient = row["מטופל"]

        try:
            time_to_minutes(row["זמן הגעה"])
        except Exception:
            errors.append(f"זמן ההגעה של {patient} אינו תקין.")

        try:
            if float(row["זמן טיפול משוער (דקות)"]) <= 0:
                raise ValueError
        except Exception:
            errors.append(f"זמן הטיפול של {patient} אינו תקין.")

        if row["רמת דחיפות"] not in URGENCY_OPTIONS:
            errors.append(f"רמת הדחיפות של {patient} אינה תקינה.")

    return errors


st.html("""
<style>
#MainMenu, footer, header[data-testid="stHeader"],
section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}
.stApp { background: #eef5f9; }
[data-testid="stMainBlockContainer"], .block-container {
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
    background: linear-gradient(135deg, #ffffff 0%, #f7fbfd 70%, #eaf7fb 100%);
}
.kicker { color: #0797aa; font-size: 12px; font-weight: 800; }
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
.note strong { color: #078fa5; }
div.stButton > button[kind="primary"] {
    background: #0b4a92 !important;
    border: 1px solid #0b4a92 !important;
    color: white !important;
    min-height: 48px !important;
    font-weight: 800 !important;
}
</style>
""")

st.html("""
<div class="hero">
    <div class="kicker">MediQueue AI</div>
    <h1 class="title">נתוני מטופלים</h1>
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

st.markdown('<div class="section-title">הגדרת התרחיש</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    number_of_patients = st.number_input(
        "מספר מטופלים", min_value=2, max_value=100, value=10, step=1
    )
with c2:
    number_of_doctors = st.number_input(
        "מספר רופאים זמינים",
        min_value=1,
        max_value=max(1, int(number_of_patients)),
        value=min(3, int(number_of_patients)),
        step=1,
    )

scenario_key = int(number_of_patients)

if st.session_state.get("patient_input_key") != scenario_key:
    st.session_state["patient_input_key"] = scenario_key
    st.session_state["patient_input_table"] = generate_default_patients(scenario_key)
    st.session_state.pop("mediqueue_scenario", None)
    clear_results()

st.markdown(
    '<div class="section-title">נתוני המטופלים בתרחיש</div>',
    unsafe_allow_html=True,
)
st.caption(
    "הזן עבור כל מטופל זמן הגעה, זמן טיפול משוער ורמת דחיפות. "
    "הערכים ההתחלתיים הם נתוני דוגמה בלבד וניתנים לשינוי."
)

edited_df = st.data_editor(
    st.session_state["patient_input_table"].copy(),
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    key="patient_scenario_editor",
    column_config={
        "מטופל": st.column_config.TextColumn("מטופל", disabled=True),
        "זמן הגעה": st.column_config.TextColumn(
            "זמן הגעה", help="שעת הגעת המטופל למרפאה בפורמט HH:MM."
        ),
        "זמן טיפול משוער (דקות)": st.column_config.NumberColumn(
            "זמן טיפול משוער (דקות)",
            min_value=1,
            max_value=240,
            step=1,
            help="משך הטיפול המשוער עבור המטופל.",
        ),
        "רמת דחיפות": st.column_config.SelectboxColumn(
            "רמת דחיפות",
            options=URGENCY_OPTIONS,
            required=True,
            help=(
                "רמת הדחיפות משמשת בקביעת סדר הטיפול. "
                "כאשר מספר מטופלים כבר ממתינים, מטופל בדחיפות גבוהה יקבל קדימות. "
                "כאשר הדחיפות זהה, נשמר סדר ההגעה."
            ),
        ),
    },
)

validation_errors = validate_patients(edited_df)

urgency_counts = (
    edited_df["רמת דחיפות"]
    .value_counts()
    .reindex(URGENCY_OPTIONS, fill_value=0)
)

for column, label, urgency in zip(
    st.columns(3),
    ["דחיפות גבוהה", "דחיפות בינונית", "דחיפות נמוכה"],
    URGENCY_OPTIONS,
):
    with column:
        st.metric(label, int(urgency_counts[urgency]))

if edited_df["רמת דחיפות"].nunique() == 1:
    st.warning(
        "כל המטופלים מוגדרים כרגע באותה רמת דחיפות. "
        "המערכת עדיין תפעל, אך כדי להדגים את השפעת רמת הדחיפות "
        "על סדר הטיפול מומלץ להגדיר לפחות שתי רמות דחיפות שונות."
    )

for error in validation_errors:
    st.error(error)

st.info(
    "זמן ההמתנה יתקבל כתוצאה של ניהול התור ולא כקלט. "
    "לכל מטופל תחושב ההמתנה לפי: תחילת טיפול פחות זמן הגעה."
)

st.markdown(
    '<div class="section-title">המשך לניהול התור</div>',
    unsafe_allow_html=True,
)

if st.button(
    "שמור תרחיש והמשך לניהול התור",
    type="primary",
    use_container_width=True,
    disabled=bool(validation_errors),
):
    final_scenario = edited_df.copy()
    final_scenario["urgency_score"] = (
        final_scenario["רמת דחיפות"].map(URGENCY_SCORES).astype(int)
    )
    final_scenario["_arrival_minutes"] = final_scenario["זמן הגעה"].apply(time_to_minutes)
    final_scenario = (
        final_scenario.sort_values(["_arrival_minutes", "מטופל"])
        .reset_index(drop=True)
    )

    st.session_state["mediqueue_scenario"] = {
        "number_of_patients": int(number_of_patients),
        "number_of_doctors": int(number_of_doctors),
        "patients": final_scenario.copy(),
        "data_source": "user_defined_scenario",
        "waiting_time_definition": "treatment_start_minus_arrival_time",
    }
    st.session_state["patient_input_table"] = edited_df.copy()
    clear_results()

    st.success(
        f"התרחיש נשמר בהצלחה: {int(number_of_patients)} מטופלים "
        f"ו-{int(number_of_doctors)} רופאים."
    )

    for page in ["pages/2_Queue_Management.py", "pages/Queue_Management.py"]:
        if (PROJECT_ROOT / page).exists():
            st.switch_page(page)
            break
    else:
        st.info(
            "התרחיש נשמר בהצלחה. "
            "לא נמצא קובץ עמוד ניהול התור בתיקיית pages."
        )

st.html("""
<div class="note">
    <strong>הקשר לדרישות הפרויקט:</strong><br>
    MediQueue AI היא מערכת גנרית לניהול תורים.
    המשתמש מגדיר את מספר המטופלים, מספר הרופאים,
    זמן ההגעה, זמן הטיפול המשוער ורמת הדחיפות עבור כל מטופל.
    <br><br>
    בהתאם להערת המרצה, זמני ההגעה וזמני ההמתנה הם חלק מרכזי במודל.
    זמן ההגעה מוזן ישירות כנתון תרחיש,
    ואילו זמן ההמתנה מחושב על-ידי המערכת לאחר הפעלת מנגנון ניהול התור.
    <br><br>
    בעמוד הבא המערכת תשתמש באותו תרחיש בדיוק כדי לחשב:
    סדר טיפול, זמן המתנה לכל מטופל,
    חלוקת המטופלים בין הרופאים וניצול המשאבים.
</div>
""")
