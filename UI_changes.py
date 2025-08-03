import streamlit as st
import pandas as pd
import math

# Load player data from CSV
@st.cache_data
def load_players():
    df = pd.read_csv("fake_player_data_updated.csv")
    return df.to_dict(orient="records")

def format_height(inches):
    feet = inches // 12
    remaining_inches = inches % 12
    return f"{feet}'{remaining_inches}\""

# Main Streamlit app
st.set_page_config(page_title="Player Cards", layout="wide")
st.title("Player Roster")

# Sidebar filters
search_term = st.text_input("Search by player name")
positions = ["All", "QB", "RB", "WR", "TE", "OL", "DL", "LB", "DB", "K", "P"]
grades = ["All", "2026", "2027", "2028", "2029",'2030']
selected_position = st.selectbox("Filter by position", positions)
selected_grade = st.selectbox("Filter by grade", grades)

# Load and filter players
players = load_players()
if search_term:
    players = [p for p in players if search_term.lower() in p["name"].lower()]
if selected_position != "All":
    players = [p for p in players if p["position"] == selected_position]
if selected_grade != "All":
    players = [p for p in players if str(p["class"]) == selected_grade]

# Pagination setup
players_per_page = 12
page_number = st.session_state.get("page_number", 0)
num_pages = math.ceil(len(players) / players_per_page)

start = page_number * players_per_page
end = start + players_per_page
visible_players = players[start:end]

# Custom CSS for hover effect
st.markdown("""
    <style>
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    .card {
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        background: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Display cards in grid
cols = st.columns(3)
for idx, player in enumerate(visible_players):
    col = cols[idx % 3]
    with col:
        html_card = f"""
        <a href='https://google.com' target='_blank' style='text-decoration: none;'>
        <div class="card">
            <h3 style='margin-bottom: 5px;'>{player['name']}</h3>
            <p style='margin-top: -5px; font-size: 13px; color: #6b7280;'>{player.get('high_school', 'Unknown HS')}</p>
            <div style="margin: 10px 0;">
                <span style="font-size: 12px; font-weight: bold; background: #eef; padding: 4px 8px; border-radius: 10px; margin-right: 5px;">{player['position']}</span>
                <span style="font-size: 12px; font-weight: bold; background: #eee; padding: 4px 8px; border-radius: 10px;">{player['class']}</span>
            </div>
            <div style="display: flex; gap: 10px; margin: 10px 0;">
                <div style="background: #f8fafc; padding: 10px; border-radius: 10px; flex: 1; text-align: center;">
                    <div style="font-size: 12px; color: #6b7280;">Height</div>
                    <div style="font-weight: bold; color: black;">{format_height(player['height'])}</div>
                </div>
                <div style="background: #f8fafc; padding: 10px; border-radius: 10px; flex: 1; text-align: center;">
                    <div style="font-size: 12px; color: #6b7280;">Weight</div>
                    <div style="font-weight: bold; color: black;">{player['weight']} lbs</div>
                </div>
            </div>
            <div style="display: flex; gap: 10px;">
                <div style="background: #ecfdf5; padding: 10px; border-radius: 10px; flex: 1; text-align: center;">
                    <div style="font-size: 12px; color: #059669;">Frame Score</div>
                    <div style="font-weight: bold; color: black;">{player['score_weight']}</div>
                </div>
                <div style="background: #f0f9ff; padding: 10px; border-radius: 10px; flex: 1; text-align: center;">
                    <div style="font-size: 12px; color: #0284c7;">RAS Score</div>
                    <div style="font-weight: bold; color: black;">{player['ras_score']} / 10</div>
                </div>
            </div>
        </div></a>
        """
        st.markdown(html_card, unsafe_allow_html=True)

# Navigation buttons
prev_col, _, next_col = st.columns([1, 10, 1])
with prev_col:
    if page_number > 0:
        if st.button("⬅️ Previous"):
            st.session_state.page_number = page_number - 1
with next_col:
    if page_number < num_pages - 1:
        if st.button("Next ➡️"):
            st.session_state.page_number = page_number + 1
