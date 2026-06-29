import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide", page_title="Volume & Delta Dashboard")

st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #020617, #000814);
    color: #e2e8f0;
}
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #000814, #020617);
}
div[data-testid="stPlotlyChart"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
.card {
    background: linear-gradient(145deg, rgba(15,23,42,0.9), rgba(2,6,23,0.95));
    border-radius: 10px;
    padding: 5px;
    margin-bottom: 6px;
    border: 1px solid rgba(56,189,248,0.15);
    box-shadow: 0 4px 12px rgba(0,0,0,0.9), 0 0 12px rgba(56,189,248,0.15);
    transition: all 0.2s ease;
}
.card:hover { transform: translateY(-2px); }
.card-title { font-size: 10px; margin-bottom: 2px; color: #38bdf8; }
h3 { font-size: 14px; margin: 6px 0 3px 0; }
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #38bdf8; }
</style>
""", unsafe_allow_html=True)

st.title("📊 Volume & Delta Dashboard")

# -------------------------------------------------
# LOAD DATA — full history, never filtered
# -------------------------------------------------
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv("delta.csv")
    df['date']        = pd.to_datetime(df['date'], dayfirst=False)
    df['total_delta'] = df['delta']
    df['abs_delta']   = df['delta'].abs()
    return df

try:
    df_full = load_data()          # ← full data, never touched after this
except FileNotFoundError:
    st.error("❌ `delta.csv` not found.")
    st.stop()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
if st.sidebar.button("↺ Refresh Data"):
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")

products = sorted(df_full['product_code'].dropna().unique())
selected_products = st.sidebar.multiselect(
    "Select Product",
    options=products,
    default=products
)

st.sidebar.markdown("---")

total_days = (df_full['date'].max() - df_full['date'].min()).days + 1

days = st.sidebar.slider(
    "📅 Display Window (days)",
    min_value=5,
    max_value=max(100, total_days),
    value=min(20, total_days)
)

st.sidebar.markdown("---")

ma_period = st.sidebar.slider(
    "📈 Average Line Period (days)",
    min_value=2,
    max_value=30,
    value=5
)

# -------------------------------------------------
# CHART BUILDER
# MA computed on full history → display window sliced after
# -------------------------------------------------
def make_chart(dff_full, ma_period, days):

    # 1 — sort full instrument history
    dff_full = dff_full.sort_values('date').reset_index(drop=True)

    # 2 — MA on full history so changing display window never affects it
    dff_full['vol_ma']   = (
        dff_full['total_volume']
        .rolling(window=ma_period, min_periods=1)
        .mean()
    )
    dff_full['delta_ma'] = (
        dff_full['abs_delta']
        .rolling(window=ma_period, min_periods=1)
        .mean()
    )

    # 3 — slice to display window only after MA is done
    cutoff = dff_full['date'].max() - pd.Timedelta(days=days - 1)
    dff = dff_full[dff_full['date'] >= cutoff].reset_index(drop=True)

    dff['x']        = dff.index.astype(str)
    dff['date_str'] = dff['date'].dt.strftime('%Y-%m-%d')

    delta_colors = [
        '#22c55e' if x >= 0 else '#ef4444'
        for x in dff['total_delta']
    ]

    border_width = [0] * len(dff)
    if border_width:
        border_width[-1] = 1

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        row_heights=[0.5, 0.5]
    )

    # ── Volume bars + MA ──
    fig.add_trace(go.Bar(
        x=dff['x'],
        y=dff['total_volume'],
        name='Volume',
        marker=dict(
            color='rgba(56,189,248,0.5)',
            line=dict(color='#facc15', width=border_width)
        ),
        customdata=dff[['date_str', 'total_volume']].values,
        hovertemplate="<b>%{customdata[0]}</b><br>Vol: %{customdata[1]:,}<extra></extra>"
    ), row=1, col=1)

    fig.add_trace(go.Scatter(
        x=dff['x'],
        y=dff['vol_ma'],
        name=f'Vol MA{ma_period}',
        mode='lines',
        line=dict(color='#f59e0b', width=1.5),
        customdata=dff[['date_str', 'vol_ma']].values,
        hovertemplate="<b>%{customdata[0]}</b><br>Vol MA{}: %{{customdata[1]:,.0f}}<extra></extra>".format(ma_period)
    ), row=1, col=1)

    # ── Abs Delta bars + MA ──
    fig.add_trace(go.Bar(
        x=dff['x'],
        y=dff['abs_delta'],
        name='|Delta|',
        marker=dict(
            color=delta_colors,
            line=dict(color='#facc15', width=border_width)
        ),
        customdata=dff[['date_str', 'total_delta']].values,
        hovertemplate="<b>%{customdata[0]}</b><br>Δ: %{customdata[1]:,}<extra></extra>"
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=dff['x'],
        y=dff['delta_ma'],
        name=f'|Δ| MA{ma_period}',
        mode='lines',
        line=dict(color='#a78bfa', width=1.5),
        customdata=dff[['date_str', 'delta_ma']].values,
        hovertemplate="<b>%{customdata[0]}</b><br>|Δ| MA{}: %{{customdata[1]:,.0f}}<extra></extra>".format(ma_period)
    ), row=2, col=1)

    fig.update_layout(
        height=200,
        margin=dict(l=2, r=2, t=5, b=2),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e2e8f0", size=9),
        hovermode="x unified",
        bargap=0.2
    )

    fig.update_xaxes(showticklabels=False, showgrid=False)
    fig.update_yaxes(showgrid=False, zeroline=False)

    return fig

# -------------------------------------------------
# DASHBOARD
# pass df_full instrument slice — not the filtered df
# -------------------------------------------------
cols_per_row = 5

for product in selected_products:

    # filter by product only — NO date filter here
    product_df = df_full[df_full['product_code'] == product]
    if product_df.empty:
        continue

    st.subheader(f"📦 {product}")

    instruments = list(product_df['instrument'].unique())

    for i in range(0, len(instruments), cols_per_row):

        row_instruments = instruments[i:i+cols_per_row]
        cols = st.columns(cols_per_row)

        for j in range(cols_per_row):
            with cols[j]:

                if j >= len(row_instruments):
                    st.markdown(
                        "<div style='height:200px; visibility:hidden;'></div>",
                        unsafe_allow_html=True
                    )
                    continue

                inst = row_instruments[j]

                # full instrument history → MA computed inside, window sliced inside
                dff_full = product_df[product_df['instrument'] == inst].copy()

                fig = make_chart(dff_full, ma_period, days)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="card-title">{inst}</div>',
                    unsafe_allow_html=True
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
