"""
UI Utility Functions for RAG-SQL Assistant

This module provides utility functions for UI components.
"""

import streamlit as st
import time
import random
from typing import List

def stream_text_with_cursor(text: str):
    """
    Stream text with a red cursor effect.
    
    Args:
        text: The text to stream
    """
    # Create a placeholder for the streaming text
    placeholder = st.empty()
    
    # Split the text into words
    words = text.split()
    displayed_text = ""
    
    # Stream each word with a random delay
    for i, word in enumerate(words):
        # Add the word to the displayed text
        displayed_text += word + " "
        
        # Display text with red cursor
        placeholder.markdown(f"{displayed_text}**<span style='color:red; font-size:1.25em; font-weight:bold;'>|</span>**", unsafe_allow_html=True)
        
        # Small random delay between words (0.01 to 0.05 seconds)
        time.sleep(random.uniform(0.02, 0.1))
    
    # Final text without cursor
    placeholder.markdown(displayed_text)
    
    return displayed_text