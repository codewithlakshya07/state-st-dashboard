import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# -----------------------
# STYLE (bigger tabs + cleaner UI)
# -----------------------
st.markdown("""
<style>

/* Fix tab container overflow */
div[data-testid="stTabs"] > div {
    overflow-x: auto !important;
    white-space: nowrap;
}

/* Make tabs visible and scrollable */
button[data-baseweb="tab"] {
    font-size: 16px !important;
    padding: 10px 20px !important;
    margin-right: 8px !important;
}

/* Ensure full width usage */
.block-container {
    max-width: 100% !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Remove clipping issue */
section.main > div {
    overflow: visible !important;
}

</style>
""", unsafe_allow_html=True)
# -----------------------
# LOAD DATA
# -----------------------
df = pd.read_csv("final_dataset.csv")
df_ind = pd.read_csv("indicator_dataset.csv")

# -----------------------
# TABS FIRST (controls visibility)
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

    # HEADER + SELECTOR ONLY HERE
    col1, col2 = st.columns([3,1])

    with col1:
        st.title("🚀 State S&T Ecosystem Dashboard")

    with col2:
        selected_state = st.selectbox(
            "Select State",
            sorted(df['state_name'].unique())
        )

    state_data = df[df['state_name'] == selected_state].iloc[0]
    state_ind = df_ind[df_ind['state_name'] == selected_state].iloc[0]
    avg_vals = df[['P1','P2','P3','P4']].mean()

    # KPI ROW
    k1, k2, k3, k4 = st.columns(4)

    best_pillar = max(['P1','P2','P3','P4'], key=lambda x: state_data[x])
    worst_pillar = min(['P1','P2','P3','P4'], key=lambda x: state_data[x])

    k1.metric("Composite Score", f"{state_data['Composite_score']:.2f}")
    k2.metric("Typology", state_data['typology'])
    k3.metric("Best Pillar", best_pillar)
    k4.metric("Worst Pillar", worst_pillar)

    st.markdown("---")

    # SYSTEM VIEW (NO QUADRANTS)
    st.markdown("## 📍 System Position")

    fig = px.scatter(
        df,
        x='P1',
        y='P3',
        color='typology',
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
    )
)
    fig.update_layout(
    legend=dict(
        title="Typology",
        orientation="h",          # horizontal legend
        yanchor="bottom",
        y=1.02,
        xanchor="center",
        x=0.5,
        font=dict(size=14),
        title_font=dict(size=16)
    )
)
    fig.update_layout(height=500)

    st.plotly_chart(fig, use_container_width=True)

    # NATIONAL COMPARISON
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

    # FULL INSIGHT (RESTORED QUALITY)
    st.markdown("## 💡 Key Insight")

    p1 = state_data['P1']
    p3 = state_data['P3']
    avg_p1 = df['P1'].mean()
    avg_p3 = df['P3'].mean()

    if p1 > avg_p1 and p3 < avg_p3:
        st.warning(
            f"{selected_state} demonstrates a **resource utilization gap** — "
            "despite higher-than-average financial investment, research output remains below the national benchmark. "
            "This suggests inefficiencies in converting funding into measurable innovation outcomes."
        )

    elif p1 < avg_p1 and p3 > avg_p3:
        st.success(
            f"{selected_state} is an **efficiency-driven performer**, generating higher research output despite lower investment levels. "
            "This reflects strong institutional effectiveness and optimal use of limited resources."
        )

    elif p1 > avg_p1 and p3 > avg_p3:
        st.success(
            f"{selected_state} represents a **balanced and high-performing ecosystem**, "
            "with strong investment translating effectively into research outcomes."
        )

    else:
        st.error(
            f"{selected_state} shows **structural capacity limitations**, with both investment and output below national averages. "
            "Focused policy intervention and ecosystem strengthening are required."
        )

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

    st.caption("All indicator values are normalized (0–1 scale) for comparability.")

    # ======================
    # ROW 1 → FINANCING + GOVERNANCE
    # ======================
    col1, col2 = st.columns(2)

    # FINANCING (P1) — USE NORMALIZED
    f_df = pd.DataFrame({
        'Indicator': ['F1: Budget', 'F2: Utilisation', 'F3: Growth'],
        'Value': [
            round(state_ind['F1_norm'], 2),
            round(state_ind['F2_norm'], 2),
            round(state_ind['F3_norm'], 2)
        ]
    })

    fig_f = px.bar(
        f_df,
        x='Indicator',
        y='Value',
        text='Value',
        title="💰 Financing (P1)",
        range_y=[0, 1]
    )
    fig_f.update_traces(textposition='outside')
    fig_f.update_layout(yaxis_title="Normalized Score")

    col1.plotly_chart(fig_f, use_container_width=True)

    # GOVERNANCE (P2)
    g_df = pd.DataFrame({
        'Indicator': ['G1: Presence', 'G2: Governance', 'G3: Activity', 'G4: Ecosystem'],
        'Value': [
            state_ind['G1_presence'],  # binary (0/1) → keep as is
            round(state_ind['G2_norm'], 2),
            round(state_ind['G3_norm'], 2),
            round(state_ind['G4_norm'], 2)
        ]
    })

    fig_g = px.bar(
        g_df,
        x='Indicator',
        y='Value',
        text='Value',
        title="🏛 Governance (P2)",
        range_y=[0, 1]
    )
    fig_g.update_traces(textposition='outside')
    fig_g.update_layout(yaxis_title="Score")

    col2.plotly_chart(fig_g, use_container_width=True)

    # ======================
    # ROW 2 → RESEARCH + OUTREACH
    # ======================
    col3, col4 = st.columns(2)

    # RESEARCH (P3) — USE NORMALIZED
    r_df = pd.DataFrame({
        'Indicator': ['R1: Publications', 'R2: Citations', 'R3: Innovation'],
        'Value': [
            round(state_ind['R1_norm'], 2),
            round(state_ind['R2_norm'], 2),
            round(state_ind['R3_norm'], 2)
        ]
    })

    fig_r = px.bar(
        r_df,
        x='Indicator',
        y='Value',
        text='Value',
        title="🔬 Research Output (P3)",
        range_y=[0, 1]
    )
    fig_r.update_traces(textposition='outside')
    fig_r.update_layout(yaxis_title="Normalized Score")

    col3.plotly_chart(fig_r, use_container_width=True)

    # OUTREACH (P4) — USE NORMALIZED
    o_df = pd.DataFrame({
        'Indicator': ['O1: Programs', 'O2: Reach', 'O3: Engagement'],
        'Value': [
            round(state_ind['O1_norm'], 2),
            round(state_ind['O2_norm'], 2),
            round(state_ind['O3_norm'], 2)
        ]
    })

    fig_o = px.bar(
        o_df,
        x='Indicator',
        y='Value',
        text='Value',
        title="🌐 Outreach (P4)",
        range_y=[0, 1]
    )
    fig_o.update_traces(textposition='outside')
    fig_o.update_layout(yaxis_title="Normalized Score")

    col4.plotly_chart(fig_o, use_container_width=True)

# =======================
# TAB 3 — COMPARE STATES (FULLY CLEAN)
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

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=[data_1['P1'], data_1['P2'], data_1['P3'], data_1['P4']],
        theta=categories,
        fill='toself',
        name=state_1
    ))

    fig_radar.add_trace(go.Scatterpolar(
        r=[data_2['P1'], data_2['P2'], data_2['P3'], data_2['P4']],
        theta=categories,
        fill='toself',
        name=state_2
    ))

    fig_radar.update_layout(height=500)

    st.plotly_chart(fig_radar, use_container_width=True)

    # COMPARISON INSIGHT
    st.markdown("## 💡 Comparison Insight")

    if data_1['Composite_score'] > data_2['Composite_score']:
        st.success(f"{state_1} outperforms {state_2} overall.")
    elif data_2['Composite_score'] > data_1['Composite_score']:
        st.success(f"{state_2} outperforms {state_1} overall.")
    else:
        st.info("Both states perform similarly.")