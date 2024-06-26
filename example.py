import streamlit as st
from streamlit_elements import elements, mui, dashboard, html
import json
import os
import plotly.express as px
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode

# Configure page
st.set_page_config(page_title="TheraAI", page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items=None)

# Fixed header with CSS
st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: white;
        z-index: 1000;
        box-shadow: 0 4px 2px -2px gray;
    }
    .spacer {
        margin-top: 120px;
    }
    </style>
    <div class="fixed-header">
        <h1 style='text-align: center; font-size: 100px;'>
            <span style='color: #000000;'>Thera</span><span style='color: #4169E1; margin-left: 10px;'>AI</span>
        </h1>
    </div>
    <div class="spacer"></div>
""", unsafe_allow_html=True)

# Define the file path to save the layout
layout_file_path = "layout.json"

# Function to load the layout from a file or use the default layout
def load_layout():
    if os.path.exists(layout_file_path):
        with open(layout_file_path, "r") as f:
            return json.load(f)
    else:
        return [
            dashboard.Item("thera", 0, 0, 8, 0.5, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("camera", 2, 2, 2, 2, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("emotion-panel", 0, 4, 2, 2, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("chat-panel", 2, 4, 2, 2, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("dashboard", 0, 6, 2, 2, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("line-chart", 4, 2, 4, 2, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("nivo-chart", 4, 4, 4, 2, isDraggable=True, isResizable=True, moved=True),
        ]

# Function to save the layout to a file
def save_layout(updated_layout):
    with open(layout_file_path, "w") as f:
        json.dump(updated_layout, f)

# Load the saved layout if available, otherwise use the default layout
layout = load_layout()

# Define the layout change handler to update the layout file and session state
def handle_layout_change(updated_layout):
    save_layout(updated_layout)
    st.session_state["layout"] = updated_layout

# Initialize session state layout if not already set
if "layout" not in st.session_state:
    st.session_state["layout"] = layout

# Dashboard with draggable and resizable items
with elements("dashboard"):
    with dashboard.Grid(st.session_state["layout"], onLayoutChange=handle_layout_change):
        
        # Thera Panel
        with mui.Paper("Thera: ", key="thera"):
            st.markdown("### Thera Panel Content")

        # Camera Panel
        with mui.Paper("Camera: ", key="camera"):
            webrtc_streamer(key="camera", mode=WebRtcMode.SENDRECV, rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})

        # Emotions Panel
        with mui.Paper("Emotions: ", key="emotion-panel"):
            st.markdown("### Emotion Analysis")

        # Chatbot Panel
        with mui.Paper("Chatbot ", key="chat-panel"):
            if "chat_history" not in st.session_state:
                st.session_state["chat_history"] = []
            
            user_input = st.text_input("You: ")
            if user_input:
                st.session_state["chat_history"].append(("You", user_input))
                st.session_state["chat_history"].append(("Bot", f"Echo: {user_input}"))  # Replace with actual bot response logic

            # Display chat history
            for sender, message in st.session_state["chat_history"]:
                st.write(f"**{sender}:** {message}")

        # Dashboard Panel
        with mui.Paper("Dashboard ", key="dashboard"):
            st.markdown("### Dashboard Content")

        # Line Chart Panel
        with mui.Paper("Line Chart ", key="line-chart"):
            df = px.data.gapminder().query("year==2007")
            fig = px.line(df, x="gdpPercap", y="lifeExp", title="GDP vs Life Expectancy")
            st.plotly_chart(fig)

        # Nivo Chart Panel
        with mui.Paper("Nivo Chart ", key="nivo-chart"):
            st.markdown("### Nivo Chart Content")

