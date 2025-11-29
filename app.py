import streamlit as st
import pandas as pd
import json
import time
import textwrap

# Ensure st.set_page_config is the very first command
st.set_page_config(page_title="TikTok Reality Check", layout="wide", initial_sidebar_state="expanded")

# 1. CSS Loading Fix
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file {file_name} not found. Using default styles.")
    except Exception as e:
        st.error(f"Error loading CSS: {str(e)}")

# Call CSS function
local_css("styles.css")

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

# JS for Draggable Slider
drag_js = textwrap.dedent("""
<script>
(function() {
    const containers = document.querySelectorAll('.scroll-container');
    containers.forEach(container => {
        let isDown = false;
        let startX;
        let scrollLeft;
        container.addEventListener('mousedown', (e) => {
            isDown = true;
            container.style.cursor = 'grabbing';
            startX = e.pageX - container.offsetLeft;
            scrollLeft = container.scrollLeft;
        });
        container.addEventListener('mouseleave', () => {
            isDown = false;
            container.style.cursor = 'grab';
        });
        container.addEventListener('mouseup', () => {
            isDown = false;
            container.style.cursor = 'grab';
        });
        container.addEventListener('mousemove', (e) => {
            if (!isDown) return;
            e.preventDefault();
            const x = e.pageX - container.offsetLeft;
            const walk = (x - startX) * 2;
            container.scrollLeft = scrollLeft - walk;
        });
    });
})();
</script>
""")

# Session state init
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False

if "dataframe" not in st.session_state:
    st.session_state.dataframe = None

# Sidebar settings
st.sidebar.title("Settings")
avg_duration = st.sidebar.slider("Average video duration (seconds)", min_value=10, max_value=60, value=30)
st.sidebar.checkbox("Dark Mode (Always On)", value=True, disabled=True)
guilt_trip_mode = st.sidebar.checkbox("Enable 'Guilt Trip' Mode", value=True)

# 2. View 1: Upload Logic
if not st.session_state.data_loaded:
    # Clean centered Title (no indentation at start)
    st.markdown(textwrap.dedent("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1>TikTok Reality Check</h1>
        <p style="font-size: 1.2rem; color: rgba(255, 255, 255, 0.7); margin-top: 1rem;">
            Discover how much time you've spent scrolling
        </p>
    </div>
    """), unsafe_allow_html=True)
    
    # File Uploader
    uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])
    
    # Logic: File Uploader -> Spinner -> Sleep -> Parsing (Robust) -> Save State -> Rerun
    if uploaded_file is not None:
        # Spinner
        with st.spinner("🔍 Decoding digital footprint..."):
            # Sleep
            time.sleep(1.5)
        
        # Parsing (Robust)
        try:
            json_data = json.load(uploaded_file)
            
            # Extract path: Activity -> Video Browsing History -> VideoList
            try:
                video_list = json_data['Activity']['Video Browsing History']['VideoList']
                
                # Create DataFrame
                df = pd.DataFrame(video_list)
                
                # Convert Date to datetime
                df['Date'] = pd.to_datetime(df['Date'])
                
                # Save State
                st.session_state.dataframe = df
                st.session_state.data_loaded = True
                
                # Rerun
                st.rerun()
                
            except (KeyError, TypeError):
                st.error("Could not find video history. Check JSON format. Expected path: ['Activity']['Video Browsing History']['VideoList']")
        
        except json.JSONDecodeError:
            st.error("Error: Invalid JSON file. Please upload a valid JSON file.")
        except Exception as e:
            st.error(f"Error: An unexpected error occurred: {str(e)}")

# 3. View 2: Dashboard (The Redesign)
else:
    df = st.session_state.dataframe
    
    # Perform calculations
    total_videos = len(df)
    total_seconds = total_videos * avg_duration
    total_hours = total_seconds / 3600
    total_days = total_hours / 24
    
    # Header: "YOUR STATS" (HTML - no indentation at start)
    st.markdown(textwrap.dedent("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>YOUR STATS</h2>
    </div>
    """), unsafe_allow_html=True)
    
    # SECTION 1: Interactive Stat Cards (HTML Replacement for st.metric)
    # Construct HTML: Create a string stats_html (no indentation at start of lines)
    stats_html = '<div class="stats-row">'
    stats_html += f'<div class="stat-card"><div class="stat-value">{total_videos:,}</div><div class="stat-label">Total Videos</div></div>'
    stats_html += f'<div class="stat-card"><div class="stat-value">{round(total_hours, 1):,}</div><div class="stat-label">Hours Wasted</div></div>'
    stats_html += f'<div class="stat-card"><div class="stat-value">{round(total_days, 2):,}</div><div class="stat-label">Days Lost</div></div>'
    stats_html += '</div>'
    
    # Render
    st.markdown(stats_html, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECTION 2: Absurd Slider (Horizontal)
    st.markdown("<h2>The Absurd Reality</h2>", unsafe_allow_html=True)
    
    # List of items - Ensure absurd_items is populated correctly based on total_hours
    absurd_items = []
    
    # Cook instant noodles (3 minutes per pack = 0.05 hours)
    if total_hours >= 0.05:
        noodle_count = int(total_hours / 0.05)
        absurd_items.append({'icon': '🍜', 'text': f'Cook {noodle_count:,} packs of instant noodles'})
    
    # Pet cat (5 minutes = 0.083 hours)
    if total_hours >= 0.083:
        pet_count = int(total_hours / 0.083)
        absurd_items.append({'icon': '🐱', 'text': f'Pet a cat {pet_count:,} times'})
    
    # Become President of Argentina (4 year term = ~35,000 hours)
    if total_hours >= 35000:
        pres_count = int(total_hours / 35000)
        absurd_items.append({'icon': '🇦🇷', 'text': f'Become President of Argentina {pres_count} times'})
    
    # Walk to the Moon (~76,880 hours round trip)
    if total_hours >= 76880:
        absurd_items.append({'icon': '🌙', 'text': 'Walk to the Moon and back'})
    elif total_hours >= 38440:
        absurd_items.append({'icon': '🌙', 'text': 'Walk to the Moon (one way)'})
    
    # Additional items
    if total_hours >= 1000:
        one_piece_count = int(total_hours / 1000)
        absurd_items.append({'icon': '🏴‍☠️', 'text': f'Watch the entire One Piece anime {one_piece_count} times'})
    
    if total_hours >= 10000:
        govt_count = int(total_hours / 10000)
        absurd_items.append({'icon': '⚔️', 'text': f'Overthrow a government {govt_count} times'})
    
    if total_hours >= 1000:
        lang_count = int(total_hours / 1000)
        absurd_items.append({'icon': '🗣️', 'text': f'Learn {lang_count} languages to fluency'})
    
    if total_hours >= 50:
        book_count = int(total_hours / 50)
        absurd_items.append({'icon': '📚', 'text': f'Read War and Peace {book_count} times'})
    
    if total_hours >= 100:
        marathon_count = int(total_hours / 100)
        absurd_items.append({'icon': '🏃', 'text': f'Train for and run {marathon_count} marathons'})
    
    if total_hours >= 2000:
        house_count = int(total_hours / 2000)
        absurd_items.append({'icon': '🏠', 'text': f'Build {house_count} houses from scratch'})
    
    # Construct HTML: Build single, continuous string without line breaks between div tags
    if absurd_items:
        slider_html = '<div class="scroll-container">'
        for item in absurd_items:
            slider_html += f'<div class="scroll-card"><div class="icon">{item["icon"]}</div><div class="title">{item["text"]}</div></div>'
        slider_html += '</div>'
        # Inject JavaScript for dragging AFTER the slider HTML in the same st.markdown call
        slider_html += drag_js
        # Render via st.markdown
        st.markdown(slider_html, unsafe_allow_html=True)
    else:
        st.markdown(textwrap.dedent("""
        <div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.7);">
            <p style="font-size: 1.2rem;">Keep scrolling to unlock absurd comparisons! 📱</p>
        </div>
        """), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECTION 3: Persona
    df['Hour'] = df['Date'].dt.hour
    hourly_counts = df.groupby('Hour').size().reset_index(name='Views')
    
    # Peak hour logic
    def get_period(hour):
        if 23 <= hour or hour <= 5:
            return "Night"
        elif 6 <= hour <= 11:
            return "Morning"
        elif 12 <= hour <= 17:
            return "Afternoon"
        else:  # 18-22
            return "Evening"
    
    # Add period to hourly counts
    hourly_counts['Period'] = hourly_counts['Hour'].apply(get_period)
    period_counts = hourly_counts.groupby('Period')['Views'].sum()
    
    # Find peak period
    peak_period = period_counts.idxmax()
    
    # Determine persona based on peak period and guilt trip mode
    if guilt_trip_mode:
        personas = {
            "Night": ("🧟 Sleep Deprived Zombie", "You're sacrificing your health for late-night scrolling. Your future self will thank you for stopping."),
            "Morning": ("☕ Caffeine-Dependent Scroller", "Starting your day with TikTok instead of purpose. What a way to set the tone."),
            "Afternoon": ("😴 Productivity Killer", "The middle of the day, prime time for getting things done. But here you are, scrolling."),
            "Evening": ("🌙 Mindless Binger", "Winding down? More like winding up your dopamine receptors. Sleep quality? What's that?")
        }
    else:
        personas = {
            "Night": ("🦉 The Night Owl", "You spend your night hours trapped in the scroll loop."),
            "Morning": ("☀️ The Early Bird", "You spend your morning hours trapped in the scroll loop."),
            "Afternoon": ("☕ The Lunchtime Scroller", "You spend your afternoon hours trapped in the scroll loop."),
            "Evening": ("🌇 The Evening Binger", "You spend your evening hours trapped in the scroll loop.")
        }
    
    persona_title, persona_description = personas[peak_period]
    
    # Render <div class="glass-card"> with Persona info (no indentation at start)
    st.markdown(textwrap.dedent(f"""
    <div class="glass-card">
        <div class="persona-title">{persona_title}</div>
        <div class="persona-message">{persona_description}</div>
    </div>
    """), unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # SECTION 4: Banner
    # Render .game-banner (English text - no indentation at start)
    st.markdown(textwrap.dedent("""
    <div class="game-banner">
        <h2>🚀 COMING SOON: My Little Me</h2>
        <p><strong>Stop feeding algorithms. Start feeding yourself.</strong></p>
        <p>The first Tamagotchi that grows based on your <strong>REAL</strong> actions. Read a book? Your character gets smarter. Went for a run? It gets stronger. Gamify your life.</p>
    </div>
    """), unsafe_allow_html=True)
    
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
