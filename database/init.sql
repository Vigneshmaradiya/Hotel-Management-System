-- Hotel Management System Database Schema - PostgreSQL
-- Drop database if exists and create new one
DROP DATABASE IF EXISTS hotel_management;
CREATE DATABASE hotel_management;

-- Connect to the database
\c hotel_management

-- Create Rooms Table
CREATE TABLE rooms (
    id SERIAL PRIMARY KEY,
    room_number VARCHAR(10) NOT NULL UNIQUE,
    room_type VARCHAR(50) NOT NULL,
    price INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'available' CHECK (status IN ('available', 'occupied', 'maintenance')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Guests Table
CREATE TABLE guests (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Bookings Table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    guest_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    check_in_date DATE NOT NULL,
    check_out_date DATE NOT NULL,
    total_amount INTEGER NOT NULL,
    status VARCHAR(20) DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'checked-in', 'checked-out', 'cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (guest_id) REFERENCES guests(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

-- Create trigger function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for auto-updating updated_at
CREATE TRIGGER update_rooms_updated_at BEFORE UPDATE ON rooms
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_guests_updated_at BEFORE UPDATE ON guests
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bookings_updated_at BEFORE UPDATE ON bookings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert Sample Rooms
INSERT INTO rooms (room_number, room_type, price, status) VALUES
('101', 'Single', 500, 'available'),
('102', 'Single', 500, 'available'),
('201', 'Double', 800, 'available'),
('202', 'Double', 800, 'available'),
('301', 'Suite', 1500, 'available'),
('302', 'Suite', 1500, 'available'),
('401', 'Deluxe', 2000, 'available'),
('402', 'Deluxe', 2000, 'available');

-- Insert Sample Guests
INSERT INTO guests (first_name, last_name, email, phone, address) VALUES
('John', 'Doe', 'john.doe@example.com', '555-0101', '123 Main St, City, State'),
('Jane', 'Smith', 'jane.smith@example.com', '555-0102', '456 Oak Ave, City, State'),
('Robert', 'Johnson', 'robert.j@example.com', '555-0103', '789 Pine Rd, City, State');

-- Insert Sample Bookings
INSERT INTO bookings (guest_id, room_id, check_in_date, check_out_date, total_amount, status) VALUES
(1, 1, '2024-12-10', '2024-12-15', 2500, 'confirmed'),
(2, 3, '2024-12-12', '2024-12-14', 1600, 'confirmed');

-- Update room status for booked rooms
UPDATE rooms SET status = 'occupied' WHERE id IN (1, 3);

-- Create indexes for better performance
CREATE INDEX idx_room_status ON rooms(status);
CREATE INDEX idx_guest_email ON guests(email);
CREATE INDEX idx_booking_dates ON bookings(check_in_date, check_out_date);
CREATE INDEX idx_booking_status ON bookings(status);
