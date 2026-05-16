package com.hackathon.rootcauseanalyser.LogIngestionServiceMS.dto;

import lombok.*;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Setter
@Getter
public class LogEntryDTO {

    private LocalDateTime timestamp;
    private String logLevel;
    private String serviceName;
    private String message;
    private String requestId;
    private String user;
    private String clientIp;
    private String timeTaken;
}
