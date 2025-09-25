#!/usr/bin/env python3
"""
Unit tests for the clinic data management system.
"""
import unittest
import os
import tempfile
from patient import Patient
from clinic import ClinicDataManager


class TestPatient(unittest.TestCase):
    """Test cases for the Patient class."""
    
    def setUp(self):
        """Set up test patient data."""
        self.patient_data = {
            'patient_id': 'TEST001',
            'name': 'Test Patient',
            'age': 30,
            'phone_number': '+1-555-0123',
            'email': 'test@email.com',
            'address': '123 Test St',
            'medical_history': 'No significant history'
        }
    
    def test_patient_creation(self):
        """Test patient object creation."""
        patient = Patient(**self.patient_data)
        self.assertEqual(patient.patient_id, 'TEST001')
        self.assertEqual(patient.name, 'Test Patient')
        self.assertEqual(patient.age, 30)
        self.assertEqual(patient.phone_number, '+1-555-0123')
        self.assertEqual(patient.email, 'test@email.com')
    
    def test_patient_to_dict(self):
        """Test converting patient to dictionary."""
        patient = Patient(**self.patient_data)
        patient_dict = patient.to_dict()
        
        self.assertEqual(patient_dict['patient_id'], 'TEST001')
        self.assertEqual(patient_dict['name'], 'Test Patient')
        self.assertEqual(patient_dict['age'], 30)
        self.assertIn('created_at', patient_dict)
        self.assertIn('updated_at', patient_dict)
    
    def test_patient_from_dict(self):
        """Test creating patient from dictionary."""
        patient = Patient(**self.patient_data)
        patient_dict = patient.to_dict()
        
        new_patient = Patient.from_dict(patient_dict)
        self.assertEqual(new_patient.patient_id, patient.patient_id)
        self.assertEqual(new_patient.name, patient.name)
        self.assertEqual(new_patient.age, patient.age)
    
    def test_patient_update(self):
        """Test updating patient information."""
        patient = Patient(**self.patient_data)
        original_updated_at = patient.updated_at
        
        patient.update(name='Updated Name', age=31)
        
        self.assertEqual(patient.name, 'Updated Name')
        self.assertEqual(patient.age, 31)
        self.assertGreater(patient.updated_at, original_updated_at)
    
    def test_patient_str_representation(self):
        """Test string representation of patient."""
        patient = Patient(**self.patient_data)
        patient_str = str(patient)
        
        self.assertIn('TEST001', patient_str)
        self.assertIn('Test Patient', patient_str)
        self.assertIn('30', patient_str)


class TestClinicDataManager(unittest.TestCase):
    """Test cases for the ClinicDataManager class."""
    
    def setUp(self):
        """Set up test environment."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.manager = ClinicDataManager(self.temp_file.name)
        
        self.test_patient = Patient(
            patient_id='TEST001',
            name='Test Patient',
            age=25,
            phone_number='+1-555-0123',
            email='test@email.com'
        )
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_add_patient(self):
        """Test adding a patient."""
        result = self.manager.add_patient(self.test_patient)
        self.assertTrue(result)
        self.assertEqual(self.manager.get_patient_count(), 1)
        
        # Test adding duplicate patient
        duplicate_result = self.manager.add_patient(self.test_patient)
        self.assertFalse(duplicate_result)
        self.assertEqual(self.manager.get_patient_count(), 1)
    
    def test_get_patient(self):
        """Test retrieving a patient."""
        self.manager.add_patient(self.test_patient)
        
        retrieved_patient = self.manager.get_patient('TEST001')
        self.assertIsNotNone(retrieved_patient)
        self.assertEqual(retrieved_patient.name, 'Test Patient')
        
        # Test getting non-existent patient
        non_existent = self.manager.get_patient('NONEXISTENT')
        self.assertIsNone(non_existent)
    
    def test_update_patient(self):
        """Test updating patient information."""
        self.manager.add_patient(self.test_patient)
        
        result = self.manager.update_patient('TEST001', name='Updated Name', age=26)
        self.assertTrue(result)
        
        updated_patient = self.manager.get_patient('TEST001')
        self.assertEqual(updated_patient.name, 'Updated Name')
        self.assertEqual(updated_patient.age, 26)
        
        # Test updating non-existent patient
        result = self.manager.update_patient('NONEXISTENT', name='Test')
        self.assertFalse(result)
    
    def test_delete_patient(self):
        """Test deleting a patient."""
        self.manager.add_patient(self.test_patient)
        self.assertEqual(self.manager.get_patient_count(), 1)
        
        result = self.manager.delete_patient('TEST001')
        self.assertTrue(result)
        self.assertEqual(self.manager.get_patient_count(), 0)
        
        # Test deleting non-existent patient
        result = self.manager.delete_patient('NONEXISTENT')
        self.assertFalse(result)
    
    def test_search_patients(self):
        """Test searching for patients."""
        # Add multiple patients
        patient1 = Patient('P001', 'John Smith', 30, '+1-555-0001', 'john@email.com')
        patient2 = Patient('P002', 'Jane Johnson', 25, '+1-555-0002', 'jane@email.com')
        patient3 = Patient('P003', 'Bob Smith', 40, '+1-555-0003', 'bob@email.com')
        
        self.manager.add_patient(patient1)
        self.manager.add_patient(patient2)
        self.manager.add_patient(patient3)
        
        # Search by name
        results = self.manager.search_patients('Smith')
        self.assertEqual(len(results), 2)
        
        # Search by phone
        results = self.manager.search_patients('555-0002')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'Jane Johnson')
        
        # Search by email
        results = self.manager.search_patients('john@email.com')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, 'John Smith')
    
    def test_get_statistics(self):
        """Test getting clinic statistics."""
        # Test empty statistics
        stats = self.manager.get_statistics()
        self.assertEqual(stats['total_patients'], 0)
        self.assertEqual(stats['average_age'], 0)
        
        # Add patients and test statistics
        patients = [
            Patient('P001', 'Patient 1', 20, '+1-555-0001'),
            Patient('P002', 'Patient 2', 30, '+1-555-0002'),
            Patient('P003', 'Patient 3', 40, '+1-555-0003'),
            Patient('P004', 'Patient 4', 60, '+1-555-0004')
        ]
        
        for patient in patients:
            self.manager.add_patient(patient)
        
        stats = self.manager.get_statistics()
        self.assertEqual(stats['total_patients'], 4)
        self.assertEqual(stats['average_age'], 37.5)
        self.assertIn('age_distribution', stats)
    
    def test_data_persistence(self):
        """Test that data persists across manager instances."""
        # Add patient to first manager
        self.manager.add_patient(self.test_patient)
        
        # Create new manager with same file
        new_manager = ClinicDataManager(self.temp_file.name)
        
        # Check that patient was loaded
        self.assertEqual(new_manager.get_patient_count(), 1)
        retrieved_patient = new_manager.get_patient('TEST001')
        self.assertIsNotNone(retrieved_patient)
        self.assertEqual(retrieved_patient.name, 'Test Patient')


if __name__ == '__main__':
    unittest.main()