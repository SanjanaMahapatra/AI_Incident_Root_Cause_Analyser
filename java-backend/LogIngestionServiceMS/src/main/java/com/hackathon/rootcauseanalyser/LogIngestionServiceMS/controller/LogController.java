package com.hackathon.rootcauseanalyser.LogIngestionServiceMS.controller;

import com.hackathon.rootcauseanalyser.LogIngestionServiceMS.dto.LogEntryDTO;
import com.hackathon.rootcauseanalyser.LogIngestionServiceMS.entity.LogEntry;
import com.hackathon.rootcauseanalyser.LogIngestionServiceMS.service.LogIngestionService;
import org.springframework.data.jpa.domain.Specification;
import static org.springframework.data.jpa.domain.Specification.where;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.*;

@RestController
@RequestMapping("/api/logs")
public class LogController {

    private final LogIngestionService logIngestionService;

    public LogController(LogIngestionService logIngestionService) {
        this.logIngestionService = logIngestionService;
    }

    @PostMapping("/ingest")
    public List<LogEntry> ingestLogs(@RequestBody List<LogEntryDTO> logs) {
        return logIngestionService.ingestLogs(logs);
    }

    @GetMapping
    public List<LogEntry> getLogs(
            @RequestParam(required = false) String logLevel,
            @RequestParam(required = false) String serviceName,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime from,
            @RequestParam(required = false) @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime to) {

        Specification<LogEntry> spec = where((Specification<LogEntry>) null);
        if (logLevel != null) spec = spec.and((root, q, cb) -> cb.equal(root.get("logLevel"), logLevel));
        if (serviceName != null) spec = spec.and((root, q, cb) -> cb.equal(root.get("serviceName"), serviceName));
        if (from != null) spec = spec.and((root, q, cb) -> cb.greaterThanOrEqualTo(root.get("timestamp"), from));
        if (to != null) spec = spec.and((root, q, cb) -> cb.lessThanOrEqualTo(root.get("timestamp"), to));
        return logIngestionService.getLogs(spec);
    }

    @GetMapping("/{id}")
    public LogEntry getLog(@PathVariable Long id) {
        return logIngestionService.getLogById(id);
    }

}
