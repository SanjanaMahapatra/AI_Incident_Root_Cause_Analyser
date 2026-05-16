package com.hackathon.rootcauseanalyser.IncidentServiceMS.repository;

import com.hackathon.rootcauseanalyser.IncidentServiceMS.entity.Alert;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AlertRepository extends JpaRepository<Alert, Long> {
    List<Alert> findByIncidentId(Long incidentId);
}
