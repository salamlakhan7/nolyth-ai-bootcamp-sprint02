import streamlit as st
import requests
import time

# Point this at your deployed FastAPI backend URL
BACKEND_URL = "https://titanic-survival-prediction-ajac.onrender.com"

st.set_page_config(page_title="Titanic Survival Predictor", page_icon="🚢")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


def call_backend_with_retry(method, url, max_retries=5, **kwargs):
    """
    Render's free tier spins the backend down after inactivity - the first
    request after that can take 30-50s to wake it, and may briefly fail
    with a ConnectionError while it's still starting up. This retries a
    few times with a short wait in between, so the app recovers on its own
    instead of showing an error to the user.
    """
    last_error = None
    for attempt in range(max_retries):
        try:
            resp = requests.request(method, url, timeout=90, **kwargs)
            return resp
        except requests.exceptions.ConnectionError as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(5)
    raise last_error


def register_user(username, password):
    return call_backend_with_retry(
        "POST", f"{BACKEND_URL}/register",
        json={"username": username, "password": password},
    )


def login_user(username, password):
    return call_backend_with_retry(
        "POST", f"{BACKEND_URL}/login",
        data={"username": username, "password": password},
    )


def get_auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


st.title("🚢 Titanic Survival Predictor")
st.caption("Note: this app uses a free-tier backend that may take up to a minute to wake up on first use.")

# ---------- Auth ----------
if st.session_state.token is None:
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            with st.spinner("Connecting to server (may take a moment if it's waking up)..."):
                try:
                    resp = login_user(login_username, login_password)
                except requests.exceptions.ConnectionError:
                    st.error("Could not reach the server after several attempts. Please try again in a minute.")
                    resp = None

            if resp is not None:
                if resp.status_code == 200:
                    st.session_state.token = resp.json()["access_token"]
                    st.session_state.username = login_username
                    st.rerun()
                else:
                    st.error("Login failed - check your username/password.")

    with tab_register:
        st.subheader("Register")
        reg_username = st.text_input("Choose a username", key="reg_username")
        reg_password = st.text_input("Choose a password", type="password", key="reg_password")
        if st.button("Register"):
            with st.spinner("Connecting to server (may take a moment if it's waking up)..."):
                try:
                    resp = register_user(reg_username, reg_password)
                except requests.exceptions.ConnectionError:
                    st.error("Could not reach the server after several attempts. Please try again in a minute.")
                    resp = None

            if resp is not None:
                if resp.status_code == 201:
                    st.success("Registered successfully - you can log in now.")
                else:
                    st.error(resp.json().get("detail", "Registration failed."))

# ---------- Main app (after login) ----------
else:
    st.sidebar.write(f"Logged in as **{st.session_state.username}**")
    if st.sidebar.button("Log out"):
        st.session_state.token = None
        st.session_state.username = None
        st.rerun()

    tab_predict, tab_history = st.tabs(["Predict", "History"])

    with tab_predict:
        st.subheader("Enter passenger details")

        col1, col2 = st.columns(2)
        with col1:
            pclass = st.selectbox("Passenger Class", [1, 2, 3], index=2)
            sex_label = st.selectbox("Sex", ["Male", "Female"])
            sex = 0 if sex_label == "Male" else 1
            age = st.slider("Age", 0, 80, 28)
            fare = st.number_input("Fare ($)", min_value=0.0, max_value=600.0, value=32.0)

        with col2:
            family_size = st.slider("Family Size (including self)", 1, 11, 1)
            has_cabin = st.selectbox("Has Cabin Recorded?", ["No", "Yes"])
            has_cabin = 0 if has_cabin == "No" else 1
            embarked = st.selectbox("Port of Embarkation", ["C", "Q", "S"])
            title = st.selectbox("Title", ["Mr", "Mrs", "Miss", "Master", "Rare"])

        if st.button("Predict Survival"):
            payload = {
                "pclass": pclass,
                "sex": sex,
                "age": age,
                "fare": fare,
                "family_size": family_size,
                "has_cabin": has_cabin,
                "embarked": embarked,
                "title": title,
            }

            with st.spinner("Getting prediction..."):
                try:
                    resp = call_backend_with_retry(
                        "POST", f"{BACKEND_URL}/predict",
                        json=payload, headers=get_auth_headers(),
                    )
                except requests.exceptions.ConnectionError:
                    st.error("Could not reach the server after several attempts. Please try again in a minute.")
                    resp = None

            if resp is not None:
                if resp.status_code == 200:
                    result = resp.json()
                    st.write("### Results")

                    c1, c2 = st.columns(2)
                    with c1:
                        st.metric(
                            "Logistic Regression",
                            "Survived" if result["logistic_prediction"] == 1 else "Did Not Survive",
                            f"{result['logistic_probability']*100:.1f}% probability",
                        )
                    with c2:
                        st.metric(
                            "Random Forest",
                            "Survived" if result["rf_prediction"] == 1 else "Did Not Survive",
                            f"{result['rf_probability']*100:.1f}% probability",
                        )
                else:
                    st.error("Prediction failed. Try logging in again.")

    with tab_history:
        st.subheader("Your Prediction History")
        with st.spinner("Loading history..."):
            try:
                resp = call_backend_with_retry(
                    "GET", f"{BACKEND_URL}/history", headers=get_auth_headers(),
                )
            except requests.exceptions.ConnectionError:
                st.error("Could not reach the server after several attempts. Please try again in a minute.")
                resp = None

        if resp is not None:
            if resp.status_code == 200:
                records = resp.json()
                if records:
                    st.dataframe(records)
                else:
                    st.info("No predictions yet - try the Predict tab.")
            else:
                st.error("Could not load history.")