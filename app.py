import streamlit as st
import qrcode
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- MOBILE OPTIMIZED CSS ---
st.markdown("""
<style>
    /* 1. COMPACT BUTTONS FOR MOBILE */
    .stButton>button { 
        width: 100%; border-radius: 8px; height: 3em; 
        font-weight: bold; background-color: #111; color: #00FF41; 
        border: 1px solid #444; font-size: 0.9rem;
    }
    /* 2. BLUR THE CAMERA & RESULT */
    div[data-testid="stCameraInput"] video {
        filter: blur(12px) brightness(0.8) !important;
        border: 3px solid #00FF41 !important;
        height: 200px !important;
    }
    div[data-testid="stCameraInput"] img {
        filter: blur(15px) grayscale(1) !important;
    }
    /* 3. TIGHTEN SPACING */
    .block-container { padding-top: 1rem !important; }
</style>
""", unsafe_allow_html=True)

if 'amt' not in st.session_state: st.session_state.amt = 5.00
if 'item' not in st.session_state: st.session_state.item = "Pint"

# --- SIDEBAR ---
st.sidebar.title("💳 David's Terminal")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")
pin_input = st.sidebar.text_input("Staff PIN", type="password")

if pin_input == "1234":
    # ---------------- DAVID'S MOBILE CONTROL ----------------
    st.subheader(f"💰 Set Price: £{st.session_state.amt:.2f}")
    
    # MOVE INPUTS TO THE TOP SO THEY ARE VISIBLE
    c_amt, c_itm = st.columns([1, 1.5])
    with c_amt:
        st.session_state.amt = st.number_input("£ Amount", value=st.session_state.amt, step=0.01, format="%.2f")
    with c_itm:
        st.session_state.item = st.text_input("Drink Name", value=st.session_state.item)

    st.write("---")
    
    # COMPACT MENU GRID (2 Columns to save vertical space)
    st.write("### ⚡ Quick Select")
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        if st.button("🍺 PINTS"): st.session_state.item = "Pint"; st.session_state.amt = 5.00; st.rerun()
        if st.button("🍏 CIDERS"): st.session_state.item = "Cider"; st.session_state.amt = 5.25; st.rerun()
    with row1_col2:
        if st.button("🍷 WINE"): st.session_state.item = "Wine"; st.session_state.amt = 6.50; st.rerun()
        if st.button("🥃 MIXERS"): st.session_state.item = "Mixer"; st.session_state.amt = 7.50; st.rerun()
    
    if st.button("🍹 COCKTAILS"): st.session_state.item = "Cocktail"; st.session_state.amt = 12.00; st.rerun()

    st.write("---")
    
    # CAMERA SECTION
    st.write(f"### 📸 Step 2: Privacy Scan")
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}&noshare=true"
    
    card_photo = st.camera_input("CAPTURE CARD")

    if card_photo:
        st.success("✅ AUDIT LOGGED")
        st.link_button(f"💸 EXECUTE £{st.session_state.amt:.2f} TRANSFER", pay_url)
        if st.button("🔄 RESET"): st.rerun()

else:
    # ---------------- CUSTOMER VIEW ----------------
    st.write(f"### 📱 Scan to Pay: £{st.session_state.amt:.2f}")
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}&noshare=true"
    qr = qrcode.make(pay_url); buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=350)
    st.info("Staff: PIN required for admin.")

st.caption("v3.5 | Mobile Optimized | HQ: The New Inn")
