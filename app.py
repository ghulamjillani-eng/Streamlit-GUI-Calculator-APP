import streamlit as st
import math

# --- Session State Initialization ---
# 'expression' stores the string being typed (e.g., "12+3*5")
# 'result' stores the outcome of the last calculation or "Error"
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'result' not in st.session_state:
    st.session_state.result = "0"

# --- Calculator Logic Functions ---

def press(symbol):
    """Appends a symbol (number or operator) to the current expression."""
    # If the last action was a calculation, clear the expression before adding a new symbol
    if st.session_state.result not in ["0", "Error"] and st.session_state.expression == "":
        st.session_state.expression = str(st.session_state.result)
        st.session_state.result = "0"

    # Prevent leading operators unless the expression is empty (allowing negative numbers)
    if not st.session_state.expression and symbol in ('*', '/'):
        return

    # Replace last operator if a new one is pressed immediately after
    operators = ('+', '-', '*', '/')
    if st.session_state.expression and st.session_state.expression[-1] in operators and symbol in operators:
        st.session_state.expression = st.session_state.expression[:-1] + symbol
    else:
        st.session_state.expression += str(symbol)

def calculate():
    """Evaluates the current expression and updates the result."""
    try:
        # Use str(st.session_state.expression) to ensure it's a string
        # Replace the custom exponentiation symbol (^) with Python's (**)
        expr = st.session_state.expression.replace('^', '**')

        # Use the built-in eval function for calculation
        final_result = str(eval(expr))
        st.session_state.result = final_result
        st.session_state.expression = "" # Clear expression after successful calculation

    except ZeroDivisionError:
        st.session_state.result = "Error: Division by zero"
        st.session_state.expression = ""
    except Exception:
        st.session_state.result = "Error: Invalid input"
        st.session_state.expression = ""

def clear_all():
    """Resets the expression and result."""
    st.session_state.expression = ""
    st.session_state.result = "0"

def delete_last():
    """Removes the last character from the expression."""
    st.session_state.expression = st.session_state.expression[:-1]

# --- Streamlit UI Layout ---

st.set_page_config(layout="wide", page_title="Streamlit Calculator")

st.markdown(
    """
    <style>
    .big-font {
        font-size: 3rem !important;
        text-align: right;
        padding-right: 15px;
        color: #f0f0f0;
        background-color: #262730;
        border-radius: 8px;
        margin-bottom: 5px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    .small-font {
        font-size: 1.5rem !important;
        text-align: right;
        padding-right: 15px;
        color: #999999;
        height: 30px;
        display: flex;
        align-items: center;
        justify-content: flex-end;
    }
    .stButton>button {
        width: 100%;
        height: 80px;
        font-size: 1.5rem;
        border-radius: 12px;
        transition: all 0.2s;
    }
    .operator-button button {
        background-color: #ff9500;
        color: white;
    }
    .equals-button button {
        background-color: #007aff;
        color: white;
    }
    .clear-button button, .delete-button button {
        background-color: #5856d6;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🔢 Streamlit Calculator")

# --- Display Area ---

# Result display (smaller text)
st.markdown(f'<div class="small-font">{st.session_state.result}</div>', unsafe_allow_html=True)

# Current expression display (main, larger text)
display_text = st.session_state.expression if st.session_state.expression else st.session_state.result
if display_text == "0" and st.session_state.result != "0":
    display_text = st.session_state.result # Show result clearly if expression is empty

st.markdown(f'<div class="big-font">{display_text}</div>', unsafe_allow_html=True)


# --- Button Layout (4x5 Grid) ---

buttons = [
    ('C', 'clear-button', clear_all), ('Del', 'delete-button', delete_last), ('^', 'operator-button', lambda: press('^')), ('/', 'operator-button', lambda: press('/')),
    ('7', '', lambda: press('7')), ('8', '', lambda: press('8')), ('9', '', lambda: press('9')), ('*', 'operator-button', lambda: press('*')),
    ('4', '', lambda: press('4')), ('5', '', lambda: press('5')), ('6', '', lambda: press('6')), ('-', 'operator-button', lambda: press('-')),
    ('1', '', lambda: press('1')), ('2', '', lambda: press('2')), ('3', '', lambda: press('3')), ('+', 'operator-button', lambda: press('+')),
    ('0', '', lambda: press('0')), ('.', '', lambda: press('.')), ('=', 'equals-button', calculate),
]

# Create the 4-column layout
col1, col2, col3, col4 = st.columns(4)
cols = [col1, col2, col3, col4]

for i, (symbol, class_name, action) in enumerate(buttons):
    col = cols[i % 4]

    # Special handling for the last row to make '=' button span two columns
    if i == len(buttons) - 1: # Last button is '='
        # '=' takes the remaining space, using col3 and col4
        st.columns([1, 1, 2])[2].button(symbol, key=symbol, on_click=action, help=f"Class: {class_name}", disabled=(symbol in ('^', '/', '*', '+', '-') and not st.session_state.expression))
        break # Exit loop after placing '='

    with col:
        # Create the button with the appropriate style and action
        st.button(
            symbol,
            key=symbol,
            on_click=action,
            help=f"Class: {class_name}",
            # Use custom CSS class for styling
            # Note: Streamlit's class application is limited, using key to help target via CSS
        )

# A small section to provide guidance on running the app
st.markdown(
    """
    ---
    **How to run this app:**
    1. Save the code above as `app.py` and the dependency list as `requirements.txt`.
    2. Open your terminal in the same directory.
    3. Install dependencies: `pip install -r requirements.txt`
    4. Run the app: `streamlit run app.py`
    """
)

