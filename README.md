# 🏨 Hotel Management System

A comprehensive Hotel Management System built with **Streamlit** (Frontend), **FastAPI** (Backend REST API), and **PostgreSQL** (Database).

## 📋 Features

- **Room Management**: Add, update, delete, and view hotel rooms
- **Guest Management**: Manage guest information and profiles
- **Booking System**: Create, view, and cancel room bookings
- **Dashboard**: Overview of hotel operations with metrics and statistics
- **Real-time Updates**: Dynamic status updates for rooms and bookings
- **RESTful API**: Well-structured backend API for all operations
- **Cloud-Ready**: Dockerized backend ready for deployment

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: FastAPI (Dockerized)
- **Database**: PostgreSQL (Supabase)
- **API Communication**: REST API
- **Python Version**: 3.11+

## 📁 Project Structure

```
HMS/
├── backend/
│   ├── main.py           # FastAPI application and endpoints
│   ├── models.py         # Pydantic models for data validation
│   └── database.py       # Database connection utilities
├── frontend/
│   └── app.py           # Streamlit application
├── database/
│   └── init.sql         # Database initialization script
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- DBeaver or MySQL Workbench (optional, for database management)

### 2. Database Setup

1. Open your MySQL client (DBeaver, MySQL Workbench, or command line)
2. Connect to MySQL using:
   - Host: `localhost`
   - Port: `3306`
   - User: `root`
   - Password: `pass123`

3. Execute the database initialization script:
   ```sql
   source /path/to/HMS/database/init.sql
   ```
   Or manually run the SQL script from `database/init.sql`

### 3. Python Environment Setup

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Environment Configuration

The `.env` file is already configured with your MySQL credentials:
```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=pass123
DB_NAME=hotel_management
```

If needed, modify these values to match your MySQL setup.

### 5. Running the Application

#### Start the Backend API (Terminal 1):
```bash
cd backend
python main.py
```
The API will be available at: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

#### Start the Frontend (Terminal 2):
```bash
cd frontend
streamlit run app.py
```
The frontend will open automatically in your browser at: `http://localhost:8501`

## 📖 API Endpoints

### Rooms
- `GET /rooms` - Get all rooms
- `GET /rooms/{room_id}` - Get specific room
- `POST /rooms` - Create new room
- `PUT /rooms/{room_id}` - Update room
- `DELETE /rooms/{room_id}` - Delete room
- `GET /available-rooms` - Get available rooms

### Guests
- `GET /guests` - Get all guests
- `GET /guests/{guest_id}` - Get specific guest
- `POST /guests` - Create new guest
- `PUT /guests/{guest_id}` - Update guest
- `DELETE /guests/{guest_id}` - Delete guest

### Bookings
- `GET /bookings` - Get all bookings
- `GET /bookings/{booking_id}` - Get specific booking
- `POST /bookings` - Create new booking
- `PUT /bookings/{booking_id}` - Update booking
- `DELETE /bookings/{booking_id}` - Cancel booking

## 🎯 Usage Guide

### Dashboard
- View overall statistics (total rooms, available rooms, guests, bookings)
- See recent bookings
- View room status distribution
- Analyze revenue by room type

### Room Management
1. **View Rooms**: See all rooms with their details and status
2. **Add Room**: Create new rooms with room number, type, price, and status
3. **Update/Delete**: Modify existing room details or remove rooms

### Guest Management
1. **View Guests**: See all registered guests
2. **Add Guest**: Register new guests with contact information
3. **Update/Delete**: Modify guest details or remove guests

### Booking Management
1. **View Bookings**: See all bookings with complete details
2. **Create Booking**: Make new reservations by selecting guest, room, and dates
3. **Manage Booking**: View booking details and cancel if needed

## ☁️ Cloud Deployment

### Deploy to Production

This application is production-ready with Docker support. Deploy your backend to a cloud service for global access:

#### Quick Deploy Options:

1. **Railway** (Recommended - Easiest)
   - Free tier: 500 hours/month
   - Auto-deploys from GitHub
   - See [BACKEND_DEPLOYMENT.md](BACKEND_DEPLOYMENT.md) for detailed instructions

2. **Render** 
   - Free tier with auto-sleep
   - Blueprint included ([render.yaml](render.yaml))

3. **Fly.io**
   - Free tier with 3 VMs
   - Configuration ready ([fly.toml](fly.toml))

#### Deploy Frontend (Streamlit Cloud):

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Deploy this repository
4. Set main file: `frontend/app.py`
5. Add secret in settings:
   ```toml
   API_BASE_URL = "https://your-backend-url.com"
   ```

**📖 Full deployment guide**: See [BACKEND_DEPLOYMENT.md](BACKEND_DEPLOYMENT.md)

## 🔧 Troubleshooting

### Database Connection Issues
- Ensure MySQL service is running
- Verify credentials in `.env` file
- Check if database `hotel_management` exists

### API Not Responding
- Ensure backend is running on port 8000
- Check for port conflicts
- Verify firewall settings

### Frontend Can't Connect to API
- Ensure backend is running before starting frontend
- Check API_BASE_URL in `frontend/app.py` (default: `http://localhost:8000`)

## 📝 Sample Data

The database initialization script includes sample data:
- 8 rooms (various types: Single, Double, Suite, Deluxe)
- 3 sample guests
- 2 sample bookings

## 🔐 Security Notes

- Change default MySQL password in production
- Use environment variables for sensitive data
- Implement authentication for production use
- Add input validation and sanitization

## 📈 Future Enhancements

- User authentication and authorization
- Payment processing integration
- Email notifications for bookings
- Advanced reporting and analytics
- Mobile application
- Room service management
- Staff management module

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Support

For issues or questions, please refer to the API documentation at `http://localhost:8000/docs`

---
**Version**: 1.0
**Last Updated**: December 2024
