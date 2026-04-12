import streamlit as st
import qrcode
from io import BytesIO

# --- THE MASTER KILL-SWITCH ---
# Set this to True for active clients, False to cut them off.
access_granted = True 

st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️")

if not access_granted:
    st.error("⚠️ TERMINAL INACTIVE")
    st.info("Please contact your Sovereign Architect to renew your license.")
    st.stop() # This stops the rest of the app from loading.

# --- REST OF THE CODE (Only runs if access_granted is True) ---
st.sidebar.title("🏢 Merchant Setup")
biz_name = st.sidebar.text_input("Business Name", value="Eastgate Bar")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")

st.title(f"🛡️ {biz_name} Terminal")

if 'amt' not in st.session_state: st.session_state.amt = 5.00

st.write("### ⚡ Quick Select")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🍺 Pint (£5.00)"): st.session_state.amt = 5.00
with col2:
    if st.button("🍎 Cider (£5.60)"): st.session_state.amt = 5.60
with col3:
    if st.button("🥤 Soft (£2.50)"): st.session_state.amt = 2.50

amount = st.number_input("Final Amount (£)", min_value=1.00, value=st.session_state.amt)

# QR Logic
pay_url = f"https://monzo.me/{handle}/{amount}?d={biz_name.replace(' ', '%20')}"
qr = qrcode.make(pay_url)
buf = BytesIO()
qr.save(buf, format="PNG")

st.write("---")
st.image(buf, caption=f"Scan to pay £{amount:.2f}", width=380)
st.success(f"✨ Saving 9p+ on this round.")

# --- THE SOVEREIGN SHIELD (Staff Access) ---
st.sidebar.markdown("---")
st.sidebar.write("### 🔐 Staff Terminal")
pin_input = st.sidebar.text_input("Enter Access PIN", type="password")

if pin_input == "1234":
    st.sidebar.success("Terminal Unlocked 🛡️")
    # This is where we show the "Hidden" Tap button for the barmaid
    st.write("---")
    if st.button("💳 TRIGGER PHYSICAL CARD TAP", use_container_width=True):
        st.balloons()
        st.info(f"READY: Customer should tap their card for £{st.session_state.amt:.2f}")
elif pin_input != "":
    st.sidebar.error("Access Denied 🚫")
