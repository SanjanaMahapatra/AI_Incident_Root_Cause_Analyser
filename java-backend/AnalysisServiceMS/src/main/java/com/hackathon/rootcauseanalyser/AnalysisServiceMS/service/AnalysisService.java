package com.hackathon.rootcauseanalyser.AnalysisServiceMS.service;

import com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto.AnalysisRequestDTO;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto.FeedbackDTO;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.entity.AnalysisResult;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.entity.AnalysisStatus;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.exception.AnalysisException;
import com.hackathon.rootcauseanalyser.AnalysisServiceMS.repository.AnalysisRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.http.HttpStatus;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Slf4j
@Service
@RequiredArgsConstructor
public class AnalysisService {

    private final AnalysisRepository analysisRepository;
    private final RestTemplate restTemplate;

    @Value("${python.genai.url}")
    private String pythonGenAiUrl;

    /**
     * Request a new analysis. Saves a PENDING record and triggers async call to Python.
     */
    public Optional<AnalysisResult> requestAnalysis(AnalysisRequestDTO request){
        AnalysisResult result = null;
        // Async call to Python GenAI service
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            Map<String, Object> payload = new HashMap<>();
            payload.put("incident_id", request.getIncidentId());
            payload.put("analysis_type", request.getAnalysisType());

            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(payload, headers);
            ResponseEntity<String> response = restTemplate.postForEntity(pythonGenAiUrl, entity, String.class);

            HttpStatusCode statusCode = response.getStatusCode();
            String responseBody = response.getBody();

            if(statusCode.is2xxSuccessful()) {
                result = AnalysisResult.builder()
                        .incidentId(request.getIncidentId())
                        .analysisType(request.getAnalysisType())
                        .status(AnalysisStatus.APPROVED)
                        .resultText(responseBody)
                        .build();

                analysisRepository.save(result);

            }else{
                throw new AnalysisException("Error when returning AI response from GenAI service with status: " + statusCode + "and response: " + responseBody);
            }

            return Optional.of(result);

        }catch(Exception e) {
            log.error("Error when returning AI response from GenAI service for incidentId {} : {}", request.getIncidentId(), e.getMessage());
            result = AnalysisResult.builder()
                    .incidentId(request.getIncidentId())
                    .analysisType(request.getAnalysisType())
                    .status(AnalysisStatus.PENDING)
                    .resultText("Error: " + e.getMessage())
                    .build();
            return Optional.of(result);
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