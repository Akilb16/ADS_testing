import streamlit as st
import base64

def get_logo_base64():
    """Convert logo to base64 for embedding"""
    try:
        with open("Files/ADS_logo.jpg", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

def login():
    # Hide Streamlit UI elements for clean login page
    st.markdown("""
        <style>
        .stApp > header {
            background-color: transparent;
        }
        .stApp {
            background: linear-gradient(135deg, #f5f7fb 0%, #e8f2f5 100%);
        }
        [data-testid="stHeader"] {
            height: 0rem;
        }
        [data-testid="stToolbar"] {
            right: 2rem;
        }
        [data-testid="stDecoration"] {
            display: none;
        }
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 2rem;
        }
        .login-card {
            background: white;
            padding: 3rem 2.5rem;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
            max-width: 450px;
            width: 100%;
            text-align: center;
            border-top: 4px solid #5DB5C8;
        }
        .logo-container {
            margin-bottom: 2rem;
        }
        .logo-container img {
            max-width: 80px;
            height: 80px;
            margin-bottom: 1rem;
        }
        .brand-title {
            color: #2C3E50;
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        .brand-subtitle {
            color: #5DB5C8;
            font-size: 0.95rem;
            font-weight: 600;
            margin-bottom: 2rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .login-form {
            margin-top: 2rem;
        }
        .stTextInput > div > div > input {
            background-color: #f8f9fb !important;
            border: 2px solid #e1e5e9 !important;
            border-radius: 12px !important;
            padding: 1rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            height: 38px !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #5DB5C8 !important;
            box-shadow: 0 0 0 3px rgba(93, 181, 200, 0.1) !important;
            background-color: white !important;
        }
        .stTextInput > label {
            color: #2C3E50 !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.5rem !important;
        }
        .login-button {
            background: linear-gradient(135deg, #5DB5C8 0%, #4A9DB8 100%) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 1rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            margin-top: 1.5rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(93, 181, 200, 0.3) !important;
        }
        .login-button:hover {
            background: linear-gradient(135deg, #4A9DB8 0%, #3A8DA8 100%) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(93, 181, 200, 0.4) !important;
        }
        .error-message {
            background-color: #fef2f2;
            border: 1px solid #fecaca;
            color: #dc2626;
            padding: 1rem;
            border-radius: 12px;
            margin-top: 1rem;
            font-size: 0.9rem;
            font-weight: 500;
        }
        .footer-text {
            color: #94a3b8;
            font-size: 0.8rem;
            margin-top: 2rem;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    if "login_attempted" not in st.session_state:
        st.session_state["login_attempted"] = False

    logo_base64 = get_logo_base64()
    col1, col2 = st.columns(2, gap="large",vertical_alignment="center")
        # Use a single container for centering
        #st.markdown('<div class="login-container">', unsafe_allow_html=True)
    with col1:
        cola,colb,colc = st.columns([2,8,2],gap="large",vertical_alignment="center")
        with colb:
            if logo_base64:
                st.image(f'data:image/jpeg;base64,{logo_base64}', width=500,use_container_width=True)

    with col2:
        
        
        
        
        st.markdown('<h1 class="brand-title">ADS AI Document Processor</h1>', unsafe_allow_html=True)
        st.markdown('<p class="brand-subtitle">AUDIT • TAX • ADVISORY</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    
        # Login form
        st.markdown('<div class="login-form">', unsafe_allow_html=True)
        username = st.text_input("Username", key="login_user", placeholder="Enter your username")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="Enter your password")
        if st.button("Sign In", key="login_btn", help="Click to sign in"):
            st.session_state["login_attempted"] = True
            if username == "user" and password == "user":
                st.session_state["authenticated"] = True
                st.session_state["login_attempted"] = False
                st.rerun()
            else:
                st.session_state["authenticated"] = False
        if st.session_state["login_attempted"] and not st.session_state.get("authenticated", False):
            st.markdown("""
                <div class="error-message">
                    ❌ Invalid username or password. Please try again.
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    # Footer
    st.markdown("""
        <div class="footer-text">
            © 2025 ADS Auditors. Secure AI Document Processing System.
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
