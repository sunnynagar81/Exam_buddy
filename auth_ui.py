import streamlit as st
from auth import create_user, verify_user


def render_auth():
    st.markdown(
        """
        <div class="app-hero">
            <h1>🔐 Welcome to Exam Buddy</h1>
            <p>Login karo ya naya account banao. Har user ke notes alag rehte hain.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_login, tab_signup = st.tabs(["🔑 Login", "✨ Sign up"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.form_submit_button("Login", use_container_width=True):
                if verify_user(username, password):
                    st.session_state.user = username.strip().lower()
                    st.rerun()
                else:
                    st.error("Username ya password galat hai.")

    with tab_signup:
        with st.form("signup_form"):
            new_user = st.text_input("Choose a username", key="signup_user")
            new_pass = st.text_input("Choose a password", type="password", key="signup_pass")
            confirm = st.text_input("Confirm password", type="password", key="signup_confirm")
            if st.form_submit_button("Create account", use_container_width=True):
                if new_pass != confirm:
                    st.error("Dono passwords match nahi kar rahe.")
                else:
                    ok, message = create_user(new_user, new_pass)
                    if ok:
                        st.success(message)
                    else:
                        st.error(message)