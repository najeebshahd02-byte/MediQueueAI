from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="MediQueue AI | ניהול התור", layout="wide", initial_sidebar_state="collapsed")
ROOT = Path(__file__).resolve().parents[1]
URGENCY = {"גבוהה": 3, "בינונית": 2, "נמוכה": 1}

# ---------- Helpers ----------
def to_min(t):
    p = str(t).split(":")
    return int(p[0]) * 60 + int(p[1]) + (int(p[2]) / 60 if len(p) > 2 else 0)

def to_time(m):
    m = int(round(m)) % 1440
    return f"{m//60:02d}:{m%60:02d}"

def run_queue(df, n_docs):
    df = df.copy().reset_index(drop=True)
    df["_arr"] = df["זמן הגעה"].apply(to_min)
    df["_srv"] = pd.to_numeric(df["זמן טיפול משוער (דקות)"], errors="coerce")
    df["_urg"] = df["רמת דחיפות"].map(URGENCY)
    df["_ord"] = range(len(df))

    if df["_srv"].isna().any() or (df["_srv"] <= 0).any() or df["_urg"].isna().any():
        raise ValueError("יש נתוני קלט לא תקינים.")

    first_arrival = df["_arr"].min()
    available = {d: first_arrival for d in range(1, n_docs + 1)}
    busy = {d: 0.0 for d in range(1, n_docs + 1)}
    remaining, rows, order = set(df.index), [], 1

    while remaining:
        event = max(min(available.values()), min(df.loc[i, "_arr"] for i in remaining))
        free_docs = sorted(d for d, t in available.items() if t <= event)
        waiting = [i for i in remaining if df.loc[i, "_arr"] <= event]

        while free_docs and waiting:
            d = free_docs.pop(0)
            i = min(waiting, key=lambda x: (-df.loc[x, "_urg"], df.loc[x, "_arr"], df.loc[x, "_ord"]))
            r = df.loc[i]

            start = max(r["_arr"], event, available[d])
            wait = start - r["_arr"]
            end = start + r["_srv"]

            available[d] = end
            busy[d] += r["_srv"]

            rows.append({
                "סדר טיפול": order,
                "מטופל": r["מטופל"],
                "רמת דחיפות": r["רמת דחיפות"],
                "זמן הגעה": to_time(r["_arr"]),
                "רופא משויך": f"רופא {d}",
                "תחילת טיפול": to_time(start),
                "סיום טיפול": to_time(end),
                "זמן טיפול משוער (דקות)": round(r["_srv"], 1),
                "זמן המתנה (דקות)": round(wait, 1),
            })

            remaining.remove(i)
            order += 1
            waiting = [x for x in remaining if df.loc[x, "_arr"] <= event]

    results = pd.DataFrame(rows)
    horizon = max(1.0, max(available.values()) - first_arrival)

    util = pd.DataFrame([
        {
            "רופא": f"רופא {d}",
            "מספר מטופלים שהוקצו": int((results["רופא משויך"] == f"רופא {d}").sum()),
            "זמן טיפול כולל (דקות)": round(busy[d], 1),
            "ניצול (%)": round(min(100, busy[d] / horizon * 100), 1),
        }
        for d in range(1, n_docs + 1)
    ])

    system_util = min(100, sum(busy.values()) / (n_docs * horizon) * 100)
    return results, util, float(system_util), float(horizon)

# ---------- Style ----------
st.html("""
<style>
#MainMenu,footer,header[data-testid="stHeader"],section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"]{display:none!important}
.stApp{background:#eef5f9}
.block-container{max-width:1450px!important;padding:20px 30px 45px!important}
.hero{direction:rtl;padding:28px 32px;border:1px solid #dceaf2;border-radius:20px;
background:linear-gradient(135deg,#fff,#f7fbfd 70%,#eaf7fb)}
.title{color:#07265f;font-size:36px;font-weight:900;margin:7px 0 0}
.subtitle{color:#5c7186;font-size:13px;line-height:1.8;margin-top:9px}
.section-title{direction:rtl;color:#075e92;font-size:21px;font-weight:900;margin:26px 0 12px}
[data-testid="stMetric"]{min-height:112px;padding:15px 17px;border:1px solid #dce9f1;border-radius:15px;background:#fff}
[data-testid="stMetricValue"]{color:#075b94;font-weight:900}
.note{direction:rtl;margin-top:15px;padding:14px 17px;border:1px solid #d7edf3;border-radius:12px;
background:#eef9fc;color:#49687d;font-size:12px;line-height:1.8}
.note strong{color:#078fa5}
</style>
""")

st.html("""
<div class="hero">
<div style="color:#0797aa;font-size:12px;font-weight:800">MediQueue AI</div>
<div class="title">ניהול התור</div>
<div class="subtitle">
זהו השלב השני במערכת. העמוד מקבל את התרחיש שנשמר ב"נתוני מטופלים"
ומחשב לפי תורת התורים את סדר הטיפול, זמני ההמתנה, חלוקת המטופלים בין הרופאים וניצול המשאבים.
</div></div>
""")

# ---------- Load scenario ----------
if "mediqueue_scenario" not in st.session_state:
    st.warning("לא נמצא תרחיש שמור. יש לחזור לנתוני מטופלים ולשמור תרחיש.")
    st.stop()

scenario = st.session_state["mediqueue_scenario"]
n_patients = int(scenario["number_of_patients"])
n_doctors = int(scenario["number_of_doctors"])
patients = scenario["patients"].copy()

try:
    results, doctor_util, system_util, horizon = run_queue(patients, n_doctors)
except Exception as e:
    st.error("אירעה שגיאה בחישוב ניהול התור.")
    st.exception(e)
    st.stop()

# ---------- Metrics ----------
avg_wait = float(results["זמן המתנה (דקות)"].mean())
median_wait = float(results["זמן המתנה (דקות)"].median())
max_wait = float(results["זמן המתנה (דקות)"].max())
waited = int((results["זמן המתנה (דקות)"] > 0).sum())
waited_pct = waited / n_patients * 100

if avg_wait <= 5 and system_util < 75:
    status = "עומס נמוך"
elif avg_wait <= 15 and system_util < 90:
    status = "עומס בינוני"
else:
    status = "עומס גבוה"

# ---------- Save for next pages ----------
st.session_state["mediqueue_queue_results"] = {
    "number_of_patients": n_patients,
    "number_of_doctors": n_doctors,
    "patients_input": patients.copy(),
    "results": results.copy(),
    "doctor_utilization": doctor_util.copy(),
    "system_utilization": system_util,
    "simulation_horizon_minutes": horizon,
    "avg_wait": avg_wait,
    "median_wait": median_wait,
    "max_wait": max_wait,
    "patients_waited": waited,
    "waited_percent": waited_pct,
    "queue_status": status,
}
st.session_state.pop("mediqueue_analysis", None)
st.session_state.pop("mediqueue_decision_support", None)

# ---------- Display ----------
st.markdown('<div class="section-title">תוצאות ניהול התור</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("מספר מטופלים", n_patients)
c2.metric("מספר רופאים", n_doctors)
c3.metric("זמן המתנה ממוצע", f"{avg_wait:.1f} דקות")
c4.metric("ניצול משאבים", f"{system_util:.1f}%")

c1, c2, c3 = st.columns(3)
c1.metric("מצב התור", status)
c2.metric("מטופלים שהמתינו", f"{waited} ({waited_pct:.1f}%)")
c3.metric("זמן המתנה מקסימלי", f"{max_wait:.1f} דקות")

st.markdown('<div class="section-title">סדר הטיפול וחלוקת המטופלים בין הרופאים</div>', unsafe_allow_html=True)
st.dataframe(results, use_container_width=True, hide_index=True, height=min(700, 38 * len(results) + 40))

st.markdown('<div class="section-title">ניצול הרופאים</div>', unsafe_allow_html=True)
st.dataframe(doctor_util, use_container_width=True, hide_index=True)

st.html(f"""
<div class="note">
<strong>לוגיקת MediQueue AI:</strong><br>
המערכת משתמשת בזמני הגעה, זמני טיפול, רמות דחיפות ומספר הרופאים.
זמן ההמתנה מחושב לפי: <strong>תחילת טיפול − זמן הגעה</strong>.<br><br>
כאשר רופא מתפנה נבחר רק מטופל שכבר הגיע; עדיפות גבוהה קודמת,
ובתוך אותה רמת דחיפות נשמר FCFS. הטיפול Non-preemptive.<br><br>
הפלטים של הפרויקט: <strong>סדר טיפול, זמן המתנה, חלוקה בין רופאים וניצול משאבים</strong>.
התוצאות נשמרות ומועברות ישירות לעמוד "ניתוח התור".
</div>
""")

st.markdown('<div class="section-title">המשך במערכת</div>', unsafe_allow_html=True)
back, nxt = st.columns(2)

with back:
    if st.button("חזרה לנתוני מטופלים", use_container_width=True):
        for p in ["pages/1_Patient_Data.py", "pages/Patient_Data.py"]:
            if (ROOT / p).exists():
                st.switch_page(p)
                break

with nxt:
    if st.button("המשך לניתוח התור", type="primary", use_container_width=True):
        for p in ["pages/3_Queue_Analysis.py", "pages/Queue_Analysis.py"]:
            if (ROOT / p).exists():
                st.switch_page(p)
                break