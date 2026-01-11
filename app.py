import streamlit as st
import pandas as pd
import json
import os

# --- Constants & Configuration ---
DATA_FILE = "devices_config.json"
DEFAULT_DEVICE_NAME = "My Device"

# Default values for a new device
DEFAULT_VALUES = {
    "exchange_rate": 1.0,
    "normal_rate": 120.0,
    "ot_rate": 300.0,
    "super_ot_rate": 420.0,
    "per_diem_euro_mult": 4.0,
    "per_diem_other_mult": 3.5,
    "withdrawal_currency": "USD",
    "cathay_rate": 31.6,
    "superrich_rate_usd": 34.0,
    "superrich_rate_twd": 1.05,
    "transport_rate": 700.0,
    "bh_hours": 89,
    "bh_mins": 38,
    "p1_hours": 175,
    "p1_mins": 43,
    "p2_hours": 158,
    "p2_mins": 37,
    "base_salary": 16000.0,
    "position_allowance": 1000.0,
    "transport_trips": 6
}

# --- Helper Functions ---

def load_all_data():
    """Load all devices data from JSON file."""
    if not os.path.exists(DATA_FILE):
        return {DEFAULT_DEVICE_NAME: DEFAULT_VALUES.copy()}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {DEFAULT_DEVICE_NAME: DEFAULT_VALUES.copy()}

def save_all_data(data):
    """Save all devices data to JSON file."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def update_current_device_data():
    """Update the current device's data in the global data dict from session state."""
    current_device = st.session_state.get("selected_device_name", DEFAULT_DEVICE_NAME)
    
    # Ensure data dict exists in session state
    if "all_data" not in st.session_state:
        st.session_state.all_data = load_all_data()
    
    # Initialize device entry if missing
    if current_device not in st.session_state.all_data:
        st.session_state.all_data[current_device] = DEFAULT_VALUES.copy()
        
    # Update values from widgets
    # We iterate over DEFAULT_VALUES keys to know what to save
    for key in DEFAULT_VALUES.keys():
        if key in st.session_state:
            st.session_state.all_data[current_device][key] = st.session_state[key]
            
    save_all_data(st.session_state.all_data)

def load_device_to_state():
    """Load the selected device's data into session state widgets."""
    current_device = st.session_state.get("selected_device_name")
    
    if "all_data" not in st.session_state:
        st.session_state.all_data = load_all_data()
        
    # If device not in data (newly added), create it
    if current_device and current_device not in st.session_state.all_data:
        st.session_state.all_data[current_device] = DEFAULT_VALUES.copy()
    
    device_data = st.session_state.all_data.get(current_device, DEFAULT_VALUES.copy())
    
    # Update session state keys for widgets
    for key, val in device_data.items():
        st.session_state[key] = val

def on_input_change():
    """Callback when any input changes."""
    update_current_device_data()

# --- Page Config ---
st.set_page_config(
    page_title="Salary Calculation App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 Salary App: EVA Calculation")

# --- Initialization ---
if "all_data" not in st.session_state:
    st.session_state.all_data = load_all_data()

# Handle Query Params for Auto-Login
# Check if 'device' param exists and is valid
query_params = st.query_params
initial_device = query_params.get("device", None)

if initial_device and initial_device in st.session_state.all_data:
    if "selected_device_name" not in st.session_state:
        st.session_state.selected_device_name = initial_device

# Get list of devices
device_list = list(st.session_state.all_data.keys())

# --- Sidebar: Device Management ---
st.sidebar.header("📱 Device Management")

# Select Device
# We use a placeholder for the selector to allow adding new devices to update the list
device_placeholder = st.sidebar.empty()

# Add New Device
with st.sidebar.expander("➕ Add New Device"):
    new_device_name = st.text_input("New Device Name")
    if st.button("Create Device"):
        if new_device_name and new_device_name not in st.session_state.all_data:
            st.session_state.all_data[new_device_name] = DEFAULT_VALUES.copy()
            save_all_data(st.session_state.all_data)
            # Force reload to get new device in list
            st.rerun()
        elif new_device_name in st.session_state.all_data:
            st.error("Device already exists!")

# Update device list after potential addition
device_list = list(st.session_state.all_data.keys())

# Select Box Logic
# If state has no selected device, default to first available
if "selected_device_name" not in st.session_state:
    if device_list:
        st.session_state.selected_device_name = device_list[0]
    else:
        st.session_state.selected_device_name = DEFAULT_DEVICE_NAME

# If the selected device in state is not in the list (deleted?), reset
if st.session_state.selected_device_name not in device_list:
     st.session_state.selected_device_name = device_list[0] if device_list else DEFAULT_DEVICE_NAME

def on_device_change():
    """Callback when device selection changes."""
    # Update Query Param
    st.query_params["device"] = st.session_state.selected_device_name
    load_device_to_state()

# The actual selectbox
selected_device = device_placeholder.selectbox(
    "Select Device Profile",
    options=device_list,
    key="selected_device_name",
    on_change=on_device_change
)

# Ensure session state is populated for the current device on first run
# We check if a specific key exists, if not, we load
if "exchange_rate" not in st.session_state:
    load_device_to_state()
    # Also ensure query param is set on first load if missing
    if "device" not in st.query_params:
         st.query_params["device"] = st.session_state.selected_device_name

# --- Sidebar: Rates Configuration ---
st.sidebar.header("⚙️ Rates Configuration")
st.sidebar.info("Rates based on 'EVA - Salary Calculation' sheet")

# Exchange Rate
st.sidebar.number_input("Exchange Rate (THB/Unit)", step=0.01, key="exchange_rate", on_change=on_input_change)

st.sidebar.subheader("Hourly Rates (THB)")
# Defaults from Excel analysis
st.sidebar.number_input("Normal Rate", step=1.0, key="normal_rate", on_change=on_input_change)
st.sidebar.number_input("OT Rate (Hour 71-80)", step=1.0, key="ot_rate", on_change=on_input_change) # 2.5x
st.sidebar.number_input("Super OT Rate (Hour >80)", step=1.0, key="super_ot_rate", on_change=on_input_change) # 3.5x

st.sidebar.markdown("---")
st.sidebar.subheader("💸 Per Diem Conversion Logic")

# Step 1: Withdraw
st.sidebar.caption("Step 1: Withdrawal (Taiwan)")
st.sidebar.number_input("Per Diem Multiplier (EUR/AME/AUS)", step=0.1, key="per_diem_euro_mult", on_change=on_input_change) # C27
st.sidebar.number_input("Per Diem Multiplier (Other)", step=0.1, key="per_diem_other_mult", on_change=on_input_change) # C28

st.sidebar.radio("Withdraw Per Diem As:", ["USD", "TWD"], key="withdrawal_currency", on_change=on_input_change)

cathay_rate = 1.0
if st.session_state.withdrawal_currency == "TWD":
    st.sidebar.markdown("""<a href="https://www.cathaybk.com.tw/cathaybk/personal/product/deposit/currency-billboard/" target="_blank"> Check Cathay United Bank Rate (USD -> TWD)</a>""", unsafe_allow_html=True)
    st.sidebar.number_input("Cathay Rate (USD to TWD)", step=0.1, key="cathay_rate", on_change=on_input_change)
    cathay_rate = st.session_state.cathay_rate

# Step 2: Exchange
st.sidebar.caption("Step 2: Exchange (Thailand)")
st.sidebar.markdown("""<a href="https://www.superrichthailand.com/#!/en/exchange#rate-section" target="_blank"> Check SuperRich Thailand Rate (Central Ladprao)</a>""", unsafe_allow_html=True)

if st.session_state.withdrawal_currency == "USD":
    st.sidebar.number_input("SuperRich Rate (USD -> THB)", step=0.1, key="superrich_rate_usd", on_change=on_input_change)
    superrich_rate = st.session_state.superrich_rate_usd
else:
    st.sidebar.number_input("SuperRich Rate (TWD -> THB)", step=0.01, key="superrich_rate_twd", on_change=on_input_change)
    superrich_rate = st.session_state.superrich_rate_twd

st.sidebar.subheader("Transportation")
st.sidebar.number_input("Transport Rate per Trip", step=50.0, key="transport_rate", on_change=on_input_change) # C35

# --- Main Inputs ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Block Hours")
    st.number_input("Block Hours (Hours)", step=1, min_value=0, key="bh_hours", on_change=on_input_change)
    st.number_input("Block Hours (Minutes)", step=1, max_value=59, min_value=0, key="bh_mins", on_change=on_input_change)
    
    st.subheader("🌍 Per Diem")
    st.number_input("Per Diem (EUR/AME/AUS) Hours", step=1, min_value=0, key="p1_hours", on_change=on_input_change)
    st.number_input("Per Diem (EUR/AME/AUS) Minutes", step=1, max_value=59, min_value=0, key="p1_mins", on_change=on_input_change)
    
    st.number_input("Per Diem (Other regions) Hours", step=1, min_value=0, key="p2_hours", on_change=on_input_change)
    st.number_input("Per Diem (Other regions) Minutes", step=1, max_value=59, min_value=0, key="p2_mins", on_change=on_input_change)

with col2:
    st.subheader("💵 Salary & Other")
    st.number_input("Base Salary", step=100.0, key="base_salary", on_change=on_input_change)
    st.number_input("Position Allowance", step=100.0, key="position_allowance", on_change=on_input_change)
    st.number_input("Transportation (Trips)", step=1, min_value=0, key="transport_trips", on_change=on_input_change)

# --- Calculations ---
# Extract values from session state for clarity in formula
bh_hours = st.session_state.bh_hours
bh_mins = st.session_state.bh_mins
normal_rate = st.session_state.normal_rate
ot_rate = st.session_state.ot_rate
super_ot_rate = st.session_state.super_ot_rate
p1_hours = st.session_state.p1_hours
p1_mins = st.session_state.p1_mins
p2_hours = st.session_state.p2_hours
p2_mins = st.session_state.p2_mins
per_diem_euro_mult = st.session_state.per_diem_euro_mult
per_diem_other_mult = st.session_state.per_diem_other_mult
base_salary = st.session_state.base_salary
position_allowance = st.session_state.position_allowance
transport_trips = st.session_state.transport_trips
transport_rate = st.session_state.transport_rate

# 1. Block Hour Income
total_bh = bh_hours + (bh_mins / 60.0)
bh_normal_hrs = min(total_bh, 70)
bh_ot_hrs = max(min(total_bh - 70, 10), 0)
bh_super_ot_hrs = max(total_bh - 80, 0)

income_normal = bh_normal_hrs * normal_rate
income_ot = bh_ot_hrs * ot_rate
income_super_ot = bh_super_ot_hrs * super_ot_rate
total_bh_income = income_normal + income_ot + income_super_ot

# 2. Per Diem Income logic
# Base (USD)
p1_total = p1_hours + (p1_mins / 60.0)
p2_total = p2_hours + (p2_mins / 60.0)
total_per_diem_units = (per_diem_euro_mult * p1_total) + (per_diem_other_mult * p2_total)
per_diem_base_usd = total_per_diem_units

# Step 1: Withdraw
if st.session_state.withdrawal_currency == "TWD":
    holding_amount = per_diem_base_usd * cathay_rate
    holding_currency = "TWD"
    step1_trace = f"{per_diem_base_usd:,.2f} USD * {cathay_rate} (Cathay) = {holding_amount:,.2f} TWD"
else:
    holding_amount = per_diem_base_usd
    holding_currency = "USD"
    step1_trace = f"{per_diem_base_usd:,.2f} USD (No conversion)"

# Step 2: Exchange to THB
per_diem_thb = holding_amount * superrich_rate
step2_trace = f"{holding_amount:,.2f} {holding_currency} * {superrich_rate} (SuperRich) = {per_diem_thb:,.2f} THB"

# 4. Other
transport_income = transport_trips * transport_rate

# Total
grand_total_thb = total_bh_income + per_diem_thb + base_salary + position_allowance + transport_income

# --- Display Results ---
st.divider()
st.header("📊 Result Summary")

metric_col1, metric_col2, metric_col3 = st.columns(3)

metric_col1.metric("Total Monthly Income (THB)", f"{grand_total_thb:,.2f} THB")
metric_col2.metric("Per Diem Income (Converted)", f"{per_diem_thb:,.2f} THB")
metric_col3.metric("Withdrawal Amount", f"{holding_amount:,.2f} {holding_currency}")

st.subheader("Detailed Breakdown")
breakdown_data = {
    "Category": [
        "Block Hour (Normal 0-70h)", 
        "Block Hour (OT 71-80h)",
        "Block Hour (Super OT >80h)",
        "Per Diem Base (USD)",
        "Step 1: Withdrawal",
        "Step 2: Exchange (THB)",
        "Base Salary",
        "Position Allowance",
        "Transportation"
    ],
    "Details": [
        f"{bh_normal_hrs:.2f} hrs @ {normal_rate} THB",
        f"{bh_ot_hrs:.2f} hrs @ {ot_rate} THB",
        f"{bh_super_ot_hrs:.2f} hrs @ {super_ot_rate} THB",
        f"{p1_total:.2f}hrs*4 + {p2_total:.2f}hrs*3.5",
        step1_trace,
        step2_trace,
        "Flat Rate",
        "Flat Rate",
        f"{transport_trips} trips @ {transport_rate} THB"
    ],
    "Amount": [
        f"{income_normal:,.2f} THB",
        f"{income_ot:,.2f} THB",
        f"{income_super_ot:,.2f} THB",
        f"{per_diem_base_usd:,.2f} USD",
        f"{holding_amount:,.2f} {holding_currency}",
        f"{per_diem_thb:,.2f} THB",
        f"{base_salary:,.2f} THB",
        f"{position_allowance:,.2f} THB",
        f"{transport_income:,.2f} THB"
    ]
}

df_breakdown = pd.DataFrame(breakdown_data)
st.table(df_breakdown)
