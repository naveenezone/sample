package ca.n4softsol.projects.sample.controllers;

import ca.n4softsol.projects.sample.models.Patient;
import ca.n4softsol.projects.sample.repositories.PatientRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;

@RestController
@RequestMapping("/api/patients")
public class PatientController {

    private final PatientRepository patientRepository;

    public PatientController(PatientRepository patientRepository) {
        this.patientRepository = patientRepository;
    }

    // Read all
    @GetMapping
    public List<Patient> getAll() {
        return patientRepository.findAll();
    }

    // Read one
    @GetMapping("/{id}")
    public ResponseEntity<Patient> getById(@PathVariable Long id) {
        return patientRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // Create
    @PostMapping
    public ResponseEntity<Patient> create(@RequestBody Patient payload) {
        // Ignore incoming id to avoid accidental overwrite
        payload.setId(null);
        Patient saved = patientRepository.save(payload);
        return ResponseEntity.created(URI.create("/api/patients/" + saved.getId())).body(saved);
    }

    // Update (replace basic attributes)
    @PutMapping("/{id}")
    public ResponseEntity<Patient> update(@PathVariable Long id, @RequestBody Patient payload) {
        return patientRepository.findById(id)
                .map(existing -> {
                    existing.setFirstName(payload.getFirstName());
                    existing.setLastName(payload.getLastName());
                    existing.setAge(payload.getAge());
                    // For simplicity, clinicalData updates are not handled here
                    Patient saved = patientRepository.save(existing);
                    return ResponseEntity.ok(saved);
                })
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // Delete
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!patientRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        patientRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
