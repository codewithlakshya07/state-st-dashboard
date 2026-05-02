import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# -----------------------
# STYLE
# -----------------------
st.markdown("""
<style>
div[data-testid="stTabs"] > div {
    overflow-x: auto !important;
    white-space: nowrap;
}
button[data-baseweb="tab"] {
    font-size: 16px !important;
    padding: 10px 20px !important;
    margin-right: 8px !important;
}
.block-container {
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("final_dataset.csv")
df_ind = pd.read_csv("indicator_dataset.csv")  # FIXED

# -----------------------
# COLOR MAP (FIXED)
# -----------------------
palette = {
    'Efficiency Leaders': '#377eb8',   # blue
    'Investment-Inefficient States': '#ff7f00',
    'Capacity-Rich, Output-Constrained': '#4daf4a',
    'Low Capacity States': '#e41a1c'   # red
}

# -----------------------
# TABS
# -----------------------
tab1, tab2, tab3 = st.tabs([
    "📍 System Overview",
    "🔬 Indicators",
    "⚔️ Compare States"
])

# =======================
# TAB 1 — SYSTEM OVERVIEW
# =======================
with tab1:

    col1, col2 = st.columns([3,1])

    with col1:
        st.title("🚀 State S&T Ecosystem Dashboard")

    with col2:
        selected_state = st.selectbox(
            "Select State",
            sorted(df['state_name'].unique())
        )

    state_data = df[df['state_name'] == selected_state].iloc[0]
    avg_vals = df[['P1','P2','P3','P4']].mean()

    # KPI
    k1, k2, k3, k4 = st.columns(4)

    best_pillar = max(['P1','P2','P3','P4'], key=lambda x: state_data[x])
    worst_pillar = min(['P1','P2','P3','P4'], key=lambda x: state_data[x])

    k1.metric("Composite Score", f"{state_data['Composite_score']:.2f}")
    k2.metric("Typology", state_data['typology'])
    k3.metric("Best Pillar", best_pillar)
    k4.metric("Worst Pillar", worst_pillar)

    st.markdown("---")

    # -----------------------
    # SCATTER (FIXED)
    # -----------------------
    st.markdown("## 📍 System Position")

    fig = px.scatter(
        df,
        x='P1',
        y='P3',
        color='typology',
        color_discrete_map=palette,
        size='Composite_score',
        hover_name='state_name',
        size_max=25
    )

    sel = df[df['state_name'] == selected_state]

    fig.add_scatter(
    x=sel['P1'],
    y=sel['P3'],
    mode='markers+text',
    text=[selected_state],
    textposition="top center",
    name=f"Selected: {selected_state}",   
    marker=dict(
        size=18,
        color='white',
        line=dict(width=3, color='red')
    ),
    showlegend=True   
)

    fig.update_layout(
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title=""
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------
    # COMPARISON
    # -----------------------
    st.markdown("## 📊 State vs National Average")

    comp = pd.DataFrame({
        'Pillar': ['P1','P2','P3','P4'],
        'State': [state_data['P1'], state_data['P2'], state_data['P3'], state_data['P4']],
        'Average': [avg_vals['P1'], avg_vals['P2'], avg_vals['P3'], avg_vals['P4']]
    })

    fig2 = go.Figure()
    fig2.add_bar(x=comp['Pillar'], y=comp['State'], name='State')
    fig2.add_bar(x=comp['Pillar'], y=comp['Average'], name='National Avg')
    fig2.update_layout(barmode='group', height=400)

    st.plotly_chart(fig2, use_container_width=True)

    # -----------------------
    # INSIGHT
    # -----------------------
    st.markdown("## 💡 Key Insight")

    p1, p3 = state_data['P1'], state_data['P3']
    avg_p1, avg_p3 = df['P1'].mean(), df['P3'].mean()

    if p1 > avg_p1 and p3 < avg_p3:
        st.warning(f"{selected_state} shows high investment but low output → inefficiency.")
    elif p1 < avg_p1 and p3 > avg_p3:
        st.success(f"{selected_state} is efficiency-driven with strong output.")
    elif p1 > avg_p1 and p3 > avg_p3:
        st.success(f"{selected_state} is a balanced high performer.")
    else:
        st.error(f"{selected_state} has structural capacity gaps.")

# =======================
# TAB 2 — INDICATORS
# =======================
with tab2:

    st.title("🔬 Indicator Analysis")

    selected_state = st.selectbox(
        "Select State",
        sorted(df['state_name'].unique()),
        key="ind_state"
    )

    state_ind = df_ind[df_ind['state_name'] == selected_state].iloc[0]

    st.caption("All indicator values are normalized (0–1 scale).")

    col1, col2 = st.columns(2)

    # P1
    f_df = pd.DataFrame({
        'Indicator': ['F1: Budget', 'F2: Per Capita', 'F3: Share'],
        'Value': [state_ind['F1'], state_ind['F2'], state_ind['F3']]
    })
    col1.plotly_chart(px.bar(f_df, x='Indicator', y='Value', text='Value', range_y=[0,1]), use_container_width=True)

    # P2 (FIXED)
    g_df = pd.DataFrame({
        'Indicator': ['G3: Activity', 'G4: Ecosystem'],
        'Value': [state_ind['G3'], state_ind['G4']]
    })
    col2.plotly_chart(px.bar(g_df, x='Indicator', y='Value', text='Value', range_y=[0,1]), use_container_width=True)

    col3, col4 = st.columns(2)

    # P3
    r_df = pd.DataFrame({
        'Indicator': ['R1', 'R2', 'R3'],
        'Value': [state_ind['R1'], state_ind['R2'], state_ind['R3']]
    })
    col3.plotly_chart(px.bar(r_df, x='Indicator', y='Value', text='Value', range_y=[0,1]), use_container_width=True)

    # P4
    o_df = pd.DataFrame({
        'Indicator': ['O1', 'O2', 'O3'],
        'Value': [state_ind['O1'], state_ind['O2'], state_ind['O3']]
    })
    col4.plotly_chart(px.bar(o_df, x='Indicator', y='Value', text='Value', range_y=[0,1]), use_container_width=True)

# =======================
# TAB 3 — COMPARE STATES
# =======================
with tab3:

    st.title("⚔️ Compare Two States")

    c1, c2 = st.columns(2)

    with c1:
        state_1 = st.selectbox("State 1", sorted(df['state_name'].unique()))

    with c2:
        state_2 = st.selectbox("State 2", sorted(df['state_name'].unique()), index=1)

    data_1 = df[df['state_name'] == state_1].iloc[0]
    data_2 = df[df['state_name'] == state_2].iloc[0]

    categories = ['P1','P2','P3','P4']

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=[data_1[c] for c in categories], theta=categories, fill='toself', name=state_1))
    fig.add_trace(go.Scatterpolar(r=[data_2[c] for c in categories], theta=categories, fill='toself', name=state_2))

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 💡 Comparison Insight")

    if data_1['Composite_score'] > data_2['Composite_score']:
        st.success(f"{state_1} outperforms {state_2}.")
    elif data_2['Composite_score'] > data_1['Composite_score']:
        st.success(f"{state_2} outperforms {state_1}.")
    else:
        st.info("Both states perform similarly.")