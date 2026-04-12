import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="Eastgate Sovereign Terminal", page_icon="🛡️")

# --- SIDEBAR: MERCHANT SETUP ---
st.sidebar.title("🏢 Merchant Setup")
biz_name = st.sidebar.text_input("Business Name", value="Eastgate Bar")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")
fee_leech = 0.0175 # 1.75% standard fee

# --- APP INTERFACE ---
st.title(f"🛡️ {biz_name} Terminal")

if 'amt' not in st.session_state: 
    st.session_state.amt = 5.00

# --- THE SPEED RAIL (CATEGORIES) ---
st.write("### ⚡ Quick Select")

# Row 1: Pints & Ciders
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🍺 Standard Pint (£5.00)"): st.session_state.amt = 5.00
with col2:
    if st.button("🍎 Cider/Premium (£5.60)"): st.session_state.amt = 5.60
with col3:
    if st.button("🥤 Soft Drink (£2.50)"): st.session_state.amt = 2.50

# Row 2: Spirits & Cocktails
col4, col5, col6 = st.columns(3)
with col4:
    if st.button("🥃 Single + Mixer (£6.50)"): st.session_state.amt = 6.50
with col5:
    if st.button("🍹 Double + Mixer (£8.50)"): st.session_state.amt = 8.50
with col6:
    if st.button("🍸 Cocktail (£10.00)"): st.session_state.amt = 10.00

# Manual entry for anything else (e.g., a specific bottle of wine)
amount = st.number_input("Final Amount to Charge (£)", min_value=1.00, step=0.05, value=st.session_state.amt)

# --- THE PITCH ---
saved = amount * fee_leech
st.success(f"✨ Gaffer: You are keeping **£{saved:.2f}** more on this round.")

# --- DYNAMIC QR GENERATION ---
# The URL includes the Business Name as the reference so the Gaffer knows what the payment is for.
pay_url = f"https://monzo.me/{handle}/{amount}?d={biz_name.replace(' ', '%20')}"
qr = qrcode.make(pay_url)
buf = BytesIO()
qr.save(buf, format="PNG")

st.write("---")
st.image(buf, caption=f"Customer Scan: £{amount:.2f}", width=380)

st.info(f"Connected to: {handle}")
st.warning("💳 For Physical Cards: Use 'Tap to Pay' in Monzo App.")
