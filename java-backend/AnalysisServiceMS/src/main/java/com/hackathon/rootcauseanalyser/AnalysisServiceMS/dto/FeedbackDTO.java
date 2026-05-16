package com.hackathon.rootcauseanalyser.AnalysisServiceMS.dto;

import com.hackathon.rootcauseanalyser.AnalysisServiceMS.entity.AnalysisStatus;
import jakarta.validation.constraints.NotNull;
import lombok.*;

@Data
@AllArgsConstructor
@NoArgsConstructor
@Getter
@Setter
public class FeedbackDTO {

    @NotNull
    private String feedback;

    @NotNull
    private AnalysisStatus status;
}
