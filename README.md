# Clinic Data Management System

A comprehensive clinic data management system for handling patient information, built with Python. This system provides CRUD operations, data persistence, search functionality, and statistical reporting for clinic patient data.

## Features

- **Patient Management**: Add, view, update, and delete patient records
- **Data Persistence**: JSON-based data storage with automatic save/load
- **Search Functionality**: Search patients by name, phone number, or email
- **Statistics**: View clinic statistics including patient count, average age, and age distribution
- **CLI Interface**: User-friendly command-line interface for easy interaction
- **Data Validation**: Input validation and error handling
- **Testing**: Comprehensive unit test suite

## Quick Start

### 1. Initialize with Sample Data
```bash
python3 sample_data.py
```

### 2. Run the CLI Application
```bash
python3 clinic_cli.py
```

### 3. Run Tests
```bash
python3 test_clinic.py
```

## System Components

### Core Classes

#### `Patient` (patient.py)
Represents a patient with the following attributes:
- `patient_id`: Unique identifier
- `name`: Full name
- `age`: Patient age
- `phone_number`: Contact phone number
- `email`: Email address (optional)
- `address`: Home address (optional)
- `medical_history`: Brief medical history (optional)
- `created_at`: Record creation timestamp
- `updated_at`: Last update timestamp

#### `ClinicDataManager` (clinic.py)
Manages patient data with methods for:
- Adding new patients
- Retrieving patient information
- Updating patient records
- Deleting patients
- Searching patients
- Generating statistics
- Data persistence (JSON file storage)

### CLI Interface (clinic_cli.py)

Interactive command-line interface with the following options:
1. **Add Patient** - Create new patient records
2. **View Patient** - Display detailed patient information
3. **List All Patients** - Show summary of all patients
4. **Update Patient** - Modify existing patient information
5. **Delete Patient** - Remove patient records
6. **Search Patients** - Find patients by name, phone, or email
7. **View Statistics** - Display clinic statistics
8. **Exit** - Close the application

## Usage Examples

### Adding a New Patient
```python
from patient import Patient
from clinic import ClinicDataManager

# Create a clinic manager
manager = ClinicDataManager()

# Create a new patient
patient = Patient(
    patient_id="P009",
    name="Alice Cooper",
    age=29,
    phone_number="+1-555-0199",
    email="alice.cooper@email.com",
    address="123 Rock St, Music City, TN 12345",
    medical_history="No significant medical history"
)

# Add patient to the system
if manager.add_patient(patient):
    print("Patient added successfully!")
```

### Searching for Patients
```python
# Search by name
results = manager.search_patients("Smith")

# Search by phone number
results = manager.search_patients("555-0101")

# Search by email
results = manager.search_patients("alice.cooper")
```

### Getting Statistics
```python
stats = manager.get_statistics()
print(f"Total patients: {stats['total_patients']}")
print(f"Average age: {stats['average_age']:.1f}")
print("Age distribution:")
for age_group, count in stats['age_distribution'].items():
    print(f"  {age_group}: {count} patients")
```

## Data Storage

Patient data is stored in JSON format in `clinic_data.json`. The file structure is:

```json
{
  "patients": [
    {
      "patient_id": "P001",
      "name": "John Smith",
      "age": 35,
      "phone_number": "+1-555-0101",
      "email": "john.smith@email.com",
      "address": "123 Main St, Anytown, ST 12345",
      "medical_history": "Hypertension, controlled with medication",
      "created_at": "2024-01-01T10:00:00.000000",
      "updated_at": "2024-01-01T10:00:00.000000"
    }
  ]
}
```

## Testing

The system includes comprehensive unit tests covering:
- Patient object creation and manipulation
- Data manager CRUD operations
- Search functionality
- Statistics generation
- Data persistence

Run tests with:
```bash
python3 test_clinic.py -v
```

## Sample Data

The system comes with sample patient data that can be loaded using:
```bash
python3 sample_data.py
```

This creates 8 sample patient records with diverse demographics for testing and demonstration purposes.

## Requirements

- Python 3.6+
- No external dependencies (uses only Python standard library)

## File Structure

```
clinic-data-system/
├── README.md
├── requirements.txt
├── patient.py          # Patient data model
├── clinic.py           # Clinic data manager
├── clinic_cli.py       # Command-line interface
├── sample_data.py      # Sample data generator
├── test_clinic.py      # Unit tests
└── clinic_data.json    # Data storage file (created automatically)
```

## Contributing

When contributing to this project:
1. Run the test suite to ensure all tests pass
2. Add tests for new functionality
3. Follow the existing code style and documentation patterns
4. Update the README if adding new features

## License

This project is provided as-is for educational and demonstration purposes.
