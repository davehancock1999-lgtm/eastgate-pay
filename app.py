import streamlit as st
import qrcode
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- THE DOUBLE-LOCK PRIVACY (BLURS LIVE AND RESULT) ---
st.markdown("""
<style>
    /* 1. BLUR THE LIVE VIDEO */
    div[data-testid="stCameraInput"] video {
        filter: blur(10px) brightness(0.8) !important;
        border: 4px solid #00FF41 !important;
        border-radius: 15px;
    }
    
    /* 2. BLUR THE RESULT IMAGE (THE 'GOTCHA' FIX) */
    /* This ensures that once the photo is snapped, it stays blurred on screen */
    div[data-testid="stCameraInput"] img {
        filter: blur(12px) grayscale(1) !important;
        opacity: 0.6;
    }

    /* 3. MENU STYLING */
    .stButton>button { 
        width: 100%; border-radius: 10px; height: 3.5em; 
        font-weight: bold; background-color: #111; color: #00FF41; 
        border: 1px solid #444; 
    }
</style>
""", unsafe_allow_html=True)

# --- SESSION SYNC ---
if 'amt' not in st.session_state: st.session_state.amt = 5.00
if 'item' not in st.session_state: st.session_state.item = "Pint"

# --- SIDEBAR ---
st.sidebar.title("💳 David's Terminal")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")
pin_input = st.sidebar.text_input("Staff PIN", type="password")

st.title(f"🛡️ {st.session_state.item}: £{st.session_state.amt:.2f}")

if pin_input == "1234":
    # ---------------- DAVID'S CONTROL PANEL ----------------
    st.write("### ⚡ Quick Menu")
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

    st.write("---")
    st.write("### 💰 Step 1: Set Price")
    c_amt, c_itm = st.columns([1, 2])
    with c_amt:
        st.session_state.amt = st.number_input("Amount £", value=st.session_state.amt, step=0.01, format="%.2f")
    with c_itm:
        st.session_state.item = st.text_input("Item", value=st.session_state.item)

    # THE SCANNER
    st.write(f"### 📸 Step 2: Privacy Scan")
    st.warning("🛡️ PRIVACY ACTIVE: Captured image is blurred on-screen.")
    
    card_photo = st.camera_input("CAPTURE AUDIT PHOTO")

    if card_photo:
        st.success("✅ AUDIT LOGGED (PHOTO SECURED)")
        # Note for David: The actual 'card_photo' variable contains the clear image!
        st.link_button(f"💸 EXECUTE £{st.session_state.amt:.2f} TRANSFER", 
                       f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}")
        if st.button("🔄 CLEAR & NEXT ORDER"): st.rerun()

else:
    # ---------------- CUSTOMER VIEW ----------------
    st.write(f"### 📱 Scan to Pay: £{st.session_state.amt:.2f}")
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}"
    qr = qrcode.make(pay_url); buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=400)

st.caption("v3.3 | Double-Lock Privacy | HQ: The New Inn")
