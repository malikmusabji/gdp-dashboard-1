import streamlit as st
import sqlite3
import pandas as pd
from PyPDF2 import PdfReader
import io
import requests
from datetime import datetime
import pytz
import base64

# Function to get user's timezone based on IP address
def get_user_timezone():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            return data.get("timezone", "UTC")
    except:
        pass
    return "UTC"

# Function to display flip clock based on the user's time zone
def display_flip_clock():
    user_timezone = get_user_timezone()
    now = datetime.now(pytz.timezone(user_timezone))

    flipclock_html = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flipclock/0.7.8/flipclock.min.css">
    <div id="flip-clock" style="display: flex; justify-content: center;"></div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flipclock/0.7.8/flipclock.min.js"></script>
    <script type="text/javascript">
        document.addEventListener("DOMContentLoaded", function() {{
            var clock = new FlipClock(document.getElementById('flip-clock'), {{
                clockFace: 'TwentyFourHourClock',
                showSeconds: true
            }});
        }});
    </script>
    """
    
    st.components.v1.html(flipclock_html, height=150)

# Function to add JavaScript for detecting tab changes
def detect_tab_switch():
    js_code = """
    <script>
        document.addEventListener("visibilitychange", function() {
            if (document.hidden) {
                alert("You are moving away from this page! Please stay on this tab.");
            }
        });
    </script>
    """
    st.components.v1.html(js_code)

# Function to display a session timer that counts up from the user's login time
def display_session_timer():
    if "login_time" in st.session_state:
        # Calculate the elapsed time since login in seconds
        elapsed_time = (datetime.now(pytz.timezone(get_user_timezone())) - st.session_state.login_time).total_seconds()
        session_timer_html = f"""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/flipclock/0.7.8/flipclock.min.css">
        <div id="session-timer" style="display: flex; justify-content: center;"></div>
        
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/flipclock/0.7.8/flipclock.min.js"></script>
        <script type="text/javascript">
            document.addEventListener("DOMContentLoaded", function() {{
                var timer = new FlipClock(document.getElementById('session-timer'), {{
                    clockFace: 'MinuteCounter',
                    autoStart: true
                }});
                // Set the timer to start from the elapsed time
                timer.setTime({int(elapsed_time)});
                timer.start();
            }});
        </script>
        """
        
        st.components.v1.html(session_timer_html, height=150)

# Placeholder for user authentication status
login_status = False

# Simple user credentials (You can extend this to a more secure method)
USER_CREDENTIALS = {
    "user1": "password1",
    "user2": "password2"
}

# Function for the login page
def login():
    st.title("Login Page")

    # Get user input for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Initialize a button for login
    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.success(f"Welcome, {username}!")
            return True  # Authentication successful
        else:
            st.error("Invalid username or password.")
            return False  # Authentication failed
    return False
            if user:
                st.success(f"Welcome, {username}!")
                st.session_state.login_time = datetime.now(pytz.timezone(get_user_timezone()))
                st.session_state.login_status = True
                return True
            else:
                st.error("Invalid username or password.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            conn.close()
    return False

@st.cache_data
def load_default_timetable():
    # Sample timetable data
    data = {
        "Time": ["09-10 AM", "10-11 AM", "11-12 AM", "12-01 PM", "01-02 PM", "02-03 PM", "03-04 PM", "04-05 PM"],
        "Monday": ["Lecture / G:All C:PEV112 / R: 56-703 / S:BO301"] * 8,
        "Tuesday": ["Lecture / G:All C:PEV112 / R: 56-703 / S:BO301"] * 8,
        "Wednesday": ["Practical / G:1 C:PEV112 / R: 56-703 / S:BO301"] * 8,
        "Thursday": [""] * 8,
        "Friday": [""] * 8,
        "Saturday": [""] * 8
    }
    return pd.DataFrame(data)

def load_course_info():
    # Sample course information
    course_data = {
        "CourseCode": ["BTY396", "BTY416", "BTY441", "BTY463", "BTY464", "BTY496", "BTY499", "BTY651", "ICT202B", "PEA402", "PESS01", "PEV112"],
        "CourseType": ["CR", "CR", "EM", "CR", "CR", "CR", "CR", "PW", "CR", "OM", "PE", "OM"],
        "CourseName": ["BIOSEPARATION ENGINEERING", "BIOSEPARATION ENGINEERING LABORATORY", "PHARMACEUTICAL ENGINEERING", 
                       "BIOINFORMATICS AND COMPUTATIONAL BIOLOGY", "BIOINFORMATICS AND COMPUTATIONAL BIOLOGY LABORATORY", 
                       "METABOLIC ENGINEERING", "SEMINAR ON SUMMER TRAINING", "QUALITY CONTROL AND QUALITY ASSURANCE", 
                       "AI, ML AND EMERGING TECHNOLOGIES", "ANALYTICAL SKILLS -II", "MENTORING - VII", "VERBAL ABILITY"],
        "Credits": [3, 1, 3, 2, 1, 2, 3, 3, 2, 4, 0, 3],
        "Faculty": ["Dr. Ajay Kumar", "Dr. Ajay Kumar", "Dr. Shashank Garg", "Dr. Anish Kumar", 
                    "Dr. Anish Kumar", "Dr. Shashank Garg", "", "Dr. Aarti Bains", 
                    "Dr. Piyush Kumar Yadav", "Kamal Deep", "", "Jaskiranjit Kaur"]
    }
    return pd.DataFrame(course_data)

def display_pdf(pdf_file):
    pdf_data = pdf_file.read()
    base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def home():
    st.title("Academic Schedule and Course Information")
    st.write("Welcome to the Home Page.")
    
    display_flip_clock()
    display_session_timer()

    timetable_df = load_default_timetable()
    tab1, tab2, tab3 = st.tabs(["Weekly Schedule", "Course Information", "PDF View"])

    with tab1:
        st.subheader("Weekly Class Schedule")
        st.dataframe(timetable_df)

    with tab2:
        st.subheader("Course Information")
        course_info_df = load_course_info()
        st.dataframe(course_info_df)

    with tab3:
        st.subheader("Upload and View PDF")
        uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_pdf is not None:
            display_pdf(uploaded_pdf)

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Choose a page", ("Home", "Simulation", "Reading Material", "Questions"))

    # Logout button in the sidebar
    if st.sidebar.button("Logout"):
        st.session_state.login_status = False
        st.session_state.pop('login_time', None)
        st.success("You have been logged out.")

    # Call the function to detect tab switches
    detect_tab_switch()
    
    if page == "Home":
        home()
    elif page == "Simulation":
        st.title("Simulation")
        display_flip_clock()
        display_session_timer()
        st.write("Implement simulations")
    elif page == "Reading Material":
        st.title("Reading Material")
        display_flip_clock()
        display_session_timer()
        st.write("Here are some flashcards/reading material to engage students.")
    elif page == "Questions":
        st.title("Questions")
        display_flip_clock()
        display_session_timer()
        st.write("Welcome to the Engaging Page.")

def app():
    init_db()
    if "login_status" not in st.session_state:
        st.session_state.login_status = False

    if not st.session_state.login_status:
        login()
    if st.session_state.get("login_status"):
        main()

if __name__ == "__main__":
    app()
