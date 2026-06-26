import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
st.set_page_config(layout="wide", page_title="VAP Terminal")

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap');

/* ── BASE ── */
.stApp {
    background: #080c14;
    color: #c9d1d9;
    font-family: 'Inter', sans-serif;
}

section[data-testid="stSidebar"] {
    background: #0a0f1a;
    border-right: 1px solid #1a2235;
}

section[data-testid="stSidebar"] * {
    font-family: 'JetBrains Mono', monospace !important;
    color: #4a5a6e !important;
}

section[data-testid="stSidebar"] label {
    font-size: 10px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #2d3a4f !important;
}

/* SIDEBAR MULTISELECT */
[data-testid="stMultiSelect"] > div {
    background: #0d1525 !important;
    border: 1px solid #1a2235 !important;
    border-radius: 4px !important;
    color: #38bdf8 !important;
}

[data-testid="stMultiSelect"] span {
    background: rgba(56,189,248,0.1) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56,189,248,0.2) !important;
    border-radius: 3px !important;
    font-size: 10px !important;
}

/* SIDEBAR SLIDER */
[data-testid="stSlider"] > div > div > div {
    background: #38bdf8 !important;
}

[data-testid="stSlider"] .rc-slider-track {
    background: linear-gradient(90deg, #1e4a6e, #38bdf8) !important;
}

[data-testid="stSlider"] .rc-slider-rail {
    background: #1a2235 !important;
}

/* PLOTLY CHART */
div[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}

/* ── TITLE BAR ── */
.term-header {
    background: #0d1220;
    border: 1px solid #1a2235;
    border-radius: 8px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.term-logo {
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 3px;
}

.term-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    padding: 2px 8px;
    border-radius: 3px;
    background: rgba(56,189,248,0.1);
    color: #38bdf8;
    border: 1px solid rgba(56,189,248,0.2);
    letter-spacing: 1px;
    margin-left: 10px;
}

.term-live {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    padding: 2px 8px;
    border-radius: 3px;
    background: rgba(34,197,94,0.1);
    color: #22c55e;
    border: 1px solid rgba(34,197,94,0.25);
    letter-spacing: 1px;
    margin-left: 6px;
}

.term-time {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #2d4560;
}

/* ── STAT STRIP ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 12px;
}

.stat-card {
    background: #0d1525;
    border: 1px solid #1a2235;
    border-radius: 6px;
    padding: 10px 12px;
}

.stat-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #2d4560;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.stat-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    color: #e2e8f0;
}

.stat-value.pos { color: #22c55e; }
.stat-value.neg { color: #ef4444; }

.stat-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #2d4560;
    margin-top: 3px;
}

/* ── SECTION HEADER ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 14px 0 8px;
    padding-bottom: 6px;
    border-bottom: 1px solid #111a28;
}

.section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 2px;
}

.section-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    padding: 2px 8px;
    border-radius: 3px;
    background: rgba(56,189,248,0.07);
    color: #38bdf8;
    border: 1px solid rgba(56,189,248,0.15);
    letter-spacing: 1px;
}

.section-count {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #1e2d3d;
    margin-left: auto;
}

/* ── INSTRUMENT CARD ── */
.inst-card {
    background: #0d1525;
    border: 1px solid #1a2235;
    border-radius: 6px;
    overflow: hidden;
    transition: border-color 0.2s;
    margin-bottom: 0;
}

.inst-card:hover {
    border-color: rgba(56,189,248,0.3);
}

.inst-card-header {
    padding: 5px 8px 4px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid #111a28;
}

.inst-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #38bdf8;
    letter-spacing: 0.5px;
}

.inst-delta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 700;
}

.inst-delta.pos { color: #22c55e; }
.inst-delta.neg { color: #ef4444; }

.inst-footer {
    padding: 3px 8px;
    display: flex;
    justify-content: space-between;
    border-top: 1px solid #111a28;
}

.inst-stat {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    color: #1e2d3d;
}

.inst-stat span { color: #3a5068; }

/* ── STATUS BAR ── */
.statusbar {
    background: #060a10;
    border: 1px solid #111a28;
    border-radius: 6px;
    padding: 5px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #1e2d3d;
}

.statusbar span { color: #2d4560; }
.statusbar b { color: #38bdf8; font-weight: 500; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: #1a2235; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #38bdf8; }

/* HIDE STREAMLIT DECORATIONS */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("delta.csv")
    df['date']        = pd.to_datetime(df['date'])
    df['total_delta'] = df['delta']
    df['abs_delta']   = df['delta'].abs()
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ `delta.csv` not found. Commit it to your repo root.")
    st.stop()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.markdown(
    '<div style="font-family:JetBrains Mono,monospace; font-size:13px; font-weight:700; '
    'color:#38bdf8; letter-spacing:3px; padding: 8px 0 16px;">VAP TERMINAL</div>',
    unsafe_allow_html=True
)

products = sorted(df['product_code'].dropna().unique())

selected_products = st.sidebar.multiselect(
    "PRODUCTS",
    options=products,
    default=products
)

days = st.sidebar.slider("DAYS", 5, 100, 20)

# -------------------------------------------------
# FILTER
# -------------------------------------------------
df = df[df['product_code'].isin(selected_products)]

cutoff_date = df['date'].max() - pd.Timedelta(days=days)
df = df[df['date'] >= cutoff_date]

# -------------------------------------------------
# HEADER BAR
# -------------------------------------------------
from datetime import datetime

st.markdown(f"""
<div class="term-header">
    <div style="display:flex; align-items:center;">
        <div class="term-logo">VAP</div>
        <div class="term-badge">TERMINAL v2</div>
        <div class="term-live">● LIVE</div>
    </div>
    <div class="term-time">UTC &nbsp; {datetime.utcnow().strftime('%H:%M:%S')} &nbsp;&nbsp; SESSION {datetime.utcnow().strftime('%Y-%m-%d')}</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# STAT STRIP
# -------------------------------------------------
total_vol   = df['total_volume'].sum()
net_delta   = df['total_delta'].sum()
buy_vol     = df['buying_volume'].sum()
sell_vol    = df['selling_volume'].sum()

def fmt(n):
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.1f}K"
    return str(n)

delta_class = "pos" if net_delta >= 0 else "neg"
delta_sign  = "+" if net_delta >= 0 else ""
buy_pct     = buy_vol / total_vol * 100 if total_vol else 0
sell_pct    = 100 - buy_pct

st.markdown(f"""
<div class="stat-grid">
    <div class="stat-card">
        <div class="stat-label">Total Volume</div>
        <div class="stat-value">{fmt(total_vol)}</div>
        <div class="stat-sub">{days}d window</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Net Delta</div>
        <div class="stat-value {delta_class}">{delta_sign}{fmt(net_delta)}</div>
        <div class="stat-sub">{"Buy pressure" if net_delta >= 0 else "Sell pressure"}</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Buy Volume</div>
        <div class="stat-value pos">{fmt(buy_vol)}</div>
        <div class="stat-sub">{buy_pct:.1f}% of total</div>
    </div>
    <div class="stat-card">
        <div class="stat-label">Sell Volume</div>
        <div class="stat-value neg">{fmt(sell_vol)}</div>
        <div class="stat-sub">{sell_pct:.1f}% of total</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
COLS = 5

for product in selected_products:

    product_df = df[df['product_code'] == product]
    if product_df.empty:
        continue

    instruments = list(product_df['instrument'].unique())

    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">{product}</div>
        <div class="section-tag">VOLUME & DELTA</div>
        <div class="section-count">{len(instruments)} INSTRUMENTS</div>
    </div>
    """, unsafe_allow_html=True)

    for i in range(0, len(instruments), COLS):

        row_insts = instruments[i:i+COLS]
        cols      = st.columns(COLS)

        for j in range(COLS):
            with cols[j]:

                if j >= len(row_insts):
                    st.markdown("<div style='height:160px'></div>", unsafe_allow_html=True)
                    continue

                inst = row_insts[j]

                dff = (
                    product_df[product_df['instrument'] == inst]
                    .sort_values('date')
                    .reset_index(drop=True)
                )

                dff['x']        = dff.index.astype(str)
                dff['date_str'] = dff['date'].dt.strftime('%Y-%m-%d')

                last_delta = dff['total_delta'].iloc[-1] if len(dff) else 0
                delta_sign = "+" if last_delta >= 0 else ""
                delta_cls  = "pos" if last_delta >= 0 else "neg"

                # card header
                st.markdown(f"""
                <div class="inst-card">
                    <div class="inst-card-header">
                        <div class="inst-name">{inst}</div>
                        <div class="inst-delta {delta_cls}">{delta_sign}{int(last_delta):,}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # chart
                colors = [
                    '#22c55e' if x >= 0 else '#ef4444'
                    for x in dff['total_delta']
                ]

                opacity_colors = [
                    'rgba(34,197,94,0.4)' if x >= 0 else 'rgba(239,68,68,0.4)'
                    for x in dff['total_delta']
                ]
                opacity_colors[-1] = colors[-1]  # last bar full opacity

                border_w = [0] * len(dff)
                if border_w: border_w[-1] = 1

                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.02,
                    row_heights=[0.42, 0.58]
                )

                fig.add_trace(go.Bar(
                    x=dff['x'],
                    y=dff['abs_delta'],
                    marker=dict(
                        color=opacity_colors,
                        line=dict(color='#facc15', width=border_w)
                    ),
                    customdata=dff[['date_str','total_delta']].values,
                    hovertemplate="<b>%{customdata[0]}</b><br>Δ %{customdata[1]:,}<extra></extra>"
                ), row=1, col=1)

                vol_colors = ['rgba(56,189,248,0.3)'] * len(dff)
                if vol_colors: vol_colors[-1] = '#38bdf8'

                fig.add_trace(go.Bar(
                    x=dff['x'],
                    y=dff['total_volume'],
                    marker=dict(
                        color=vol_colors,
                        line=dict(color='#facc15', width=border_w)
                    ),
                    customdata=dff[['date_str','total_volume']].values,
                    hovertemplate="<b>%{customdata[0]}</b><br>Vol %{customdata[1]:,}<extra></extra>"
                ), row=2, col=1)

                fig.update_layout(
                    height=140,
                    margin=dict(l=0, r=0, t=0, b=0),
                    showlegend=False,
                    plot_bgcolor="#0d1525",
                    paper_bgcolor="#0d1525",
                    font=dict(color="#38bdf8", size=8, family="JetBrains Mono"),
                    hovermode="x unified",
                    bargap=0.15,
                    hoverlabel=dict(
                        bgcolor="#0d1525",
                        bordercolor="#1a2235",
                        font=dict(color="#e2e8f0", size=10, family="JetBrains Mono")
                    )
                )

                fig.update_xaxes(
                    showticklabels=False,
                    showgrid=False,
                    zeroline=False,
                    showline=False
                )

                fig.update_yaxes(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    showticklabels=False
                )

                st.plotly_chart(fig, use_container_width=True)

                # card footer
                total_v = int(dff['total_volume'].sum())
                st.markdown(f"""
                <div style="background:#0d1525; border:1px solid #1a2235; border-top:none;
                     border-radius:0 0 6px 6px; padding:3px 8px;
                     display:flex; justify-content:space-between; margin-top:-8px;">
                    <div class="inst-stat">VOL <span>{fmt(total_v)}</span></div>
                    <div class="inst-stat {delta_cls}">Δ <span style="color:{'#22c55e' if last_delta>=0 else '#ef4444'}">{delta_sign}{fmt(int(last_delta))}</span></div>
                </div>
                """, unsafe_allow_html=True)

# -------------------------------------------------
# STATUS BAR
# -------------------------------------------------
st.markdown(f"""
<div class="statusbar">
    <div>VAP DASHBOARD — VOLUME & DELTA ANALYTICS</div>
    <div style="display:flex; gap:20px;">
        <div><span>DATA</span> <b>delta.csv</b></div>
        <div><span>ROWS</span> <b>{len(df):,}</b></div>
        <div><span>WINDOW</span> <b>{days}d</b></div>
        <div><span>UPDATED</span> <b>{datetime.utcnow().strftime('%H:%M:%S')}</b></div>
    </div>
</div>
""", unsafe_allow_html=True)
