import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
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
    box-shadow: 
        0 4px 12px rgba(0,0,0,0.9),
        0 0 12px rgba(56,189,248,0.15);
    transition: all 0.2s ease;
}

.card:hover {
    transform: translateY(-2px);
}

.card-title {
    font-size: 10px;
    margin-bottom: 2px;
    color: #38bdf8;
}

h3 {
    font-size: 14px;
    margin: 6px 0 3px 0;
}

::-webkit-scrollbar {
    width: 4px;
}
::-webkit-scrollbar-thumb {
    background: #38bdf8;
}

</style>
""", unsafe_allow_html=True)

st.title("📊 Volume & Delta Dashboard")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("delta.csv")
    df['date']       = pd.to_datetime(df['date'])
    df['total_delta'] = df['delta']
    df['abs_delta']   = df['delta'].abs()
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "❌ `delta.csv` not found.  \n"
        "Make sure the file is committed to the **root** of your GitHub repo."
    )
    st.stop()

# -------------------------------------------------
# FILTERS
# -------------------------------------------------
products = sorted(df['product_code'].dropna().unique())

selected_products = st.sidebar.multiselect(
    "Select Product",
    options=products,
    default=products
)

df = df[df['product_code'].isin(selected_products)]

days = st.sidebar.slider("Days", 5, 100, 20)

cutoff_date = df['date'].max() - pd.Timedelta(days=days)
df = df[df['date'] >= cutoff_date]

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
cols_per_row = 5

for product in selected_products:

    product_df = df[df['product_code'] == product]
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
                        "<div style='height:150px; visibility:hidden;'></div>",
                        unsafe_allow_html=True
                    )
                    continue

                inst = row_instruments[j]

                dff = (
                    product_df[product_df['instrument'] == inst]
                    .sort_values('date')
                    .reset_index(drop=True)
                )

                dff['x']        = dff.index.astype(str)
                dff['date_str'] = dff['date'].dt.strftime('%Y-%m-%d')

                colors = [
                    '#22c55e' if x >= 0 else '#ef4444'
                    for x in dff['total_delta']
                ]

                border_width = [0] * len(dff)
                if border_width:
                    border_width[-1] = 1

                fig = make_subplots(
                    rows=2, cols=1,
                    shared_xaxes=True,
                    vertical_spacing=0.01,
                    row_heights=[0.4, 0.6]
                )

                fig.add_trace(go.Bar(
                    x=dff['x'],
                    y=dff['abs_delta'],
                    marker=dict(
                        color=colors,
                        line=dict(color='#facc15', width=border_width)
                    ),
                    customdata=dff['date_str'],
                    hovertemplate="<b>Date:</b> %{customdata}<br>Δ: %{y}<extra></extra>"
                ), row=1, col=1)

                fig.add_trace(go.Bar(
                    x=dff['x'],
                    y=dff['total_volume'],
                    marker=dict(
                        color='#38bdf8',
                        line=dict(color='#facc15', width=border_width)
                    ),
                    customdata=dff['date_str'],
                    hovertemplate="<b>Date:</b> %{customdata}<br>Vol: %{y}<extra></extra>"
                ), row=2, col=1)

                fig.update_layout(
                    height=150,
                    margin=dict(l=2, r=2, t=5, b=2),
                    showlegend=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#e2e8f0", size=9),
                    hovermode="x unified"
                )

                fig.update_xaxes(showticklabels=False)
                fig.update_yaxes(showgrid=False)

                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown(
                    f'<div class="card-title">{inst}</div>',
                    unsafe_allow_html=True
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
