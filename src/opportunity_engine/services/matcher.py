"""
Service matcher for mapping diagnoses to consulting services.
"""
from typing import Dict, List, Set

from src.org_diagnosis_ai.models.diagnosis import Diagnosis, DiagnosisType
from src.opportunity_engine.models.opportunity import OpportunityService


# Mapping of diagnosis types to recommended services
DIAGNOSIS_SERVICE_MAP: Dict[DiagnosisType, List[OpportunityService]] = {
    DiagnosisType.FINANCE_IMMATURITY: [
        OpportunityService.FINANCIAL_STRUCTURING,
        OpportunityService.FP_A_IMPLEMENTATION,
    ],
    DiagnosisType.OPERATIONAL_CHAOS: [
        OpportunityService.OPERATIONS_PROCESSES,
        OpportunityService.FINANCIAL_STRUCTURING,
    ],
    DiagnosisType.DATA_BLINDNESS: [
        OpportunityService.DATA_DASHBOARDS,
        OpportunityService.FP_A_IMPLEMENTATION,
    ],
    DiagnosisType.GOVERNANCE_GAP: [
        OpportunityService.GOVERNANCE_ADVISORY,
        OpportunityService.EXECUTIVE_COACHING,
    ],
    DiagnosisType.LEADERSHIP_GAP: [
        OpportunityService.EXECUTIVE_COACHING,
        OpportunityService.GOVERNANCE_ADVISORY,
    ],
    DiagnosisType.GROWTH_SCALING: [
        OpportunityService.OPERATIONS_PROCESSES,
        OpportunityService.FINANCIAL_STRUCTURING,
        OpportunityService.FP_A_IMPLEMENTATION,
    ],
    DiagnosisType.MARKET_EXPANDING: [
        OpportunityService.FINANCIAL_STRUCTURING,
        OpportunityService.M_AND_A_SUPPORT,
    ],
    DiagnosisType.PRODUCT_MATURITY: [
        OpportunityService.OPERATIONS_PROCESSES,
        OpportunityService.DATA_DASHBOARDS,
    ],
}


class ServiceMatcher:
    """Matches diagnoses to consulting services."""

    def __init__(self):
        self.diagnosis_map = DIAGNOSIS_SERVICE_MAP

    def match_services(self, diagnoses: List[Diagnosis]) -> List[OpportunityService]:
        """
        Match diagnoses to recommended services.
        
        Args:
            diagnoses: List of diagnoses for a company
            
        Returns:
            List of recommended services (de-duplicated and prioritized)
        """
        recommended: Set[OpportunityService] = set()

        for diagnosis in diagnoses:
            services = self.diagnosis_map.get(diagnosis.diagnosis_type, [])
            recommended.update(services)

        # Convert to list and maintain priority order
        priority_order = [
            OpportunityService.FINANCIAL_STRUCTURING,
            OpportunityService.FP_A_IMPLEMENTATION,
            OpportunityService.OPERATIONS_PROCESSES,
            OpportunityService.DATA_DASHBOARDS,
            OpportunityService.GOVERNANCE_ADVISORY,
            OpportunityService.EXECUTIVE_COACHING,
            OpportunityService.M_AND_A_SUPPORT,
            OpportunityService.IPO_PREPARATION,
        ]

        # Sort by priority
        result = sorted(
            recommended,
            key=lambda s: priority_order.index(s) if s in priority_order else 999
        )

        return result

    def get_service_description(self, service: OpportunityService) -> str:
        """Get human-readable description of a service."""
        descriptions = {
            OpportunityService.FINANCIAL_STRUCTURING: (
                "Estruturação financeira: controles, processos, e governança financeira"
            ),
            OpportunityService.FP_A_IMPLEMENTATION: (
                "Implementação de FP&A: planejamento, orçamento, e análise financeira"
            ),
            OpportunityService.OPERATIONS_PROCESSES: (
                "Otimização de operações: processos, eficiência, e escalabilidade"
            ),
            OpportunityService.DATA_DASHBOARDS: (
                "Dashboards e BI: visualização de dados e KPIs para decisão"
            ),
            OpportunityService.GOVERNANCE_ADVISORY: (
                "Consultoria de governança: board, comitês, e estrutura de decisão"
            ),
            OpportunityService.EXECUTIVE_COACHING: (
                "Coaching executivo: desenvolvimento de liderança"
            ),
            OpportunityService.M_AND_A_SUPPORT: (
                "Suporte a M&A: due diligence e integração"
            ),
            OpportunityService.IPO_PREPARATION: (
                "Preparação para IPO: compliance, relatórios, e governança"
            ),
        }
        return descriptions.get(service, "Serviço de consultoria")
