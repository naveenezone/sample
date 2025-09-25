#!/usr/bin/env python3
"""
Command Line Interface for Clinic Data Management System.
"""
import sys
from typing import Optional
from patient import Patient
from clinic import ClinicDataManager


class ClinicCLI:
    """Command line interface for clinic data management."""
    
    def __init__(self):
        """Initialize the CLI with a clinic data manager."""
        self.manager = ClinicDataManager()
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("         CLINIC DATA MANAGEMENT SYSTEM")
        print("="*50)
        print("1. Add Patient")
        print("2. View Patient")
        print("3. List All Patients")
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Search Patients")
        print("7. View Statistics")
        print("8. Exit")
        print("-"*50)
    
    def get_input(self, prompt: str, required: bool = True) -> Optional[str]:
        """Get input from user with validation."""
        while True:
            value = input(prompt).strip()
            if value or not required:
                return value if value else None
            print("This field is required. Please enter a value.")
    
    def get_int_input(self, prompt: str, min_val: int = 0, max_val: int = 150) -> int:
        """Get integer input with validation."""
        while True:
            try:
                value = int(input(prompt))
                if min_val <= value <= max_val:
                    return value
                print(f"Please enter a value between {min_val} and {max_val}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def add_patient(self):
        """Add a new patient."""
        print("\n--- Add New Patient ---")
        
        patient_id = self.get_input("Patient ID: ")
        if self.manager.get_patient(patient_id):
            print(f"Error: Patient with ID '{patient_id}' already exists!")
            return
        
        name = self.get_input("Full Name: ")
        age = self.get_int_input("Age: ", 0, 150)
        phone_number = self.get_input("Phone Number: ")
        email = self.get_input("Email (optional): ", required=False)
        address = self.get_input("Address (optional): ", required=False)
        medical_history = self.get_input("Medical History (optional): ", required=False)
        
        patient = Patient(
            patient_id=patient_id,
            name=name,
            age=age,
            phone_number=phone_number,
            email=email,
            address=address,
            medical_history=medical_history
        )
        
        if self.manager.add_patient(patient):
            print(f"✓ Patient with ID '{patient_id}' added successfully!")
        else:
            print("✗ Failed to add patient.")
    
    def view_patient(self):
        """View a specific patient."""
        print("\n--- View Patient ---")
        patient_id = self.get_input("Enter Patient ID: ")
        
        patient = self.manager.get_patient(patient_id)
        if not patient:
            print(f"✗ Patient with ID '{patient_id}' not found!")
            return
        
        self.display_patient_details(patient)
    
    def display_patient_details(self, patient: Patient):
        """Display detailed patient information with privacy protection."""
        print(f"\n--- Patient Details ---")
        print(f"ID: {patient.patient_id}")
        print(f"Name: {patient.name}")
        print(f"Age: {patient.age}")
        print(f"Phone: {self._mask_sensitive_data(patient.phone_number)}")
        print(f"Email: {self._mask_sensitive_data(patient.email) if patient.email else 'Not provided'}")
        print(f"Address: {'[ADDRESS PROVIDED]' if patient.address else 'Not provided'}")
        print(f"Medical History: {'[MEDICAL HISTORY ON FILE]' if patient.medical_history else 'Not provided'}")
        print(f"Created: {patient.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Updated: {patient.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
    
    def _mask_sensitive_data(self, data: str) -> str:
        """Mask sensitive data for display purposes."""
        if not data or len(data) < 4:
            return "[PROTECTED]"
        return data[:2] + "*" * (len(data) - 4) + data[-2:]
    
    def list_all_patients(self):
        """List all patients."""
        print("\n--- All Patients ---")
        patients = self.manager.get_all_patients()
        
        if not patients:
            print("No patients found in the system.")
            return
        
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Phone':<15}")
        print("-" * 50)
        for patient in patients:
            print(f"{patient.patient_id:<10} {patient.name:<20} {patient.age:<5} {self._mask_sensitive_data(patient.phone_number):<15}")
    
    def update_patient(self):
        """Update patient information."""
        print("\n--- Update Patient ---")
        patient_id = self.get_input("Enter Patient ID to update: ")
        
        patient = self.manager.get_patient(patient_id)
        if not patient:
            print(f"✗ Patient with ID '{patient_id}' not found!")
            return
        
        print(f"Current patient ID: {patient.patient_id}")
        print("Leave fields empty to keep current values:")
        
        name = self.get_input(f"Name [current: {patient.name}]: ", required=False)
        age_str = input(f"Age [current: {patient.age}]: ").strip()
        age = int(age_str) if age_str else None
        phone_number = self.get_input(f"Phone [current: ***]: ", required=False)
        email = self.get_input(f"Email [current: ***]: ", required=False)
        address = self.get_input(f"Address [current: ***]: ", required=False)
        medical_history = self.get_input(f"Medical History [current: ***]: ", required=False)
        
        updates = {}
        if name: updates['name'] = name
        if age is not None: updates['age'] = age
        if phone_number: updates['phone_number'] = phone_number
        if email: updates['email'] = email
        if address: updates['address'] = address
        if medical_history: updates['medical_history'] = medical_history
        
        if updates:
            if self.manager.update_patient(patient_id, **updates):
                print("✓ Patient updated successfully!")
            else:
                print("✗ Failed to update patient.")
        else:
            print("No changes made.")
    
    def delete_patient(self):
        """Delete a patient."""
        print("\n--- Delete Patient ---")
        patient_id = self.get_input("Enter Patient ID to delete: ")
        
        patient = self.manager.get_patient(patient_id)
        if not patient:
            print(f"✗ Patient with ID '{patient_id}' not found!")
            return
        
        print(f"Patient to delete: ID {patient_id}")
        confirm = input("Are you sure? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            if self.manager.delete_patient(patient_id):
                print("✓ Patient deleted successfully!")
            else:
                print("✗ Failed to delete patient.")
        else:
            print("Deletion cancelled.")
    
    def search_patients(self):
        """Search for patients."""
        print("\n--- Search Patients ---")
        query = self.get_input("Enter search query (name, phone, or email): ")
        
        results = self.manager.search_patients(query)
        
        if not results:
            print("No patients found matching your search.")
            return
        
        print(f"\nFound {len(results)} patient(s):")
        print(f"{'ID':<10} {'Name':<20} {'Age':<5} {'Phone':<15}")
        print("-" * 50)
        for patient in results:
            print(f"{patient.patient_id:<10} {patient.name:<20} {patient.age:<5} {self._mask_sensitive_data(patient.phone_number):<15}")
    
    def view_statistics(self):
        """View clinic statistics."""
        print("\n--- Clinic Statistics ---")
        stats = self.manager.get_statistics()
        
        print(f"Total Patients: {stats['total_patients']}")
        if stats['total_patients'] > 0:
            print(f"Average Age: {stats['average_age']:.1f} years")
            print("\nAge Distribution:")
            for age_group, count in stats['age_distribution'].items():
                print(f"  {age_group}: {count} patients")
    
    def run(self):
        """Run the CLI application."""
        print("Welcome to the Clinic Data Management System!")
        
        while True:
            try:
                self.display_menu()
                choice = input("Select an option (1-8): ").strip()
                
                if choice == '1':
                    self.add_patient()
                elif choice == '2':
                    self.view_patient()
                elif choice == '3':
                    self.list_all_patients()
                elif choice == '4':
                    self.update_patient()
                elif choice == '5':
                    self.delete_patient()
                elif choice == '6':
                    self.search_patients()
                elif choice == '7':
                    self.view_statistics()
                elif choice == '8':
                    print("\nThank you for using the Clinic Data Management System!")
                    break
                else:
                    print("Invalid option. Please select 1-8.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                input("Press Enter to continue...")


if __name__ == "__main__":
    cli = ClinicCLI()
    cli.run()