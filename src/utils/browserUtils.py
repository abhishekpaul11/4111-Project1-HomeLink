import streamlit as st
import streamlit.components.v1 as components


def set_local_storage(key, value):
    components.html(f"""
    <script>
        localStorage.setItem("{key}", "{value}");
    </script>
    """, height=0)

# Function to get a value from the browser's localStorage
def get_local_storage(key):
    return components.html(f"""
    <script>
        var value = localStorage.getItem("{key}");
        window.parent.postMessage({{"type": "return", "key": "{key}", "value": value}}, "*");
    </script>
    """, height=0)