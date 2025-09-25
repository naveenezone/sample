#!/usr/bin/env python3
"""
Script to populate the clinic system with sample patient data.
"""
from patient import Patient
from clinic import ClinicDataManager


def create_sample_data():
    """Create sample patient data for testing the clinic system."""
    
    manager = ClinicDataManager()
    
    # Sample patients data
    sample_patients = [
        {
            'patient_id': 'P001',
            'name': 'John Smith',
            'age': 35,
            'phone_number': '+1-555-0101',
            'email': 'john.smith@email.com',
            'address': '123 Main St, Anytown, ST 12345',
            'medical_history': 'Hypertension, controlled with medication'
        },
        {
            'patient_id': 'P002',
            'name': 'Sarah Johnson',
            'age': 28,
            'phone_number': '+1-555-0102',
            'email': 'sarah.johnson@email.com',
            'address': '456 Oak Ave, Somewhere, ST 67890',
            'medical_history': 'Diabetes Type 2, regular monitoring required'
        },
        {
            'patient_id': 'P003',
            'name': 'Michael Brown',
            'age': 42,
            'phone_number': '+1-555-0103',
            'email': 'michael.brown@email.com',
            'address': '789 Pine Rd, Elsewhere, ST 54321',
            'medical_history': 'Asthma, uses inhaler as needed'
        },
        {
            'patient_id': 'P004',
            'name': 'Emily Davis',
            'age': 67,
            'phone_number': '+1-555-0104',
            'email': 'emily.davis@email.com',
            'address': '321 Elm St, Nowhere, ST 98765',
            'medical_history': 'Arthritis, heart disease family history'
        },
        {
            'patient_id': 'P005',
            'name': 'David Wilson',
            'age': 23,
            'phone_number': '+1-555-0105',
            'email': 'david.wilson@email.com',
            'address': '654 Maple Dr, Anywhere, ST 13579',
            'medical_history': 'No significant medical history'
        },
        {
            'patient_id': 'P006',
            'name': 'Lisa Anderson',
            'age': 51,
            'phone_number': '+1-555-0106',
            'email': 'lisa.anderson@email.com',
            'address': '987 Cedar Ln, Someplace, ST 24680',
            'medical_history': 'Allergies to penicillin, seasonal allergies'
        },
        {
            'patient_id': 'P007',
            'name': 'Robert Taylor',
            'age': 39,
            'phone_number': '+1-555-0107',
            'address': '147 Birch Ct, Everytown, ST 36912',
            'medical_history': 'High cholesterol, exercise regularly'
        },
        {
            'patient_id': 'P008',
            'name': 'Jennifer Martinez',
            'age': 45,
            'phone_number': '+1-555-0108',
            'email': 'jennifer.martinez@email.com',
            'address': '258 Spruce St, Hometown, ST 47823',
            'medical_history': 'Migraine headaches, stress management'
        }
    ]
    
    print("Creating sample patient data...")
    added_count = 0
    
    for patient_data in sample_patients:
        patient = Patient(**patient_data)
        if manager.add_patient(patient):
            added_count += 1
            print(f"✓ Added patient: {patient.name}")
        else:
            print(f"✗ Failed to add patient: {patient.name} (may already exist)")
    
    print(f"\nSample data creation complete!")
    print(f"Added {added_count} new patients out of {len(sample_patients)} total.")
    print(f"Total patients in system: {manager.get_patient_count()}")
    
    # Display statistics
    stats = manager.get_statistics()
    print(f"\nClinic Statistics:")
    print(f"Average age: {stats['average_age']:.1f} years")
    print("Age distribution:")
    for age_group, count in stats['age_distribution'].items():
        print(f"  {age_group}: {count} patients")


if __name__ == "__main__":
    create_sample_data()