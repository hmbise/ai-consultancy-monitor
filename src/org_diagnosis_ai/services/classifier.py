"""
Diagnosis classifier service using Groq LLM.
"""
import json
from typing import List, Optional
from uuid import UUID

from groq import Groq
from pydantic import BaseModel

from src.core.config import get_settings
from src.core.exceptions import DiagnosisException
from src.org_diagnosis_ai.models.diagnosis import Diagnosis, DiagnosisSeverity, DiagnosisType
from src.org_diagnosis_ai.prompts.diagnosis_prompts import DIAGNOSIS_PROMPT
from src.signal_scanner.models.company import Company
from src.signal_scanner.models.signal import Signal

settings = get_settings()


class DiagnosisResult(BaseModel):
    diagnosis_type: str
    urgency: str
    confidence: float
    reasoning: str
    supporting_signals: List[str]
    confidence_factors: List[str]


class DiagnosisClassifier:
    """Classifies companies based on signals using LLM."""

    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model

    async def classify_company(
        self,
        company: Company,
        signals: List[Signal],
    ) -> Diagnosis:
        """
        Generate a diagnosis for a company based on its signals.
        
        Args:
            company: Company to diagnose
            signals: List of signals for the company
            
        Returns:
            Diagnosis object
        """
        if not signals:
            raise DiagnosisException("No signals provided for diagnosis")

        # Format signals for the prompt
        signals_text = self._format_signals(signals)

        # Build the prompt
        prompt = DIAGNOSIS_PROMPT.format(
            company_name=company.name,
            industry=company.industry or "Unknown",
            funding_stage=company.funding_stage.value if company.funding_stage else "Unknown",
            employee_count=self._format_employee_count(company.employee_count_range),
            signals=signals_text,
        )

        # Call Groq API
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um analista estratégico. Responda apenas com JSON válido.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=1500,
                response_format={"type": "json_object"},
            )

            # Parse the response
            content = response.choices[0].message.content
            result = DiagnosisResult(**json.loads(content))

            # Map result to Diagnosis model
            return Diagnosis(
                company_id=company.id,
                diagnosis_type=DiagnosisType(result.diagnosis_type),
                severity=DiagnosisSeverity(result.urgency),
                summary=result.reasoning[:200] if len(result.reasoning) > 200 else result.reasoning,
                reasoning=result.reasoning,
                supporting_signals=[UUID(s) for s in result.supporting_signals],
                confidence_score=result.confidence,
                confidence_factors=result.confidence_factors,
            )

        except json.JSONDecodeError as e:
            raise DiagnosisException(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            raise DiagnosisException(f"Error during diagnosis classification: {e}")

    def _format_signals(self, signals: List[Signal]) -> str:
        """Format signals for the LLM prompt."""
        formatted = []
        for signal in signals:
            formatted.append(
                f"- [{signal.id}] {signal.signal_type.value}: {signal.title}\n"
                f"  Source: {signal.source.value}\n"
                f"  Content: {signal.content[:200]}..."
            )
        return "\n".join(formatted)

    def _format_employee_count(self, range_tuple: Optional[tuple]) -> str:
        """Format employee count range for display."""
        if not range_tuple:
            return "Unknown"
        min_count, max_count = range_tuple
        if min_count == max_count:
            return str(min_count)
        return f"{min_count}-{max_count}"

    async def batch_classify(
        self,
        companies_with_signals: List[tuple],
    ) -> List[Diagnosis]:
        """
        Classify multiple companies in batch.
        
        Args:
            companies_with_signals: List of (company, signals) tuples
            
        Returns:
            List of Diagnosis objects
        """
        diagnoses = []
        for company, signals in companies_with_signals:
            try:
                diagnosis = await self.classify_company(company, signals)
                diagnoses.append(diagnosis)
            except DiagnosisException as e:
                # Log error and continue with next company
                print(f"Error diagnosing {company.name}: {e}")
                continue
        return diagnoses
