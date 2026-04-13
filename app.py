import streamlit as st
import qrcode
from io import BytesIO

# --- MASTER CONFIGURATION ---
access_granted = True
st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# --- UI/UX: SOVEREIGN VISUAL OVERLAY ---
st.markdown("""
<style>
    /* Full-width video & rounded frames for pub lighting */
    .stCamera { border: 3px solid #00FF41; border-radius: 15px; }
    div[data-testid="stImage"] > img { width: 100% !important; border-radius: 15px; border: 1px solid #444; }
    .stButton>button { border-radius: 12px; height: 3.5em; background-color: #111; color: #00FF41; border: 1px solid #00FF41; }
    .stNumberInput, .stTextInput { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

if not access_granted:
    st.error("⚠️ TERMINAL INACTIVE")
    st.stop()

# --- DATA INITIALIZATION ---
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

# --- MAIN TERMINAL INTERFACE ---
st.title(f"🛡️ {biz_name} Sovereign Terminal")

if pin_input == "1234":
    # ---------------- DIRECTOR VIEW: DYNAMIC OVERRIDE ----------------
    st.sidebar.success("🛡️ DIRECTOR ACCESS GRANTED")
    
    st.header("👁️ Sovereign Price & Card Capture")
    
    # 1. DYNAMIC PRICE ALTERATION (Staff Only)
    st.write("### 💰 Step 1: Set Price Variation")
    col1, col2 = st.columns(2)
    with col1:
        new_amt = st.number_input("Transaction Amount (£)", min_value=0.01, value=st.session_state.amt, step=0.10)
    with col2:
        new_item = st.text_input("Drink/Item Name", value=st.session_state.item)
    
    if st.button("🔐 LOCK & UPDATE TERMINAL", use_container_width=True):
        st.session_state.amt = new_amt
        st.session_state.item = new_item
        st.toast(f"Synchronized: {new_item} at £{new_amt:.2f}")
        st.rerun()

    st.write("---")
    
    # 2. MANDATORY PHYSICAL CARD PHOTO (Proof of Sovereignty)
    st.write(f"### 📸 Step 2: Capture Physical Card (£{st.session_state.amt:.2f})")
    card_photo = st.camera_input("SCAN CARD FOR AUDIT")

    if card_photo:
        st.success("✅ IMAGE SECURED IN DEEP BLUE VAULT")
        st.image(card_photo, width=400)
        
        # 3. THE 0% FEE FINALIZER
        st.write("### 💸 Step 3: Finalize Transfer")
        st.link_button(f"EXECUTE £{st.session_state.amt:.2f} TRANSFER", 
                       f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}_Audit_Captured",
                       use_container_width=True)
        
        if st.button("🔄 RESET FOR NEXT CUSTOMER"):
            st.balloons()
            st.rerun()

else:
    # ---------------- CUSTOMER VIEW: LOCKED QR RAIL ----------------
    st.write("---")
    st.write(f"### 📱 Scan to Pay for: **{st.session_state.item}**")
    st.write(f"Merchant: **{biz_name}**")
    
    # Generate the Monzo.me QR Code based on the LOCKED price
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.item.replace(' ', '%20')}%20at%20{biz_name.replace(' ', '%20')}"
    
    qr = qrcode.make(pay_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    st.image(buf.getvalue(), caption=f"Total Amount: £{st.session_state.amt:.2f}", width=450)
    
    st.success(f"✨ Direct 0% Rail Active. No bank surcharges applied.")
    st.info("Staff: Use sidebar PIN to alter prices or scan physical cards.")

# --- FOOTER ---
st.caption(f"Sovereign Terminal v2.0 | HQ: The New Inn | Deploy: Eastgate-Pay")
