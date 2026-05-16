package com.hackathon.rootcauseanalyser.AnalysisServiceMS.service;

import com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto.AnalysisRequestDTO;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto.FeedbackDTO;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.entity.AnalysisResult;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.entity.AnalysisStatus;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.repository.AnalysisRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class AnalysisService {

    private final AnalysisRepository analysisRepository;
    private final RestTemplate restTemplate;

    @Value("${python.genai.url:http://localhost:5000/analyze}")
    private String pythonGenAiUrl;

    /**
     * Request a new analysis. Saves a PENDING record and triggers async call to Python.
     */
    public AnalysisResult requestAnalysis(AnalysisRequestDTO request) {
        AnalysisResult result = AnalysisResult.builder()
                .incidentId(request.getIncidentId())
                .analysisType(request.getAnalysisType())
                .status(AnalysisStatus.PENDING)
                .build();
        AnalysisResult saved = analysisRepository.save(result);

        // Async call to Python GenAI service
        callPythonGenAiAsync(saved.getId(), request.getIncidentId(), request.getAnalysisType());

        return saved;
    }

    @Async
    protected void callPythonGenAiAsync(Long analysisId, Long incidentId, String analysisType) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, Object> payload = new HashMap<>();
            payload.put("analysis_id", analysisId);
            payload.put("incident_id", incidentId);
            payload.put("analysis_type", analysisType);

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);
            String response = restTemplate.postForObject(pythonGenAiUrl, entity, String.class);

            // Update the analysis result with the response
            AnalysisResult result = analysisRepository.findById(analysisId)
                    .orElseThrow(() -> new RuntimeException("Analysis not found: " + analysisId));
            result.setResultText(response);
            // Keep status PENDING until human approves
            analysisRepository.save(result);
            log.info("Analysis {} completed successfully", analysisId);

        } catch (Exception e) {
            log.error("Error calling Python GenAI service for analysis {}: {}", analysisId, e.getMessage());
            AnalysisResult result = analysisRepository.findById(analysisId)
                    .orElseThrow(() -> new RuntimeException("Analysis not found: " + analysisId));
            result.setResultText("Error: " + e.getMessage());
            analysisRepository.save(result);
        }
    }

    public AnalysisResult getAnalysis(Long id) {
        return analysisRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Analysis not found with id: " + id));
    }

    public List<AnalysisResult> getAnalysesByIncident(Long incidentId) {
        return analysisRepository.findByIncidentId(incidentId);
    }

    public AnalysisResult addFeedback(Long id, FeedbackDTO feedbackDto) {
        AnalysisResult result = getAnalysis(id);
        result.setFeedback(feedbackDto.getFeedback());
        result.setStatus(feedbackDto.getStatus());
        return analysisRepository.save(result);
    }
}