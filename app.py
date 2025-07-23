import streamlit as st
import requests
from datetime import datetime
import time
from login import login
from extractor import extract_invoice
from make_client import send_to_make
from components.preview import render_preview
from components.summary import render_summary, render_accounting_summary, render_expense_summary
from components.form import render_form, render_expense_form
from streamlit_option_menu import option_menu
st.set_page_config(page_title="AI Document Processor", layout="wide")
# Add this block near the top of app.py
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# Constants
AI_BACKEND_URL = "https://ai-backend-vtzb.onrender.com/extract-invoice"

# App Config

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        padding: 2rem 1rem;
    }
    .menu-item {
        font-weight: 500;
        padding: 0.75rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        cursor: pointer;
        color: #333;
        background-color: #f7f7f7;
        border: 1px solid #ddd;
        text-align: center;
    }
    .menu-item:hover {
        background-color: #eee;
    }
    .menu-selected {
        background-color: #5DB5C8 !important;
        color: white !important;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Dropdown or radio to choose between invoice and expense
with st.sidebar:
    st.title("Main Menu")
    st.write("Select the mode to start the process")

    # Mode selection using option_menu
    mode = option_menu(
        menu_title=None,
        options=["Invoice", "Expense"],
        icons=["file-earmark-text", "credit-card"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        
        styles={
            "container": {
                "background-color": "#fff",
                "border-radius": "12px",
                "box-shadow": "0 2px 8px rgba(44,62,80,0.04)",
                "padding": "16px 12px",
                "margin-bottom": "16px"
            },
            "icon": {"color": "#444", "font-size": "20px"},
            "nav-link": {
                "font-size": "18px",
                "color": "#222",
                "background-color": "#fff",
                "font-weight": "500",
                "border-radius": "8px",
                "margin": "6px 0"
            },
            "nav-link-selected": {
                "background-color": "#5DB5C8",
                "color": "#fff",
                "font-weight": "bold",
                "border-radius": "8px"
            }
        }
    )

# Place the logout button at the bottom of the sidebar
logout_placeholder = st.sidebar.empty()
with logout_placeholder:
    if st.button("Logout", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ========== INVOICE MODE ==========
if mode == "Invoice":
    st.title("Invoice Review Dashboard")

    # Initialize session state
    if "extracted_data_list" not in st.session_state:
        uploaded_files = st.file_uploader("Upload one or more invoice files", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)
        if uploaded_files:
            if st.button("Extract the Data", type="primary", use_container_width=True):
                temp_extracted_data_list = []
                for file in uploaded_files:
                    with st.spinner(f"Extracting: {file.name}"):
                        extracted = extract_invoice(file)
                        if extracted:
                            temp_extracted_data_list.append({
                                "file": file,
                                "filename": file.name,
                                "data": extracted,
                                "data_entered_in_accounting_software": False
                            })
                            st.success(f"{file.name} extracted")
                        else:
                            st.error(f"Failed to extract {file.name}")
                if temp_extracted_data_list:
                    st.session_state["extracted_data_list"] = temp_extracted_data_list
                    st.rerun()
    else:
        extracted_data_list = st.session_state["extracted_data_list"]

        if st.button("Upload New Files", type="primary", use_container_width=True):
            st.session_state.pop("extracted_data_list", None)
            st.rerun()

        with st.expander("Extracted Data", expanded=False):
            st.write(st.session_state)

        extracted_data_count = len([i for i in extracted_data_list if not i["data_entered_in_accounting_software"]])
        accounting_data_count = len([i for i in extracted_data_list if i["data_entered_in_accounting_software"]])

        tab1, tab2 = st.tabs([
            f"Extracted Data {extracted_data_count} / {len(extracted_data_list)}",
            f"Data Entered in Accounting Software {accounting_data_count} / {len(extracted_data_list)}"
        ])

        for i, item in enumerate(extracted_data_list):
            if not item["data_entered_in_accounting_software"]:
                with tab1:
                    st.markdown(f"### Invoice {i + 1}: `{item['filename']}`")
                    col2, col3 = st.columns([1, 1.5])
                    with col2:
                        render_preview(item["file"])
                    with col3:
                        final_data = render_form(i, item["data"], item["file"])
                        if final_data:
                            st.success(f"Data prepared for `{item['file'].name}`")
                            res = send_to_make(final_data)
                            if res:
                                st.session_state["extracted_data_list"][i]["Invoice Number in accounting software"] = final_data["invoice_number"]
                                st.session_state["extracted_data_list"][i]["data_entered_in_accounting_software"] = True
                                st.toast(f"Data sent to accounting software: {final_data['invoice_number']}")
                                st.write(res)
                                time.sleep(3)
                                st.rerun()
                            else:
                                st.warning("Failed to send data.")
            else:
                with tab2:
                    st.markdown(f"### Invoice {i + 1}: `{item['filename']}`")
                    with st.container(border=True):
                        render_accounting_summary(item)

# ========== EXPENSE MODE ==========
elif mode == "Expense":
    st.title("Expense Review Dashboard")

    # Initialize session state
    if "extracted_expense_list" not in st.session_state:
        uploaded_files = st.file_uploader("Upload one or more receipt files", type=["pdf", "jpg", "jpeg", "png"], accept_multiple_files=True)
        if uploaded_files:
            if st.button("Extract the Data", type="primary", use_container_width=True):
                temp_extracted_expense_list = []
                for file in uploaded_files:
                    with st.spinner(f"Extracting: {file.name}"):
                        extracted = extract_invoice(file)
                        if extracted:
                            temp_extracted_expense_list.append({
                                "file": file,
                                "filename": file.name,
                                "data": extracted,
                                "data_entered_in_accounting_software": False
                            })
                            st.success(f"{file.name} extracted")
                        else:
                            st.error(f"Failed to extract {file.name}")
                if temp_extracted_expense_list:
                    st.session_state["extracted_expense_list"] = temp_extracted_expense_list
                    st.rerun()
    else:
        extracted_expense_list = st.session_state["extracted_expense_list"]

        if st.button("Upload New Receipts", type="primary", use_container_width=True):
            st.session_state.pop("extracted_expense_list", None)
            st.rerun()

        with st.expander("Extracted Expense Data", expanded=False):
            st.write(st.session_state)

        expense_data_count = len([i for i in extracted_expense_list if not i["data_entered_in_accounting_software"]])
        accounting_data_count = len([i for i in extracted_expense_list if i["data_entered_in_accounting_software"]])

        tab1, tab2 = st.tabs([
            f"Extracted Data {expense_data_count} / {len(extracted_expense_list)}",
            f"Data Entered in Accounting Software {accounting_data_count} / {len(extracted_expense_list)}"
        ])

        for i, item in enumerate(extracted_expense_list):
            if not item["data_entered_in_accounting_software"]:
                with tab1:
                    st.markdown(f"### Expense {i + 1}: `{item['filename']}`")
                    col2, col3 = st.columns([1, 1.5])

                    with col2:
                        render_preview(item["file"])
                    with col3:
                        final_data, submitted = render_expense_form(i, item["data"], item["file"])
                        if submitted:
                            st.success(f"Data prepared for `{item['file'].name}`")
                            res = send_to_make(final_data, type="expense")

                            if res["success"]:
                                st.session_state["extracted_expense_list"][i]["Expense Number in accounting software"] = final_data["invoice_number"]
                                st.session_state["extracted_expense_list"][i]["data_entered_in_accounting_software"] = True
                                st.toast(f"Expense sent to accounting software: {final_data['invoice_number']}")
                                time.sleep(3)
                                st.rerun()
                            else:
                                st.warning(f"Failed to send expense: {res['error']}")
            else:
                with tab2:
                    st.markdown(f"### Expense {i + 1}: `{item['filename']}`")
                    with st.container(border=True):
                        render_accounting_summary(item)

