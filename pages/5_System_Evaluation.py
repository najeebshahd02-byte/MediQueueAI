from pathlib import Path
import pandas as pd
import streamlit as st
import time

st.set_page_config(
    page_title="MediQueue AI | הערכת המערכת",
    layout="wide",
    initial_sidebar_state="collapsed"
)

ROOT = Path(__file__).resolve().parents[1]

# =========================================================
# עיצוב
# =========================================================
st.html("""
<style>
#MainMenu, footer, header[data-testid="stHeader"],
section[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.stApp {
    background: #eef5f9;
}

.block-container {
    max-width: 1450px !important;
    padding: 20px 30px 45px !important;
}

.hero {
    direction: rtl;
    padding: 28px 32px;
    border: 1px solid #dceaf2;
    border-radius: 20px;
    background: linear-gradient(135deg, #ffffff 0%, #f7fbfd 70%, #eaf7fb 100%);
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

.sec {
    direction: rtl;
    color: #075e92;
    font-size: 21px;
    font-weight: 900;
    margin: 26px 0 12px;
}

[data-testid="stMetric"] {
    min-height: 108px;
    padding: 14px 17px;
    border: 1px solid #dce9f1;
    border-radius: 15px;
    background: #ffffff;
}

[data-testid="stMetricValue"] {
    color: #075b94;
    font-weight: 900;
}

.note {
    direction: rtl;
    padding: 16px 18px;
    border: 1px solid #d7edf3;
    border-radius: 12px;
    background: #eef9fc;
    color: #49687d;
    line-height: 1.9;
    font-size: 13px;
}

.note strong {
    color: #078fa5;
}

.result-pass {
    color: #187b5d;
    font-weight: 800;
}

.result-fail {
    color: #b44343;
    font-weight: 800;
}
</style>
""")

# =========================================================
# כותרת
# =========================================================
st.html("""
<div class="hero">
    <div class="kicker">MediQueue AI</div>
    <div class="title">הערכת המערכת</div>
    <div class="subtitle">
        זהו השלב החמישי במערכת. העמוד בוחן את תקינות תוצאות ניהול התור,
        את איכות הפתרון ההיוריסטי ואת מהירות הפעלת מנגנון התור,
        על בסיס אותו תרחיש שהוגדר בשלבים הקודמים.
    </div>
</div>
""")

# =========================================================
# טעינת תוצאות מהשלבים הקודמים
# =========================================================
if "mediqueue_queue_results" not in st.session_state:
    st.warning("לא נמצאו תוצאות ניהול תור. יש להריץ קודם את עמוד ניהול התור.")
    st.stop()

q = st.session_state["mediqueue_queue_results"]

df = q["results"].copy()
patients_input = q.get("patients_input")
n_patients = int(q["number_of_patients"])
n_doctors = int(q["number_of_doctors"])
avg_wait = float(q["avg_wait"])
max_wait = float(q["max_wait"])
system_util = float(q["system_utilization"])

# =========================================================
# מדדי ביצוע
# =========================================================
st.markdown('<div class="sec">מדדי ביצוע של התרחיש</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("מספר מטופלים", n_patients)
c2.metric("מספר רופאים", n_doctors)
c3.metric("זמן המתנה ממוצע", f"{avg_wait:.1f} דקות")
c4.metric("ניצול משאבים", f"{system_util:.1f}%")

# =========================================================
# בדיקות תקינות
# =========================================================
st.markdown('<div class="sec">בדיקות תקינות</div>', unsafe_allow_html=True)

checks = []

checks.append(("כל המטופלים מופיעים בתוצאות", len(df) == n_patients))

if "זמן המתנה (דקות)" in df.columns:
    checks.append(("אין זמני המתנה שליליים", (pd.to_numeric(df["זמן המתנה (דקות)"], errors="coerce") >= 0).all()))

if "זמן טיפול משוער (דקות)" in df.columns:
    checks.append(("כל זמני הטיפול חיוביים", (pd.to_numeric(df["זמן טיפול משוער (דקות)"], errors="coerce") > 0).all()))

doctor_col = "רופא משויך" if "רופא משויך" in df.columns else "שיוך לרופא" if "שיוך לרופא" in df.columns else None
if doctor_col:
    checks.append(("לכל מטופל הוקצה רופא", df[doctor_col].notna().all()))

if "רמת דחיפות" in df.columns:
    checks.append(("לכל מטופל קיימת רמת דחיפות", df["רמת דחיפות"].notna().all()))

if {"זמן הגעה", "זמן תחילת טיפול"}.issubset(df.columns):
    def to_min(t):
        h, m = map(int, str(t)[:5].split(":"))
        return h * 60 + m

    arrival = df["זמן הגעה"].apply(to_min)
    start = df["זמן תחילת טיפול"].apply(to_min)
    checks.append(("אף טיפול לא מתחיל לפני זמן ההגעה", (start >= arrival).all()))

passed = sum(bool(ok) for _, ok in checks)
total_checks = len(checks)

check_df = pd.DataFrame({
    "בדיקה": [name for name, _ in checks],
    "תוצאה": ["עבר" if ok else "נכשל" for _, ok in checks]
})

a, b, c = st.columns(3)
a.metric("בדיקות שעברו", f"{passed}/{total_checks}")
b.metric("אחוז בדיקות שעברו", f"{(passed / total_checks * 100):.0f}%")
c.metric("זמן המתנה מקסימלי", f"{max_wait:.1f} דקות")

st.dataframe(check_df, use_container_width=True, hide_index=True)

# =========================================================
# איכות הפתרון
# =========================================================
st.markdown('<div class="sec">איכות הפתרון</div>', unsafe_allow_html=True)

st.html("""
<div class="note">
    <strong>סוג הפתרון:</strong> הפתרון שמתקבל במערכת הוא פתרון היוריסטי.
    מנגנון ניהול התור משתמש ברמת הדחיפות, בזמן ההגעה ובזמינות הרופאים.
    בתוך אותה רמת דחיפות נשמר עקרון FCFS.
    המערכת מפיקה פתרון ישים ומהיר לניהול התור, אך אינה מבטיחה פתרון אופטימלי גלובלי.
    לכן איכות הפתרון נבחנת באמצעות בדיקות תקינות ומדדי ביצוע כגון זמני המתנה וניצול משאבים.
</div>
""")

# =========================================================
# מהירות הפתרון
# מודדים את מנגנון התור עצמו ולא פעולת DataFrame פשוטה
# =========================================================
st.markdown('<div class="sec">מהירות הפתרון</div>', unsafe_allow_html=True)

def run_queue_for_timing(input_df, doctors):
    x = input_df.copy().reset_index(drop=True)

    def to_min(t):
        h, m = map(int, str(t)[:5].split(":"))
        return h * 60 + m

    urgency = {"גבוהה": 3, "בינונית": 2, "נמוכה": 1}

    x["_arrival"] = x["זמן הגעה"].apply(to_min)
    x["_service"] = pd.to_numeric(x["זמן טיפול משוער (דקות)"])
    x["_urgency"] = x["רמת דחיפות"].map(urgency)
    x["_order"] = range(len(x))

    free = [x["_arrival"].min()] * doctors
    remaining = set(x.index)

    while remaining:
        now = max(min(free), min(x.loc[i, "_arrival"] for i in remaining))
        available_docs = [d for d in range(doctors) if free[d] <= now]
        waiting = [i for i in remaining if x.loc[i, "_arrival"] <= now]

        while available_docs and waiting:
            d = available_docs.pop(0)
            i = min(
                waiting,
                key=lambda j: (
                    -x.loc[j, "_urgency"],
                    x.loc[j, "_arrival"],
                    x.loc[j, "_order"]
                )
            )
            start = max(now, free[d], x.loc[i, "_arrival"])
            free[d] = start + x.loc[i, "_service"]
            remaining.remove(i)
            waiting = [j for j in remaining if x.loc[j, "_arrival"] <= now]

if patients_input is not None and len(patients_input) > 0:
    repetitions = 200
    start_time = time.perf_counter()

    for _ in range(repetitions):
        run_queue_for_timing(patients_input, n_doctors)

    avg_runtime_ms = ((time.perf_counter() - start_time) / repetitions) * 1000

    st.metric("זמן ריצה ממוצע של מנגנון התור", f"{avg_runtime_ms:.3f} ms")

    st.html(f"""
    <div class="note">
        <strong>פירוש:</strong>
        זמן הריצה מייצג את הזמן הדרוש למערכת לחישוב סדר הטיפול,
        הקצאת המטופלים לרופאים וזמני ההמתנה.
        בתרחיש הנוכחי החישוב מתבצע בתוך מספר אלפיות השנייה,
        ולכן המערכת מספקת תוצאה במהירות גבוהה.
        <strong>זהו זמן הריצה של האלגוריתם ולא זמן ההמתנה של המטופלים.</strong>
    </div>
    """)
else:
    st.info("לא נשמר קלט המטופלים המקורי ולכן לא ניתן למדוד את זמן הריצה של מנגנון התור.")

# =========================================================
# סיכום
# =========================================================
st.markdown('<div class="sec">סיכום הערכת המערכת</div>', unsafe_allow_html=True)

status = "כל בדיקות התקינות עברו בהצלחה" if passed == total_checks else f"{passed} מתוך {total_checks} בדיקות התקינות עברו"

st.html(f"""
<div class="note">
    בתרחיש הנוכחי המערכת עיבדה <strong>{n_patients} מטופלים</strong>
    באמצעות <strong>{n_doctors} רופאים</strong>.<br><br>

    <strong>תקינות:</strong> {status}.<br>
    <strong>ביצועים:</strong> זמן ההמתנה הממוצע הוא {avg_wait:.1f} דקות,
    זמן ההמתנה המקסימלי הוא {max_wait:.1f} דקות,
    וניצול המשאבים הוא {system_util:.1f}%.<br><br>

    <strong>איכות הפתרון:</strong> הפתרון הוא היוריסטי ולא פתרון אופטימלי מוכח.
    המערכת נועדה לספק פתרון ישים ומהיר, ולתמוך בניתוח חלופות באמצעות אותם נתוני קלט.<br><br>

    תוצאות עמוד זה נשמרות כהערכת המערכת ואינן משנות את סדר הטיפול או את נתוני המטופלים שחושבו בשלבים הקודמים.
</div>
""")

st.session_state["mediqueue_system_evaluation"] = {
    "checks": check_df,
    "passed": passed,
    "total_checks": total_checks,
    "avg_wait": avg_wait,
    "max_wait": max_wait,
    "system_utilization": system_util
}

# =========================================================
# ניווט
# =========================================================
st.markdown('<div class="sec">המשך במערכת</div>', unsafe_allow_html=True)

back, next_ = st.columns(2)

with back:
    if st.button("חזרה לתמיכה בהחלטות", use_container_width=True):
        st.switch_page("pages/4_Decision_Support.py")

with next_:
    if st.button("המשך לאודות המערכת", type="primary", use_container_width=True):
        candidates = [
            "pages/6_About_System.py",
            "pages/6_About.py",
            "pages/About_System.py"
        ]

        switched = False
        for page in candidates:
            if (ROOT / page).exists():
                st.switch_page(page)
                switched = True
                break

        if not switched:
            st.info("עמוד אודות המערכת ייבנה בשלב הבא.")