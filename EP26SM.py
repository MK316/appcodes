import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Midterm Score Checker", layout="wide")

st.title("📘 Midterm Score Checker")
st.caption("Enter your email and passcode to check your midterm score.")

CSV_URL = "https://raw.githubusercontent.com/MK316/appcodes/refs/heads/main/26SEPM.csv"

@st.cache_data
def load_data(url):
    return pd.read_csv(url)

data = load_data(CSV_URL)

required_columns = ["Email", "Passcode", "Score", "Group"]
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing required column(s): {missing_columns}")
    st.stop()

data["Email"] = data["Email"].astype(str).str.strip().str.lower()
data["Passcode"] = data["Passcode"].astype(str).str.strip()
data["Score"] = pd.to_numeric(data["Score"], errors="coerce")
data["Group"] = data["Group"].astype(str).str.strip()

data = data.dropna(subset=["Score"])

# -----------------------------
# Score category
# -----------------------------
def get_performance_level(score, df):
    upper_10_cutoff = df["Score"].quantile(0.90)
    median_cutoff = df["Score"].quantile(0.50)

    if score >= upper_10_cutoff:
        return "Upper 10%"
    elif score >= median_cutoff:
        return "Upper 50%"
    else:
        return "Lower 50%"

# -----------------------------
# Student score check
# -----------------------------
st.subheader("Check Your Score")

email_input = st.text_input("Email").strip().lower()
passcode_input = st.text_input("Passcode", type="password").strip()

if st.button("Check My Score"):
    matched = data[
        (data["Email"] == email_input) &
        (data["Passcode"] == passcode_input)
    ]

    if matched.empty:
        st.error("No matching record found. Please check your email and passcode.")
    else:
        student = matched.iloc[0]
        student_score = student["Score"]
        performance_level = get_performance_level(student_score, data)

        st.success("Your record was found.")
        st.markdown("### Your Result")
        st.write(f"**Score:** {student_score:.2f}")
        st.write(f"**Performance Level:** {performance_level}")

# -----------------------------
# Overall performance plots
# -----------------------------
st.markdown("---")

if st.button("Show Overall Performance"):
    scores = data["Score"]

    mean_score = scores.mean()
    median_score = scores.median()
    min_score = scores.min()
    max_score = scores.max()
    score_range = max_score - min_score
    upper_10_cutoff = scores.quantile(0.90)

    st.markdown("## Overall Performance")

    st.write(f"**Mean:** {mean_score:.2f}")
    st.write(f"**Median:** {median_score:.2f}")
    st.write(f"**Highest Score:** {max_score:.2f}")
    st.write(f"**Lowest Score:** {min_score:.2f}")
    st.write(f"**Range:** {score_range:.2f}")
    st.write(f"**Upper 10% cutoff:** {upper_10_cutoff:.2f}")

    # 1. Dot plot ordered by score
    st.markdown("### Dot Plot: Individual Scores Ordered by Score")
    
    sorted_data = data.sort_values("Score", ascending=False).reset_index(drop=True)
    
    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.scatter(range(1, len(sorted_data) + 1), sorted_data["Score"])
    
    ax1.axhline(upper_10_cutoff, linestyle="--", label="Upper 10% cutoff")
    ax1.axhline(median_score, color="red", linestyle="--", label="Median")
    
    ax1.set_xlabel("Students ordered from highest to lowest score")
    ax1.set_ylabel("Score")
    ax1.set_ylim(0, 210)
    ax1.set_title("Individual Scores Ordered from Highest to Lowest")
    ax1.legend()
    
    st.pyplot(fig1)

    # 2. Boxplot
    st.markdown("### Boxplot of Scores")

    fig2, ax2 = plt.subplots(figsize=(8, 3))
    ax2.boxplot(scores, vert=False)
    ax2.set_xlabel("Score")
    ax2.set_title("Score Distribution")
    st.pyplot(fig2)

    # 3. Histogram
    st.markdown("### Histogram of Scores")

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.hist(scores, bins=10, edgecolor="black")
    ax3.axvline(mean_score, linestyle="--", label="Mean")
    ax3.axvline(median_score, linestyle="--", label="Median")
    ax3.set_xlabel("Score")
    ax3.set_ylabel("Frequency")
    ax3.set_title("Histogram of Scores")
    ax3.legend()
    st.pyplot(fig3)

    # 4. Boxplots by group
    st.markdown("### Boxplots by Group")

    group_order = sorted(data["Group"].dropna().unique())
    group_scores = [
        data[data["Group"] == group]["Score"].dropna()
        for group in group_order
    ]

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    ax4.boxplot(group_scores, labels=group_order)
    ax4.set_xlabel("Group")
    ax4.set_ylabel("Score")
    ax4.set_title("Score Distribution by Group")
    st.pyplot(fig4)
