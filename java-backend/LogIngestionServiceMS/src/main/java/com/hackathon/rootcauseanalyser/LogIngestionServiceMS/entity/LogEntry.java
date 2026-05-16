package com.hackathon.rootcauseanalyser.LogIngestionServiceMS.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

import java.time.LocalDateTime;

@Entity
@Table(name = "log_entry")
@Data
@Getter
@Setter
public class LogEntry {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private LocalDateTime timestamp;

    @Column(nullable = false, length = 20)
    private String logLevel;

    @Column(name = "service_name", nullable = false, length = 50)
    private String serviceName;

    @Column(nullable = false, columnDefinition = "TEXT")
    private String message;

    @Column(name = "request_id", length = 50)
    private String requestId;

    @Column(length = 50)
    private String user;

    @Column(name = "client_ip", length = 45)
    private String clientIp;

    @Column(name = "time_taken_ms")
    private Integer timeTakenMs;
}