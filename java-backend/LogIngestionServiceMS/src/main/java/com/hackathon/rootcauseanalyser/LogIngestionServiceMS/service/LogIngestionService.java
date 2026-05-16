package com.hackathon.rootcauseanalyser.LogIngestionServiceMS.service;

import com.hackathon.rootcauseanalyser.LogIngestionServiceMS.dto.LogEntryDTO;
import com.hackathon.rootcauseanalyser.LogIngestionServiceMS.entity.LogEntry;
import com.hackathon.rootcauseanalyser.LogIngestionServiceMS.repository.LogEntryRepository;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.stereotype.Service;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class LogIngestionService {

    private final LogEntryRepository logEntryRepository;

    public LogIngestionService(LogEntryRepository logEntryRepository) {
        this.logEntryRepository = logEntryRepository;
    }

    public List<LogEntry> ingestLogs(List<LogEntryDTO> dtos) {
        List<LogEntry> entities = dtos.stream().map(this::toEntity).collect(Collectors.toList());
        return logEntryRepository.saveAll(entities);
    }

    public List<LogEntry> getLogs(Specification<LogEntry> spec) {
        return logEntryRepository.findAll(spec);
    }

    public LogEntry getLogById(Long id) {
        return logEntryRepository.findById(id).orElseThrow(() -> new RuntimeException("Log not found"));
    }

    private LogEntry toEntity(LogEntryDTO dto) {
        LogEntry entry = new LogEntry();
        entry.setTimestamp(dto.getTimestamp());
        entry.setLogLevel(dto.getLogLevel());
        entry.setServiceName(dto.getServiceName());
        entry.setMessage(dto.getMessage());
        entry.setRequestId(dto.getRequestId());
        entry.setUser(dto.getUser());
        entry.setClientIp(dto.getClientIp());
        if (dto.getTimeTaken() != null && dto.getTimeTaken().endsWith("ms")) {
            String num = dto.getTimeTaken().replace("ms", "");
            entry.setTimeTakenMs(Integer.parseInt(num));
        }
        return entry;
    }
}
