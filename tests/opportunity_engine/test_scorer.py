"""
Test examples for opportunity engine.
"""
import pytest
from uuid import UUID, uuid4

from src.opportunity_engine.models.opportunity import OpportunityService, OpportunityStatus
from src.opportunity_engine.services.matcher import DIAGNOSIS_SERVICE_MAP, ServiceMatcher
from src.opportunity_engine.services.scorer import OpportunityScorer
from src.org_diagnosis_ai.models.diagnosis import Diagnosis, DiagnosisSeverity, DiagnosisType
from src.signal_scanner.models.company import Company, FundingStage


@pytest.fixture
def service_matcher():
    """Create a service matcher instance."""
    return ServiceMatcher()


@pytest.fixture
def opportunity_scorer():
    """Create an opportunity scorer instance."""
    return OpportunityScorer()


@pytest.fixture
def sample_company():
    """Create a sample company."""
    return Company(
        id=uuid4(),
        name="TestCorp",
        slug="testcorp",
        funding_stage=FundingStage.SERIES_B,
        employee_count_range=(100, 250),
    )


@pytest.fixture
def finance_immaturity_diagnosis(sample_company):
    """Create a finance immaturity diagnosis."""
    return Diagnosis(
        id=uuid4(),
        company_id=sample_company.id,
        diagnosis_type=DiagnosisType.FINANCE_IMMATURITY,
        severity=DiagnosisSeverity.HIGH,
        summary="Finance team not ready for scale",
        reasoning="Hiring for finance leadership indicates current gaps",
        supporting_signals=[],
        confidence_score=0.85,
        confidence_factors=["Recent hiring", "Series B stage"],
    )


def test_service_matcher_finance_immaturity(service_matcher, finance_immaturity_diagnosis):
    """Test that finance immaturity maps to correct services."""
    services = service_matcher.match_services([finance_immaturity_diagnosis])
    
    assert OpportunityService.FINANCIAL_STRUCTURING in services
    assert OpportunityService.FP_A_IMPLEMENTATION in services


def test_service_matcher_operational_chaos(service_matcher):
    """Test that operational chaos maps to operations services."""
    diagnosis = Diagnosis(
        id=uuid4(),
        company_id=uuid4(),
        diagnosis_type=DiagnosisType.OPERATIONAL_CHAOS,
        severity=DiagnosisSeverity.MEDIUM,
        summary="Processes not scaling",
        reasoning="Multiple hiring signals without structure",
        supporting_signals=[],
        confidence_score=0.75,
        confidence_factors=["Multiple signals"],
    )
    
    services = service_matcher.match_services([diagnosis])
    
    assert OpportunityService.OPERATIONS_PROCESSES in services


def test_scorer_priority_calculation(opportunity_scorer, sample_company, finance_immaturity_diagnosis):
    """Test priority score calculation."""
    score = opportunity_scorer.calculate_priority_score(
        sample_company,
        [finance_immaturity_diagnosis],
    )
    
    # Score should be between 0 and 1
    assert 0 <= score <= 1
    
    # High severity + Series B should give decent score
    assert score > 0.5


def test_scorer_urgency_calculation(opportunity_scorer, finance_immaturity_diagnosis):
    """Test urgency score calculation."""
    urgency = opportunity_scorer.calculate_urgency_score(
        [finance_immaturity_diagnosis],
    )
    
    # High severity should give high urgency
    assert urgency >= 0.7


def test_revenue_potential_calculation(opportunity_scorer, sample_company, finance_immaturity_diagnosis):
    """Test revenue potential calculation."""
    potential = opportunity_scorer.calculate_revenue_potential(
        sample_company,
        [finance_immaturity_diagnosis],
    )
    
    # Series B + 100-250 employees + 1 diagnosis = at least "medium"
    assert potential in ["medium", "high"]


def test_opportunity_service_enum():
    """Test opportunity service enum values."""
    assert OpportunityService.FINANCIAL_STRUCTURING.value == "financial_structuring"
    assert OpportunityService.FP_A_IMPLEMENTATION.value == "fp_a_implementation"
    assert OpportunityService.OPERATIONS_PROCESSES.value == "operations_processes"


def test_opportunity_status_enum():
    """Test opportunity status enum values."""
    assert OpportunityStatus.NEW.value == "new"
    assert OpportunityStatus.REACHED_OUT.value == "reached_out"
    assert OpportunityStatus.WON.value == "won"
    assert OpportunityStatus.LOST.value == "lost"
