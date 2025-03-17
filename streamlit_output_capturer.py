import sys
from io import StringIO
import streamlit as st

class StreamlitOutputCapturer:
    def __init__(self, placeholder, max_lines=50):
        self.placeholder = placeholder
        self.max_lines = max_lines
        self.buffer = []
        self.original_stdout = sys.stdout
        
    def write(self, text):
        # Capture output and update placeholder
        self.buffer.append(text)
        if len(self.buffer) > self.max_lines:
            self.buffer.pop(0)
        self.placeholder.code('\n'.join(self.buffer))
        
    def flush(self):
        pass  # Required for compatibility

