package com.hackathon.rootcauseanalyser.IncidentServiceMS.service;

import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.Incident;
import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.IncidentStatus;
import com.hackathon.rootcauseanalyser.IncidentServiceMS.repository.IncidentRepository;
import jakarta.transaction.Transactional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.beans.Transient;
import java.util.List;

@Service
public class IncidentService {
    @Autowired
    private IncidentRepository incidentRepo;

    public Incident createIncident(Incident incident) {
        return incidentRepo.save(incident);
    }

    public Incident getIncident(Long id) {
        return incidentRepo.findById(id)
                .orElseThrow(() -> new RuntimeException("Incident not found with id: " + id));
    }

    public List<Incident> getAllIncidents() {
        return incidentRepo.findAll();
    }

    public List<Incident> getIncidentsByStatus(IncidentStatus status) {
        return incidentRepo.findByStatus(status);
    }

    @Transactional
    public Incident updateIncident(Long id, Incident updated) {
        Incident existing = incidentRepo.findById(id).orElseThrow();
        existing.setTitle(updated.getTitle());
        existing.setDescription(updated.getDescription());
        existing.setStatus(updated.getStatus());
        existing.setAssignedTo(updated.getAssignedTo());
        existing.setLogIds(updated.getLogIds());
        return incidentRepo.save(existing);
    }

    public void deleteIncident(Long id) {
        incidentRepo.deleteById(id);
    }
}