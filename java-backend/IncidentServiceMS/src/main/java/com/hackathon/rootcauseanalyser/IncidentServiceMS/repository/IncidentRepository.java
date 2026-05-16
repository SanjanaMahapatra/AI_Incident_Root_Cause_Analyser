package com.hackathon.rootcauseanalyser.IncidentServiceMS.repository;

import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.Incident;
import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.IncidentStatus;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface IncidentRepository extends JpaRepository<Incident, Long> {
    List<Incident> findByStatus(IncidentStatus status);
}