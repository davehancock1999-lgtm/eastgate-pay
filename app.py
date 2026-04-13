import streamlit as st
import qrcode
from io import BytesIO

# --- MASTER CONFIGURATION ---
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- THE "FORCE-FILL" CSS (Sabotage Prevention) ---
st.markdown("""
<style>
    /* 1. FORCE CAMERA TO FULL AVAILABLE WIDTH & HEIGHT */
    div[data-testid="stCameraInput"] > div {
        width: 100% !important;
        max-width: 100% !important;
    }
    video {
        width: 100% !important;
        height: auto !important;
        border-radius: 15px;
        border: 6px solid #00FF41 !important; /* Visual confirmation of the Rail */
    }

    /* 2. PHYSICAL PRIVACY SHIELD (Hard Blur over the center 50% of the feed) */
    .privacy-box {
        position: absolute;
        top: 35%;
        left: 10%;
        width: 80%;
        height: 30%;
        background: rgba(0, 255, 65, 0.1);
        backdrop-filter: blur(40px) brightness(0.5); /* HEAVY BLUR */
        border: 3px dashed #00FF41;
        z-index: 999;
        pointer-events: none;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #00FF41;
        font-size: 1.5rem;
        font-weight: bold;
    }

    /* 3. SUCCESS FLASH */
    .flash-active {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        border: 30px solid #00FF41;
        z-index: 9999;
        pointer-events: none;
        animation: pulse 0.5s infinite;
    }
    @keyframes pulse { from { opacity: 0; } to { opacity: 1; } }

    /* 4. BUTTONS */
    .stButton>button { width: 100%; border-radius: 10px; height: 4em; border: 1px solid #00FF41; background: #000; color: #00FF41; }
</style>
""", unsafe_allow_html=True)

# --- DATA INITIALIZATION ---
if 'amt' not in st.session_state: st.session_state.amt = 5.00
if 'item' not in st.session_state: st.session_state.item = "Pint"

# --- SIDEBAR ---
st.sidebar.title("💳 Merchant Setup")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")
pin_input = st.sidebar.text_input("Staff PIN", type="password")

st.title(f"🛡️ Sovereign Terminal: {st.session_state.item}")

if pin_input == "1234":
    # ---------------- DIRECTOR VIEW ----------------
    st.sidebar.success("🛡️ ACCESS GRANTED")
    
    # THE COMPLETE FIXED MENU
    st.write("### ⚡ Sovereign Menu select")
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
    
    # PENNY VARIETY OVERRIDE
    st.write("### 💰 Step 1: Exact Price Adjustment")
    c_price, c_name = st.columns([1,2])
    with c_price:
        st.session_state.amt = st.number_input("Amount £", value=st.session_state.amt, step=0.01, format="%.2f")
    with c_name:
        st.session_state.item = st.text_input("Item Label", value=st.session_state.item)

    # FULL SCREEN CAMERA WITH PRIVACY
    st.write(f"### 📸 Step 2: Capture Card (£{st.session_state.amt:.2f})")
    
    # This div is the visual privacy shield
    st.markdown('<div class="privacy-box">🛡️ SOVEREIGN PRIVACY ACTIVE</div>', unsafe_allow_html=True)
    
    card_photo = st.camera_input("SCAN PHYSICAL CARD")

    if card_photo:
        # TRIGGER THE GREEN FLASH
        st.markdown('<div class="flash-active"></div>', unsafe_allow_html=True)
        st.success("✅ CAPTURED")
        
        st.link_button(f"💸 EXECUTE £{st.session_state.amt:.2f} TRANSFER", 
                       f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item}")
        
        if st.button("🔄 RESET"): st.rerun()

else:
    # ---------------- CUSTOMER VIEW ----------------
    st.write(f"### 📱 Scan to Pay: £{st.session_state.amt:.2f}")
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item}"
    qr = qrcode.make(pay_url); buf = BytesIO(); qr.save(buf, format="PNG")
    st.image(buf.getvalue(), width=450)
    st.info("Staff: Enter PIN to scan cards.")

st.caption("v2.5 | New Inn Deployment | Eastgate-Pay Rail")
