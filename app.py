"""Main controller for the TikTok Reality Check app."""

import streamlit as st
import time

import utils
import logic
import ui

# Setup page config (must be first)
st.set_page_config(page_title="TikTok Reality Check", layout="wide", initial_sidebar_state="expanded")

# Load CSS and inject JS
utils.load_css("styles.css")

# Add custom scrollbar CSS directly in Python (sometimes external CSS scrollbars get ignored)
st.markdown("""
<style>
.scroll-container {
    scrollbar-width: none !important;
    -ms-overflow-style: none !important;
}
.scroll-container::-webkit-scrollbar {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# Session State
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

# Sidebar settings
st.sidebar.title("Settings")
avg_duration = st.sidebar.slider("Average video duration (seconds)", min_value=10, max_value=60, value=30)
st.sidebar.checkbox("Dark Mode (Always On)", value=True, disabled=True)
guilt_trip_mode = st.sidebar.checkbox("Enable 'Guilt Trip' Mode", value=True)

# View 1: Upload
if not st.session_state.data_loaded:
    # Show Title
    st.markdown(ui.render_title(), unsafe_allow_html=True)
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])
    
    # Process file if uploaded
    if uploaded_file is not None:
        # Spinner
        with st.spinner("🔍 Decoding digital footprint..."):
            time.sleep(1.5)
        
        # Process JSON
        df = logic.process_json(uploaded_file)
        
        if df is not None:
            # Save State
            st.session_state.dataframe = df
            st.session_state.data_loaded = True
            st.rerun()
        else:
            st.error("Could not find video history. Check JSON format. Expected path: ['Activity']['Video Browsing History']['VideoList']")

# View 2: Dashboard
else:
    df = st.session_state.dataframe
    
    # Calculate stats
    stats = logic.calculate_stats(df, avg_duration)
    
    # Render Header
    st.markdown(ui.render_header(), unsafe_allow_html=True)
    
    # SECTION 1: Metrics
    st.markdown(ui.render_metrics(stats), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECTION 2: Absurd Slider
    st.markdown("<h2>The Absurd Reality</h2>", unsafe_allow_html=True)
    absurd_items = logic.get_absurd_items(stats['total_hours'])
    slider_html = ui.render_slider(absurd_items)
    # Inject JavaScript for dragging
    slider_html += utils.DRAG_JS
    st.markdown(slider_html, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECTION 3: Persona
    persona = logic.get_persona(df, guilt_trip_mode)
    st.markdown(ui.render_persona(persona), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECTION 4: Banner
    st.markdown(ui.render_banner(), unsafe_allow_html=True)
    
    # Button for waitlist
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("✨ Join Waitlist", key="waitlist_button", use_container_width=True):
            st.toast("You're on the list! Get ready for change.", icon="🎮")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Reset Button
    if st.button("Analyze another file", key="reset_button"):
        st.session_state.data_loaded = False
        st.session_state.dataframe = None
        st.rerun()
