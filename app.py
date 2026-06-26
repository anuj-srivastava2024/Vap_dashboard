import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

st.set_page_config(layout="wide", page_title="VAP Terminal")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&display=swap');

.stApp { background: #080c14 !important; color: #c9d1d9; }

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: #0a0f1a !important;
    border-right: 1px solid #1a2235 !important;
}

/* sidebar all text */
section[data-testid="stSidebar"] * {
    font-family: 'JetBrains Mono', monospace !important;
    color: #4a6580 !important;
}

/* sidebar labels */
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stMarkdown p {
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #2d4560 !important;
}

/* multiselect box */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] > div > div {
    background: #0d1525 !important;
    border: 1px solid #1a2235 !important;
    border-radius: 4px !important;
}

/* multiselect tags */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background: rgba(56,189,248,0.12) !important;
    border: 1px solid rgba(56,189,248,0.25) !important;
    border-radius: 3px !important;
}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] span[data-baseweb="tag"] span {
    color: #38bdf8 !important;
    font-size: 10px !important;
}

/* multiselect input text */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] input {
    color: #38bdf8 !important;
    font-size: 11px !important;
}

/* multiselect dropdown options */
section[data-testid="stSidebar"] [data-testid="stMultiSelect"] li {
    background: #0d1525 !important;
    color: #4a6580 !important;
    font-size: 11px !important;
}

section[data-testid="stSidebar"] [data-testid="stMultiSelect"] li:hover {
    background: rgba(56,189,248,0.08) !important;
    color: #38bdf8 !important;
}

/* slider track */
div[class*="stSlider"] [data-testid="stSliderTrackFill"] {
    background: #38bdf8 !important;
}

/* slider thumb */
div[class*="stSlider"] > div > div > div[role="slider"] {
    background: #38bdf8 !important;
    border: none !important;
    box-shadow: 0 0 8px rgba(56,189,248,0.6) !important;
}

/* slider value label */
div[class*="stSlider"] [data-testid="stThumbValue"],
div[class*="stSlider"] [data-testid="stTickBarMin"],
div[class*="stSlider"] [data-testid="stTickBarMax"] {
    color: #38bdf8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
}

/* MAIN */
div[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.term-header {
    background: #0d1220;
    border: 1px solid #1a2235;
    border-radius: 8px;
    padding: 8px 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
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
    color: #4a6580;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 16px 0 10px;
    padding-bottom: 7px;
    border-bottom: 1px solid #111a28;
}

.section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
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

.inst-label {
    background: #0d1525;
    border: 1px solid #1a2235;
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 5px 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.inst-name {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #38bdf8;
}

.inst-delta { font-family: 'JetBrains Mono', monospace; font-size: 9px; font-weight: 700; }
.inst-delta.pos { color: #22c55e; }
.inst-delta.neg { color: #ef4444; }

.inst-footer {
    background: #0d1525;
    border: 1px solid #1a2235;
    border-top: none;
    border-radius: 0 0 6px 6px;
    padding: 3px 8px;
    display: flex;
    justify-content: space-between;
    margin-top: -6px;
}

.inst-stat { font-family: 'JetBrains Mono', monospace; font-size: 8px; color: #1e2d3d; }
.inst-stat span { color: #3a5068; }

.statusbar {
    background: #060a10;
    border: 1px solid #111a28;
    border-radius: 6px;
    padding: 5px 14px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: #1e2d3d;
}

.statusbar span { color: #2d4560; }
.statusbar b    { color: #38bdf8; font-weight: 500; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #080c14; }
::-webkit-scrollbar-thumb { background: #1a2235; border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #38bdf8; }

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
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
    st.error("❌ delta.csv not found.")
    st.stop()

all_products = sorted(df['product_code'].dropna().unique())

# -------------------------------------------------
# SIDEBAR — native widgets only, no custom HTML
# -------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("PRODUCTS")
selected_products = st.sidebar.multiselect(
    "Select products",
    options=all_products,
    default=all_products,
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown("DAYS")
days = st.sidebar.slider(
    "Days",
    min_value=5,
    max_value=100,
    value=20,
    label_visibility="collapsed"
)

# -------------------------------------------------
# FILTER
# -------------------------------------------------
df_f   = df[df['product_code'].isin(selected_products)].copy()
cutoff = df_f['date'].max() - pd.Timedelta(days=days)
df_f   = df_f[df_f['date'] >= cutoff]

# -------------------------------------------------
# HELPERS
# -------------------------------------------------
def fmt(n):
    n = int(n)
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,}"

def make_chart(dff):
    colors_d = [
        'rgba(34,197,94,0.4)' if x >= 0 else 'rgba(239,68,68,0.4)'
        for x in dff['total_delta']
    ]
    if colors_d:
        colors_d[-1] = '#22c55e' if dff['total_delta'].iloc[-1] >= 0 else '#ef4444'

    bw = [0] * len(dff)
    if bw: bw[-1] = 1

    vc = ['rgba(56,189,248,0.3)'] * len(dff)
    if vc: vc[-1] = '#38bdf8'

    fig = make_subplots(
        rows=2, cols=1, shared_xaxes=True,
        vertical_spacing=0.02, row_heights=[0.42, 0.58]
    )

    fig.add_trace(go.Bar(
        x=dff['x'], y=dff['abs_delta'],
        marker=dict(color=colors_d, line=dict(color='#facc15', width=bw)),
        customdata=dff[['date_str', 'total_delta']].values,
        hovertemplate="<b>%{customdata[0]}</b><br>Δ %{customdata[1]:,}<extra></extra>"
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=dff['x'], y=dff['total_volume'],
        marker=dict(color=vc, line=dict(color='#facc15', width=bw)),
        customdata=dff[['date_str', 'total_volume']].values,
        hovertemplate="<b>%{customdata[0]}</b><br>Vol %{customdata[1]:,}<extra></extra>"
    ), row=2, col=1)

    fig.update_layout(
        height=145,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
        plot_bgcolor="#0d1525",
        paper_bgcolor="#0d1525",
        font=dict(color="#38bdf8", size=8, family="JetBrains Mono"),
        hovermode="x unified", bargap=0.15,
        hoverlabel=dict(
            bgcolor="#0d1525", bordercolor="#1a2235",
            font=dict(color="#e2e8f0", size=10, family="JetBrains Mono")
        )
    )
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False, showline=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showline=False, showticklabels=False)
    return fig

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(f"""
<div class="term-header">
    <div style="display:flex;align-items:center;">
        <div class="term-logo">VAP</div>
        <div class="term-badge">TERMINAL v2</div>
        <div class="term-live">● LIVE</div>
    </div>
    <div class="term-time">
        UTC &nbsp; {datetime.utcnow().strftime('%H:%M:%S')}
        &nbsp;&nbsp; SESSION {datetime.utcnow().strftime('%Y-%m-%d')}
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
COLS = 5

for product in selected_products:

    product_df = df_f[df_f['product_code'] == product]
    if product_df.empty:
        continue

    instruments = list(product_df['instrument'].unique())

    st.markdown(f"""
    <div class="section-header">
        <div class="section-title">{product}</div>
        <div class="section-tag">VOLUME &amp; DELTA</div>
        <div class="section-count">{len(instruments)} INSTRUMENTS</div>
    </div>
    """, unsafe_allow_html=True)

    for i in range(0, len(instruments), COLS):

        row_insts = instruments[i:i + COLS]
        cols      = st.columns(COLS)

        for j, col in enumerate(cols):
            with col:

                if j >= len(row_insts):
                    st.empty()
                    continue

                inst = row_insts[j]

                dff = (
                    product_df[product_df['instrument'] == inst]
                    .sort_values('date')
                    .reset_index(drop=True)
                )

                dff['x']        = dff.index.astype(str)
                dff['date_str'] = dff['date'].dt.strftime('%Y-%m-%d')

                last_delta = int(dff['total_delta'].iloc[-1]) if len(dff) else 0
                sign       = "+" if last_delta >= 0 else ""
                dcls       = "pos" if last_delta >= 0 else "neg"
                total_v    = int(dff['total_volume'].sum())

                st.markdown(f"""
                <div class="inst-label">
                    <div class="inst-name">{inst}</div>
                    <div class="inst-delta {dcls}">{sign}{last_delta:,}</div>
                </div>
                """, unsafe_allow_html=True)

                fig = make_chart(dff)
                st.plotly_chart(fig, use_container_width=True,
                                config={'displayModeBar': False})

                st.markdown(f"""
                <div class="inst-footer">
                    <div class="inst-stat">VOL <span>{fmt(total_v)}</span></div>
                    <div class="inst-stat">Δ <span style="color:{'#22c55e' if last_delta>=0 else '#ef4444'};">
                        {sign}{fmt(last_delta)}</span></div>
                </div>
                """, unsafe_allow_html=True)

# -------------------------------------------------
# STATUS BAR
# -------------------------------------------------
st.markdown(f"""
<div class="statusbar">
    <div>VAP DASHBOARD — VOLUME &amp; DELTA ANALYTICS</div>
    <div style="display:flex;gap:20px;">
        <div><span>DATA</span> <b>delta.csv</b></div>
        <div><span>ROWS</span> <b>{len(df_f):,}</b></div>
        <div><span>WINDOW</span> <b>{days}d</b></div>
        <div><span>UPDATED</span> <b>{datetime.utcnow().strftime('%H:%M:%S')}</b></div>
    </div>
</div>
""", unsafe_allow_html=True)
