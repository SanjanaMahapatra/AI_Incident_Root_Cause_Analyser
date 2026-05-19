package com.hackathon.rootcauseanalyser.LogIngestionServiceMS.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.*;

import java.time.LocalDateTime;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Setter
@Getter
public class LogEntryDTO {

    @JsonProperty("timestamp")
    private LocalDateTime timestamp;

    @JsonProperty("logLevel")
    private String logLevel;

    @JsonProperty("serviceName")
    private String serviceName;

    @JsonProperty("message")
    private String message;

    @JsonProperty("requestId")
    private String requestId;

    @JsonProperty("user")
    private String user;

    @JsonProperty("clientIp")
    private String clientIp;

    @JsonProperty("timeTaken")
    private String timeTaken;

}
