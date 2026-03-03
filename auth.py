import streamlit as st
from database import register_user, login_user

def show_auth_page():
    st.markdown("""
    <div style='text-align:center; padding: 2rem 0 1rem 0;'>
        <div style='font-family: Playfair Display, serif; font-size: 2.8rem; font-weight:900; color:#c9a84c; letter-spacing:3px;'>📚 PageVault</div>
        <div style='color:#8b9bb4; font-style:italic; font-size:1.1rem;'>Your personal library, beautifully curated.</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["  🔐  Sign In  ", "  ✨  Register  "])

    with tab1:
        _login_form()

    with tab2:
        _register_form()

def _login_form():
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        email = st.text_input("Email", placeholder="your@email.com", key="login_email")
        password = st.text_input("Password", type="password", placeholder="••••••••", key="login_password")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In →", use_container_width=True, key="login_btn"):
            if not email or not password:
                st.markdown('<div class="alert-error">⚠️ Please fill in all fields.</div>', unsafe_allow_html=True)
            else:
                ok, result = login_user(email.strip(), password)
                if ok:
                    st.session_state.user = result
                    st.session_state.page = "home"
                    st.rerun()
                else:
                    st.markdown(f'<div class="alert-error">❌ {result}</div>', unsafe_allow_html=True)



def _register_form():
    st.markdown("<br>", unsafe_allow_html=True)
    name = st.text_input("Full Name", placeholder="Jane Austen", key="reg_name")
    email = st.text_input("Email Address", placeholder="jane@example.com", key="reg_email")
    password = st.text_input("Password", type="password", placeholder="Choose a strong password", key="reg_password")
    confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password", key="reg_confirm")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Create Account →", use_container_width=True, key="reg_btn"):
        if not all([name, email, password, confirm]):
            st.markdown('<div class="alert-error">⚠️ Please fill in all fields.</div>', unsafe_allow_html=True)
        elif len(password) < 6:
            st.markdown('<div class="alert-error">⚠️ Password must be at least 6 characters.</div>', unsafe_allow_html=True)
        elif password != confirm:
            st.markdown('<div class="alert-error">⚠️ Passwords do not match.</div>', unsafe_allow_html=True)
        elif "@" not in email:
            st.markdown('<div class="alert-error">⚠️ Please enter a valid email.</div>', unsafe_allow_html=True)
        else:
            ok, msg = register_user(name.strip(), email.strip().lower(), password)
            if ok:
                st.markdown(f'<div class="alert-success">✅ {msg} Please sign in.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="alert-error">❌ {msg}</div>', unsafe_allow_html=True)