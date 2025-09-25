"""
Clinic data management system.
"""
import json
import os
from typing import List, Optional, Dict, Any
from patient import Patient


class ClinicDataManager:
    """Manages clinic patient data with persistent storage."""
    
    def __init__(self, data_file: str = "clinic_data.json"):
        """
        Initialize the clinic data manager.
        
        Args:
            data_file: Path to the JSON file for data persistence
        """
        self.data_file = data_file
        self.patients: Dict[str, Patient] = {}
        self.load_data()
    
    def load_data(self):
        """Load patient data from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    for patient_data in data.get('patients', []):
                        patient = Patient.from_dict(patient_data)
                        self.patients[patient.patient_id] = patient
                print(f"Loaded {len(self.patients)} patients from {self.data_file}")
            except Exception as e:
                print(f"Error loading data: {e}")
                self.patients = {}
    
    def save_data(self):
        """Save patient data to file."""
        try:
            data = {
                'patients': [patient.to_dict() for patient in self.patients.values()]
            }
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Saved {len(self.patients)} patients to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_patient(self, patient: Patient) -> bool:
        """
        Add a new patient to the system.
        
        Args:
            patient: Patient object to add
            
        Returns:
            True if patient was added successfully, False if patient ID already exists
        """
        if patient.patient_id in self.patients:
            return False
        
        self.patients[patient.patient_id] = patient
        self.save_data()
        return True
    
    def get_patient(self, patient_id: str) -> Optional[Patient]:
        """
        Get a patient by ID.
        
        Args:
            patient_id: ID of the patient to retrieve
            
        Returns:
            Patient object if found, None otherwise
        """
        return self.patients.get(patient_id)
    
    def get_all_patients(self) -> List[Patient]:
        """Get all patients in the system."""
        return list(self.patients.values())
    
    def update_patient(self, patient_id: str, **kwargs) -> bool:
        """
        Update patient information.
        
        Args:
            patient_id: ID of the patient to update
            **kwargs: Fields to update
            
        Returns:
            True if patient was updated successfully, False if patient not found
        """
        patient = self.patients.get(patient_id)
        if not patient:
            return False
        
        patient.update(**kwargs)
        self.save_data()
        return True
    
    def delete_patient(self, patient_id: str) -> bool:
        """
        Delete a patient from the system.
        
        Args:
            patient_id: ID of the patient to delete
            
        Returns:
            True if patient was deleted successfully, False if patient not found
        """
        if patient_id not in self.patients:
            return False
        
        del self.patients[patient_id]
        self.save_data()
        return True
    
    def search_patients(self, query: str) -> List[Patient]:
        """
        Search patients by name or phone number.
        
        Args:
            query: Search query
            
        Returns:
            List of matching patients
        """
        query = query.lower()
        results = []
        
        for patient in self.patients.values():
            if (query in patient.name.lower() or 
                query in patient.phone_number or
                (patient.email and query in patient.email.lower())):
                results.append(patient)
        
        return results
    
    def get_patient_count(self) -> int:
        """Get total number of patients."""
        return len(self.patients)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get clinic statistics."""
        if not self.patients:
            return {
                'total_patients': 0,
                'average_age': 0,
                'age_distribution': {}
            }
        
        ages = [patient.age for patient in self.patients.values()]
        age_groups = {
            '0-18': len([age for age in ages if age <= 18]),
            '19-35': len([age for age in ages if 19 <= age <= 35]),
            '36-55': len([age for age in ages if 36 <= age <= 55]),
            '56+': len([age for age in ages if age >= 56])
        }
        
        return {
            'total_patients': len(self.patients),
            'average_age': sum(ages) / len(ages),
            'age_distribution': age_groups
        }