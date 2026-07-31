import streamlit as st
import requests

# Point this at your deployed FastAPI backend URL
BACKEND_URL = "http://localhost:8000"  # change to your Hugging Face Space URL when deployed

st.set_page_config(page_title="Titanic Survival Predictor", page_icon="🚢")

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None


def register_user(username, password):
    resp = requests.post(f"{BACKEND_URL}/register", json={"username": username, "password": password})
    return resp


def login_user(username, password):
    resp = requests.post(
        f"{BACKEND_URL}/login",
        data={"username": username, "password": password},
    )
    return resp


def get_auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


st.title("🚢 Titanic Survival Predictor")

# ---------- Auth ----------
if st.session_state.token is None:
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("Login")
        login_username = st.text_input("Username", key="login_username")
        login_password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            resp = login_user(login_username, login_password)
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
            resp = register_user(reg_username, reg_password)
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
            resp = requests.post(f"{BACKEND_URL}/predict", json=payload, headers=get_auth_headers())

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
        resp = requests.get(f"{BACKEND_URL}/history", headers=get_auth_headers())
        if resp.status_code == 200:
            records = resp.json()
            if records:
                st.dataframe(records)
            else:
                st.info("No predictions yet - try the Predict tab.")
        else:
            st.error("Could not load history.")