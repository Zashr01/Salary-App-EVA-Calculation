import streamlit as st
import pandas as pd

# Page Config for better Mobile/PC experience
st.set_page_config(
    page_title="Salary Calculation App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("💰 Salary App: EVA Calculation")

# Sidebar - Rates Configuration
st.sidebar.header("⚙️ Rates Configuration")
st.sidebar.info("Rates based on 'EVA - Salary Calculation' sheet")

# Exchange Rate
exchange_rate = st.sidebar.number_input("Exchange Rate (THB/Unit)", value=1.0, step=0.01)

st.sidebar.subheader("Hourly Rates (THB)")
# Defaults from Excel analysis
normal_rate = st.sidebar.number_input("Normal Rate", value=120.0, step=1.0)
ot_rate = st.sidebar.number_input("OT Rate (Hour 71-80)", value=300.0, step=1.0) # 2.5x
super_ot_rate = st.sidebar.number_input("Super OT Rate (Hour >80)", value=420.0, step=1.0) # 3.5x

st.sidebar.markdown("---")
st.sidebar.subheader("💸 Per Diem Conversion Logic")

# Step 1: Withdraw
st.sidebar.caption("Step 1: Withdrawal (Taiwan)")
per_diem_euro_mult = st.sidebar.number_input("Per Diem Multiplier (EUR/AME/AUS)", value=4.0, step=0.1) # C27
per_diem_other_mult = st.sidebar.number_input("Per Diem Multiplier (Other)", value=3.5, step=0.1) # C28

withdrawal_currency = st.sidebar.radio("Withdraw Per Diem As:", ["USD", "TWD"])

cathay_rate = 1.0
if withdrawal_currency == "TWD":
    st.sidebar.markdown("""<a href="https://www.cathaybk.com.tw/cathaybk/personal/product/deposit/currency-billboard/" target="_blank"> Check Cathay United Bank Rate (USD -> TWD)</a>""", unsafe_allow_html=True)
    cathay_rate = st.sidebar.number_input("Cathay Rate (USD to TWD)", value=31.6, step=0.1)

# Step 2: Exchange
st.sidebar.caption("Step 2: Exchange (Thailand)")
st.sidebar.markdown("""<a href="https://www.superrichthailand.com/#!/en/exchange#rate-section" target="_blank"> Check SuperRich Thailand Rate (Central Ladprao)</a>""", unsafe_allow_html=True)

if withdrawal_currency == "USD":
    superrich_rate = st.sidebar.number_input("SuperRich Rate (USD -> THB)", value=34.0, step=0.1)
else:
    superrich_rate = st.sidebar.number_input("SuperRich Rate (TWD -> THB)", value=1.05, step=0.01)

st.sidebar.subheader("Transportation")
transport_rate = st.sidebar.number_input("Transport Rate per Trip", value=700.0, step=50.0) # C35

# Main Inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏱️ Block Hours")
    bh_hours = st.number_input("Block Hours (Hours)", value=89, step=1, min_value=0)
    bh_mins = st.number_input("Block Hours (Minutes)", value=38, step=1, max_value=59, min_value=0)
    
    st.subheader("🌍 Per Diem")
    p1_hours = st.number_input("Per Diem (EUR/AME/AUS) Hours", value=175, step=1, min_value=0)
    p1_mins = st.number_input("Per Diem (EUR/AME/AUS) Minutes", value=43, step=1, max_value=59, min_value=0)
    
    p2_hours = st.number_input("Per Diem (Other regions) Hours", value=158, step=1, min_value=0)
    p2_mins = st.number_input("Per Diem (Other regions) Minutes", value=37, step=1, max_value=59, min_value=0)

with col2:
    st.subheader("💵 Salary & Other")
    base_salary = st.number_input("Base Salary", value=16000.0, step=100.0)
    position_allowance = st.number_input("Position Allowance", value=1000.0, step=100.0)
    transport_trips = st.number_input("Transportation (Trips)", value=6, step=1, min_value=0)

# Calculations
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
if withdrawal_currency == "TWD":
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

# Display Results
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

