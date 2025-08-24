import streamlit as st
from src.workflow.workflow import Workflow

# Page config
st.set_page_config(page_title="Travel Planner", page_icon="✈️", layout="wide")

# Custom CSS for better UI
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #74ebd5 0%, #ACB6E5 100%);
        color: #2c3e50;
        font-family: 'Segoe UI', sans-serif;
    }
    .main-title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        color: #2c3e50;
        padding: 20px;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #34495e;
        margin-bottom: 30px;
    }
    .example-box {
        background-color: #ffffffcc;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        font-size: 15px;
        margin-bottom: 20px;
    }
    .response-box {
        background-color: #fefefe;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">🌍 Smart Travel Planner ✈️</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Plan your trip, stay on budget & explore the best places</div>', unsafe_allow_html=True)

# Example Input Section
st.markdown("### 📌 Example Trip Requirement")
example_prompt = """I am planning a budget-friendly trip from Allagadda to Kerala between June 25 and June 31, 2025, with a total budget of ₹15,000. Please create a detailed travel itinerary that includes:

- Round-trip transportation from Allagadda to Kerala  
- Affordable accommodation for the entire stay  
- Estimated daily food expenses  
- A list of must-visit tourist attractions in Kerala with an optimal travel route  
- Local transportation between destinations  

✅ Ensure the entire plan stays within my budget of ₹15,000.
"""

st.markdown(f"<div class='example-box'>{example_prompt}</div>", unsafe_allow_html=True)

# Sidebar Input
st.sidebar.header("📝 Enter Your Trip Details")
user_input = st.sidebar.text_area("✍️ Trip Requirements", "", height=200, placeholder="Describe your trip here...")

# Workflow initialization
graph = Workflow().create_workflow()

# Button to trigger itinerary generation
if st.sidebar.button("✨ Generate Plan"):
    if user_input.strip() == "":
        st.warning("⚠️ Please enter your trip details in the sidebar to generate a plan.")
    else:
        st.subheader("✅ Your Personalized Travel Itinerary")
        state = {"messages": [user_input]}
        response = graph.invoke(state)['messages'][-1].content

        # Display in styled box
        st.markdown(f"<div class='response-box'>{response}</div>", unsafe_allow_html=True)
