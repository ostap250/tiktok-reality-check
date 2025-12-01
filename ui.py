"""HTML generation functions for the TikTok Reality Check app."""

import textwrap
import streamlit as st
import re


def render_gradient_text(text):
    """
    Returns HTML span with gradient text styling.
    
    Args:
        text (str): Text to apply gradient to
        
    Returns:
        str: HTML span with gradient-text class
    """
    return f'<span class="gradient-text">{text}</span>'


def render_header(title="YOUR STATS", subtitle=None):
    """
    Returns HTML for the main header.
    
    Args:
        title (str): Header title text
        subtitle (str, optional): Subtitle text below the title
        
    Returns:
        str: HTML string for header
    """
    subtitle_html = ''
    if subtitle:
        subtitle_html = f'<p style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.7); margin-top: 0.5rem;">{subtitle}</p>'
    
    return textwrap.dedent(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>{title}</h2>
        {subtitle_html}
    </div>
    """)


def render_landing_marquee():
    """
    Creates a specialized HTML string for the Welcome Screen auto-slider.
    
    Returns:
        str: HTML string for landing marquee
    """
    items = [
        "📊 Deep Analysis",
        "🎭 Find Your Persona",
        "🤯 Absurd Stats",
        "🎮 Gamify Life",
        "🔒 Privacy First"
    ]
    
    # Duplicate items twice to create a seamless loop effect
    duplicated_items = items * 2
    
    items_html = ''
    for item in duplicated_items:
        items_html += f'<div class="marquee-item">{item}</div>'
    
    return textwrap.dedent(f"""
    <div class="marquee-container">
        <div class="marquee-track">
            {items_html}
        </div>
    </div>
    """)


def render_metrics(stats):
    """
    Returns HTML string for the top 3 square metric cards.
    
    Args:
        stats (dict): Dictionary with total_videos, total_hours, total_days
        
    Returns:
        str: HTML string for metrics
    """
    return textwrap.dedent(f"""
    <div class="stats-row">
        <div class="stat-card">
            <div class="stat-value">{stats["total_videos"]:,}</div>
            <div class="stat-label">Total Videos</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{round(stats["total_hours"], 1):,}</div>
            <div class="stat-label">Hours Wasted</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{round(stats["total_days"], 2):,}</div>
            <div class="stat-label">Days Lost</div>
        </div>
    </div>
    """)


def render_slider(items):
    """
    Returns HTML string for the auto-scrolling marquee slider.
    
    Args:
        items (list): List of dictionaries with icon and text keys
        
    Returns:
        str: HTML string for slider
    """
    if not items:
        return textwrap.dedent("""
        <div style="text-align: center; padding: 2rem; color: rgba(255, 255, 255, 0.7);">
            <p style="font-size: 1.2rem;">Keep scrolling to unlock absurd comparisons! 📱</p>
        </div>
        """)
    
    # Duplicate list to ensure seamless infinite scrolling loop
    display_items = items * 2
    
    # Construct HTML: Loop through items and build cards
    # Each card has card-icon and card-text (no inline styles)
    cards_html = ''
    for item in display_items:
        cards_html += f'<div class="scroll-card"><div class="card-icon">{item["icon"]}</div><div class="card-text">{item["text"]}</div></div>'
    
    # Wrap in scroll-container for auto-scrolling marquee
    return textwrap.dedent(f"""
    <div class="card-marquee-wrapper">
        <div class="card-marquee-track">
            {cards_html}
        </div>
    </div>
    """)


def render_persona(persona):
    """
    Returns HTML for the persona glass card.
    
    Emoji Fix: Separates emoji from text to prevent emoji from getting blue gradient color.
    
    Args:
        persona (dict): Dictionary with title and desc keys
        
    Returns:
        str: HTML string for persona card
    """
    title = persona['title']
    desc = persona['desc']
    
    # Extract emoji from title (emoji is typically at the start)
    # Pattern: emoji followed by space and text
    emoji_match = re.match(r'^(\S+\s)', title)
    if emoji_match:
        emoji = emoji_match.group(1).strip()
        title_text = title[len(emoji_match.group(1)):].strip()
    else:
        # If no emoji pattern found, try to extract first character if it's an emoji
        # Unicode emoji range check (simplified)
        if title and ord(title[0]) > 127:
            emoji = title[0]
            title_text = title[1:].strip()
        else:
            # No emoji found, use entire title as text
            emoji = ''
            title_text = title
    
    # Build HTML: emoji with natural color, text with gradient
    if emoji:
        emoji_html = f'<span style="font-size: 1.5em;">{emoji}</span> '
    else:
        emoji_html = ''
    title_html = render_gradient_text(title_text) if title_text else ''
    
    return textwrap.dedent(f"""
    <div class="glass-card">
        <h2>{emoji_html}{title_html}</h2>
        <p>{desc}</p>
    </div>
    """)


def render_banner():
    """
    Returns HTML for the Game Banner.
    
    Returns:
        str: HTML string for game banner
    """
    return textwrap.dedent("""
    <div class="game-banner">
        <h2>🚀 COMING SOON: My Little Me</h2>
        <p><strong>Stop feeding algorithms. Start feeding yourself.</strong></p>
        <p>The first Tamagotchi that grows based on your <strong>REAL</strong> actions. Read a book? Your character gets smarter. Went for a run? It gets stronger. Gamify your life.</p>
    </div>
    """)


def render_landing_header():
    """
    Returns HTML for the landing page header.
    
    Returns:
        str: HTML string for landing header
    """
    return textwrap.dedent("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1>TikTok Reality Check</h1>
        <p style="font-size: 1.2rem; color: rgba(255, 255, 255, 0.7); margin-top: 1rem;">
            Discover your scrolling persona and see what you could have accomplished instead
        </p>
    </div>
    """)


def render_title():
    """
    Returns HTML for the upload screen title.
    
    Returns:
        str: HTML string for title
    """
    return textwrap.dedent("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1>TikTok Reality Check</h1>
        <p style="font-size: 1.2rem; color: rgba(255, 255, 255, 0.7); margin-top: 1rem;">
            Discover how much time you've spent scrolling
        </p>
    </div>
    """)
