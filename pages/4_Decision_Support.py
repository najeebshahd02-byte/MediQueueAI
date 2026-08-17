from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="MediQueue AI | תמיכה בהחלטות", layout="wide", initial_sidebar_state="collapsed")
ROOT = Path(__file__).resolve().parents[1]
URG = {"גבוהה": 3, "בינונית": 2, "נמוכה": 1}

# ---------- Same queue logic ----------
def mins(t):
    h, m = map(int, str(t)[:5].split(":"))
    return h * 60 + m

def simulate(df, doctors):
    x = df.copy().reset_index(drop=True)
    x["a"] = x["זמן הגעה"].apply(mins)
    x["s"] = pd.to_numeric(x["זמן טיפול משוער (דקות)"])
    x["u"] = x["רמת דחיפות"].map(URG)
    x["o"] = range(len(x))

    free = [x["a"].min()] * doctors
    busy = [0] * doctors
    left, waits = set(x.index), []

    while left:
        now = max(min(free), min(x.loc[i, "a"] for i in left))
        docs = [d for d in range(doctors) if free[d] <= now]
        waiting = [i for i in left if x.loc[i, "a"] <= now]

        while docs and waiting:
            d = docs.pop(0)
            i = min(waiting, key=lambda j: (-x.loc[j, "u"], x.loc[j, "a"], x.loc[j, "o"]))
            start = max(now, free[d], x.loc[i, "a"])
            waits.append(start - x.loc[i, "a"])
            free[d] = start + x.loc[i, "s"]
            busy[d] += x.loc[i, "s"]
            left.remove(i)
            waiting = [j for j in left if x.loc[j, "a"] <= now]

    horizon = max(free) - x["a"].min()
    w = pd.Series(waits)
    return {
        "doctors": doctors,
        "avg": round(w.mean(), 1),
        "max": round(w.max(), 1),
        "waited": int((w > 0).sum()),
        "util": round(min(100, sum(busy) / (doctors * horizon) * 100), 1)
    }

# ---------- Data ----------
if "mediqueue_queue_results" not in st.session_state:
    st.error("יש להריץ קודם את שלב ניהול התור.")
    st.stop()

q = st.session_state["mediqueue_queue_results"]
patients = q["patients_input"].copy()
current = int(q["number_of_doctors"])
options = sorted(set([max(1, current - 1), current, current + 1]))
results = pd.DataFrame([simulate(patients, d) for d in options])

cur = results[results.doctors == current].iloc[0]
better = results[results.doctors == current + 1]
improved = better.iloc[0] if len(better) else cur

# ---------- Design ----------
st.html("""
<style>
#MainMenu,footer,header[data-testid="stHeader"],section[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"]{display:none!important}
.stApp{background:#f1f7fa}
.block-container{max-width:1450px!important;padding:22px 34px 50px!important}
.hero{direction:rtl;background:linear-gradient(125deg,#fff 25%,#f7fcfe 70%,#e9f7fb);
border:1px solid #d7e9f1;border-radius:22px;padding:30px 34px;margin-bottom:30px}
.brand{font-size:12px;font-weight:800;color:#0797aa}
.hero h1{font-size:39px;color:#092d68;margin:8px 0 6px;font-weight:900}
.hero p{font-size:14px;color:#61778a;margin:0}
.section{direction:rtl;font-size:23px;font-weight:900;color:#076397;margin:28px 0 15px}
.scenarios{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;direction:rtl}
.card{background:#fff;border:1px solid #dce9ef;border-radius:18px;padding:22px;box-shadow:0 3px 12px #163b5c0a}
.card.current{border:2px solid #1596ba}
.card.improved{border:2px solid #2b9f88}
.badge{display:inline-block;border-radius:20px;padding:5px 11px;font-size:11px;font-weight:800;background:#edf5f8;color:#607485}
.current .badge{background:#e8f7fb;color:#087e9e}.improved .badge{background:#eaf8f4;color:#21836f}
.docs{font-size:26px;font-weight:900;color:#10366c;margin:12px 0 18px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.metric{background:#f7fafc;border-radius:12px;padding:12px}
.metric span{display:block;font-size:11px;color:#738596;margin-bottom:5px}
.metric b{font-size:20px;color:#075f96}
.insight{direction:rtl;background:#fff;border:1px solid #d7e8ef;border-right:5px solid #1695aa;
border-radius:16px;padding:22px 25px;color:#526c7e;line-height:2}
.insight b{color:#087d97}
[data-testid="stPlotlyChart"]{background:#fff;border:1px solid #deebf1;border-radius:18px;padding:10px}
.stButton button{height:48px;border-radius:12px;font-weight:800}
</style>
""")

st.html("""
<div class="hero">
 <div class="brand">MediQueue AI</div>
 <h1>תמיכה בהחלטות</h1>
 <p>השוואת חלופות ניהוליות באמצעות שינוי מספר הרופאים בלבד, תוך שמירה על אותם מטופלים, זמני הגעה, זמני טיפול ורמות דחיפות.</p>
</div>
<div class="section">השוואת תרחישים</div>
""")

# ---------- Scenario cards ----------
cards = '<div class="scenarios">'
for _, r in results.iterrows():
    if r.doctors == current:
        cls, badge = "card current", "מצב נוכחי"
    elif r.doctors == current + 1:
        cls, badge = "card improved", "חלופה משופרת"
    else:
        cls, badge = "card", "חלופה חלופית"

    cards += f"""
    <div class="{cls}">
      <span class="badge">{badge}</span>
      <div class="docs">{int(r.doctors)} רופאים</div>
      <div class="grid">
        <div class="metric"><span>זמן המתנה ממוצע</span><b>{r.avg:.1f} דק׳</b></div>
        <div class="metric"><span>זמן המתנה מקסימלי</span><b>{r['max']:.0f} דק׳</b></div>
        <div class="metric"><span>מטופלים שהמתינו</span><b>{int(r.waited)} מתוך {len(patients)}</b></div>
        <div class="metric"><span>ניצול משאבים</span><b>{r.util:.1f}%</b></div>
      </div>
    </div>"""
cards += "</div>"
st.html(cards)

# ---------- One clean comparison chart ----------
st.markdown('<div class="section">השפעת מספר הרופאים על ביצועי התור</div>', unsafe_allow_html=True)

fig = go.Figure()
fig.add_trace(go.Bar(
    x=[f"{d} רופאים" for d in results.doctors],
    y=results["avg"],
    name="זמן המתנה ממוצע",
    text=[f"{v:.1f}" for v in results["avg"]],
    textposition="outside"
))
fig.add_trace(go.Scatter(
    x=[f"{d} רופאים" for d in results.doctors],
    y=results["util"],
    name="ניצול משאבים (%)",
    mode="lines+markers+text",
    text=[f"{v:.1f}%" for v in results["util"]],
    textposition="top center",
    yaxis="y2"
))
fig.update_layout(
    height=430, margin=dict(l=35,r=35,t=55,b=35),
    paper_bgcolor="white", plot_bgcolor="white",
    legend=dict(orientation="h", y=1.12, x=1, xanchor="right"),
    xaxis_title="מספר רופאים",
    yaxis=dict(title="זמן המתנה ממוצע (דקות)", rangemode="tozero"),
    yaxis2=dict(title="ניצול משאבים (%)", overlaying="y", side="right", range=[0,105]),
    bargap=.5
)
st.plotly_chart(fig, use_container_width=True)

# ---------- Managerial insight ----------
reduction = cur["avg"] - improved["avg"]
max_reduction = cur["max"] - improved["max"]

st.markdown('<div class="section">תובנה ניהולית</div>', unsafe_allow_html=True)
st.html(f"""
<div class="insight">
בהשוואה למצב הנוכחי של <b>{current} רופאים</b>, תרחיש של
<b>{int(improved.doctors)} רופאים</b> מפחית את זמן ההמתנה הממוצע
מ־<b>{cur["avg"]:.1f}</b> ל־<b>{improved["avg"]:.1f} דקות</b>
ואת זמן ההמתנה המקסימלי מ־<b>{cur["max"]:.0f}</b> ל־<b>{improved["max"]:.0f} דקות</b>.
במקביל, ניצול המשאבים משתנה מ־<b>{cur["util"]:.1f}%</b> ל־<b>{improved["util"]:.1f}%</b>.<br>
המערכת אינה קובעת פתרון אופטימלי, אלא מציגה את השפעת החלופות כדי לתמוך בהחלטה הניהולית.
</div>
""")

st.session_state["mediqueue_decision_support"] = results.copy()

st.markdown('<div class="section">המשך במערכת</div>', unsafe_allow_html=True)
a, b = st.columns(2)
with a:
    if st.button("חזרה לניתוח התור", use_container_width=True):
        st.switch_page("pages/3_Queue_Analysis.py")
with b:
    if st.button("המשך להערכת המערכת", type="primary", use_container_width=True):
        page = ROOT / "pages/5_System_Evaluation.py"
        if page.exists():
            st.switch_page("pages/5_System_Evaluation.py")
        else:
            st.info("עמוד הערכת המערכת ייבנה בשלב הבא.")