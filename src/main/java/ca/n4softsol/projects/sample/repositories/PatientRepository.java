package ca.n4softsol.projects.sample.repositories;

import ca.n4softsol.projects.sample.models.Patient;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PatientRepository extends JpaRepository<Patient, Long> {
    // Add derived queries here if needed, e.g., List<Patient> findByLastName(String lastName);
}
