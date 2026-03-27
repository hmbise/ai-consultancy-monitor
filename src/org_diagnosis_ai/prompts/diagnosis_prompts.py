"""
Prompts for LLM-based organizational diagnosis.
"""

DIAGNOSIS_PROMPT = """\
Você é um analista estratégico especializado em diagnosticar necessidades 
de consultoria em empresas em crescimento.

## Contexto da Empresa
Nome: {company_name}
Indústria: {industry}
Fase de Funding: {funding_stage}
Tamanho: {employee_count} funcionários

## Sinais Detectados
{signals}

## Sua Tarefa
Analise os sinais acima e determine:
1. Tipo principal de necessidade (ou "none" se não houver sinais claros)
2. Nível de urgência (low/medium/high/critical)
3. Score de confiança (0.0 - 1.0)
4. Reasoning breve explicando seu diagnóstico

## Tipos de Diagnóstico
- OPERATIONAL_CHAOS: processos manuais, falta de estrutura, crescimento desorganizado
- FINANCE_IMMATURITY: sem FP&A, controller reativo, falta de planejamento financeiro
- GOVERNANCE_GAP: decisões centralizadas, sem board, falta de governança
- DATA_BLINDNESS: sem dashboards, decisões baseadas em feeling, falta de dados
- GROWTH_SCALING: crescendo rápido sem estrutura para suportar
- MARKET_EXPANDING: expansão para novos mercados, internacionalização
- PRODUCT_MATURITY: maturidade de produto, novas linhas, inovação
- LEADERSHIP_GAP: gaps em liderança sênior, falta de experiência

## Output (JSON)
{{
  "diagnosis_type": "...",
  "urgency": "...",
  "confidence": 0.XX,
  "reasoning": "...",
  "supporting_signals": ["signal_id_1", "signal_id_2"],
  "confidence_factors": ["factor 1", "factor 2"]
}}
"""

DIAGNOSIS_SUMMARY_PROMPT = """\
Com base no diagnóstico a seguir, gere um resumo executivo de uma frase:

Diagnóstico: {diagnosis_type}
Severidade: {severity}
Raciocínio: {reasoning}

O resumo deve ser em português e destacar a necessidade principal da empresa.
"""

CONFIDENCE_SCORING_PROMPT = """\
Avalie a confiança do seguinte diagnóstico:

Sinais disponíveis: {signal_count}
Tipos de sinais: {signal_types}
Recência dos sinais: {signal_recency}
Consistência dos sinais: {signal_consistency}

Retorne um score de 0.0 a 1.0 e liste os fatores que aumentam ou diminuem a confiança.
Formato JSON:
{{
  "confidence_score": 0.XX,
  "factors": ["fator 1", "fator 2"]
}}
"""

DIAGNOSIS_TYPES_DESCRIPTION = {
    "OPERATIONAL_CHAOS": {
        "name": "Caos Operacional",
        "description": "Processos manuais, falta de estrutura organizacional, crescimento desorganizado",
        "indicators": ["Contratação massiva", "Múltiplos cargos de operações", "Reviews mencionando caos"],
    },
    "FINANCE_IMMATURITY": {
        "name": "Imaturidade Financeira",
        "description": "Sem FP&A, controller reativo, falta de planejamento financeiro estruturado",
        "indicators": ["Contratação de CFO/VP Finance", "Crescimento sem estrutura financeira", "Série A/B recente"],
    },
    "GOVERNANCE_GAP": {
        "name": "Gap de Governança",
        "description": "Decisões centralizadas, falta de board, ausência de processos de governança",
        "indicators": ["Mudança de CEO", "Crescimento acelerado", "Novos investidores"],
    },
    "DATA_BLINDNESS": {
        "name": "Cegueira de Dados",
        "description": "Sem dashboards, decisões baseadas em feeling, falta de dados estruturados",
        "indicators": ["Contratação de líderes de dados", "Crescimento sem analytics", "Múltiplos produtos"],
    },
    "GROWTH_SCALING": {
        "name": "Escalando Crescimento",
        "description": "Crescendo rápido mas sem estrutura operacional para suportar",
        "indicators": ["Rápida expansão de time", "Nova rodada de investimento", "Abertura de novos escritórios"],
    },
    "MARKET_EXPANDING": {
        "name": "Expansão de Mercado",
        "description": "Expansão para novos mercados geográficos ou verticais",
        "indicators": ["Novos escritórios", "Contratação em novas regiões", "Anúncios de expansão"],
    },
    "PRODUCT_MATURITY": {
        "name": "Maturidade de Produto",
        "description": "Evolução do produto, novas linhas, inovação estruturada",
        "indicators": ["Lançamentos de produto", "Contratação de product leaders", "Novas funcionalidades"],
    },
    "LEADERSHIP_GAP": {
        "name": "Gap de Liderança",
        "description": "Gaps em liderança sênior, falta de experiência no time executivo",
        "indicators": ["Mudanças de liderança", "Contratação de executivos", "Saida de fundadores"],
    },
}
