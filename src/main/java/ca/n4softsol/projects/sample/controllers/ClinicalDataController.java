package ca.n4softsol.projects.sample.controllers;

import ca.n4softsol.projects.sample.models.ClinicalData;
import ca.n4softsol.projects.sample.repositories.ClinicalDataRepository;
import ca.n4softsol.projects.sample.repositories.PatientRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.net.URI;
import java.util.List;
import java.time.Instant;
import java.sql.Timestamp;

@RestController
@RequestMapping("/api/clinicaldata")
public class ClinicalDataController {

    private final ClinicalDataRepository clinicalDataRepository;
    private final PatientRepository patientRepository;

    public ClinicalDataController(ClinicalDataRepository clinicalDataRepository, PatientRepository patientRepository) {
        this.clinicalDataRepository = clinicalDataRepository;
        this.patientRepository = patientRepository;
    }

    // List with optional filters
    @GetMapping
    public List<ClinicalData> list(@RequestParam(required = false) Long patientId,
                                   @RequestParam(required = false) String componentName) {
        if (patientId != null && componentName != null) {
            return clinicalDataRepository
                    .findByPatient_IdAndComponentNameOrderByMeasuredDateTimeDesc(patientId, componentName);
        }
        if (patientId != null) {
            return clinicalDataRepository.findByPatient_Id(patientId);
        }
        return clinicalDataRepository.findAll();
    }

    // Get one
    @GetMapping("/{id}")
    public ResponseEntity<ClinicalData> get(@PathVariable Long id) {
        return clinicalDataRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // Create. Accept patientId from query param or from payload.patient.id; 400 if missing.
    @PostMapping
    public ResponseEntity<ClinicalData> create(@RequestParam(name = "patientId", required = false) Long patientId,
                                               @RequestBody(required = false) ClinicalData payload) {
        Long resolvedPatientId = patientId;
        if (resolvedPatientId == null && payload != null && payload.getPatient() != null) {
            resolvedPatientId = payload.getPatient().getId();
        }
        if (resolvedPatientId == null) {
            return ResponseEntity.badRequest().build();
        }
        if (payload == null) {
            return ResponseEntity.badRequest().build();
        }
        Long finalPid = resolvedPatientId;
        return patientRepository.findById(finalPid)
                .map(patient -> {
                    payload.setId(null);
                    payload.setPatient(patient);
                    if (payload.getMeasuredDateTime() == null) {
                        // default to now if not provided
                        payload.setMeasuredDateTime(new java.sql.Timestamp(java.time.Instant.now().toEpochMilli()));
                    }
                    ClinicalData saved = clinicalDataRepository.save(payload);
                    return ResponseEntity.created(URI.create("/api/clinicaldata/" + saved.getId())).body(saved);
                })
                .orElseGet(() -> ResponseEntity.badRequest().build());
    }

    // Alternative create using path variable for patientId
    @PostMapping("/patient/{patientId}")
    public ResponseEntity<ClinicalData> createForPatient(@PathVariable Long patientId, @RequestBody(required = false) ClinicalData payload) {
        if (payload == null) {
            return ResponseEntity.badRequest().build();
        }
        return patientRepository.findById(patientId)
                .map(patient -> {
                    payload.setId(null);
                    payload.setPatient(patient);
                    if (payload.getMeasuredDateTime() == null) {
                        payload.setMeasuredDateTime(new java.sql.Timestamp(java.time.Instant.now().toEpochMilli()));
                    }
                    ClinicalData saved = clinicalDataRepository.save(payload);
                    return ResponseEntity.created(URI.create("/api/clinicaldata/" + saved.getId())).body(saved);
                })
                .orElseGet(() -> ResponseEntity.badRequest().build());
    }

    // Create using simple request params (no JSON body). Timestamp defaults to now.
    @PostMapping("/add")
    public ResponseEntity<ClinicalData> add(@RequestParam Long patientId,
                                            @RequestParam String componentName,
                                            @RequestParam String componentValue) {
        return patientRepository.findById(patientId)
                .map(patient -> {
                    ClinicalData data = new ClinicalData();
                    data.setComponentName(componentName);
                    data.setComponentValue(componentValue);
                    data.setMeasuredDateTime(Timestamp.from(Instant.now()));
                    data.setPatient(patient);
                    ClinicalData saved = clinicalDataRepository.save(data);
                    return ResponseEntity.created(URI.create("/api/clinicaldata/" + saved.getId())).body(saved);
                })
                .orElseGet(() -> ResponseEntity.badRequest().build());
    }

    // Alternative simple add using path variable for patientId
    @PostMapping("/patient/{patientId}/add")
    public ResponseEntity<ClinicalData> addForPatient(@PathVariable Long patientId,
                                                      @RequestParam String componentName,
                                                      @RequestParam String componentValue) {
        return add(patientId, componentName, componentValue);
    }

    // Update fields; optionally reassign to another patient via patientId
    @PutMapping("/{id}")
    public ResponseEntity<ClinicalData> update(@PathVariable Long id,
                                               @RequestParam(required = false) Long patientId,
                                               @RequestBody ClinicalData payload) {
        return clinicalDataRepository.findById(id)
                .map(existing -> {
                    existing.setComponentName(payload.getComponentName());
                    existing.setComponentValue(payload.getComponentValue());
                    existing.setMeasuredDateTime(payload.getMeasuredDateTime());
                    if (patientId != null) {
                        patientRepository.findById(patientId).ifPresent(existing::setPatient);
                    }
                    ClinicalData saved = clinicalDataRepository.save(existing);
                    return ResponseEntity.ok(saved);
                })
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // Delete
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!clinicalDataRepository.existsById(id)) {
            return ResponseEntity.notFound().build();
        }
        clinicalDataRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
