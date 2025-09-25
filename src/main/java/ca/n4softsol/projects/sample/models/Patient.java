package ca.n4softsol.projects.sample.models;

import jakarta.persistence.*;

import com.fasterxml.jackson.annotation.JsonIgnore;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "patient")
public class Patient {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "first_name", nullable = false, length = 100)
    private String firstName;

    @Column(name = "last_name", nullable = false, length = 100)
    private String lastName;

    @Column(nullable = false)
    private Integer age;

    // Each patient can have multiple clinical data entries
    @OneToMany(mappedBy = "patient", cascade = CascadeType.ALL, fetch = FetchType.EAGER)
    @JsonIgnore
    private List<ClinicalData> clinicalData;

    public Patient() {
    }

    public Patient(String firstName, String lastName, Integer age) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
    }

    public Long getId() {
        return id;
    }

    public Patient setId(Long id) {
        this.id = id;
        return this;
    }

    public String getFirstName() {
        return firstName;
    }

    public Patient setFirstName(String firstName) {
        this.firstName = firstName;
        return this;
    }

    public String getLastName() {
        return lastName;
    }

    public Patient setLastName(String lastName) {
        this.lastName = lastName;
        return this;
    }

    public Integer getAge() {
        return age;
    }

    public Patient setAge(Integer age) {
        this.age = age;
        return this;
    }

    public List<ClinicalData> getClinicalData() {
        return clinicalData;
    }

    public Patient setClinicalData(List<ClinicalData> clinicalData) {
        this.clinicalData = clinicalData != null ? clinicalData : new ArrayList<>();
        return this;
    }

    public Patient addClinicalData(ClinicalData data) {
        if (data == null)
            return this;
        clinicalData.add(data);
        data.setPatient(this);
        return this;
    }

    public Patient removeClinicalData(ClinicalData data) {
        if (data == null)
            return this;
        clinicalData.remove(data);
        data.setPatient(null);
        return this;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o)
            return true;
        if (o == null || getClass() != o.getClass())
            return false;

        Patient patient = (Patient) o;
        return id != null && id.equals(patient.id);
    }

    @Override
    public int hashCode() {
        return 31;
    }

    @Override
    public String toString() {
        return "Patient{" +
                "id=" + id +
                ", firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", age=" + age +
                '}';
    }
}