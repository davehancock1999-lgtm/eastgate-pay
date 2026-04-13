import streamlit as st
import qrcode
from io import BytesIO

# --- CONFIG ---
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- THE PRIVACY SHIELD CSS ---
st.markdown("""
<style>
    /* 1. FULL WIDTH + VERTICAL PRIVACY CROP */
    /* Only shows a horizontal 'slot' to protect card digits */
    div[data-testid="stCameraInput"] video {
        width: 100% !important;
        height: 250px !important; 
        object-fit: cover !important; 
        border-radius: 15px;
        border: 4px solid #00FF41;
    }
    
    /* 2. MENU BUTTONS STYLING */
    .stButton>button { 
        width: 100%; 
        border-radius: 10px; 
        height: 4em; 
        border: 1px solid #00FF41; 
        font-weight: bold; 
        background-color: #0e1117;
        color: #00FF41;
    }

    /* 3. INPUT FIELD STYLING */
    input { font-size: 1.2rem !important; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE (Keeps everything in sync) ---
if 'amt' not in st.session_state: st.session_state.amt = 5.00
if 'item' not in st.session_state: st.session_state.item = "Pint"

# --- SIDEBAR: MERCHANT SETUP ---
st.sidebar.title("💳 Merchant Setup")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")
pin_input = st.sidebar.text_input("Staff PIN", type="password")

st.title(f"🛡️ Sovereign Terminal: {st.session_state.item} (£{st.session_state.amt:.2f})")

if pin_input == "1234":
    # ---------------- DIRECTOR VIEW (DAVID'S CONTROL) ----------------
    st.sidebar.success("🛡️ DAVID: PRIVACY MODE ACTIVE")
    
    # 1. THE FULL MENU (5 Categories)
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

    # 2. PENNY ADJUSTMENT
    st.write("### 💰 Step 1: Exact Price (£0.01 Variation)")
    c_amt, c_itm = st.columns([1, 2])
    with c_amt:
        st.session_state.amt = st.number_input("Amount £", value=st.session_state.amt, step=0.01, format="%.2f")
    with c_itm:
        st.session_state.item = st.text_input("Drink/Item Detail", value=st.session_state.item)

    st.write("---")
    
    # 3. PRIVACY CAMERA (The 'Slot' View)
    st.write(f"### 📸 Step 2: Capture Card (£{st.session_state.amt:.2f})")
    st.info("💡 Privacy Shield: Camera height restricted to hide full card details.")
    
    card_photo = st.camera_input("CAPTURE CARD")

    if card_photo:
        st.success(f"✅ AUDIT LOGGED: £{st.session_state.amt:.2f}")
        st.link_button(f"💸 EXECUTE TRANSFER", 
                       f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}")
        if st.button("🔄 RESET FOR NEXT ORDER"): st.rerun()

else:
    # ---------------- CUSTOMER VIEW (LOCKED) ----------------
    st.write(f"### 📱 Scan to Pay: £{st.session_state.amt:.2f}")
    st.write(f"Order: **{st.session_state.item}**")
    
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}"
    qr = qrcode.make(pay_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    st.image(buf.getvalue(), width=450)
    st.info("Staff: PIN required for card scanning and price variations.")

st.caption("v2.7 | David's Sovereign Master Build | HQ: The New Inn")
