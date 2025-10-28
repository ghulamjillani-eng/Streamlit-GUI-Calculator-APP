import streamlit as st

st.set_page_config(page_title="GUI Calculator", page_icon="🧮", layout="centered")

st.markdown("<h1 style='text-align:center;'>🧮 GUI Calculator</h1>", unsafe_allow_html=True)

# Initialize session state for display
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Function to handle button press
def press(button):
    if button == "C":
        st.session_state.expression = ""
    elif button == "⌫":
        st.session_state.expression = st.session_state.expression[:-1]
    elif button == "=":
        try:
            # Evaluate the expression safely
            st.session_state.expression = str(eval(st.session_state.expression))
        except Exception:
            st.session_state.expression = "Error"
    else:
        st.session_state.expression += button

# Display area
st.text_input("Display", st.session_state.expression, key="display", disabled=True)

# Buttons layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
    ["C", "⌫"]
]

# Create button grid
for row in buttons:
    cols = st.columns(len(row))
    for i, button in enumerate(row):
        if cols[i].button(button):
            press(button)

st.markdown("---")
st.caption("Made with ❤️ using Streamlit")
