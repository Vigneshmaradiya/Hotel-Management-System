from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
from psycopg2.extras import RealDictCursor
from database import get_db_connection, close_db_connection
from models import (
    Room, RoomResponse, Guest, GuestResponse, 
    Booking, BookingResponse, BookingDetail
)

app = FastAPI(title="Hotel Management System API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hotel Management System API"}

# ==================== ROOM ENDPOINTS ====================

@app.get("/rooms", response_model=List[RoomResponse])
def get_rooms():
    """Get all rooms"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM rooms")
        rooms = cursor.fetchall()
        return rooms
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.get("/rooms/{room_id}", response_model=RoomResponse)
def get_room(room_id: int):
    """Get a specific room by ID"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
        room = cursor.fetchone()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        return room
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.post("/rooms", response_model=RoomResponse)
def create_room(room: Room):
    """Create a new room"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            INSERT INTO rooms (room_number, room_type, price, status)
            VALUES (%s, %s, %s, %s)
            RETURNING *
        """
        cursor.execute(query, (room.room_number, room.room_type, room.price, room.status))
        new_room = cursor.fetchone()
        connection.commit()
        return new_room
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.put("/rooms/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room: Room):
    """Update a room"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            UPDATE rooms 
            SET room_number = %s, room_type = %s, price = %s, status = %s
            WHERE id = %s
        """
        cursor.execute(query, (room.room_number, room.room_type, room.price, room.status, room_id))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Room not found")
        
        cursor.execute("SELECT * FROM rooms WHERE id = %s", (room_id,))
        updated_room = cursor.fetchone()
        return updated_room
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    """Delete a room"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM rooms WHERE id = %s", (room_id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Room not found")
        
        return {"message": "Room deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

# ==================== GUEST ENDPOINTS ====================

@app.get("/guests", response_model=List[GuestResponse])
def get_guests():
    """Get all guests"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM guests ORDER BY created_at DESC")
        guests = cursor.fetchall()
        return guests
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.get("/guests/{guest_id}", response_model=GuestResponse)
def get_guest(guest_id: int):
    """Get a specific guest by ID"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM guests WHERE id = %s", (guest_id,))
        guest = cursor.fetchone()
        if not guest:
            raise HTTPException(status_code=404, detail="Guest not found")
        return guest
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.post("/guests", response_model=GuestResponse)
def create_guest(guest: Guest):
    """Create a new guest"""
    print(f"Received guest data: {guest}")  # Debug logging
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            INSERT INTO guests (first_name, last_name, email, phone, address)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *
        """
        cursor.execute(query, (guest.first_name, guest.last_name, guest.email, guest.phone, guest.address))
        new_guest = cursor.fetchone()
        connection.commit()
        return new_guest
    except Exception as e:
        connection.rollback()
        error_msg = str(e)
        print(f"Error creating guest: {type(e).__name__}: {error_msg}")  # Better error logging
        
        # Handle unique constraint violation for email
        if "unique constraint" in error_msg.lower() or "duplicate key" in error_msg.lower():
            if "email" in error_msg.lower():
                raise HTTPException(status_code=400, detail=f"Email '{guest.email}' is already registered")
        
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {error_msg}")
    finally:
        cursor.close()
        close_db_connection(connection)

@app.put("/guests/{guest_id}", response_model=GuestResponse)
def update_guest(guest_id: int, guest: Guest):
    """Update a guest"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            UPDATE guests 
            SET first_name = %s, last_name = %s, email = %s, phone = %s, address = %s
            WHERE id = %s
        """
        cursor.execute(query, (guest.first_name, guest.last_name, guest.email, guest.phone, guest.address, guest_id))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Guest not found")
        
        cursor.execute("SELECT * FROM guests WHERE id = %s", (guest_id,))
        updated_guest = cursor.fetchone()
        return updated_guest
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.delete("/guests/{guest_id}")
def delete_guest(guest_id: int):
    """Delete a guest"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM guests WHERE id = %s", (guest_id,))
        connection.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Guest not found")
        
        return {"message": "Guest deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

# ==================== BOOKING ENDPOINTS ====================

@app.get("/bookings", response_model=List[BookingDetail])
def get_bookings():
    """Get all bookings with details"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                b.id as booking_id,
                g.first_name || ' ' || g.last_name as guest_name,
                r.room_number,
                r.room_type,
                b.check_in_date,
                b.check_out_date,
                b.total_amount,
                b.status,
                b.created_at
            FROM bookings b
            JOIN guests g ON b.guest_id = g.id
            JOIN rooms r ON b.room_id = r.id
            ORDER BY b.created_at DESC
        """
        cursor.execute(query)
        bookings = cursor.fetchall()
        return bookings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.get("/bookings/{booking_id}", response_model=BookingDetail)
def get_booking(booking_id: int):
    """Get a specific booking by ID"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        query = """
            SELECT 
                b.id as booking_id,
                g.first_name || ' ' || g.last_name as guest_name,
                r.room_number,
                r.room_type,
                b.check_in_date,
                b.check_out_date,
                b.total_amount,
                b.status,
                b.created_at
            FROM bookings b
            JOIN guests g ON b.guest_id = g.id
            JOIN rooms r ON b.room_id = r.id
            WHERE b.id = %s
        """
        cursor.execute(query, (booking_id,))
        booking = cursor.fetchone()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        return booking
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.post("/bookings", response_model=BookingResponse)
def create_booking(booking: Booking):
    """Create a new booking"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Check if room is available
        cursor.execute("SELECT status FROM rooms WHERE id = %s", (booking.room_id,))
        room = cursor.fetchone()
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        if room['status'] != 'available':
            raise HTTPException(status_code=400, detail="Room is not available")
        
        # Check for date conflicts
        conflict_query = """
            SELECT COUNT(*) as count FROM bookings
            WHERE room_id = %s 
            AND status IN ('confirmed', 'checked-in')
            AND NOT (check_out_date <= %s OR check_in_date >= %s)
        """
        cursor.execute(conflict_query, (booking.room_id, booking.check_in_date, booking.check_out_date))
        conflict = cursor.fetchone()
        if conflict and conflict['count'] > 0:
            raise HTTPException(status_code=400, detail="Room is already booked for the selected dates")
        
        # Create booking
        query = """
            INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date, total_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        cursor.execute(query, (booking.guest_id, booking.room_id, booking.check_in_date, 
                              booking.check_out_date, booking.total_amount, booking.status))
        
        booking_id = cursor.fetchone()["id"]
        
        # Update room status based on booking status and dates
        from datetime import date as date_type
        today = date_type.today()
        check_in_date = booking.check_in_date if isinstance(booking.check_in_date, date_type) else date_type.fromisoformat(str(booking.check_in_date))
        
        if booking.status == 'checked-in' or (booking.status == 'confirmed' and check_in_date <= today):
            cursor.execute("UPDATE rooms SET status = 'occupied' WHERE id = %s", (booking.room_id,))
        
        connection.commit()
        
        cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        new_booking = cursor.fetchone()
        
        if not new_booking:
            raise HTTPException(status_code=500, detail="Failed to retrieve created booking")
        
        return new_booking
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.put("/bookings/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking: Booking):
    """Update a booking and adjust room status accordingly"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Get old booking details
        cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        old_booking = cursor.fetchone()
        if not old_booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Check for date conflicts if room or dates changed
        if (booking.room_id != old_booking['room_id'] or 
            str(booking.check_in_date) != str(old_booking['check_in_date']) or 
            str(booking.check_out_date) != str(old_booking['check_out_date'])):
            
            conflict_query = """
                SELECT COUNT(*) as count FROM bookings
                WHERE room_id = %s 
                AND id != %s
                AND status IN ('confirmed', 'checked-in')
                AND NOT (check_out_date <= %s OR check_in_date >= %s)
            """
            cursor.execute(conflict_query, (booking.room_id, booking_id, booking.check_in_date, booking.check_out_date))
            conflict = cursor.fetchone()
            if conflict and conflict['count'] > 0:
                raise HTTPException(status_code=400, detail="Room is already booked for the selected dates")
        
        # Update booking
        query = """
            UPDATE bookings 
            SET guest_id = %s, room_id = %s, check_in_date = %s, 
                check_out_date = %s, total_amount = %s, status = %s
            WHERE id = %s
        """
        cursor.execute(query, (booking.guest_id, booking.room_id, booking.check_in_date,
                              booking.check_out_date, booking.total_amount, booking.status, booking_id))
        
        # Handle room status changes based on booking status
        if booking.status == 'checked-in':
            # Mark new room as occupied
            cursor.execute("UPDATE rooms SET status = 'occupied' WHERE id = %s", (booking.room_id,))
            # If room changed, free up old room
            if booking.room_id != old_booking['room_id']:
                cursor.execute("UPDATE rooms SET status = 'available' WHERE id = %s", (old_booking['room_id'],))
        
        elif booking.status == 'checked-out':
            # Free up the room
            cursor.execute("UPDATE rooms SET status = 'available' WHERE id = %s", (booking.room_id,))
        
        elif booking.status == 'cancelled':
            # Free up the room
            cursor.execute("UPDATE rooms SET status = 'available' WHERE id = %s", (booking.room_id,))
        
        elif booking.status == 'confirmed':
            # If changing from checked-in to confirmed, free the room
            if old_booking['status'] == 'checked-in':
                cursor.execute("UPDATE rooms SET status = 'available' WHERE id = %s", (old_booking['room_id'],))
        
        connection.commit()
        
        cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        updated_booking = cursor.fetchone()
        return updated_booking
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.delete("/bookings/{booking_id}")
def cancel_booking(booking_id: int):
    """Cancel a booking and free up the room"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        # Get booking details
        cursor.execute("SELECT room_id FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        if not booking:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        # Update booking status
        cursor.execute("UPDATE bookings SET status = 'cancelled' WHERE id = %s", (booking_id,))
        
        # Update room status
        cursor.execute("UPDATE rooms SET status = 'available' WHERE id = %s", (booking['room_id'],))
        
        connection.commit()
        return {"message": "Booking cancelled successfully"}
    except HTTPException:
        raise
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

@app.get("/available-rooms", response_model=List[RoomResponse])
def get_available_rooms(check_in: str = None, check_out: str = None):
    """Get available rooms, optionally filtered by date range"""
    connection = get_db_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        if check_in and check_out:
            # Get rooms that are either available or don't have conflicting bookings
            query = """
                SELECT r.* FROM rooms r
                WHERE r.id NOT IN (
                    SELECT b.room_id FROM bookings b
                    WHERE b.status IN ('confirmed', 'checked-in')
                    AND NOT (
                        b.check_out_date <= %s OR b.check_in_date >= %s
                    )
                )
            """
            cursor.execute(query, (check_in, check_out))
        else:
            # Just get rooms marked as available
            cursor.execute("SELECT * FROM rooms WHERE status = 'available'")
        
        rooms = cursor.fetchall()
        return rooms
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        close_db_connection(connection)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
