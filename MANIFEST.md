# MANIFEST — Ecossistema AI-First

## 1. Propósito
Unificar princípios, arquitetura e fluxos de trabalho de todos os produtos gerenciados pelo AI CTO OS.  
Este documento é a **fonte única de verdade** para agentes de IA (JARVIS, Synapse) e colaboradores humanos.

**Regra fundamental:**  
Sempre que uma orientação não for localizada ou compreendida, o agente **deve perguntar antes de executar qualquer ação**. Nenhuma decisão será tomada no escuro.

---

## 2. Pilares de Design

### 2.1. Filosofia
- **Entropia inicial** – aceitar caos na entrada, estruturar na saída.
- **Fricção zero** – mínimo de toques/cliques, sem campos obrigatórios.
- **Proatividade** – o sistema sugere antes de ser perguntado (digests, alertas de conexão).
- **Visualização de conexões** – relações entre itens devem ser visíveis (grafos, cards com highlights).
- **Modos distintos** – mobile = captura rápida; desktop = análise profunda.
- **Iteração rápida** – MVP com "magia mínima", depois expansão.
- **Standalone first** – cada produto deve funcionar de forma independente; integrações são opcionais e não devem criar dependência que prejudique o uso isolado.

### 2.2. Linguagem Visual
- Limpa, baseada em cards, espaçamento generoso.
- Tipografia sem serifa.
- Cores de destaque apenas para indicar conexões semânticas.
- Componentes reutilizáveis (shadcn/ui customizado).

### 2.3. Navegação
- **Sidebar esquerda** fixa, sem menus aninhados.
- **Clique no grafo → navega para página com filtro aplicado** (ex: clicar em "fintech" leva à listagem filtrada).
- **Filtros geográficos hierárquicos** (cada produto implementa a sua própria granularidade):  
  Continente → Subdivisão continental → País → Região → Estado/Província/Cantão → Cidade.

---

## 3. Stack Técnica

| Camada | Tecnologia |
|--------|------------|
| Banco de dados | Neon (PostgreSQL) – **projetos Neon** agrupam schemas por tipo |
| Organização | Neon Projects → Schemas → Tabelas |
| Backend | Next.js API routes (Vercel) + FastAPI (quando necessário) |
| Frontend | Next.js (App Router), Tailwind, shadcn/ui |
| Mobile | React Native + share extension |
| Vetorização | OpenAI embeddings, `pgvector` no Neon |
| Agentes | Claude API (Synapse, JARVIS) |
| Notificações | Pushover/Telegram (inicial), depois Firebase |

---

## 4. Dados e Modelagem

### 4.1. Neon – Estrutura de Projetos
Cada **projeto Neon** é um agrupamento lógico de schemas. Exemplo:

- `ai-foundry-core` – schemas centrais: `ai_cto_os`, `shared` 
- `ai-foundry-products` – schemas de produtos: `primordial`, `intelos`, `solar`, `ai_consultancy`
- `ai-foundry-games` – futuros schemas de jogos

**Decisão a tomar para cada produto:**  
> A qual projeto Neon o schema deste produto pertencerá?

### 4.2. Modelagem por Produto (Standalone)
Cada produto mantém suas próprias tabelas, **inclusive a de geolocalização**.  
Não há tabelas compartilhadas entre produtos, a menos que explicitamente definido como um módulo de integração opcional (ex: exportação/importação de insights via JSON).

- Cada produto que necessitar de geolocalização terá sua própria tabela `locations` (com a mesma estrutura hierárquica).
- Cada produto gerencia seus próprios embeddings, tags e entidades.

### 4.3. Tabela `locations` (exemplo de estrutura, por produto)
- Colunas: `id`, `name`, `level`, `parent_id`, `slug`, `iso_code`.
- Níveis: Continente → Subdivisão continental → País → Região → Estado/Província → Cidade.
- Referenciada internamente pelo produto.

### 4.4. AI CTO OS – Tabelas de Gestão
- `projects` – cadastro de todos os produtos do portfólio (apenas metadados, não dados de negócio).
- `insights` – armazena conexões recebidas de produtos (via integração opcional).
- `tasks` – tarefas geradas a partir de insights.

---

## 5. Gestão de Projetos (Pipeline)

- **Capacidade máxima**: 10 projetos no pipeline ativo.
- **Estados obrigatórios**:
  - **Active Sprint** (máx 4) – código sendo produzido.
  - **Discovery** – validação de mercado, arquitetura, sem código extensivo.
  - **Backlog** – ideia documentada, aguardando trigger.
  - **Maintenance** – já shipado, apenas correções.
- **Revisão mensal** para promover projetos de Backlog/Discovery.

---

## 6. Produtos Ativos (março/2026) e Definição de Projeto Neon

| Produto (Schema) | Estado | Oracle | Projeto Neon |
|------------------|--------|--------|--------------|
| AI Consultancy Monitor (`ai_consultancy`) | Active Sprint | 45 | `ai-foundry-products` |
| AI Solar Matchmaker (`solar`) | Active Sprint | 51 | `ai-foundry-products` |
| AI CTO OS (`ai_cto_os`) | Active Sprint | 50 | `ai-foundry-core` |
| Primordial (`primordial`) | Active Sprint | 37 | `ai-foundry-products` |
| REELINTEL (`intelos`) | Active Sprint | 41 | `ai-foundry-products` |
| ARTINTEL (`intelos`) | Backlog | 32 | `ai-foundry-products` |
| Housli (futuro) | Backlog | 29 | `ai-foundry-products` |

---

## 7. Fluxos de Navegação e Interação

### 7.1. Grafo → Filtro
- Qualquer visualização em grafo (Primordial, IntelOS) permite clique em nós.
- O clique gera uma URL com parâmetros de filtro (`?location_id=...`, `?tag=...`, `?project_id=...`) e redireciona para a página de listagem correspondente (ex: `/explore` ou página específica do produto).
- A página alvo aplica os filtros automaticamente.

### 7.2. Filtro Geográfico (implementado por produto)
- Cada produto que utilizar geolocalização terá seu próprio componente `LocationFilter`, baseado em sua tabela `locations`.
- O componente exibe breadcrumb e permite drill-down, atualizando a query string.

---

## 8. MVP e Ciclos de Entrega
- **MVP ≤ 14 dias**.
- Para cada sprint ativo, definir métrica de sucesso.
- Após MVP, iterar com base em feedback e insights do Synapse.

---

## 9. Integração entre Produtos (Opcional)

Produtos são **standalone** por design. Integrações são bem-vindas, mas **não obrigatórias** e não podem criar dependência que inviabilize o uso isolado.

- **Primordial → AI CTO OS**:  
  Pode enviar insights (via API ou JSON export) para o AI CTO OS. Esses insights alimentam o dashboard de gestão.

- **AI Consultancy Monitor → AI CTO OS**:  
  Pode exportar oportunidades de consultoria e diagnósticos como insights para o AI CTO OS.

- **Outros produtos → Primordial**:  
  Primordial pode receber insights de outros produtos através de um **módulo de importação** (ex: upload de JSON). Isso permite que o Synapse considere informações de outros sistemas.

- **Formato de troca**:  
  Quando integrado, o formato padrão é um JSON com metadados mínimos (ex: `{ source, content, related_project, timestamp }`). A implementação da integração é opcional e pode ser feita por módulos separados, sem alterar o núcleo do produto.

- **AI CTO OS**:  
  É o orquestrador opcional; sem ele, cada produto continua funcionando normalmente.

---

## 10. Evolução
- O MANIFEST é **vivo**; deve ser atualizado sempre que novas decisões arquiteturais ou de design forem tomadas.
- Versão controlada junto ao repositório do AI CTO OS.

---

*Última atualização: 27 de março de 2026.*
