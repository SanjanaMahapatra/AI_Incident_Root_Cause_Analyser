package com.hackathon.rootcauseanalyser.AnalysisServiceMS.repository;

import com.hackathon.rootcauseanalyser.AnalysisServiceMS.entity.AnalysisResult;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface AnalysisRepository extends JpaRepository<AnalysisResult, Long>  {

    List<AnalysisResult> findByIncidentId(Long incidentId);
}
