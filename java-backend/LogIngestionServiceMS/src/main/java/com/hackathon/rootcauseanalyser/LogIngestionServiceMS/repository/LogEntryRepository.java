package com.hackathon.rootcauseanalyser.LogIngestionServiceMS.repository;

import com.hackathon.rootcauseanalyser.LogIngestionServiceMS.entity.LogEntry;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;

public interface LogEntryRepository extends JpaRepository<LogEntry, Long>, JpaSpecificationExecutor<LogEntry> {
}
