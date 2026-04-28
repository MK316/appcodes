import streamlit as st
import pandas as pd

st.set_page_config(page_title="Midterm Score Checker", layout="centered")

st.title("📘 Midterm Score Checker")
st.caption("Enter your email and passcode to check your score and performance level.")

# -----------------------------
# 1. Load data from GitHub
# -----------------------------
CSV_URL = "https://raw.githubusercontent.com/MK316/appcodes/refs/heads/main/26SEPM.csv"
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    return df

try:
    data = load_data(CSV_URL)
except Exception as e:
    st.error("Failed to load the CSV file. Please check the GitHub raw URL.")
    st.stop()

# -----------------------------
# 2. Required columns
# -----------------------------
required_columns = ["Email", "Passcode", "Score"]

missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing required column(s): {missing_columns}")
    st.stop()

# Clean data
data["Email"] = data["Email"].astype(str).str.strip().str.lower()
data["Passcode"] = data["Passcode"].astype(str).str.strip()
data["Score"] = pd.to_numeric(data["Score"], errors="coerce")

data = data.dropna(subset=["Score"])

# -----------------------------
# 3. Login form
# -----------------------------
st.subheader("Check Your Score")

email_input = st.text_input("Email").strip().lower()
passcode_input = st.text_input("Passcode", type="password").strip()

check_button = st.button("Check My Score")

# -----------------------------
# 4. Rank category function
# -----------------------------
def get_rank_category(percentile):
    if percentile <= 5:
        return "Upper 5%"
    elif percentile <= 10:
        return "Upper 10%"
    elif percentile <= 20:
        return "Upper 20%"
    elif percentile <= 30:
        return "Upper 30%"
    elif percentile <= 50:
        return "Upper 50%"
    else:
        return "Lower 50%"

# -----------------------------
# 5. Student result
# -----------------------------
if check_button:
    matched = data[
        (data["Email"] == email_input) &
        (data["Passcode"] == passcode_input)
    ]

    if matched.empty:
        st.error("No matching record found. Please check your email and passcode.")
    else:
        student = matched.iloc[0]
        student_score = student["Score"]

        total_students = len(data)

        # Rank: 1 = highest score
        rank = (data["Score"] > student_score).sum() + 1

        # Percentile from top
        percentile_from_top = (rank / total_students) * 100

        rank_category = get_rank_category(percentile_from_top)

        st.success("Your record was found.")

        st.markdown("### Your Result")
        st.write(f"**Score:** {student_score}")
        st.write(f"**Rank:** {rank} out of {total_students}")
        st.write(f"**Performance Level:** {rank_category}")

# -----------------------------
# 6. Overall performance
# -----------------------------
st.markdown("---")

if st.button("Show Overall Performance"):
    mean_score = data["Score"].mean()
    median_score = data["Score"].median()
    min_score = data["Score"].min()
    max_score = data["Score"].max()
    score_range = max_score - min_score

    st.markdown("### Overall Performance")

    st.write(f"**Mean:** {mean_score:.2f}")
    st.write(f"**Median:** {median_score:.2f}")
    st.write(f"**Highest Score:** {max_score:.2f}")
    st.write(f"**Lowest Score:** {min_score:.2f}")
    st.write(f"**Range:** {score_range:.2f}")
