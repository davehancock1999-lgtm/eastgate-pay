import streamlit as st
import qrcode
from io import BytesIO

# --- SOVEREIGN CONFIGURATION ---
BUSINESS_NAME = "Eastgate Bar"
MONZO_HANDLE = "davidhancock62"  # Change this if the Gaffer's handle is different
FEE_PERCENTAGE = 0.0175  # The 1.75% "Leech" Tax

st.set_page_config(page_title="Eastgate Sovereign Terminal", page_icon="🛡️")

# --- SIDEBAR ADMIN ---
st.sidebar.title("🔐 Admin Console")
is_active = st.sidebar.toggle("System Live", value=True)

if not is_active:
    st.title("🚫 SYSTEM OFFLINE")
    st.error("Please contact David Hancock for system access.")
    st.stop()

st.title("🛡️ Eastgate Sovereign Terminal")
st.subheader("0% Fee Universal Rail")

# --- PHASE 2: PRESET BUTTONS (THE SPEED RAIL) ---
st.write("### 🍺 Quick Tap Menu")
col1, col2, col3 = st.columns(3)

# Initialize session state for amount
if 'amt' not in st.session_state:
    st.session_state.amt = 5.00

with col1:
    if st.button("Pint (£5.00)"):
        st.session_state.amt = 5.00
with col2:
    if st.button("Double (£8.50)"):
        st.session_state.amt = 8.50
with col3:
    if st.button("Round (£20.00)"):
        st.session_state.amt = 20.00

# --- MANUAL INPUT ---
amount = st.number_input("Enter Custom Amount (£)", min_value=0.01, step=0.10, value=st.session_state.amt)

# --- THE CALCULATOR OF FREEDOM ---
saved_fee = amount * FEE_PERCENTAGE
st.success(f"✨ **Leech-Free Transaction:** You are saving **£{saved_fee:.2f}** in bank fees on this order.")

# --- GENERATE THE UNIVERSAL RAIL ---
payment_url = f"https://monzo.me/{MONZO_HANDLE}/{amount}?d={BUSINESS_NAME.replace(' ', '%20')}"

st.write("---")
st.write("### ⚡ UNIVERSAL SCAN POINT")
st.write("*(Works for iPhone, Android, and Digital Wallets)*")

# Generate QR
qr = qrcode.make(payment_url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.image(buf, caption=f"Scan to pay £{amount} to {BUSINESS_NAME}", width=300)

# --- THE PHYSICAL CARD BRIDGE ---
st.write("---")
st.write("### 💳 PHYSICAL PLASTIC CARD?")
st.warning("To accept a physical card with 0% fees, open your **Monzo Business App** and select **'Tap to Pay on iPhone'**.")

st.markdown(f"[🔗 Direct Payment Link](sslocal://flow/file_open?url=%7Bpayment_url%7D&flow_extra=eyJsaW5rX3R5cGUiOiJjb2RlX2ludGVycHJldGVyIn0=)")
