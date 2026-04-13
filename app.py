import streamlit as st
import qrcode
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- THE "ZOOM & CHOP" PRIVACY CSS ---
st.markdown("""
<style>
    /* 1. PHYSICAL CROP: This forces the video to only show the BOTTOM half */
    div[data-testid="stCameraInput"] video {
        width: 100% !important;
        height: 180px !important; /* Extremely short height */
        object-fit: cover !important;
        object-position: bottom !important; /* FORCES THE VIEW TO THE BOTTOM OF THE LENS */
        border-radius: 12px;
        border: 4px solid #00FF41;
    }

    /* 2. THE BUTTON GRID */
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3.5em; 
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

# --- MAIN ---
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

    st.write("---")
    st.write("### 💰 Step 1: Set Exact Price")
    c_amt, c_itm = st.columns([1, 2])
    with c_amt:
        st.session_state.amt = st.number_input("Amount £", value=st.session_state.amt, step=0.01, format="%.2f")
    with c_itm:
        st.session_state.item = st.text_input("Drink Name", value=st.session_state.item)

    # 3. THE PRIVACY SCANNER
    st.write(f"### 📸 Step 2: Privacy Scan (£{st.session_state.amt:.2f})")
    st.warning("🛡️ PRIVACY SHIELD: Only the bottom of the card is visible to hide digits.")
    
    card_photo = st.camera_input("TAKE AUDIT PHOTO")

    if card_photo:
        st.success("✅ AUDIT CAPTURED")
        st.link_button(f"💸 EXECUTE £{st.session_state.amt:.2f} TRANSFER", f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}")
        if st.button("🔄 RESET"): st.rerun()

else:
    # ---------------- CUSTOMER VIEW ----------------
    st.write(f"### 📱 Scan to Pay: £{st.session_state.amt:.2f}")
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}"
    qr = qrcode.make(pay_url); buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=400)

st.caption("v3.1 | Bottom-Crop Privacy | David's Build")
