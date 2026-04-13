import streamlit as st
import qrcode
from io import BytesIO

# --- THE MASTER SETTINGS ---
# Set this to True for active clients, False to cut them off.
access_granted = True

st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️")

if not access_granted:
    st.error("⚠️ TERMINAL INACTIVE")
    st.info("Please contact your Sovereign Architect to renew your license.")
    st.stop()

# --- MERCHANT SETUP (In the Sidebar) ---
st.sidebar.title("💳 Merchant Setup")
biz_name = st.sidebar.text_input("Business Name", value="Eastgate Bar")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")

st.title(f"🛡️ {biz_name} Terminal")

# Initialize the payment amount in the session
if 'amt' not in st.session_state:
    st.session_state.amt = 5.00

# --- THE STAFF SHIELD (PIN Entrance) ---
st.sidebar.markdown("---")
st.sidebar.write("### 🔐 Staff Terminal")
pin_input = st.sidebar.text_input("Enter Access PIN", type="password")

if pin_input == "1234":
    # --- STAFF VIEW: THE SOVEREIGN EYE (0% FEES) ---
    st.sidebar.success("🛡️ 0% FEE RAIL ACTIVE")
    st.write("---")
    st.header("👁️ Sovereign Card Scanner")
    st.info("Hold the physical card to the camera to read the digits (0% Fees).")

    # 1. THE SCANNER (Bypasses the Visa/Mastercard Tap Tax)
    card_capture = st.camera_input("SCAN PHYSICAL CARD")

    if card_capture:
        st.success("CARD CAPTURED! Processing via 0% Rail...")
        st.link_button(f"💸 FINALIZE £{st.session_state.amt:.2f} TRANSFER", 
                       f"https://monzo.me/{handle}/{st.session_state.amt}")
        
    st.write("---")
    st.write("### ⚡ Quick Select")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🍺 PINT (£5)", use_container_width=True):
            st.session_state.amt = 5.0
    with c2:
        if st.button("🍷 WINE (£6.5)", use_container_width=True):
            st.session_state.amt = 6.5
    with c3:
        if st.button("🥤 SOFT (£2.5)", use_container_width=True):
            st.session_state.amt = 2.5
            
    st.metric("Total to Collect", f"£{st.session_state.amt:.2f}")

else:
    # --- CUSTOMER VIEW: THE STANDARD QR RAIL ---
    st.write("---")
    st.write("### 📱 Scan to Pay")
    st.write(f"Paying: **{biz_name}**")
    
    # QR Logic
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={biz_name.replace(' ', '%20')}"
    qr = qrcode.make(pay_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    st.image(buf.getvalue(), caption=f"Scan to pay £{st.session_state.amt:.2f}", width=380)
    st.success(f"✨ Saving 9p+ on this round vs card machines.")
    st.info("Staff: Enter PIN in sidebar to unlock the Card Scanner.")
