"""HTML generation functions for the TikTok Reality Check app."""

import textwrap


def render_metrics(stats):
    """
    Returns HTML string for the top 3 square metric cards.
    
    Args:
        stats (dict): Dictionary with total_videos, total_hours, total_days
        
    Returns:
        str: HTML string for metrics
    """
    html = '<div class="stats-row">'
    html += f'<div class="stat-card"><div class="stat-value">{stats["total_videos"]:,}</div><div class="stat-label">Total Videos</div></div>'
    html += f'<div class="stat-card"><div class="stat-value">{round(stats["total_hours"], 1):,}</div><div class="stat-label">Hours Wasted</div></div>'
    html += f'<div class="stat-card"><div class="stat-value">{round(stats["total_days"], 2):,}</div><div class="stat-label">Days Lost</div></div>'
    html += '</div>'
    return html


def render_slider(items):
    """
    Returns HTML string for the horizontal slider.
    
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
    
    html = '<div class="scroll-container">'
    for item in items:
        html += f'<div class="scroll-card"><div class="icon">{item["icon"]}</div><div class="title">{item["text"]}</div></div>'
    html += '</div>'
    return html


def render_persona(persona):
    """
    Returns HTML for the persona glass card.
    
    Args:
        persona (dict): Dictionary with title and desc keys
        
    Returns:
        str: HTML string for persona card
    """
    return textwrap.dedent(f"""
    <div class="glass-card">
        <div class="persona-title">{persona['title']}</div>
        <div class="persona-message">{persona['desc']}</div>
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


def render_header():
    """
    Returns HTML for the main header.
    
    Returns:
        str: HTML string for header
    """
    return textwrap.dedent("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2>YOUR STATS</h2>
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

