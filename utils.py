"""Utility functions for the TikTok Reality Check app."""

import streamlit as st
import textwrap


def load_css(file_name):
    """
    Reads CSS file and injects it via st.markdown.
    
    Args:
        file_name (str): Path to the CSS file
        
    Returns:
        None
    """
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS file {file_name} not found. Using default styles.")
    except Exception as e:
        st.error(f"Error loading CSS: {str(e)}")


# JavaScript code to enable "Click & Drag" scrolling for .scroll-container
DRAG_JS = textwrap.dedent("""
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

