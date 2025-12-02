"""Main controller for the TikTok Reality Check app."""

import streamlit as st
import time

import utils
import logic
import ui

# 1. Setup: Page config (Wide)
st.set_page_config(page_title="TikTok Reality Check", layout="wide", initial_sidebar_state="expanded")

# Import modules and Load CSS
utils.load_css()

# Add custom scrollbar CSS
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

# 2. State: Initialize session state
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

if "stats" not in st.session_state:
    st.session_state.stats = None

if "persona" not in st.session_state:
    st.session_state.persona = None

if "absurd_items" not in st.session_state:
    st.session_state.absurd_items = None

if "last_calc_time" not in st.session_state:
    st.session_state.last_calc_time = 0

# 3. Sidebar: Settings
st.sidebar.title("Settings")
avg_duration = st.sidebar.slider("Average video duration (seconds)", min_value=10, max_value=60, value=15)
st.sidebar.caption("ℹ️ Note: The global average watch time is ~15s per video. Adjust if you are a fast scroller.")
st.sidebar.checkbox("Dark Mode (Always On)", value=True, disabled=True)
guilt_trip_mode = st.sidebar.checkbox("Enable 'Guilt Trip' Mode", value=True)

# 4. VIEW 1: Landing Page (if not loaded)
if not st.session_state.data_loaded:
    # 1. Header
    st.markdown(ui.render_landing_header(), unsafe_allow_html=True)
    
    # 2. Marquee
    st.markdown(ui.render_landing_marquee(), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3. Uploader Section
    uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. User Guide
    ui.render_user_guide()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 5. Email CTA Button
    col_cta1, col_cta2, col_cta3 = st.columns([1, 2, 1])
    with col_cta2:
        ui.render_cta_button()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 6. Footer Note
    st.markdown(
        "<p style='text-align: center; color: rgba(255, 255, 255, 0.6); font-size: 0.9rem; margin-top: 0.5rem;'>"
        "Currently supports TikTok JSON. Instagram & YouTube coming soon."
        "</p>",
        unsafe_allow_html=True
    )
    
    # Logic: On upload -> Spinner -> logic.process_json
    if uploaded_file is not None:
        # Spinner
        with st.spinner("🔍 Decoding digital footprint..."):
            time.sleep(1.5)
        
        try:
            # Process JSON
            df = logic.process_json(uploaded_file)
            
            # If success -> Calculate stats -> Save to State -> Rerun
            stats = logic.calculate_stats(df, avg_duration)
            persona = logic.get_persona(df, guilt_trip_mode)
            absurd_items = logic.get_absurd_items(stats['total_hours'])
            
            # Save to State
            st.session_state.dataframe = df
            st.session_state.stats = stats
            st.session_state.persona = persona
            st.session_state.absurd_items = absurd_items
            st.session_state.data_loaded = True
            
            # Rerun
            st.rerun()
        
        except ValueError as e:
            # If error -> Show st.error with the exception message
            st.error(f"⚠️ {str(e)}")
        except Exception as e:
            st.error(f"⚠️ An unexpected error occurred: {str(e)}")

# 5. VIEW 2: Dashboard (if loaded)
else:
    # Cooldown Logic: Throttle rapid recalculations
    current_time = time.time()
    time_since_last_calc = current_time - st.session_state.last_calc_time
    
    if time_since_last_calc < 1.0:
        # Throttle: Wait for cooldown period
        time.sleep(1.0 - time_since_last_calc)
    
    # Dynamic Updates: Recalculate stats with current avg_duration
    # This ensures the slider changes trigger immediate updates
    df = st.session_state.dataframe
    stats = logic.calculate_stats(df, avg_duration)
    persona = logic.get_persona(df, guilt_trip_mode)
    absurd_items = logic.get_absurd_items(stats['total_hours'])
    
    # Update session state with new calculations
    st.session_state.stats = stats
    st.session_state.persona = persona
    st.session_state.absurd_items = absurd_items
    st.session_state.last_calc_time = time.time()
    
    # Call ui.render_metrics(stats)
    st.markdown(ui.render_metrics(stats), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call ui.render_slider(absurd_items)
    st.markdown("<h2>The Absurd Reality</h2>", unsafe_allow_html=True)
    st.markdown(ui.render_slider(absurd_items), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call ui.render_persona(persona)
    st.markdown(ui.render_persona(persona), unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Call ui.render_banner()
    st.markdown(ui.render_banner(), unsafe_allow_html=True)
    
    # Button for waitlist
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("✨ Join Waitlist", key="waitlist_button", use_container_width=True):
            st.toast("You're on the list! Get ready for change.", icon="🎮")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Button "Analyze another file" -> Reset state -> Rerun
    if st.button("Analyze another file", key="reset_button"):
        st.session_state.data_loaded = False
        st.session_state.dataframe = None
        st.session_state.stats = None
        st.session_state.persona = None
        st.session_state.absurd_items = None
        st.rerun()
