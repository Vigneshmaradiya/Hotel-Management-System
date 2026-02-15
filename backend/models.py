from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class Room(BaseModel):
    room_number: str
    room_type: str
    price: int
    status: str = "available"

class RoomResponse(Room):
    id: int

class Guest(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Optional[str] = None

class GuestResponse(Guest):
    id: int
    created_at: datetime

class Booking(BaseModel):
    guest_id: int
    room_id: int
    check_in_date: date
    check_out_date: date
    total_amount: int
    status: str = "confirmed"

class BookingResponse(Booking):
    id: int
    created_at: datetime

class BookingDetail(BaseModel):
    booking_id: int
    guest_name: str
    room_number: str
    room_type: str
    check_in_date: date
    check_out_date: date
    total_amount: int
    status: str
    created_at: datetime
