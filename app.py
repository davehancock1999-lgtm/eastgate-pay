import streamlit as st
import qrcode
from io import BytesIO

st.set_page_config(page_title="Sovereign Rail Factory", page_icon="🛡️")

# --- SOVEREIGN CONTROL (The Kill-Switch) ---
st.sidebar.title("🔐 Admin Console")
is_active = st.sidebar.toggle("Subscription Active", value=True)

if not is_active:
    st.title("🚫 SYSTEM OFFLINE")
    st.error("Please contact David Hancock for subscription renewal.")
    st.stop()

# --- THE FACTORY INTERFACE ---
st.title("🛡️ Eastgate Sovereign Factory")
st.write("0% Fee Global FinTech Engine")

# Merchant Details
partner_name = st.text_input("Merchant Name", "Eastgate Bar")
partner_handle = st.text_input("Merchant Monzo Handle", "davidhancock62")
amount = st.number_input("Amount (£)", value=5.00)

if st.button("🏁 GENERATE LIVE RAIL"):
    # The 0% Fee Monzo Rail Logic
    live_url = f"https://monzo.me/{partner_handle}/{amount}?d={partner_name.replace(' ', '%20')}"
    
    # Generate the QR Code
    qr = qrcode.make(live_url)
    buf = BytesIO()
    qr.save(buf)
    
    # Deployment to the Frontline
    st.divider()
    st.image(buf.getvalue(), caption="BARMAN'S MASTER CARD")
    st.success(f"STATUS: ACTIVE. 0% Fees for {partner_name}")
    st.info(f"Direct Rail: {live_url}")
    
    st.warning("👉 Staff: Save this QR to your favorites for instant customer scanning.")