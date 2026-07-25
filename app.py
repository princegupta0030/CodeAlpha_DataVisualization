import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================
st.set_page_config(
    page_title="🏏 IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================
st.markdown("""
<style>

.main{
    background:#0E1117;
}

.block-container{
    padding-top:2rem;
}

.metric-card{
    background:#1B1F24;
    padding:18px;
    border-radius:15px;
    text-align:center;
    border:1px solid #2A2F36;
}

.metric-card h1{
    color:#F39C12;
}

hr{
    margin-top:10px;
    margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    matches=pd.read_csv("datasets/matches.csv")
    deliveries=pd.read_csv("datasets/deliveries.csv")
    return matches,deliveries

matches,deliveries=load_data()

# ==========================================================
# HEADER
# ==========================================================

st.title("🏏 IPL Analytics Dashboard")

st.markdown("""
Interactive Business Intelligence Dashboard built using

✅ Streamlit

✅ Plotly

✅ Pandas
""")

st.markdown("---")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Dashboard Filters")

season=st.sidebar.selectbox(
    "Season",
    sorted(matches["season"].unique())
)

teams=sorted(
    list(
        set(matches["team1"].dropna().unique()) |
        set(matches["team2"].dropna().unique())
    )
)

team=st.sidebar.selectbox(
    "Team",
    ["All Teams"]+teams
)

venues=sorted(matches["venue"].dropna().unique())

venue=st.sidebar.selectbox(
    "Venue",
    ["All Venues"]+venues
)

players=sorted(deliveries["batter"].dropna().unique())

player=st.sidebar.selectbox(
    "Player",
    ["All Players"]+players
)

# ==========================================================
# FILTER DATA
# ==========================================================

filtered_matches=matches.copy()

filtered_matches=filtered_matches[
    filtered_matches["season"]==season
]

if team!="All Teams":

    filtered_matches=filtered_matches[
        (filtered_matches["team1"]==team) |
        (filtered_matches["team2"]==team)
    ]

if venue!="All Venues":

    filtered_matches=filtered_matches[
        filtered_matches["venue"]==venue
    ]

filtered_deliveries=deliveries[
    deliveries["match_id"].isin(filtered_matches["id"])
]

if player!="All Players":

    filtered_deliveries=filtered_deliveries[
        filtered_deliveries["batter"]==player
    ]

# ==========================================================
# KPIs
# ==========================================================

total_matches=filtered_matches.shape[0]

total_runs=filtered_deliveries["total_runs"].sum()

total_wickets=filtered_deliveries["is_wicket"].sum()

total_sixes=(filtered_deliveries["batsman_runs"]==6).sum()

c1,c2,c3,c4=st.columns(4)

with c1:

    st.markdown(f"""
    <div class="metric-card">
    <h4>🏏 Matches</h4>
    <h1>{total_matches}</h1>
    </div>
    """,unsafe_allow_html=True)

with c2:

    st.markdown(f"""
    <div class="metric-card">
    <h4>🏃 Runs</h4>
    <h1>{total_runs}</h1>
    </div>
    """,unsafe_allow_html=True)

with c3:

    st.markdown(f"""
    <div class="metric-card">
    <h4>🎳 Wickets</h4>
    <h1>{total_wickets}</h1>
    </div>
    """,unsafe_allow_html=True)

with c4:

    st.markdown(f"""
    <div class="metric-card">
    <h4>🔥 Sixes</h4>
    <h1>{total_sixes}</h1>
    </div>
    """,unsafe_allow_html=True)

st.markdown("---")

# ==========================================================
# TABS
# ==========================================================

overview,teams_tab,players_tab,venues_tab=st.tabs(
[
"📊 Overview",
"🏆 Teams",
"🏏 Players",
"🏟 Venues"
]
)

# ==========================================================
# OVERVIEW TAB
# ==========================================================

with overview:

    left,right=st.columns(2)

    with left:

        st.subheader("📈 Matches Per Season")

        season_data=(
            matches
            .groupby("season")
            .size()
            .reset_index(name="Matches")
        )

        fig=px.bar(
            season_data,
            x="season",
            y="Matches",
            text="Matches",
            color="Matches",
            title="Matches Per Season"
        )

        st.plotly_chart(fig,use_container_width=True)

    with right:

        st.subheader("🏆 Winning Teams")

        winners=(
            filtered_matches["winner"]
            .value_counts()
            .reset_index()
        )

        winners.columns=["Team","Wins"]

        fig=px.bar(
            winners,
            x="Team",
            y="Wins",
            color="Wins",
            text="Wins",
            title="Winning Teams"
        )

        st.plotly_chart(fig,use_container_width=True)

    left,right=st.columns(2)

    with left:

        st.subheader("🥧 Toss Decision")

        toss=(
            filtered_matches["toss_decision"]
            .value_counts()
            .reset_index()
        )

        toss.columns=["Decision","Count"]

        fig=px.pie(
            toss,
            names="Decision",
            values="Count",
            hole=.45,
            title="Toss Decision"
        )

        st.plotly_chart(fig,use_container_width=True)

    with right:

        st.subheader("🏟 Top Venues")

        venues_data=(
            filtered_matches["venue"]
            .value_counts()
            .head(10)
            .reset_index()
        )

        venues_data.columns=["Venue","Matches"]

        fig=px.bar(
            venues_data,
            x="Venue",
            y="Matches",
            text="Matches",
            color="Matches",
            title="Top Venues"
        )

        st.plotly_chart(fig,use_container_width=True)
        # Teams Tab

with teams_tab:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏏 Top Run Scorers")

        top_runs = (
            filtered_deliveries
            .groupby("batter")["batsman_runs"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        top_runs.columns = ["Batter", "Runs"]

        fig = px.bar(
            top_runs,
            x="Batter",
            y="Runs",
            color="Runs",
            text="Runs",
            title="Top 10 Run Scorers"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("🎳 Top Wicket Takers")

        wickets = filtered_deliveries[
            filtered_deliveries["is_wicket"] == 1
        ]

        top_wickets = (
            wickets.groupby("bowler")
            .size()
            .sort_values(ascending=False)
            .head(10)
            .reset_index(name="Wickets")
        )

        fig = px.bar(
            top_wickets,
            x="bowler",
            y="Wickets",
            color="Wickets",
            text="Wickets",
            title="Top 10 Wicket Takers"
        )

        st.plotly_chart(fig, use_container_width=True)


# Players Tab

with players_tab:

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🔥 Top Six Hitters")

        sixes = filtered_deliveries[
            filtered_deliveries["batsman_runs"] == 6
        ]

        top_sixes = (
            sixes.groupby("batter")
            .size()
            .sort_values(ascending=False)
            .head(10)
            .reset_index(name="Sixes")
        )

        fig = px.bar(
            top_sixes,
            x="batter",
            y="Sixes",
            color="Sixes",
            text="Sixes",
            title="Top Six Hitters"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        st.subheader("💥 Top Four Hitters")

        fours = filtered_deliveries[
            filtered_deliveries["batsman_runs"] == 4
        ]

        top_fours = (
            fours.groupby("batter")
            .size()
            .sort_values(ascending=False)
            .head(10)
            .reset_index(name="Fours")
        )

        fig = px.bar(
            top_fours,
            x="batter",
            y="Fours",
            color="Fours",
            text="Fours",
            title="Top Four Hitters"
        )

        st.plotly_chart(fig, use_container_width=True)


# Venues Tab

with venues_tab:

    st.subheader("📋 Filtered Match Data")

    st.dataframe(
        filtered_matches,
        use_container_width=True,
        hide_index=True
    )

    csv = filtered_matches.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇ Download Filtered Data",
        data=csv,
        file_name="filtered_matches.csv",
        mime="text/csv"
    )

    st.markdown("---")

    st.subheader("🏟 Top Match Venues")

    venue_summary = (
        filtered_matches["venue"]
        .value_counts()
        .reset_index()
    )

    venue_summary.columns = ["Venue", "Matches"]

    fig = px.bar(
        venue_summary,
        x="Venue",
        y="Matches",
        color="Matches",
        text="Matches",
        title="Matches Played at Each Venue"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.caption(
    "🏏 IPL Analytics Dashboard | Built using Streamlit, Plotly & Pandas"
)