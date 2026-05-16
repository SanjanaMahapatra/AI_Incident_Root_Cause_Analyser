package com.hackathon.rootcauseanalyser.IncidentServiceMS.entity;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "alert")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class Alert {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "incident_id")
    private Incident incident;

    private String ruleName;
    private LocalDateTime triggeredAt;
    private String severity;
    private String message;
    private boolean resolved;
}