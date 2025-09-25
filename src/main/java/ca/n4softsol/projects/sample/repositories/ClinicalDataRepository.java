package ca.n4softsol.projects.sample.repositories;

import ca.n4softsol.projects.sample.models.ClinicalData;
import ca.n4softsol.projects.sample.models.Patient;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ClinicalDataRepository extends JpaRepository<ClinicalData, Long> {
    // Find all clinical data for a given patient
    List<ClinicalData> findByPatient(Patient patient);

    // Or by patient id for convenience
    List<ClinicalData> findByPatient_Id(Long patientId);

    // Filter by component name
    List<ClinicalData> findByPatient_IdAndComponentNameOrderByMeasuredDateTimeDesc(Long patientId, String componentName);
}
