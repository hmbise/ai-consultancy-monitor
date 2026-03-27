"""
Angle generator for creating engagement strategies.
"""
from typing import List, Optional
from uuid import UUID

from groq import Groq

from src.core.config import get_settings
from src.opportunity_engine.models.opportunity import Opportunity

settings = get_settings()


ANGLE_GENERATION_PROMPT = """\
Você é um especialista em estratégia de vendas B2B para consultoria de negócios.

## Contexto da Oportunidade
Empresa: {company_name}
Indústria: {industry}
Serviços Recomendados: {services}
Diagnósticos: {diagnoses}
Score de Prioridade: {priority_score}

## Sua Tarefa
Gere 3 ângulos de abordagem diferentes para iniciar uma conversa com esta empresa.

Cada ângulo deve:
1. Ser personalizado para o contexto da empresa
2. Mencionar um insight específico sobre a situação deles
3. Propor valor imediato (não uma venda direta)
4. Ter um tom consultivo, não agressivo

## Formato de Saída (JSON)
{{
  "angles": [
    {{
      "title": "Título do ângulo",
      "approach": "Como abordar - 2-3 frases",
      "insight": "Insight específico sobre a empresa",
      "value_proposition": "Valor que podemos oferecer",
      "tone": "consultative|urgent|strategic"
    }}
  ]
}}
"""


class EngagementAngle(BaseModel):
    title: str
    approach: str
    insight: str
    value_proposition: str
    tone: str


class AngleGenerator:
    """Generates engagement angles for opportunities."""

    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model

    async def generate_angles(
        self,
        opportunity: Opportunity,
        company_info: dict,
        diagnoses: List[dict],
    ) -> List[EngagementAngle]:
        """
        Generate engagement angles for an opportunity.
        
        Args:
            opportunity: The opportunity to generate angles for
            company_info: Company information dictionary
            diagnoses: List of diagnosis information
            
        Returns:
            List of engagement angles
        """
        import json

        prompt = ANGLE_GENERATION_PROMPT.format(
            company_name=company_info.get("name", "Empresa"),
            industry=company_info.get("industry", "Technology"),
            services=", ".join([s.value for s in opportunity.recommended_services]),
            diagnoses=", ".join([d.get("type", "") for d in diagnoses]),
            priority_score=opportunity.priority_score,
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um especialista em estratégia de vendas B2B.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=1500,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content
            result = json.loads(content)

            return [EngagementAngle(**angle) for angle in result.get("angles", [])]

        except Exception as e:
            # Fallback angles if LLM fails
            return self._generate_fallback_angles(opportunity, company_info)

    def _generate_fallback_angles(
        self,
        opportunity: Opportunity,
        company_info: dict,
    ) -> List[EngagementAngle]:
        """Generate fallback angles if LLM fails."""
        company_name = company_info.get("name", "Sua empresa")

        return [
            EngagementAngle(
                title="Abordagem Consultiva",
                approach=(
                    f"Notamos que {company_name} está em uma fase de crescimento interessante. "
                    f"Gostaríamos de compartilhar alguns insights sobre como empresas similares "
                    f"têm estruturado suas operações durante essa fase."
                ),
                insight="Empresa em fase de crescimento com necessidades de estruturação",
                value_proposition="Insights gratuitos sobre melhores práticas do mercado",
                tone="consultative",
            ),
            EngagementAngle(
                title="Abordagem de Urgência",
                approach=(
                    f"Vimos que {company_name} está contratando liderança financeira. "
                    f"Isso geralmente indica um momento crítico que pode se beneficiar de "
                    f"suporte estratégico adicional."
                ),
                insight="Contratação de liderança indica momento de transformação",
                value_proposition="Suporte imediato para acelerar a estruturação",
                tone="urgent",
            ),
            EngagementAngle(
                title="Abordagem Estratégica",
                approach=(
                    f"Como parceiros de várias empresas em fase {company_info.get('funding_stage', 'de crescimento')}, "
                    f"temos dados interessantes sobre como estruturar operações de forma escalável. "
                    f"Gostaria de compartilhar?"
                ),
                insight="Benchmark de empresas em fase similar",
                value_proposition="Acesso a dados e benchmarks exclusivos",
                tone="strategic",
            ),
        ]
