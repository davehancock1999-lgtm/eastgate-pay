import streamlit as st
import qrcode
from io import BytesIO

# --- MASTER CONFIGURATION ---
access_granted = True
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# UI/UX: Custom CSS for 15th-Century Pub Lighting & Modern Fintech Contrast
st.markdown("""
<style>
    .stCamera { border: 3px solid #00FF41 !important; border-radius: 15px; }
    div[data-testid="stImage"] > img { width: 100% !important; border-radius: 15px; border: 1px solid #444; }
    .stButton>button { border-radius: 12px; height: 3.5em; font-weight: bold; background-color: #0e1117; color: #00FF41; border: 1px solid #00FF41; }
    .stNumberInput input { font-size: 1.5rem !important; color: #00FF41 !important; }
</style>
""", unsafe_allow_html=True)

if not access_granted:
    st.error("⚠️ TERMINAL INACTIVE")
    st.stop()

# --- DATA INITIALIZATION (Session Persistence) ---
# This ensures prices stay synced across the entire app
if 'amt' not in st.session_state:
    st.session_state.amt = 5.00
if 'item' not in st.session_state:
    st.session_state.item = "Pint"

# --- SIDEBAR: MERCHANT & SHIELD ---
st.sidebar.title("💳 Merchant Setup")
biz_name = st.sidebar.text_input("Business Name", value="Eastgate Bar")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")

st.sidebar.markdown("---")
st.sidebar.write("### 🔐 Staff Shield")
pin_input = st.sidebar.text_input("Enter Access PIN", type="password")

st.title(f"🛡️ {biz_name} Sovereign Terminal")

if pin_input == "1234":
    # ---------------- DIRECTOR VIEW: DYNAMIC OVERRIDE ----------------
    st.sidebar.success("🛡️ DIRECTOR ACCESS ACTIVE")
    
    st.header("👁️ Sovereign Price & Card Capture")

    # 1. FIXED CATEGORY PRESETS (Instant Selection)
    st.write("### ⚡ Quick Select")
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        if st.button("🍺 PINTS", use_container_width=True):
            st.session_state.item = "Pint"; st.session_state.amt = 5.00; st.rerun()
    with c2:
        if st.button("🍷 WINE", use_container_width=True):
            st.session_state.item = "Wine"; st.session_state.amt = 6.50; st.rerun()
    with c3:
        if st.button("🍏 CIDER", use_container_width=True):
            st.session_state.item = "Cider"; st.session_state.amt = 5.20; st.rerun()
    with c4:
        if st.button("🥃 MIXER", use_container_width=True):
            st.session_state.item = "Mixer"; st.session_state.amt = 7.50; st.rerun()
    with c5:
        if st.button("🍹 COCKTAIL", use_container_width=True):
            st.session_state.item = "Cocktail"; st.session_state.amt = 9.00; st.rerun()

    # 2. PENNY-PRECISE ALTERATION (Step 1)
    # This section updates the session state IMMEDIATELY so Step 2 matches
    st.write("### 💰 Step 1: Set Exact Price (Penny Variation)")
    col_amt, col_name = st.columns([1, 2])
    with col_amt:
        # Step=0.01 allows for penny-level control (e.g. £4.11)
        st.session_state.amt = st.number_input("Transaction Amount (£)", min_value=0.01, value=st.session_state.amt, step=0.01, format="%.2f")
    with col_name:
        st.session_state.item = st.text_input("Drink/Item Detail", value=st.session_state.item)

    st.write("---")
    
    # 3. CARD CAPTURE (Step 2 - GUARANTEED SYNC)
    # The label below will now change as soon as you type in Step 1
    st.write(f"### 📸 Step 2: Capture Physical Card (£{st.session_state.amt:.2f})")
    card_photo = st.camera_input("SCAN CARD FOR AUDIT")

    if card_photo:
        st.success(f"✅ AUDIT SECURED: £{st.session_state.amt:.2f} {st.session_state.item}")
        st.image(card_photo, width=400)
        
        # 4. THE 0% FEE FINALIZER
        st.write("### 💸 Step 3: Finalize Transfer")
        st.link_button(f"EXECUTE £{st.session_state.amt:.2f} TRANSFER", 
                       f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}_Sovereign_Audit",
                       use_container_width=True)
        
        if st.button("🔄 CLEAR & RESET TERMINAL"):
            st.balloons()
            st.rerun()

else:
    # ---------------- CUSTOMER VIEW: THE LOCKED QR RAIL ----------------
    st.write("---")
    st.write(f"### 📱 Scan to Pay for: **{st.session_state.item}**")
    
    # Generate the Monzo.me QR Code
    # This URL is dynamic and matches whatever the Staff sets in Step 1
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}%20at%20{biz_name.replace(' ', '%20')}"
    
    qr = qrcode.make(pay_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    st.image(buf.getvalue(), caption=f"Total Amount Due: £{st.session_state.amt:.2f}", width=400)
    st.info("Staff: Use PIN in sidebar to adjust prices or scan cards.")

# --- FOOTER ---
st.caption(f"Sovereign Terminal v2.2 | Penny-Precise & Multi-Category | HQ: The New Inn")
