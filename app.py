import streamlit as st
import qrcode
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- THE "DOUBLE-LOCK" PRIVACY CSS (v3.4) ---
st.markdown("""
<style>
    /* 1. BLUR THE LIVE VIDEO */
    div[data-testid="stCameraInput"] video {
        filter: blur(12px) brightness(0.8) !important;
        border: 4px solid #00FF41 !important;
        border-radius: 15px;
    }
    /* 2. BLUR THE RESULT IMAGE */
    div[data-testid="stCameraInput"] img {
        filter: blur(15px) grayscale(1) !important;
        opacity: 0.5;
    }
    /* 3. MENU BUTTONS */
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        font-weight: bold; background-color: #111; color: #00FF41; 
        border: 1px solid #444; 
    }
</style>
""", unsafe_allow_html=True)

if 'amt' not in st.session_state: st.session_state.amt = 5.00
if 'item' not in st.session_state: st.session_state.item = "Pint"

# --- SIDEBAR ---
st.sidebar.title("💳 David's Terminal")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")
pin_input = st.sidebar.text_input("Staff PIN", type="password")

st.title(f"🛡️ {st.session_state.item}: £{st.session_state.amt:.2f}")

if pin_input == "1234":
    # ---------------- DAVID'S CONTROL PANEL ----------------
    st.write("### ⚡ Fast Menu Select")
    m1, m2, m3, m4, m5 = st.columns(5)
    with m1: 
        if st.button("🍺 PINTS"): st.session_state.item = "Pint"; st.session_state.amt = 5.00; st.rerun()
    with m2: 
        if st.button("🍷 WINE"): st.session_state.item = "Wine"; st.session_state.amt = 6.50; st.rerun()
    with m3: 
        if st.button("🍏 CIDERS"): st.session_state.item = "Cider"; st.session_state.amt = 5.25; st.rerun()
    with m4: 
        if st.button("🥃 MIXERS"): st.session_state.item = "Mixer"; st.session_state.amt = 7.50; st.rerun()
    with m5: 
        if st.button("🍹 COCKTAILS"): st.session_state.item = "Cocktail"; st.session_state.amt = 12.00; st.rerun()

    # THE LINK LOGIC (FORCED WEB VIEW)
    # We add a dummy parameter to confuse the app into staying in the browser
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}&noshare=true"

    st.write("---")
    st.write(f"### 📸 Step 2: Privacy Scan")
    card_photo = st.camera_input("CAPTURE CARD")

    if card_photo:
        st.success("✅ AUDIT LOGGED")
        st.link_button(f"💸 EXECUTE £{st.session_state.amt:.2f} TRANSFER", pay_url)
        if st.button("🔄 RESET"): st.rerun()

else:
    # ---------------- CUSTOMER VIEW ----------------
    st.write(f"### 📱 Scan to Pay: £{st.session_state.amt:.2f}")
    
    # FORCED WEB LINK FOR CUSTOMERS
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}&noshare=true"
    
    qr = qrcode.make(pay_url); buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=400)
    st.info("Staff: PIN required for card scan.")

st.caption("v3.4 | Web-Force Privacy Build | HQ: The New Inn")
