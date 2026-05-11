import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(page_title="Score Checker", layout="wide")

st.title("🍰 S26 Midterm Score Checker")
st.caption("Select your course and check your score using the required information.")

# -----------------------------
# Dataset links
# -----------------------------
DATASETS = {
    "Engpro": "https://raw.githubusercontent.com/MK316/appcodes/refs/heads/main/26SEPM.csv",
    "Phonetics": "https://raw.githubusercontent.com/MK316/appcodes/refs/heads/main/26SPhoneticsMidterm.csv"  # Update later
}

dataset_name = st.selectbox("Select dataset:", list(DATASETS.keys()))
CSV_URL = DATASETS[dataset_name]

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data(url):
    return pd.read_csv(url)

data = load_data(CSV_URL)

st.caption(f"Current dataset: {dataset_name}")

# -----------------------------
# Required columns
# -----------------------------
if dataset_name == "Phonetics":
    required_columns = [
        "Names", "SID", "Passcode", "Group",
        "Written", "Transcription", "Total"
    ]
else:
    required_columns = ["Email", "Passcode", "Score", "Group"]

missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    st.error(f"Missing required column(s): {missing_columns}")
    st.stop()

# -----------------------------
# Data cleaning
# -----------------------------
data["Passcode"] = data["Passcode"].astype(str).str.strip()
data["Group"] = data["Group"].astype(str).str.strip()

if dataset_name == "Phonetics":
    data["Names"] = data["Names"].astype(str).str.strip()
    data["SID"] = data["SID"].astype(str).str.strip()

    data["Written"] = pd.to_numeric(data["Written"], errors="coerce")
    data["Transcription"] = pd.to_numeric(data["Transcription"], errors="coerce")
    data["Total"] = pd.to_numeric(data["Total"], errors="coerce")

    score_column = "Total"

else:
    data["Email"] = data["Email"].astype(str).str.strip().str.lower()
    data["Score"] = pd.to_numeric(data["Score"], errors="coerce")

    score_column = "Score"

# Remove rows with invalid score
data = data.dropna(subset=[score_column])

# -----------------------------
# Score category
# -----------------------------
def get_performance_level(score, df, score_col):
    upper_10_cutoff = df[score_col].quantile(0.90)
    median_cutoff = df[score_col].quantile(0.50)

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

if dataset_name == "Phonetics":
    sid_input = st.text_input(
        "SID",
        placeholder="Type your student ID"
    ).strip()

    passcode_input = st.text_input(
        "Passcode",
        type="password",
        placeholder="Type your passcode"
    ).strip()

else:
    email_input = st.text_input(
        "Email",
        placeholder="example: student123@university.ac.kr"
    ).strip().lower()

    passcode_input = st.text_input(
        "Passcode",
        type="password",
        placeholder="Type your passcode"
    ).strip()

# -----------------------------
# Check button
# -----------------------------
if st.button("Check My Score"):

    if dataset_name == "Phonetics":
        sid_matched = data[data["SID"] == sid_input]
        passcode_matched = data[data["Passcode"] == passcode_input]

        both_matched = data[
            (data["SID"] == sid_input) &
            (data["Passcode"] == passcode_input)
        ]

        if both_matched.empty:
            if sid_matched.empty and passcode_matched.empty:
                st.error("Both SID and Passcode do not match.")
            elif sid_matched.empty:
                st.error("SID does not match.")
            elif passcode_matched.empty:
                st.error("Passcode does not match.")
            else:
                st.error("SID and Passcode do not match the same record.")

        else:
            student = both_matched.iloc[0]
            total_score = student["Total"]
            performance_level = get_performance_level(total_score, data, score_column)

            st.success("Your record was found.")
            st.markdown("### Your Result")

            st.write(f"**Name:** {student['Names']}")
            st.write(f"**SID:** {student['SID']}")
            st.write(f"**Group:** {student['Group']}")
            st.write(f"**Written Exam Score:** {student['Written']:.2f}")
            st.write(f"**Transcription Score:** {student['Transcription']:.2f}")
            st.write(f"**Total Score:** {student['Total']:.2f} / 100")
            st.write(f"**Performance Level:** {performance_level}")

    else:
        email_matched = data[data["Email"] == email_input]
        passcode_matched = data[data["Passcode"] == passcode_input]

        both_matched = data[
            (data["Email"] == email_input) &
            (data["Passcode"] == passcode_input)
        ]

        if both_matched.empty:
            if email_matched.empty and passcode_matched.empty:
                st.error("Both Email and Passcode do not match.")
            elif email_matched.empty:
                st.error("Email does not match.")
            elif passcode_matched.empty:
                st.error("Passcode does not match.")
            else:
                st.error("Email and Passcode do not match the same record.")

        else:
            student = both_matched.iloc[0]
            student_score = student["Score"]
            performance_level = get_performance_level(student_score, data, score_column)

            st.success("Your record was found.")
            st.markdown("### Your Result")

            st.write(f"**Score:** {student_score:.2f}")
            st.write(f"**Performance Level:** {performance_level}")

# -----------------------------
# Overall performance plots
# -----------------------------
st.markdown("---")

if st.button("Show Overall Performance"):
    scores = data[score_column]

    mean_score = scores.mean()
    median_score = scores.median()
    min_score = scores.min()
    max_score = scores.max()
    score_range = max_score - min_score
    upper_10_cutoff = scores.quantile(0.90)

    # -----------------------------
    # Axis range by dataset
    # -----------------------------
    if dataset_name == "Phonetics":
        y_min, y_max = 0, 100
    else:
        y_min, y_max = 0, 210

    st.markdown("## Overall Performance")

    if dataset_name == "Phonetics":
        st.caption("Performance statistics and plots are based on the Total score.")
    else:
        st.caption("Performance statistics and plots are based on the Score column.")

    st.write(f"**Mean:** {mean_score:.2f}")
    st.write(f"**Median:** {median_score:.2f}")
    st.write(f"**Highest Score:** {max_score:.2f}")
    st.write(f"**Lowest Score:** {min_score:.2f}")
    st.write(f"**Range:** {score_range:.2f}")
    st.write(f"**Upper 10% cutoff:** {upper_10_cutoff:.2f}")

    # -----------------------------
    # 1. Dot plot ordered by score
    # -----------------------------
    st.markdown("### Dot Plot: Individual Scores Ordered by Score")

    sorted_data = data.sort_values(score_column, ascending=False).reset_index(drop=True)

    fig1, ax1 = plt.subplots(figsize=(10, 4))
    ax1.scatter(range(1, len(sorted_data) + 1), sorted_data[score_column])

    ax1.axhline(upper_10_cutoff, linestyle="--", label="Upper 10% cutoff")
    ax1.axhline(median_score, linestyle="--", label="Median")

    ax1.set_xlabel("Students ordered from highest to lowest score")
    ax1.set_ylabel(score_column)
    ax1.set_ylim(y_min, y_max)
    ax1.set_title("Individual Scores Ordered from Highest to Lowest")
    ax1.legend()

    st.pyplot(fig1)

    # -----------------------------
    # 2. Boxplot
    # -----------------------------
    st.markdown("### Boxplot of Scores")

    fig2, ax2 = plt.subplots(figsize=(8, 3))
    ax2.boxplot(scores, vert=False)
    ax2.set_xlabel(score_column)
    ax2.set_xlim(y_min, y_max)
    ax2.set_title("Score Distribution")

    st.pyplot(fig2)

    # -----------------------------
    # 3. Histogram
    # -----------------------------
    st.markdown("### Histogram of Scores")

    fig3, ax3 = plt.subplots(figsize=(8, 4))
    ax3.hist(scores, bins=10, edgecolor="black")

    ax3.axvline(mean_score, linestyle="--", label="Mean")
    ax3.axvline(median_score, linestyle="--", label="Median")

    ax3.set_xlabel(score_column)
    ax3.set_ylabel("Frequency")
    ax3.set_xlim(y_min, y_max)
    ax3.set_title("Histogram of Scores")
    ax3.legend()

    st.pyplot(fig3)

    # -----------------------------
    # 4. Boxplots by group
    # -----------------------------
    st.markdown("### Boxplots by Group")

    def sort_group_label(x):
        x = str(x).strip()
        if x.upper().startswith("G"):
            try:
                return int(x.upper().replace("G", ""))
            except ValueError:
                return 999
        return 999

    group_order = sorted(
        data["Group"].dropna().unique(),
        key=sort_group_label
    )

    group_scores = [
        data[data["Group"] == group][score_column].dropna()
        for group in group_order
    ]

    pastel_colors = [
        "#FADADD", "#D8E2DC", "#FFE5B4", "#CDE7F0",
        "#E4D7F5", "#D5F5E3", "#F9E79F", "#F5CBA7"
    ]

    fig4, ax4 = plt.subplots(figsize=(10, 5))

    box = ax4.boxplot(
        group_scores,
        labels=group_order,
        patch_artist=True
    )

    for patch, color in zip(box["boxes"], pastel_colors):
        patch.set_facecolor(color)

    ax4.set_xlabel("Group")
    ax4.set_ylabel(score_column)
    ax4.set_ylim(y_min, y_max)
    ax4.set_title("Score Distribution by Group")

    st.pyplot(fig4)
