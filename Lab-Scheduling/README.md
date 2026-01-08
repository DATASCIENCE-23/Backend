# Lab Scheduling Module

## Overview
Hospital Management System - Laboratory Scheduling Module providing comprehensive laboratory test management functionality with complete workflow automation from order creation to report generation.

## 🚀 Features

### Core Functionality
- **Lab Order Management** - Create and manage laboratory test orders from doctors
- **Appointment Scheduling** - Schedule lab appointments with technicians and availability checking
- **Sample Collection** - Track sample collection process (in-lab and home collection)
- **Result Management** - Enter, validate, and verify test results with abnormal value detection
- **Report Generation** - Generate comprehensive lab reports with EMR integration

### Advanced Features
- **Quality Control** - Result verification and approval workflow
- **Business Rule Enforcement** - Status transitions and validation
- **Home Collection Support** - Schedule and manage home sample collection
- **EMR Integration** - Seamless integration with Electronic Medical Records
- **Comprehensive Error Handling** - Structured error responses and logging
- **Interactive API Documentation** - Full Swagger UI documentation

## 📚 API Documentation

### Swagger UI Access
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc  
- **OpenAPI Schema**: http://localhost:8000/openapi.json
- **25+ API Endpoints** fully documented with examples and try-it-out functionality

### Documentation Features
- Complete workflow documentation
- Interactive testing interface
- Request/response examples
- Authentication guidance
- Error handling documentation
- Business rule explanations

## 🏗️ Project Structure

```
Lab-Scheduling/
├── controllers/              # HTTP request handlers
│   ├── lab_order_controller.py
│   ├── lab_schedule_controller.py
│   ├── lab_result_controller.py
│   └── lab_report_controller.py
├── models/                   # SQLAlchemy database models
│   ├── lab_order.py         # Lab order model with enums
│   ├── lab_schedule.py      # Appointment scheduling model
│   ├── lab_result.py        # Test result model
│   ├── lab_report.py        # Report generation model
│   ├── lab_technician.py    # Technician management model
│   └── lab_test.py          # Test definition model
├── repositories/             # Data access layer
│   ├── lab_order_repository.py
│   ├── lab_schedule_repository.py
│   ├── lab_result_repository.py
│   └── lab_report_repository.py
├── services/                 # Business logic layer
│   ├── lab_order_service.py
│   ├── lab_schedule_service.py
│   ├── lab_result_service.py
│   └── lab_report_service.py
├── routes/                   # API endpoint definitions
│   ├── lab_order_routes.py
│   ├── lab_schedule_routes.py
│   ├── lab_result_routes.py
│   └── lab_report_routes.py
├── schemas/                  # Pydantic request/response models
│   ├── lab_order.py
│   ├── lab_schedule.py
│   ├── lab_result.py
│   ├── lab_report.py
│   └── base.py
├── postman/                  # API testing collection
│   ├── Lab_Scheduling_API.postman_collection.json
│   └── Lab_Scheduling_Environment.postman_environment.json
├── main.py                   # FastAPI application entry point
├── config.py                 # Configuration management
├── database.py               # Database connection setup
├── exceptions.py             # Custom exception classes
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── sample_data.sql           # Sample data for testing
└── fix_sample_data.sql       # Database fixes and updates
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL database
- Required Python packages (see requirements.txt)

### Installation

1. **Clone and navigate to the directory:**
   ```bash
   cd Backend-develop/Backend-develop/Lab-Scheduling
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables in `.env`:**
   ```env
   DB_NAME=hospitalmanagement
   DB_USER=hms_user
   DB_PASSWORD=CloudComputing
   DB_HOST=localhost
   DB_PORT=5432
   DEBUG=True
   ```

4. **Set up the database:**
   ```bash
   # Create database tables (handled automatically on startup)
   # Optionally load sample data:
   psql -h localhost -U hms_user -d hospitalmanagement -f sample_data.sql
   ```

5. **Run the application:**
   ```bash
   python main.py
   ```

### 🌐 Access Points
- **Application Root**: http://localhost:8000
- **Swagger Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **API Base**: http://localhost:8000/api

## 📋 API Endpoints

### 🧪 Lab Orders (`/api/lab-orders/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/` | Create new lab order |
| `GET` | `/patient/{patient_id}` | Get patient's lab orders |
| `GET` | `/{order_id}` | Get specific lab order details |
| `PUT` | `/{order_id}/status` | Update order status |
| `GET` | `/doctor/{doctor_id}` | Get doctor's lab orders |
| `GET` | `/priority/{priority}` | Get orders by priority level |
| `GET` | `/pending` | Get all pending orders |
| `GET` | `/urgent` | Get urgent priority orders |

### 📅 Lab Scheduling (`/api/lab-schedule/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/available-slots/{date}` | Check available time slots |
| `POST` | `/` | Book lab appointment |
| `GET` | `/technician/{technician_id}` | Get technician's schedule |
| `GET` | `/{schedule_id}` | Get specific schedule details |
| `PUT` | `/{schedule_id}/status` | Update schedule status |
| `GET` | `/home-collections/` | Get home collection schedules |

### 📊 Lab Results (`/api/lab-results/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/` | Enter new test results |
| `GET` | `/order/{order_id}` | Get results by order |
| `GET` | `/{result_id}` | Get specific result details |
| `PUT` | `/{result_id}/verify` | Verify test results |
| `GET` | `/abnormal/` | Get abnormal results |
| `GET` | `/pending-verification/` | Get results pending verification |

### 📋 Lab Reports (`/api/lab-reports/`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/` | Generate new lab report |
| `GET` | `/patient/{patient_id}` | Get patient's reports |
| `GET` | `/{report_id}` | Get specific report |
| `PUT` | `/{report_id}/finalize` | Finalize report |
| `GET` | `/finalized/` | Get all finalized reports |
| `PUT` | `/{report_id}/integrate-emr` | Integrate with EMR |

## 🔐 Authentication
All API endpoints require JWT authentication. Include the token in the Authorization header:
```http
Authorization: Bearer <your-jwt-token>
```

## 🔄 Workflow

### Complete Lab Process Flow
1. **Doctor creates lab order** → `POST /api/lab-orders/`
2. **Patient schedules appointment** → `POST /api/lab-schedule/`
3. **Technician collects samples** → `PUT /api/lab-schedule/{id}/status`
4. **Lab staff enters results** → `POST /api/lab-results/`
5. **Results are verified** → `PUT /api/lab-results/{id}/verify`
6. **Report is generated** → `POST /api/lab-reports/`
7. **Report is finalized** → `PUT /api/lab-reports/{id}/finalize`
8. **EMR integration** → `PUT /api/lab-reports/{id}/integrate-emr`

### Status Transitions
- **Orders**: `PENDING` → `SCHEDULED` → `IN_PROGRESS` → `COMPLETED`
- **Schedules**: `SCHEDULED` → `IN_PROGRESS` → `COMPLETED`
- **Results**: `PENDING_VERIFICATION` → `VERIFIED`
- **Reports**: `DRAFT` → `PENDING_FINALIZATION` → `FINALIZED`

## ⚠️ Error Handling
The API uses standard HTTP status codes with structured error responses:

| Code | Status | Description |
|------|--------|-------------|
| `200` | Success | Request completed successfully |
| `201` | Created | Resource created successfully |
| `400` | Bad Request | Invalid request data or business rule violation |
| `401` | Unauthorized | Authentication required |
| `403` | Forbidden | Insufficient permissions |
| `404` | Not Found | Resource not found |
| `409` | Conflict | Business rule conflict |
| `422` | Unprocessable Entity | Data validation errors |
| `500` | Internal Server Error | Server error |

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": "Additional error details"
  }
}
```

## 🗄️ Database Models

### Core Entities
- **LabOrder** - Laboratory test orders with priority and status
- **LabSchedule** - Appointment scheduling with technician assignment
- **LabResult** - Test results with verification and abnormal detection
- **LabReport** - Comprehensive reports with EMR integration
- **LabTechnician** - Technician management and scheduling
- **LabTest** - Test definitions and configurations

### Key Enums
- **OrderStatus**: `PENDING`, `SCHEDULED`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`
- **OrderPriority**: `NORMAL`, `URGENT`, `STAT`
- **ScheduleStatus**: `SCHEDULED`, `IN_PROGRESS`, `COMPLETED`, `CANCELLED`
- **SampleType**: `BLOOD`, `URINE`, `STOOL`, `SALIVA`, `OTHER`
- **ResultStatus**: `PENDING_VERIFICATION`, `VERIFIED`, `REJECTED`
- **ReportStatus**: `DRAFT`, `PENDING_FINALIZATION`, `FINALIZED`

## 🧪 Testing

### Postman Collection
Pre-configured Postman collection available in `postman/` directory:
- **Collection**: `Lab_Scheduling_API.postman_collection.json`
- **Environment**: `Lab_Scheduling_Environment.postman_environment.json`
- **Features**: All endpoints with examples, automated tests, and environment variables

### Sample Data
Use the provided SQL files for testing:
```bash
# Load sample data
psql -h localhost -U hms_user -d hospitalmanagement -f sample_data.sql

# Apply fixes if needed
psql -h localhost -U hms_user -d hospitalmanagement -f fix_sample_data.sql
```

## 🏗️ Architecture

### Clean Architecture Pattern
- **Models**: SQLAlchemy ORM models with relationships
- **Schemas**: Pydantic models for request/response validation
- **Repositories**: Data access abstraction layer
- **Services**: Business logic and workflow management
- **Controllers**: HTTP request handling and validation
- **Routes**: API endpoint definitions and documentation

### Key Design Principles
- **Separation of Concerns** - Clear layer separation
- **Dependency Injection** - Loose coupling between components
- **Error Handling** - Comprehensive exception management
- **Validation** - Input validation at multiple layers
- **Documentation** - Self-documenting API with examples

## 🚀 Production Deployment

### Environment Configuration
```env
# Production settings
FLASK_ENV=production
DEBUG=False

# Database (use production credentials)
DB_NAME=hospitalmanagement_prod
DB_USER=prod_user
DB_PASSWORD=secure_password
DB_HOST=prod-db-server
DB_PORT=5432

# Security
CORS_ORIGINS=["https://yourdomain.com"]
TRUSTED_HOSTS=["yourdomain.com"]
```

### Deployment Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Configure production database credentials
- [ ] Set up proper CORS origins
- [ ] Configure trusted hosts
- [ ] Set up centralized logging
- [ ] Use production WSGI server (Gunicorn/Uvicorn)
- [ ] Set up SSL/TLS certificates
- [ ] Configure monitoring and health checks
- [ ] Set up backup procedures

### Production Server
```bash
# Using Uvicorn (recommended for FastAPI)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Using Gunicorn with Uvicorn workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 📞 Support & Documentation

### Getting Help
1. **Interactive API Docs**: Visit `/docs` when the application is running
2. **Postman Collection**: Use the provided collection for testing
3. **Error Messages**: Check structured error responses for details
4. **Logs**: Review application logs for debugging information

### Additional Resources
- **ERD Documentation**: `lab_appointment_erd.md`
- **User Stories**: `lab_appointment_user_story.md`
- **API Specification**: Available at `/openapi.json`
- **Health Monitoring**: `/health` endpoint for system status

---

## 📄 License
Hospital Management System License - See application configuration for details.

## 👥 Contact
- **API Support**: lab-api-support@hospital.example.com
- **Documentation**: https://hospital.example.com/support
- **Terms of Service**: https://hospital.example.com/terms