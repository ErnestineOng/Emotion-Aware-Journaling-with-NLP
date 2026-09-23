import streamlit as st
import pandas as pd
import os
from datetime import datetime
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import LabelEncoder
import plotly.express as px  
import calendar
from datetime import date, timedelta
import calendar

# === File Constants ===
USERS_FILE = "users.csv"
HISTORY_FILE = "journaling_history_new.csv"

# === Create necessary CSV files if not exist ===
if not os.path.exists(USERS_FILE):
    pd.DataFrame(columns=["full_name", "password"]).to_csv(USERS_FILE, index=False)

if not os.path.exists(HISTORY_FILE):
    pd.DataFrame(columns=["name", "date", "mood", "entry", "sentiment", "reflection_answer"]).to_csv(HISTORY_FILE, index=False)

# === Mood Options ===
mood_options = ["😢 Sad", "😡 Angry", "😔 Lonely", "💭 Nostalgic", "😐 Numb", "🌤️ Happy"]

# === Load Sentiment and Emotion Models ===
sent_pipeline = pipeline("sentiment-analysis")

model_path = "C:/KULIAH/SEMS 2/AI PROJECT/emotion_model2"
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

label_encoder = LabelEncoder()
label_encoder.fit(['anger', 'fear', 'happy', 'love', 'sadness', 'surprise'])

# === Helper Functions ===
def highlight_negative_words(text):
    words = text.split()
    highlighted = []
    for word in words:
        inputs = tokenizer(word, return_tensors="pt", truncation=True, padding=True)
        outputs = model(**inputs)
        pred = outputs.logits.argmax(dim=-1).item()
        label = label_encoder.inverse_transform([pred])[0]

        if label == 'sadness':
            highlighted.append(f"<span style='color:red'>{word}</span>")
        elif label == 'happy':
            highlighted.append(f"<span style='color:green'>{word}</span>")
        else:
            highlighted.append(word)
    return " ".join(highlighted)

def get_reflection_question(sentiment):
    if sentiment == "POSITIVE":
        return "What brought joy or fulfillment in this moment?"
    elif sentiment == "NEGATIVE":
        return "What challenges are you facing, and how might you overcome them?"
    else:
        return "What thoughts or emotions come to mind as you reflect?"

def authenticate_user(full_name, password):
    import pandas as pd  # Make sure pandas is imported

    df = pd.read_csv(USERS_FILE)
    df["full_name"] = df["full_name"].str.strip().str.lower()
    name_cleaned = full_name.strip().lower()

    if name_cleaned not in df["full_name"].values:
        return "please_sign_up"

    stored_password = str(df[df["full_name"] == name_cleaned]["password"].values[0]).strip()
    if stored_password == password.strip():
        return "success"
    else:
        return "incorrect_password"

def register_user(full_name, password):
    df = pd.read_csv(USERS_FILE)
    full_name_cleaned = full_name.strip().lower()
    if (df["full_name"].str.strip().str.lower() == full_name_cleaned).any():
        return False
    df.loc[len(df.index)] = [full_name.strip(), password]
    df.to_csv(USERS_FILE, index=False)
    return True

def draw_calendar_sidebar(mood_map):
    today = date.today()
    year = today.year
    month = today.month
    cal = calendar.Calendar(firstweekday=0)

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    for i, day in enumerate(weekdays):
        cols[i].markdown(f"**{day}**")

    # Kalender minggu per minggu
    week = [None] * 7
    for day in cal.itermonthdates(year, month):
        if day.month != month:
            continue

        weekday = day.weekday()
        week[weekday] = day

        if weekday == 6:  # Akhir minggu
            cols = st.columns(7)
            for i, d in enumerate(week):
                if d:
                    mood = mood_map.get(d, "No entry")
                    if cols[i].button(str(d.day), key=f"{d}-{mood}"):
                        st.session_state.selected_date = d
                else:
                    cols[i].markdown(" ")
            week = [None] * 7

    # Sisa minggu terakhir
    if any(week):
        cols = st.columns(7)
        for i, d in enumerate(week):
            if d:
                mood = mood_map.get(d, "No entry")
                if cols[i].button(str(d.day), key=f"{d}-{mood}"):
                    st.session_state.selected_date = d
            else:
                cols[i].markdown(" ")

    # Tampilkan mood dari tanggal yang diklik
    selected = st.session_state.get("selected_date")
    if selected:
        mood = mood_map.get(selected, None)
        if mood:
            st.success(f"Mood on {selected}: {mood}")
        else:
            st.info("No journal entry on this date.")

import streamlit as st
from datetime import date
import calendar

def draw_calendar_sidebar2(mood_map):
    today = date.today()
    year, month = today.year, today.month
    cal = calendar.Calendar(firstweekday=0)

    selected = st.session_state.get("selected_date")

    # 🧼 CSS for compact calendar (fit into ~300px sidebar)
    st.markdown("""
        <style>
        .calendar-button {
            padding: 2px 0;
            margin: 1px;
            font-size: 12px;
            width: 28px;
            height: 28px;
            border-radius: 6px;
            border: 1px solid #ccc;
            text-align: center;
            background-color: white;
        }
        .calendar-button:hover {
            background-color: #f0f0f0;
            cursor: pointer;
        }
        .calendar-button.today {
            background-color: #d0f0ff;
            font-weight: bold;
        }
        .calendar-button.selected {
            background-color: #2c7be5;
            color: white;
            font-weight: bold;
        }
        .tooltip-wrapper {
            position: relative;
            display: inline-block;
        }
        .tooltip-wrapper .tooltip {
            visibility: hidden;
            width: 100px;
            background-color: #333;
            color: #fff;
            text-align: center;
            padding: 4px 6px;
            border-radius: 4px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 11px;
        }
        .tooltip-wrapper:hover .tooltip {
            visibility: visible;
            opacity: 1;
        }
        </style>
    """, unsafe_allow_html=True)

    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    cols = st.columns(7)
    for i, wd in enumerate(weekdays):
        cols[i].markdown(f"<div style='font-size:12px; text-align:center; font-weight:600'>{wd}</div>", unsafe_allow_html=True)

    week = [None] * 7
    for day in cal.itermonthdates(year, month):
        if day.month != month:
            continue
        week[day.weekday()] = day

        if day.weekday() == 6:  # End of week
            _draw_week(week, mood_map, today, selected)
            week = [None] * 7

    if any(week):
        _draw_week(week, mood_map, today, selected)

def _draw_week(week, mood_map, today, selected):
    cols = st.columns(7)
    for i, day in enumerate(week):
        if not day:
            cols[i].markdown(" ")
            continue

        mood = mood_map.get(day, "No entry")
        tooltip = mood if mood != "No entry" else "No entry"
        is_today = day == today
        is_selected = day == selected
        css_class = "calendar-button"
        if is_today:
            css_class += " today"
        if is_selected:
            css_class += " selected"

        html = f"""
        <div class="tooltip-wrapper">
            <button class="{css_class}" onclick="fetch('', {{method:'POST'}})">{day.day}</button>
            <span class="tooltip">{tooltip}</span>
        </div>
        """

        cols[i].markdown(html, unsafe_allow_html=True)


# === Streamlit App ===
st.set_page_config(page_title="H2H Journal", layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

if not st.session_state.logged_in:
    st.title("Welcome to H2H Personal Journal")
    menu = st.radio("Login or Sign Up", ["Log In", "Sign Up"])

    name = st.text_input("Full Name")
    password = str(st.text_input("Password", type="password"))

    if menu == "Log In":
        if st.button("Log In"):
            auth_result = authenticate_user(name, password)
            
            if auth_result == "success":
                st.success("Login successful!")
                st.session_state.logged_in = True
                st.session_state.user = name.strip()
                st.rerun()
            elif auth_result == "incorrect_password":
                st.error("Incorrect password.")
            elif auth_result == "please_sign_up":
                st.error("Name not found. Please sign up first.")
    else:
        if st.button("Sign Up"):
            if register_user(name, password):
                st.success("Account created! Logging you in...")
                st.session_state.logged_in = True
                st.session_state.user = name.strip()
                st.rerun()
            else:
                st.warning("Name already registered.")
else:
    # === Main App After Login ===
    st.title(f"Welcome, {st.session_state.user} 👋")

    menu = st.sidebar.selectbox("Menu", ["Home", "View Journal History", "Log Out"])
    with st.sidebar:
        st.title("📆 Mood Calendar")
        # Load journal history
        df = pd.read_csv(HISTORY_FILE)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        user_data = df[df["name"].str.lower() == st.session_state.user.lower()]
        mood_map = {row["date"]: row["mood"] for _, row in user_data.iterrows()}

        draw_calendar_sidebar2(mood_map)

        # Display past 7 days as a mini mood log 
        st.markdown("### 🗓️ Last 7 Days Mood Log")
        last_7 = sorted(mood_map.items(), reverse=True)[0:7]
        for d, mood_emoji in last_7:
            st.markdown(f"{d}: {mood_emoji}")

    if menu == "Home":
        st.subheader("Write Your Journal")

        #mood = st.selectbox("How do you feel today?", mood_options)
        # Initialize mood selection in session state if not set
        if "selected_mood" not in st.session_state:
            st.session_state.selected_mood = None

        # Show message only if mood not selected
        if st.session_state.selected_mood is None:
            st.markdown("### Choose your mood")

        # Create mood selection dropdown
        selected = st.selectbox("Mood", ["-- Select Mood --"] + mood_options)

        # Update session state only if user selects a valid mood
        if selected != "-- Select Mood --":
            st.session_state.selected_mood = selected
            
        entry = st.text_area("Write your journal here:")

        if st.button("Analyze"):
            if entry:
                result = sent_pipeline(entry)[0]
                sentiment = result["label"].upper()
                question = get_reflection_question(sentiment)
                st.session_state.highlighted = highlight_negative_words(entry)
                st.session_state.sentiment = sentiment
                st.session_state.question = question
                st.session_state.reflection = ""
            else:
                st.error("Please enter something!")

        if "question" in st.session_state:
            st.markdown("### Highlighted Emotions:")
            st.markdown(st.session_state.highlighted, unsafe_allow_html=True)

            st.subheader("Reflective Question:")
            st.session_state.reflection = st.text_area(st.session_state.question)

            if st.button("Save Entry"):
                new_entry = pd.DataFrame([[ 
                    st.session_state.user,
                    datetime.now().isoformat(),
                    selected,
                    entry,
                    st.session_state.sentiment,
                    st.session_state.reflection
                ]], columns=["name", "date", "mood", "entry", "sentiment", "reflection_answer"])

                new_entry.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
                st.success("Journal saved!")

                for key in ["highlighted", "question", "reflection", "sentiment"]:
                    if key in st.session_state:
                        del st.session_state[key]
    
    elif menu == "View Journal History":
        st.subheader(f"Journal History for {st.session_state.user}")
        df = pd.read_csv(HISTORY_FILE)

        # Filter data pengguna
        user_data = df[df["name"].str.lower() == st.session_state.user.lower()]

        if user_data.empty:
            st.info("No entries yet.")
        else:
            # Pastikan kolom 'date' dalam format datetime dan urutkan dari terbaru
            user_data["date"] = pd.to_datetime(user_data["date"])
            user_data = user_data.sort_values("date", ascending=False)

            for _, row in user_data.iterrows():
                st.markdown(f"**Date:** {row['date'].strftime('%Y-%m-%d')}")
                st.markdown(f"**Mood:** {row['mood']}")
                st.markdown(f"**Sentiment:** {row['sentiment']}")

                # Highlight negative words (gunakan fungsi yang sudah kamu buat)
                highlighted = highlight_negative_words(row['entry'])
                st.markdown("**Highlighted Entry:**", unsafe_allow_html=True)
                st.markdown(highlighted, unsafe_allow_html=True)

                st.markdown(f"**Reflection:** {row['reflection_answer']}")
                st.markdown("---")

    elif menu == "Log Out":
        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()
    
    