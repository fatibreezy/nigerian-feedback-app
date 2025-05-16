import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# -- Initialize feedback storage
FEEDBACK_FILE = "feedback.csv"
if not os.path.exists(FEEDBACK_FILE):
    df_init = pd.DataFrame(columns=["Post", "Region", "Response Type", "Feedback", "Name"])
    df_init.to_csv(FEEDBACK_FILE, index=False)

# --- Government Posts (Updated) ---
government_posts = [
    "🧾 Tax Reform Bill 2025",
    "📢 3MTT Cohort 3 Registration Opens",
    "📝 JAMB Announces Rewriting of Exams for Some Candidates",
    "💼 Nestlé Nigeria Graduate Trainee Program 2025",
    "⚡ Power Supply Reform",
    "💰 New Minimum Wage Proposal",
    "🛡️ Security Enhancement Initiative",
    "📚 Education Budget Update",
    "🏥 Healthcare Improvement Plan",
    "🎓 Youth Empowerment Program",
]

regions = [
    "South West", "South East", "South South",
    "North West", "North East", "North Central", "FCT"
]

st.set_page_config(page_title="NaijaGov Feedback Portal", layout="wide")

st.title("🇳🇬 NaijaGov Feedback Portal")
st.write("Give your voice on key government and national updates. You can remain anonymous!")

# --- Select Post and Region ---
post = st.selectbox("Select a government post or update", government_posts)
region = st.selectbox("Select your region (optional)", [""] + regions)

# --- Feedback Form ---
st.subheader("📢 Respond to Update")
response_type = st.radio("Type of feedback", ["Suggestion", "Concern", "Note to Government"])
feedback = st.text_area("Write your feedback")
name = st.text_input("Name (leave blank for anonymous)")

if st.button("Submit Feedback"):
    if feedback.strip() == "":
        st.warning("Please write some feedback before submitting.")
    else:
        new_entry = pd.DataFrame([{
            "Post": post,
            "Region": region if region else "Unknown",
            "Response Type": response_type,
            "Feedback": feedback,
            "Name": name if name else "Anonymous"
        }])
        new_entry.to_csv(FEEDBACK_FILE, mode='a', header=False, index=False)
        st.success("✅ Your feedback has been recorded!")

# --- Data Display ---
st.subheader("📊 Interaction Stats")
if os.path.exists(FEEDBACK_FILE):
    df = pd.read_csv(FEEDBACK_FILE)

    # Filter by post
    selected_post = st.selectbox("Select post to view reactions", government_posts)
    filtered = df[df["Post"] == selected_post]

    if not filtered.empty:
        st.write(f"Total Feedback Entries: {len(filtered)}")
        st.dataframe(filtered)

        # Chart
        chart_data = filtered["Response Type"].value_counts()
        st.bar_chart(chart_data)
    else:
        st.info("No feedback for this post yet.")
