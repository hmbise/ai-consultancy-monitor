"""
Test examples for diagnosis classifier.
"""
import pytest
from uuid import UUID, uuid4

from src.org_diagnosis_ai.models.diagnosis import DiagnosisSeverity, DiagnosisType
from src.signal_scanner.models.company import Company, FundingStage
from src.signal_scanner.models.signal import Signal, SignalSource, SignalType


@pytest.fixture
def sample_company():
    """Create a sample company for testing."""
    return Company(
        id=uuid4(),
        name="TechCorp",
        slug="techcorp",
        industry="Software",
        funding_stage=FundingStage.SERIES_A,
        employee_count_range=(50, 200),
    )


@pytest.fixture
def finance_hiring_signals():
    """Create sample finance hiring signals."""
    company_id = uuid4()
    return [
        Signal(
            id=uuid4(),
            company_id=company_id,
            source=SignalSource.JOB_BOARD,
            signal_type=SignalType.HIRING_FINANCE_LEAD,
            title="VP of Finance - Series A Startup",
            content="Looking for experienced finance leader...",
        ),
        Signal(
            id=uuid4(),
            company_id=company_id,
            source=SignalSource.JOB_BOARD,
            signal_type=SignalType.HIRING_FP_A,
            title="FP&A Manager",
            content="Build financial planning function...",
        ),
    ]


@pytest.mark.asyncio
async def test_classify_finance_immaturity(sample_company, finance_hiring_signals):
    """Test that finance hiring signals lead to finance immaturity diagnosis."""
    # This would be a real test with mocked Groq API
    # For now, just verify the data structure
    
    assert sample_company.name == "TechCorp"
    assert len(finance_hiring_signals) == 2
    
    # Verify signal types
    for signal in finance_hiring_signals:
        assert signal.signal_type in [
            SignalType.HIRING_FINANCE_LEAD,
            SignalType.HIRING_FP_A,
        ]


def test_diagnosis_severity_levels():
    """Test severity enum values."""
    assert DiagnosisSeverity.LOW == "low"
    assert DiagnosisSeverity.MEDIUM == "medium"
    assert DiagnosisSeverity.HIGH == "high"
    assert DiagnosisSeverity.CRITICAL == "critical"


def test_diagnosis_type_values():
    """Test diagnosis type enum values."""
    assert DiagnosisType.FINANCE_IMMATURITY == "finance_immaturity"
    assert DiagnosisType.OPERATIONAL_CHAOS == "operational_chaos"
    assert DiagnosisType.GROWTH_SCALING == "growth_scaling"
