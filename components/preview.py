import streamlit as st

def render_preview(file):
    st.markdown("### Invoice File")
    if file.type == "application/pdf":
        st.info("PDF uploaded (preview not shown).")
    else:
        st.image(file.getvalue(), use_container_width=True)
