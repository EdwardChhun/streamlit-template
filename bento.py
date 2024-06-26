import streamlit as st
from streamlit_elements import elements, mui, dashboard
import json
import os


st.set_page_config(page_title="TheraAI", page_icon=None, layout="wide", initial_sidebar_state="collapsed", menu_items=None)

st.markdown("""
    <h1 style='text-align: center; font-size: 100px;'>
        <span style='color: #FFFFFF;'>Thera</span><span style='color: #4169E1; margin-left: 10px;'>AI</span>
    </h1>
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
            dashboard.Item("camera", 0, 0, 2, 2, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("emotion-panel", 1, 0, 1, 1, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("chat-panel", 1, 1, 1, 1, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("dashboard", 0, 2, 1, 1, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("line-chart", 0, 2, 1, 1, isDraggable=True, isResizable=True, moved=True),
            dashboard.Item("nivo-chart", 0, 2, 1, 1, isDraggable=True, isResizable=True, moved=True),
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

with elements("dashboard"):
    with dashboard.Grid(st.session_state["layout"], onLayoutChange=handle_layout_change):
        mui.Paper("Thera: ", key="thera")
        mui.Paper("Camera: ", key="camera")
        mui.Paper("Emotions: ", key="emotion-panel")
        mui.Paper("Chatbot ", key="chat-panel")
        mui.Paper("Dashboard ", key="dashboard")
        mui.Paper("Line Chart ", key="line-chart")
        mui.Paper("Nivo Chart ", key="nivo-chart")
