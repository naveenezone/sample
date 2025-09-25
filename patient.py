"""
Patient data model for clinic management system.
"""
from datetime import datetime
from typing import Optional, Dict, Any
import json


class Patient:
    """Represents a patient in the clinic system."""
    
    def __init__(self, patient_id: str, name: str, age: int, 
                 phone_number: str, email: Optional[str] = None,
                 address: Optional[str] = None, medical_history: Optional[str] = None):
        """
        Initialize a Patient object.
        
        Args:
            patient_id: Unique identifier for the patient
            name: Full name of the patient
            age: Age of the patient
            phone_number: Contact phone number
            email: Email address (optional)
            address: Home address (optional)
            medical_history: Brief medical history (optional)
        """
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.medical_history = medical_history
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert patient object to dictionary."""
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'age': self.age,
            'phone_number': self.phone_number,
            'email': self.email,
            'address': self.address,
            'medical_history': self.medical_history,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Patient':
        """Create patient object from dictionary."""
        patient = cls(
            patient_id=data['patient_id'],
            name=data['name'],
            age=data['age'],
            phone_number=data['phone_number'],
            email=data.get('email'),
            address=data.get('address'),
            medical_history=data.get('medical_history')
        )
        if 'created_at' in data:
            patient.created_at = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            patient.updated_at = datetime.fromisoformat(data['updated_at'])
        return patient
    
    def update(self, **kwargs):
        """Update patient information."""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['patient_id', 'created_at']:
                setattr(self, key, value)
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        """String representation of patient."""
        return f"Patient({self.patient_id}): {self.name}, Age: {self.age}"
    
    def __repr__(self) -> str:
        """Detailed representation of patient."""
        return (f"Patient(patient_id='{self.patient_id}', name='{self.name}', "
                f"age={self.age}, phone_number='{self.phone_number}')")