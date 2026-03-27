"""
Opportunity scoring algorithms.
"""
from typing import List

from src.org_diagnosis_ai.models.diagnosis import Diagnosis, DiagnosisSeverity
from src.signal_scanner.models.company import Company, FundingStage


class OpportunityScorer:
    """Scores opportunities based on various factors."""

    def __init__(self):
        # Scoring weights
        self.weights = {
            "diagnosis_severity": 0.30,
            "diagnosis_confidence": 0.20,
            "funding_stage": 0.15,
            "company_size": 0.15,
            "signal_recency": 0.10,
            "service_fit": 0.10,
        }

    def calculate_priority_score(
        self,
        company: Company,
        diagnoses: List[Diagnosis],
    ) -> float:
        """
        Calculate overall priority score (0.0 - 1.0).
        
        Factors:
        - Diagnosis severity
        - Diagnosis confidence
        - Company funding stage
        - Company size
        - Signal recency
        """
        scores = {
            "diagnosis_severity": self._score_diagnosis_severity(diagnoses),
            "diagnosis_confidence": self._score_diagnosis_confidence(diagnoses),
            "funding_stage": self._score_funding_stage(company),
            "company_size": self._score_company_size(company),
            "signal_recency": self._score_signal_recency(diagnoses),
        }

        # Calculate weighted average
        total_score = sum(
            scores.get(key, 0) * weight
            for key, weight in self.weights.items()
            if key in scores
        )

        return round(min(total_score, 1.0), 2)

    def calculate_urgency_score(
        self,
        diagnoses: List[Diagnosis],
    ) -> float:
        """
        Calculate urgency score based on diagnosis severity and types.
        
        Critical signals:
        - Multiple high/critical severity diagnoses
        - Recent funding
        - Rapid hiring patterns
        """
        if not diagnoses:
            return 0.0

        severity_scores = {
            DiagnosisSeverity.LOW: 0.2,
            DiagnosisSeverity.MEDIUM: 0.5,
            DiagnosisSeverity.HIGH: 0.8,
            DiagnosisSeverity.CRITICAL: 1.0,
        }

        # Average severity score
        avg_severity = sum(
            severity_scores.get(d.severity, 0)
            for d in diagnoses
        ) / len(diagnoses)

        # Boost for multiple high-severity diagnoses
        high_severity_count = sum(
            1 for d in diagnoses
            if d.severity in (DiagnosisSeverity.HIGH, DiagnosisSeverity.CRITICAL)
        )

        if high_severity_count >= 2:
            avg_severity = min(avg_severity * 1.2, 1.0)

        return round(avg_severity, 2)

    def calculate_revenue_potential(
        self,
        company: Company,
        diagnoses: List[Diagnosis],
    ) -> str:
        """
        Estimate revenue potential: "low", "medium", "high".
        
        Factors:
        - Company size (employees)
        - Funding stage
        - Number and severity of diagnoses
        """
        score = 0

        # Size factor
        if company.employee_count_range:
            min_emp, max_emp = company.employee_count_range
            if max_emp < 50:
                score += 1
            elif max_emp < 200:
                score += 2
            else:
                score += 3

        # Funding stage factor
        funding_scores = {
            FundingStage.PRE_SEED: 1,
            FundingStage.SEED: 1,
            FundingStage.SERIES_A: 2,
            FundingStage.SERIES_B: 3,
            FundingStage.SERIES_C: 3,
            FundingStage.SERIES_D_PLUS: 3,
            FundingStage.IPO: 3,
        }
        score += funding_scores.get(company.funding_stage, 1)

        # Diagnosis complexity factor
        score += len(diagnoses)

        # Map score to revenue potential
        if score <= 3:
            return "low"
        elif score <= 6:
            return "medium"
        else:
            return "high"

    def calculate_fit_score(
        self,
        diagnoses: List[Diagnosis],
        recommended_services: List,
    ) -> float:
        """
        Calculate fit score based on alignment between diagnoses and services.
        
        Returns:
            Score between 0.0 and 1.0
        """
        if not diagnoses or not recommended_services:
            return 0.0

        # Check if services directly address diagnoses
        diagnosis_types = {d.diagnosis_type for d in diagnoses}

        # This is a simplified fit calculation
        # In production, use more sophisticated matching
        base_fit = 0.7

        # Boost for high confidence diagnoses
        high_confidence = sum(
            1 for d in diagnoses
            if d.confidence_score > 0.8
        )

        if high_confidence >= 2:
            base_fit = min(base_fit + 0.2, 1.0)

        return round(base_fit, 2)

    def _score_diagnosis_severity(self, diagnoses: List[Diagnosis]) -> float:
        """Score based on severity of diagnoses."""
        if not diagnoses:
            return 0.0

        severity_values = {
            DiagnosisSeverity.LOW: 0.25,
            DiagnosisSeverity.MEDIUM: 0.50,
            DiagnosisSeverity.HIGH: 0.75,
            DiagnosisSeverity.CRITICAL: 1.0,
        }

        max_severity = max(
            severity_values.get(d.severity, 0)
            for d in diagnoses
        )

        return max_severity

    def _score_diagnosis_confidence(self, diagnoses: List[Diagnosis]) -> float:
        """Score based on confidence of diagnoses."""
        if not diagnoses:
            return 0.0

        avg_confidence = sum(d.confidence_score for d in diagnoses) / len(diagnoses)
        return avg_confidence

    def _score_funding_stage(self, company: Company) -> float:
        """Score based on company funding stage."""
        stage_scores = {
            FundingStage.PRE_SEED: 0.3,
            FundingStage.SEED: 0.4,
            FundingStage.SERIES_A: 0.6,
            FundingStage.SERIES_B: 0.8,
            FundingStage.SERIES_C: 0.9,
            FundingStage.SERIES_D_PLUS: 0.9,
            FundingStage.IPO: 1.0,
        }
        return stage_scores.get(company.funding_stage, 0.5)

    def _score_company_size(self, company: Company) -> float:
        """Score based on company size."""
        if not company.employee_count_range:
            return 0.5

        min_emp, max_emp = company.employee_count_range
        avg_emp = (min_emp + max_emp) / 2

        if avg_emp < 20:
            return 0.3
        elif avg_emp < 50:
            return 0.5
        elif avg_emp < 150:
            return 0.7
        elif avg_emp < 500:
            return 0.9
        else:
            return 1.0

    def _score_signal_recency(self, diagnoses: List[Diagnosis]) -> float:
        """Score based on recency of supporting signals."""
        # Simplified - would check actual signal dates in production
        return 0.7
