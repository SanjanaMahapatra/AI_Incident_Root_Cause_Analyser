package com.hackathon.rootcauseanalyser.AnalysisServiceMS.controller;


import com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto.AnalysisRequestDTO;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto.FeedbackDTO;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.entity.AnalysisResult;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.exception.AnalysisException;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.service.AnalysisService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/api/analysis")
public class AnalyseResultController {

    @Autowired
    private AnalysisService analysisService;

    @PostMapping
    public AnalysisResult requestAnalysis(@Valid @RequestBody AnalysisRequestDTO request) {
        Optional<AnalysisResult> optional = analysisService.requestAnalysis(request);
        return optional.orElseThrow(() -> new AnalysisException("Failed to analyse the incident: " + request.getIncidentId()));
    }

    @GetMapping("/{id}")
    public AnalysisResult getAnalysis(@PathVariable Long id) {
        return analysisService.getAnalysis(id);
    }

    @GetMapping("/incident/{incidentId}")
    public List<AnalysisResult> getByIncident(@PathVariable Long incidentId) {
        return analysisService.getAnalysesByIncident(incidentId);
    }

    @PutMapping("/{id}/feedback")
    public AnalysisResult addFeedback(@PathVariable Long id,
                                      @Valid @RequestBody FeedbackDTO feedbackDto) {
        return analysisService.addFeedback(id, feedbackDto);
    }
}
