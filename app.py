import streamlit as st
import qrcode
from io import BytesIO

# --- THE MASTER SETTINGS ---
# Set to False to remotely cut off terminal access
access_granted = True

st.set_page_config(page_title="Sovereign Terminal", page_icon="🛡️", layout="wide")

# UI/UX: Custom CSS for Full-Width and Green Success Flash
st.markdown("""
<style>
    .stCamera { border-radius: 15px; border: 2px solid #00FF41; }
    div[data-testid="stImage"] > img { width: 100% !important; border-radius: 15px; }
    .stButton>button { border-radius: 10px; height: 3em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if not access_granted:
    st.error("⚠️ TERMINAL INACTIVE")
    st.info("Please contact your Sovereign Architect to renew your license.")
    st.stop()

# --- MERCHANT & MENU SETUP ---
st.sidebar.title("💳 Merchant Setup")
biz_name = st.sidebar.text_input("Business Name", value="Eastgate Bar")
handle = st.sidebar.text_input("Monzo Handle", value="davidhancock62")

# THE SOVEREIGN PRICE MANIFEST (Locked - No User Tampering)
MENU = {
    "PINT": 5.00,
    "WINE": 6.50,
    "SOFT": 2.50,
    "SPIRIT": 7.50
}

# Initialize session state for payment logic
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = "PINT"
if 'amt' not in st.session_state:
    st.session_state.amt = MENU["PINT"]

st.title(f"🛡️ {biz_name} Sovereign Terminal")

# --- THE STAFF SHIELD (PIN Entrance) ---
st.sidebar.markdown("---")
st.sidebar.write("### 🔐 Staff Terminal")
pin_input = st.sidebar.text_input("Enter Access PIN", type="password")

# --- MAIN LOGIC GATE ---
if pin_input == "1234":
    # ---------------- STAFF VIEW: THE SOVEREIGN EYE ----------------
    st.sidebar.success("🛡️ 0% FEE RAIL ACTIVE")
    
    st.header("👁️ Sovereign Card Capture & Audit")
    st.info(f"Currently Charging: **{st.session_state.selected_item} (£{st.session_state.amt:.2f})**")

    # 1. MANDATORY PHYSICAL CARD PHOTO
    st.write("### 📸 Step 1: Capture Physical Card")
    card_capture = st.camera_input("SCAN CARD FOR AUDIT")

    if card_capture:
        st.success("✅ IMAGE SECURED. Bypassing Visa/Mastercard Tap Tax.")
        st.image(card_capture, caption="Audit Log: Card Verified", width=400)
        
        # 2. THE 0% FEE FINALIZER (Only appears after photo)
        st.write("### 💸 Step 2: Finalize Payment")
        st.link_button(f"EXECUTE £{st.session_state.amt:.2f} TRANSFER", 
                       f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.selected_item}%20Audit_Captured",
                       use_container_width=True)
        
        if st.button("CLEAR & RESET TERMINAL"):
            st.balloons()
            st.rerun()
            
    st.write("---")
    st.write("### ⚡ Sovereign Quick Select")
    cols = st.columns(len(MENU))
    for i, (item, price) in enumerate(MENU.items()):
        if cols[i].button(f"{item}\n£{price}", use_container_width=True):
            st.session_state.selected_item = item
            st.session_state.amt = price
            st.rerun()

else:
    # ---------------- CUSTOMER VIEW: THE STANDARD QR RAIL ----------------
    st.write("---")
    st.write(f"### 📱 Scan to Pay: **{st.session_state.selected_item}**")
    st.write(f"Merchant: **{biz_name}**")
    
    # Generate the Monzo.me QR Code
    pay_url = f"https://monzo.me/{handle}/{st.session_state.amt}?d={st.session_state.selected_item}%20at%20{biz_name.replace(' ', '%20')}"
    
    qr = qrcode.make(pay_url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    
    st.image(buf.getvalue(), caption=f"Total Amount: £{st.session_state.amt:.2f}", width=400)
    
    st.success(f"✨ Direct Payment Active. 0% Merchant Fees Applied.")
    st.info("Staff: Enter PIN in sidebar to unlock Physical Card Scanner.")

# Footer Audit
st.caption(f"Sovereign Terminal Build v1.2 | Inhabiting: The New Inn (HQ) | Deploying: Eastgate")
