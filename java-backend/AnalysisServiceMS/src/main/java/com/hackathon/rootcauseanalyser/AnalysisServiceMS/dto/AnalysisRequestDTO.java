package com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto;

import jakarta.validation.constraints.NotNull;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class AnalysisRequestDTO {
    @NotNull
    private Long incidentId;

    @NotNull
    private String analysisType;
}