"""Utility functions for the TikTok Reality Check app."""

import streamlit as st


def load_css(file_name="styles.css"):
    """
    Reads CSS file and injects it via st.markdown.
    
    Args:
        file_name (str): Path to the CSS file (default: "styles.css")
        
    Returns:
        None
    """
    try:
        with open(file_name) as f:
            data = f.read()
            st.markdown(f'<style>{data}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file {file_name} not found. Using default styles.")
    except Exception as e:
        st.error(f"Error loading CSS: {str(e)}")


def inject_custom_js():
    """
    Returns JavaScript string to enable "Click & Drag" scrolling for .scroll-container.
    
    Returns:
        str: JavaScript code wrapped in <script> tags
    """
    return """
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
"""
