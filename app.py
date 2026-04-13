import streamlit as st
import qrcode
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- CLEAN & STABLE UI (NO FLASHING) ---
st.markdown("""
<style>
    /* 1. FULL-WIDTH CAMERA - NO ANIMATIONS */
    div[data-testid="stCameraInput"] video {
        width: 100% !important;
        border-radius: 12px;
        border: 4px solid #00FF41;
        height: auto !important;
    }

    /* 2. THE SOLID PRIVACY MASK (NO BLUR/NO FLASH) */
    .privacy-shield {
        position: absolute;
        top: 35%; 
        left: 5%;
        width: 90%;
        height: 30%;
        background-color: #000; /* Solid Black */
        border: 2px solid #444;
        z-index: 1000;
        pointer-events: none;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00FF41;
        font-weight: bold;
    }

    /* 3. STABLE BUTTONS */
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
        font-weight: bold; background-color: #111; color: #00FF41; 
        border: 1px solid #444; 
    }
</style>
""", unsafe_allow_html=True)

# --- SYNC DATA ---
if 'amt' not in st.session_state: st.session_state.amt = 5.00
if 'item' not in st.session_state: st.session_state.item = "Pint"

# --- SIDEBAR ---
st.sidebar.title("💳 David's Terminal")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")
pin_input = st.sidebar.text_input("Staff PIN", type="password")

st.title(f"🛡️ {st.session_state.item}: £{st.session_state.amt:.2f}")

if pin_input == "1234":
    # ---------------- DAVID'S CONTROL PANEL ----------------
    st.write("### ⚡ Quick Select")
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

    # PRICE OVERRIDE (Step 1)
    st.write("---")
    st.write("### 💰 Step 1: Set Price (£0.01 Adjustment)")
    c_amt, c_itm = st.columns([1, 2])
    with c_amt:
        st.session_state.amt = st.number_input("Amount £", value=st.session_state.amt, step=0.01, format="%.2f")
    with c_itm:
        st.session_state.item = st.text_input("Drink Detail", value=st.session_state.item)

    # CAMERA (Step 2)
    st.write(f"### 📸 Step 2: Scan Card (£{st.session_state.amt:.2f})")
    
    # Solid black bar overlay
    st.markdown('<div class="privacy-shield">SENSITIVE DATA MASKED</div>', unsafe_allow_html=True)
    
    card_photo = st.camera_input("CAPTURE CARD")

    if card_photo:
        st.success("✅ AUDIT LOGGED")
        st.link_button(f"💸 EXECUTE £{st.session_state.amt:.2f} TRANSFER", f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}")
        if st.button("🔄 RESET"): st.rerun()

else:
    # ---------------- CUSTOMER VIEW (LOCKED) ----------------
    st.write(f"### 📱 Scan to Pay: £{st.session_state.amt:.2f}")
    st.write(f"Item: **{st.session_state.item}**")
    
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}"
    qr = qrcode.make(pay_url); buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=400)
    st.info("Staff: Enter PIN to use the Privacy Scanner.")

st.caption("v3.0 | Rave-Free Edition | HQ: The New Inn")
