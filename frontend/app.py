import streamlit as st
import requests
import pandas as pd
from datetime import date, timedelta
import os

# API base URL - Use environment variable or Streamlit secrets, fallback to localhost
API_BASE_URL = os.getenv("API_BASE_URL", st.secrets.get("API_BASE_URL", "http://localhost:8000"))

# Page configuration
st.set_page_config(
    page_title="Hotel Management System",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
    }
    div[data-testid="stNotification"] {
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for notifications
if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ''
if 'notification_type' not in st.session_state:
    st.session_state.notification_type = 'success'

# Sidebar navigation
st.sidebar.title("🏨 HMS Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Rooms", "Guests", "Bookings"]
)

# Helper functions
def fetch_data(endpoint, params=None):
    """Fetch data from API"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

def post_data(endpoint, data):
    """Post data to API"""
    try:
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        # Try to extract error message from response
        try:
            error_detail = e.response.json().get('detail', str(e))
            st.error(f"Error: {error_detail}")
        except:
            st.error(f"Error posting data: {e}")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error posting data: {e}")
        return None

def put_data(endpoint, data):
    """Update data via API"""
    try:
        response = requests.put(f"{API_BASE_URL}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error updating data: {e}")
        return None

def delete_data(endpoint):
    """Delete data via API"""
    try:
        response = requests.delete(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Error deleting data: {e}")
        return False

# ==================== DASHBOARD PAGE ====================
if page == "Dashboard":
    st.markdown('<h1 class="main-header">🏨 Hotel Management System Dashboard</h1>', unsafe_allow_html=True)
    
    # Fetch dashboard data
    rooms = fetch_data("/rooms")
    guests = fetch_data("/guests")
    bookings = fetch_data("/bookings")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Rooms", len(rooms))
    
    with col2:
        available_rooms = len([r for r in rooms if r['status'] == 'available'])
        st.metric("Available Rooms", available_rooms)
    
    with col3:
        st.metric("Total Guests", len(guests))
    
    with col4:
        active_bookings = len([b for b in bookings if b['status'] in ['confirmed', 'checked-in']])
        st.metric("Active Bookings", active_bookings)
    
    st.divider()
    
    # Recent bookings
    st.subheader("📋 Recent Bookings")
    if bookings:
        df = pd.DataFrame(bookings)
        df = df[['booking_id', 'guest_name', 'room_number', 'room_type', 'check_in_date', 'check_out_date', 'total_amount', 'status']]
        st.dataframe(df, width='stretch')
    else:
        st.info("No bookings found.")
    
    st.divider()
    
    # Room status distribution
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🚪 Room Status Distribution")
        if rooms:
            status_counts = pd.DataFrame(rooms)['status'].value_counts()
            st.bar_chart(status_counts)
        else:
            st.info("No room data available.")
    
    with col2:
        st.subheader("💰 Revenue by Room Type")
        if bookings:
            df = pd.DataFrame(bookings)
            revenue_by_type = df.groupby('room_type')['total_amount'].sum()
            st.bar_chart(revenue_by_type)
        else:
            st.info("No booking data available.")

# ==================== ROOMS PAGE ====================
elif page == "Rooms":
    st.markdown('<h1 class="main-header">🚪 Room Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["View Rooms", "Add Room", "Update/Delete Room"])
    
    # View Rooms Tab
    with tab1:
        st.subheader("All Rooms")
        rooms = fetch_data("/rooms")
        
        if rooms:
            df = pd.DataFrame(rooms)
            # Add color coding for status
            st.dataframe(
                df.style.applymap(
                    lambda x: 'background-color: #90EE90' if x == 'available' 
                    else 'background-color: #FFB6C1' if x == 'occupied' 
                    else 'background-color: #FFD700',
                    subset=['status']
                ),
                width='stretch'
            )
        else:
            st.info("No rooms found.")
    
    # Add Room Tab
    with tab2:
        st.subheader("Add New Room")
        with st.form("add_room_form"):
            col1, col2 = st.columns(2)
            with col1:
                room_number = st.text_input("Room Number", placeholder="e.g., 101")
                room_type = st.selectbox("Room Type", ["Single", "Double", "Suite", "Deluxe"])
            with col2:
                price = st.number_input("Price per Night (Rs)", min_value=0, step=10)
                status = st.selectbox("Status", ["available", "occupied", "maintenance"])
            
            submit = st.form_submit_button("Add Room")
            
            if submit:
                if room_number and price > 0:
                    room_data = {
                        "room_number": room_number,
                        "room_type": room_type,
                        "price": price,
                        "status": status
                    }
                    result = post_data("/rooms", room_data)
                    if result:
                        st.success(f"✅ Room {room_number} added successfully!")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Update/Delete Room Tab
    with tab3:
        st.subheader("Update or Delete Room")
        rooms = fetch_data("/rooms")
        
        if rooms:
            room_options = {f"{r['room_number']} - {r['room_type']}": r['id'] for r in rooms}
            selected_room = st.selectbox("Select Room", list(room_options.keys()))
            
            if selected_room:
                room_id = room_options[selected_room]
                room = next((r for r in rooms if r['id'] == room_id), None)
                
                if room:
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        with st.form("update_room_form"):
                            col_a, col_b = st.columns(2)
                            with col_a:
                                new_room_number = st.text_input("Room Number", value=room['room_number'])
                                new_room_type = st.selectbox("Room Type", ["Single", "Double", "Suite", "Deluxe"], 
                                                            index=["Single", "Double", "Suite", "Deluxe"].index(room['room_type']))
                            with col_b:
                                new_price = st.number_input("Price per Night (Rs)", value=int(room['price']), min_value=0, step=10)
                                new_status = st.selectbox("Status", ["available", "occupied", "maintenance"], 
                                                         index=["available", "occupied", "maintenance"].index(room['status']))
                            
                            update_submit = st.form_submit_button("Update Room")
                            
                            if update_submit:
                                updated_data = {
                                    "room_number": new_room_number,
                                    "room_type": new_room_type,
                                    "price": new_price,
                                    "status": new_status
                                }
                                result = put_data(f"/rooms/{room_id}", updated_data)
                                if result:
                                    st.success("✅ Room updated successfully!")
                                    st.rerun()
                    
                    with col2:
                        st.write("")
                        st.write("")
                        if st.button("🗑️ Delete Room", type="secondary"):
                            if delete_data(f"/rooms/{room_id}"):
                                st.success("✅ Room deleted successfully!")
                                st.rerun()
        else:
            st.info("No rooms available.")

# ==================== GUESTS PAGE ====================
elif page == "Guests":
    st.markdown('<h1 class="main-header">👥 Guest Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["View Guests", "Add Guest", "Update/Delete Guest"])
    
    # View Guests Tab
    with tab1:
        st.subheader("All Guests")
        guests = fetch_data("/guests")
        
        if guests:
            df = pd.DataFrame(guests)
            df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
            st.dataframe(df, width='stretch')
        else:
            st.info("No guests found.")
    
    # Add Guest Tab
    with tab2:
        st.subheader("Add New Guest")
        with st.form("add_guest_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                email = st.text_input("Email")
            with col2:
                phone = st.text_input("Phone")
                address = st.text_area("Address", height=100)
            
            submit = st.form_submit_button("Add Guest")
            
            if submit:
                if first_name and last_name and email and phone:
                    guest_data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "phone": phone,
                        "address": address
                    }
                    result = post_data("/guests", guest_data)
                    if result:
                        st.success(f"✅ Guest {first_name} {last_name} added successfully!")
                        st.balloons()
                        st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Update/Delete Guest Tab
    with tab3:
        st.subheader("Update or Delete Guest")
        guests = fetch_data("/guests")
        
        if guests:
            guest_options = {f"{g['first_name']} {g['last_name']} ({g['email']})": g['id'] for g in guests}
            selected_guest = st.selectbox("Select Guest", list(guest_options.keys()))
            
            if selected_guest:
                guest_id = guest_options[selected_guest]
                guest = next((g for g in guests if g['id'] == guest_id), None)
                
                if guest:
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        with st.form("update_guest_form"):
                            col_a, col_b = st.columns(2)
                            with col_a:
                                new_first_name = st.text_input("First Name", value=guest['first_name'])
                                new_last_name = st.text_input("Last Name", value=guest['last_name'])
                                new_email = st.text_input("Email", value=guest['email'])
                            with col_b:
                                new_phone = st.text_input("Phone", value=guest['phone'])
                                new_address = st.text_area("Address", value=guest['address'] or "", height=100)
                            
                            update_submit = st.form_submit_button("Update Guest")
                            
                            if update_submit:
                                updated_data = {
                                    "first_name": new_first_name,
                                    "last_name": new_last_name,
                                    "email": new_email,
                                    "phone": new_phone,
                                    "address": new_address
                                }
                                result = put_data(f"/guests/{guest_id}", updated_data)
                                if result:
                                    st.success("✅ Guest updated successfully!")
                                    st.rerun()
                    
                    with col2:
                        st.write("")
                        st.write("")
                        if st.button("🗑️ Delete Guest", type="secondary"):
                            if delete_data(f"/guests/{guest_id}"):
                                st.success("✅ Guest deleted successfully!")
                                st.rerun()
        else:
            st.info("No guests available.")

# ==================== BOOKINGS PAGE ====================
elif page == "Bookings":
    st.markdown('<h1 class="main-header">📅 Booking Management</h1>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["View Bookings", "Create Booking", "Manage Booking"])
    
    # View Bookings Tab
    with tab1:
        st.subheader("All Bookings")
        bookings = fetch_data("/bookings")
        
        if bookings:
            df = pd.DataFrame(bookings)
            st.dataframe(df, width='stretch')
        else:
            st.info("No bookings found.")
    
    # Create Booking Tab
    with tab2:
        st.subheader("Create New Booking")
        
        guests = fetch_data("/guests")
        
        if not guests:
            st.warning("Please add guests first before creating a booking.")
        else:
            # Date selection first
            col1, col2 = st.columns(2)
            with col1:
                check_in = st.date_input("Check-in Date", value=date.today(), key="create_checkin")
            with col2:
                check_out = st.date_input("Check-out Date", value=date.today() + timedelta(days=1), key="create_checkout")
            
            if check_out <= check_in:
                st.error("Check-out date must be after check-in date.")
            else:
                # Fetch available rooms for selected dates
                available_rooms = fetch_data("/available-rooms", {
                    "check_in": check_in.isoformat(),
                    "check_out": check_out.isoformat()
                })
                
                if not available_rooms:
                    st.warning("No rooms available for the selected dates. Please try different dates.")
                else:
                    st.success(f"Found {len(available_rooms)} available room(s) for selected dates!")
                    
                    with st.form("add_booking_form"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            guest_options = {f"{g['first_name']} {g['last_name']}": g['id'] for g in guests}
                            selected_guest = st.selectbox("Select Guest", list(guest_options.keys()))
                            guest_id = guest_options[selected_guest]
                            
                            room_options = {f"{r['room_number']} - {r['room_type']} (Rs{r['price']}/night)": r for r in available_rooms}
                            selected_room = st.selectbox("Select Room", list(room_options.keys()))
                            room = room_options[selected_room]
                        
                        with col2:
                            nights = (check_out - check_in).days
                            total_amount = nights * int(room['price'])
                            st.metric("Number of Nights", nights)
                            st.metric("Total Amount", f"Rs {total_amount}")
                            
                            status = st.selectbox("Booking Status", ["confirmed", "checked-in"])
                        
                        submit = st.form_submit_button("Create Booking", width='stretch')
                        
                        if submit:
                            booking_data = {
                                "guest_id": guest_id,
                                "room_id": room['id'],
                                "check_in_date": check_in.isoformat(),
                                "check_out_date": check_out.isoformat(),
                                "total_amount": total_amount,
                                "status": status
                            }
                            result = post_data("/bookings", booking_data)
                            if result:
                                st.success("✅ Booking created successfully!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.error("❌ Failed to create booking. Please try again.")
    
    # Manage Booking Tab
    with tab3:
        st.subheader("Manage Bookings")
        bookings = fetch_data("/bookings")
        
        if bookings:
            # Filter active bookings
            active_bookings = [b for b in bookings if b['status'] != 'cancelled']
            
            if not active_bookings:
                st.info("No active bookings to manage.")
            else:
                booking_options = {f"Booking #{b['booking_id']} - {b['guest_name']} (Room {b['room_number']}) - {b['status']}": b['booking_id'] for b in active_bookings}
                selected_booking = st.selectbox("Select Booking", list(booking_options.keys()))
                
                if selected_booking:
                    booking_id = booking_options[selected_booking]
                    booking = next((b for b in bookings if b['booking_id'] == booking_id), None)
                    
                    if booking:
                        # Display current booking info
                        st.info(f"**Current Status:** {booking['status'].upper()}")
                        
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Editable booking form
                            with st.form("update_booking_form"):
                                st.write("### Update Booking Details")
                                
                                # Get guests and rooms
                                guests = fetch_data("/guests")
                                all_rooms = fetch_data("/rooms")
                                
                                col_a, col_b = st.columns(2)
                                
                                with col_a:
                                    # Guest selection
                                    guest_options = {f"{g['first_name']} {g['last_name']}": g['id'] for g in guests}
                                    current_guest = next((k for k, v in guest_options.items() if booking['guest_name'] in k), list(guest_options.keys())[0])
                                    selected_guest = st.selectbox("Guest", list(guest_options.keys()), index=list(guest_options.keys()).index(current_guest))
                                    new_guest_id = guest_options[selected_guest]
                                    
                                    # Room selection
                                    room_options = {f"{r['room_number']} - {r['room_type']}": r['id'] for r in all_rooms}
                                    current_room = f"{booking['room_number']} - {booking['room_type']}"
                                    selected_room_str = st.selectbox("Room", list(room_options.keys()), 
                                                                    index=list(room_options.keys()).index(current_room) if current_room in room_options else 0)
                                    new_room_id = room_options[selected_room_str]
                                    room_price = next((r['price'] for r in all_rooms if r['id'] == new_room_id), 0)
                                
                                with col_b:
                                    # Dates
                                    from datetime import datetime
                                    current_checkin = datetime.strptime(str(booking['check_in_date']), '%Y-%m-%d').date()
                                    current_checkout = datetime.strptime(str(booking['check_out_date']), '%Y-%m-%d').date()
                                    
                                    new_check_in = st.date_input("Check-in Date", value=current_checkin, key="manage_checkin")
                                    new_check_out = st.date_input("Check-out Date", value=current_checkout, key="manage_checkout")
                                    
                                    # Status
                                    status_options = ["confirmed", "checked-in", "checked-out", "cancelled"]
                                    current_status_idx = status_options.index(booking['status'])
                                    new_status = st.selectbox("Status", status_options, index=current_status_idx)
                                
                                # Calculate new total
                                if new_check_out > new_check_in:
                                    new_nights = (new_check_out - new_check_in).days
                                    new_total_amount = new_nights * int(room_price)
                                    st.info(f"Nights: {new_nights} | Total: Rs {new_total_amount}")
                                else:
                                    st.error("Check-out must be after check-in")
                                    new_total_amount = booking['total_amount']
                                
                                col_btn1, col_btn2 = st.columns(2)
                                with col_btn1:
                                    update_submit = st.form_submit_button("💾 Update Booking", width='stretch', type="primary")
                                with col_btn2:
                                    cancel_in_form = st.form_submit_button("❌ Cancel Booking", width='stretch')
                                
                                if update_submit:
                                    if new_check_out > new_check_in:
                                        updated_booking = {
                                            "guest_id": new_guest_id,
                                            "room_id": new_room_id,
                                            "check_in_date": new_check_in.isoformat(),
                                            "check_out_date": new_check_out.isoformat(),
                                            "total_amount": new_total_amount,
                                            "status": new_status
                                        }
                                        result = put_data(f"/bookings/{booking_id}", updated_booking)
                                        if result:
                                            st.success("✅ Booking updated successfully!")
                                            st.rerun()
                                        else:
                                            st.error("❌ Failed to update booking. Room might be booked for selected dates.")
                                    else:
                                        st.error("Invalid dates selected")
                                
                                if cancel_in_form:
                                    if delete_data(f"/bookings/{booking_id}"):
                                        st.success("✅ Booking cancelled successfully!")
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to cancel booking")
                        
                        with col2:
                            st.write("### Current Info")
                            st.write(f"**Guest:** {booking['guest_name']}")
                            st.write(f"**Room:** {booking['room_number']}")
                            st.write(f"**Type:** {booking['room_type']}")
                            st.write(f"**Check-in:** {booking['check_in_date']}")
                            st.write(f"**Check-out:** {booking['check_out_date']}")
                            st.write(f"**Amount:** Rs{booking['total_amount']}")
                            
                            # Status guide
                            st.write("")
                            st.write("**Status Guide:**")
                            st.caption("• Confirmed: Booking reserved")
                            st.caption("• Checked-in: Guest arrived")
                            st.caption("• Checked-out: Completed")
                            st.caption("• Cancelled: Booking cancelled")
        else:
            st.info("No bookings available.")

# Footer
st.sidebar.divider()
st.sidebar.info("🏨 Hotel Management System")
