package com.hackathon.rootcauseanalyser.IncidentServiceMS.controller;

import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.Alert;
import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.Incident;
import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.IncidentStatus;
import com.hackathon.rootcauseanalyser.IncidentServiceMS.repository.AlertRepository;
import com.hackathon.rootcauseanalyser.IncidentServiceMS.service.IncidentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.*;

@RestController
@RequestMapping("/api/incidents")
public class IncidentController {
    @Autowired
    private IncidentService incidentService;
    @Autowired private AlertRepository alertRepo;

    @PostMapping
    public Incident createIncident(@RequestBody Incident incident) {
        return incidentService.createIncident(incident);
    }

    @GetMapping
    public List<Incident> listIncidents(@RequestParam(required = false) IncidentStatus status) {
        if (status != null) {
            return incidentService.getIncidentsByStatus(status);
        } else {
            return incidentService.getAllIncidents();
        }
    }

    @GetMapping("/{id}")
    public Incident getIncident(@PathVariable Long id) {
        return incidentService.getIncident(id);
    }

    @PutMapping("/{id}")
    public Incident updateIncident(@PathVariable Long id, @RequestBody Incident incident) {
        return incidentService.updateIncident(id, incident);
    }

    @DeleteMapping("/{id}")
    public void deleteIncident(@PathVariable Long id) {
        incidentService.deleteIncident(id);
    }

    @PostMapping("/{id}/alerts")
    public Alert addAlert(@PathVariable Long id, @RequestBody Alert alert) {
        Incident incident = incidentService.getIncident(id);
        alert.setIncident(incident);
        alert.setTriggeredAt(LocalDateTime.now());
        return alertRepo.save(alert);
    }

    @GetMapping("/{id}/alerts")
    public List<Alert> getAlertsForIncident(@PathVariable Long id) {
        return alertRepo.findByIncidentId(id);
    }
}
