"""
Email template engine for generating outreach emails.
"""
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from src.opportunity_engine.models.opportunity import Opportunity


class EmailTemplate(BaseModel):
    subject: str
    body: str
    tone: str
    call_to_action: str


# Email templates by tone and context
EMAIL_TEMPLATES = {
    "consultative": {
        "subject": "Insight sobre {company_name} - {topic}",
        "opening": "Olá {first_name},",
        "body": """
Acompanhamos o crescimento de {company_name} e notamos alguns padrões interessantes que podem ser relevantes para vocês neste momento.

{insight}

{value_proposition}

Gostaria de compartilhar alguns benchmarks de empresas em fase similar? Sem compromisso - apenas um bate-papo rápido de 15 minutos.
""",
        "closing": "Abraços,\n{sender_name}",
    },
    "urgent": {
        "subject": "{company_name} - momento crítico para estruturação",
        "opening": "Oi {first_name},",
        "body": """
Vimos que {company_name} está {trigger_event}. Isso geralmente indica um momento em que a estruturação operacional se torna crítica.

{insight}

{value_proposition}

Podemos ajudar a acelerar essa transição. Topa uma conversa rápida esta semana?
""",
        "closing": "Abraços,\n{sender_name}",
    },
    "strategic": {
        "subject": "Benchmarks para {company_name} - {topic}",
        "opening": "Olá {first_name},",
        "body": """
Como consultoria de {industry}, trabalhamos com várias empresas em fase {funding_stage} e compilamos dados interessantes sobre estruturação operacional.

{insight}

{value_proposition}

Gostaria de compartilhar esses insights? Podemos agendar uma call de 20 minutos - sem pitch de venda, apenas troca de conhecimento.
""",
        "closing": "Atenciosamente,\n{sender_name}",
    },
}


class TemplateEngine:
    """Generates email templates for outreach."""

    def __init__(self):
        self.templates = EMAIL_TEMPLATES

    def generate_email(
        self,
        opportunity: Opportunity,
        angle: dict,
        recipient_name: str,
        sender_name: str,
        company_info: dict,
    ) -> EmailTemplate:
        """
        Generate an email based on the engagement angle.
        
        Args:
            opportunity: The opportunity context
            angle: The engagement angle to use
            recipient_name: Name of the recipient
            sender_name: Name of the sender
            company_info: Company information dictionary
            
        Returns:
            EmailTemplate with subject and body
        """
        tone = angle.get("tone", "consultative")
        template = self.templates.get(tone, self.templates["consultative"])

        # Build variables
        company_name = company_info.get("name", "Sua empresa")
        first_name = recipient_name.split()[0] if recipient_name else "Olá"

        # Determine topic based on services
        services = opportunity.recommended_services
        topic = self._get_topic_from_services(services)

        # Determine trigger event
        trigger_event = self._get_trigger_event(opportunity)

        # Build body
        body_parts = [
            template["opening"].format(first_name=first_name),
            "",
            template["body"].format(
                company_name=company_name,
                first_name=first_name,
                insight=angle.get("insight", ""),
                value_proposition=angle.get("value_proposition", ""),
                topic=topic,
                trigger_event=trigger_event,
                funding_stage=company_info.get("funding_stage", "de crescimento"),
                industry=company_info.get("industry", "tecnologia"),
            ).strip(),
            "",
            template["closing"].format(sender_name=sender_name),
        ]

        subject = template["subject"].format(
            company_name=company_name,
            topic=topic,
        )

        body = "\n".join(body_parts)

        return EmailTemplate(
            subject=subject,
            body=body,
            tone=tone,
            call_to_action="Agendar uma conversa de 15-20 minutos",
        )

    def _get_topic_from_services(self, services) -> str:
        """Generate email topic from recommended services."""
        if not services:
            return "crescimento"

        service_topics = {
            "financial_structuring": "estruturação financeira",
            "fp_a_implementation": "FP&A e planejamento",
            "operations_processes": "otimização operacional",
            "data_dashboards": "dados e dashboards",
            "governance_advisory": "governança corporativa",
            "executive_coaching": "desenvolvimento de liderança",
            "m_and_a_support": "M&A e expansão",
            "ipo_preparation": "preparação para escala",
        }

        primary_service = services[0].value if hasattr(services[0], "value") else str(services[0])
        return service_topics.get(primary_service, "crescimento estratégico")

    def _get_trigger_event(self, opportunity: Opportunity) -> str:
        """Determine the trigger event for the email."""
        services = opportunity.recommended_services
        if not services:
            return "em uma fase de crescimento"

        primary = services[0].value if hasattr(services[0], "value") else str(services[0])

        triggers = {
            "financial_structuring": "contratando liderança financeira",
            "fp_a_implementation": "expandindo a operação financeira",
            "operations_processes": "escalando operações",
            "data_dashboards": "investindo em dados e analytics",
            "governance_advisory": "estruturando governança",
            "executive_coaching": "fortalecendo liderança",
            "m_and_a_support": "expandindo via aquisições",
            "ipo_preparation": "se preparando para próxima fase",
        }

        return triggers.get(primary, "em crescimento acelerado")
