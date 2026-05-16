package com.hackathon.rootcauseanalyser.IncidentServiceMS.entity;

import com.hackathon.rootcauseanalyser.IncidentServiceMS.utility.JSONListConverter;
import jakarta.persistence.*;
import lombok.*;

import javax.print.attribute.standard.Severity;
import java.time.LocalDateTime;
import java.util.*;

@Entity
@Table(name = "incident")
@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class Incident {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String title;
    private String description;

    @Enumerated(EnumType.STRING)
    private Severity severity;

    @Enumerated(EnumType.STRING)
    private IncidentStatus status;

    @Column(name = "created_at")
    private LocalDateTime createdAt;

    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    @Column(name = "assigned_to")
    private String assignedTo;

    @Convert(converter = JSONListConverter.class)
    @Column(columnDefinition = "TEXT")
    private List<Long> logIds;

    @OneToMany(mappedBy = "incident", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Alert> alerts;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}