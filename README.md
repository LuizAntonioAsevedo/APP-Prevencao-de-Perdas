# 🤖 Agente Inteligente de Prevenção de Perdas

Sistema desenvolvido em **Python** para apoiar processos de **Prevenção de Perdas em operações de e-commerce e logística**, utilizando análise de dados, interpretação de perguntas em linguagem natural, Skills especializadas, Tools, MCP, banco de dados SQLite e interface web.

> **Projeto de portfólio — os dados utilizados são fictícios e destinados exclusivamente para fins educacionais e demonstrativos.**

---

## 📌 Sobre o projeto

O **Agente Inteligente de Prevenção de Perdas** foi desenvolvido para demonstrar como conceitos de **Inteligência Artificial, análise de dados, automação e arquitetura de agentes** podem ser aplicados a problemas relacionados a operações logísticas e e-commerce.

O sistema trabalha com dados de:

* Remessas;
* Ocorrências;
* Rotas;
* Transportadoras;
* Valores de perdas;
* Status das ocorrências.

O agente interpreta perguntas em linguagem natural, identifica a intenção e a entidade envolvida e direciona a solicitação para a Skill responsável pela análise.

Exemplos de perguntas:

```text
Quais são as perdas?

Quais são as rotas?

Quais são as transportadoras?

Quais são as anomalias?

Quais são os riscos?

Faça um relatório completo.
```

---

# 🎯 Finalidade

O principal objetivo do projeto é desenvolver uma solução capaz de **apoiar profissionais de Prevenção de Perdas na identificação de pontos de atenção, análise de indicadores e priorização de investigações**.

O agente não substitui a análise humana.

Sua função é:

1. Receber uma pergunta;
2. Interpretar a intenção do usuário;
3. Identificar a entidade envolvida;
4. Consultar os dados através da arquitetura MCP;
5. Direcionar os dados para a Skill adequada;
6. Executar a análise;
7. Apresentar os resultados;
8. Apoiar a tomada de decisão humana.

---

# ⚠️ Regra de controle

Os indicadores apresentados pelo sistema representam **pontos de atenção, anomalias ou riscos identificados**.

Uma anomalia não constitui, isoladamente, evidência de fraude ou irregularidade.

Decisões críticas devem ser avaliadas e validadas pela equipe responsável.

```text
ANOMALIA ≠ FRAUDE
```

---

# 🧠 Arquitetura

A arquitetura evoluiu progressivamente até a V5.6.

O fluxo atual utiliza:

```text
USUÁRIO
   │
   ▼
INTERFACE
   │
   ▼
AGENTE
   │
   ▼
INTERPRETADOR
   │
   ▼
MCP CLIENT
   │
   ▼
MCP SERVER
   │
   ▼
TOOLS
   │
   ▼
DADOS / SQLITE
   │
   ▼
SKILLS
   │
   ▼
RESULTADO
   │
   ▼
DECISÃO HUMANA
```

### Fluxo detalhado

```text
Pergunta do usuário
        │
        ▼
app/interpretador.py
        │
        ├── intenção
        └── entidade
        │
        ▼
app/agente.py
        │
        ▼
app/mcp/cliente.py
        │
        ▼
app/mcp/servidor.py
        │
        ▼
app/tools/
        │
        ▼
SQLite / dados externos
        │
        ▼
Skills de análise
        │
        ▼
Resultado
```

A arquitetura foi organizada para separar responsabilidades entre as diferentes camadas do sistema.

---

# 🤖 Agente

Arquivo principal:

```text
app/agente.py
```

Responsável pela:

* Orquestração da aplicação;
* Interpretação da pergunta;
* Consulta dos dados através do MCP;
* Direcionamento para as Skills;
* Formatação dos resultados;
* Interação com o usuário.

---

# 🔎 Interpretador

Arquivo:

```text
app/interpretador.py
```

O interpretador separa a compreensão da pergunta da execução da análise.

O fluxo é:

```text
PERGUNTA
   ↓
INTENÇÃO
   ↓
ENTIDADE
   ↓
AGENTE
   ↓
SKILL
```

Exemplo:

```text
"Qual transportadora apresenta maior risco?"
```

Pode ser interpretado como:

```text
intenção: priorizar
entidade: transportadora
```

O agente utiliza essas informações para executar a análise correspondente.

---

# 🔌 MCP — Model Context Protocol

A partir da V5, o projeto passou a utilizar **MCP (Model Context Protocol)** como camada de comunicação entre o Agente e as ferramentas de acesso aos dados.

Na V5.6, o MCP deixou de ser apenas uma estrutura de teste e passou a fazer parte efetivamente do fluxo de execução do Agente.

Arquivos principais:

```text
app/mcp/

├── __init__.py
├── servidor.py
├── cliente.py
└── testar_cliente.py
```

### MCP Server

Arquivo:

```text
app/mcp/servidor.py
```

O servidor MCP disponibiliza ferramentas para consulta dos dados.

Ferramentas disponíveis:

```text
testar_mcp()

consultar_ocorrencias()

consultar_remessas()

consultar_rotas()

consultar_transportadoras()
```

### MCP Client

Arquivo:

```text
app/mcp/cliente.py
```

O cliente MCP estabelece a comunicação com o servidor e obtém os conjuntos de dados necessários para o Agente.

O fluxo principal é:

```text
AGENTE
   ↓
MCP CLIENT
   ↓
MCP SERVER
   ↓
TOOLS
   ↓
DADOS
```

### Resultado da integração

Na V5.6, o Agente foi validado utilizando efetivamente os dados recuperados através do MCP.

---

# 🧩 Skills

O projeto possui seis Skills especializadas.

## 1. `analisar_perdas`

Responsável pela análise geral das ocorrências e perdas.

Apresenta informações como:

* Quantidade total de ocorrências;
* Valor total registrado;
* Ocorrências em investigação;
* Ocorrências por tipo;
* Impacto financeiro por tipo;
* Tipo de ocorrência mais frequente;
* Tipo com maior impacto financeiro.

---

## 2. `analisar_rotas`

Analisa o comportamento das diferentes rotas logísticas.

Indicadores utilizados:

* Quantidade de remessas;
* Quantidade de ocorrências;
* Índice de ocorrência;
* Valor das perdas registradas.

---

## 3. `analisar_transportadoras`

Analisa os indicadores das transportadoras.

Indicadores:

* Quantidade de remessas;
* Quantidade de ocorrências;
* Índice de ocorrência;
* Valor total das perdas;
* Média de perda por ocorrência.

---

## 4. `analisar_anomalias`

Identifica pontos de atenção com base nos indicadores de:

* Rotas;
* Transportadoras.

As classificações indicam níveis de atenção e não representam, isoladamente, confirmação de irregularidade.

---

## 5. `priorizar_riscos`

Realiza a priorização das rotas de acordo com os indicadores de risco.

As rotas podem ser classificadas em:

* BAIXO;
* MÉDIO;
* ALTO;
* CRÍTICO.

A classificação considera critérios definidos na lógica da Skill, combinando frequência das ocorrências e impacto financeiro.

---

## 6. `gerar_relatorio`

Consolida informações do sistema em um relatório de Prevenção de Perdas.

O relatório pode apresentar:

* Resumo executivo;
* Rotas prioritárias;
* Pontos de atenção;
* Análise das transportadoras;
* Recomendações;
* Observações de controle.

---

# 🛠️ Tools

A arquitetura possui uma camada específica de Tools.

Diretório:

```text
app/tools/
```

Principais componentes:

```text
dados.py
ler_csv.py
validar_csv.py
normalizar_dados.py
importar_externo.py
```

### `dados.py`

Disponibiliza funções para obtenção dos dados utilizados pelas Skills:

```text
obter_remessas()
obter_ocorrencias()
obter_rotas()
obter_transportadoras()
```

### Tools de dados externos

O projeto também possui ferramentas para trabalhar com arquivos CSV externos:

```text
ler_csv()
validar_csv()
normalizar_ocorrencias()
importar_ocorrencias_externas()
```

O fluxo de dados externos é:

```text
CSV EXTERNO
    ↓
LEITURA
    ↓
VALIDAÇÃO
    ↓
NORMALIZAÇÃO
    ↓
IMPORTAÇÃO
    ↓
SQLITE
    ↓
MCP
    ↓
SKILLS
```

Essa estrutura permite que o projeto evolua futuramente para fontes de dados externas reais.

---

# 🗄️ Banco de dados

O projeto utiliza **SQLite** como banco de dados relacional.

Banco:

```text
dados/prevencao_perdas.db
```

Principais tabelas:

```text
remessas
ocorrencias
rotas
transportadoras
```

A camada de acesso ao banco está organizada em:

```text
app/database/

├── conexao.py
├── criar_banco.py
├── importar_dados.py
├── validar_banco.py
└── consultas.py
```

---

# 📥 Dados externos

A partir da V5, foi criada uma estrutura para permitir a entrada de dados externos através de arquivos CSV.

O sistema realiza:

```text
Arquivo CSV
    ↓
Leitura
    ↓
Validação
    ↓
Normalização
    ↓
Importação
    ↓
SQLite
```

A validação verifica, entre outros aspectos:

* Existência das colunas obrigatórias;
* Registros vazios;
* Valores numéricos;
* Estrutura básica do arquivo.

Essa camada foi criada pensando na futura substituição dos dados fictícios por dados operacionais estruturados.

---

# 🌐 Interface Web

O projeto possui uma interface web desenvolvida com **Streamlit**.

Principais arquivos:

```text
app/interface.py
app/dashboard.py
```

A interface apresenta informações relacionadas às análises de:

* Perdas;
* Rotas;
* Transportadoras;
* Riscos.

A arquitetura foi organizada para separar a interface da lógica do Dashboard.

Fluxo:

```text
Interface
   ↓
Dashboard
   ↓
Agente / análises
   ↓
Dados
```

---

# 🛠️ Tecnologias utilizadas

## Python 3.13

Principal linguagem utilizada no desenvolvimento.

Utilizada para:

* Desenvolvimento do agente;
* Implementação das Skills;
* Implementação das Tools;
* Interpretação das perguntas;
* Processamento dos dados;
* Regras de negócio;
* Priorização de riscos;
* Geração de relatórios;
* Integração com MCP;
* Interface web.

---

## SQLite

Banco de dados relacional utilizado para armazenar os dados da aplicação.

---

## CSV

Utilizado como fonte de dados fictícios e também como mecanismo de entrada para testes de dados externos.

---

## MCP — Model Context Protocol

Utilizado como camada de comunicação entre o Agente e as ferramentas responsáveis pelo acesso aos dados.

---

## Streamlit

Utilizado para construção da interface web e do Dashboard.

---

## Visual Studio Code

Utilizado como ambiente principal de desenvolvimento.

---

## Git

Utilizado para controle de versões e criação dos checkpoints do projeto.

---

## GitHub

Utilizado para armazenamento, versionamento e apresentação do projeto como portfólio profissional.

---

# 🗂️ Estrutura atual do projeto

```text
APP-Prevencao-de-Perdas/

│
├── app/
│   │
│   ├── agente.py
│   ├── interpretador.py
│   ├── interface.py
│   ├── dashboard.py
│   │
│   ├── mcp/
│   │   ├── __init__.py
│   │   ├── servidor.py
│   │   ├── cliente.py
│   │   └── testar_cliente.py
│   │
│   ├── database/
│   │   ├── conexao.py
│   │   ├── criar_banco.py
│   │   ├── importar_dados.py
│   │   ├── validar_banco.py
│   │   └── consultas.py
│   │
│   ├── skills/
│   │   ├── analisar_anomalias.py
│   │   ├── analisar_perdas.py
│   │   ├── analisar_rotas.py
│   │   ├── analisar_transportadoras.py
│   │   ├── gerar_relatorio.py
│   │   └── priorizar_riscos.py
│   │
│   └── tools/
│       ├── dados.py
│       ├── ler_csv.py
│       ├── validar_csv.py
│       ├── normalizar_dados.py
│       └── importar_externo.py
│
├── dados/
│   ├── remessas.csv
│   ├── ocorrencias.csv
│   ├── rotas.csv
│   ├── transportadoras.csv
│   └── prevencao_perdas.db
│
├── .venv/
│
└── README.md
```

---

# 📊 Dados utilizados

Os dados são fictícios e simulam uma operação de logística e e-commerce.

## Base original

A base original utilizada no projeto possui:

```text
30 remessas
18 ocorrências
4 rotas
2 transportadoras
```

Valor original registrado nas ocorrências:

```text
R$ 28.360,00
```

Tipos de ocorrência da base original:

```text
EXTRAVIO        6
AVARIA          5
DIVERGENCIA     3
FURTO           2
DEVOLUCAO       2
```

---

## Dados externos de teste

Durante a evolução da V5, foram utilizados registros externos fictícios para validar o processo de importação.

Foram adicionadas 3 ocorrências de teste:

```text
3 registros externos
R$ 3.550,00 em perdas
```

Assim, o banco utilizado durante os testes da V5.6 passou a apresentar:

```text
21 ocorrências
R$ 31.910,00 em perdas registradas
```

Esses registros também são fictícios e fazem parte exclusivamente do ambiente demonstrativo do projeto.

---

# 📈 Indicadores analisados

O sistema trabalha com indicadores relacionados a:

### Índice de ocorrência

Relação entre ocorrências e remessas analisadas.

### Valor das perdas

Valor financeiro registrado nas ocorrências.

### Frequência de ocorrências

Quantidade de ocorrências por:

* Rota;
* Transportadora;
* Tipo de ocorrência.

### Média de perda por ocorrência

Permite analisar o impacto financeiro médio das ocorrências.

### Classificação de risco

As rotas podem ser classificadas de acordo com os critérios definidos na lógica da Skill `priorizar_riscos`.

---

# 💡 Exemplos de utilização

Após iniciar o agente:

```text
=== AGENTE DE PREVENÇÃO DE PERDAS ===

Digite uma pergunta para o agente.

Digite 'sair' para encerrar.
```

O usuário pode realizar perguntas como:

```text
Quais são as perdas?
```

```text
Quais são as rotas?
```

```text
Quais são as transportadoras?
```

```text
Quais são as anomalias?
```

```text
Quais são os riscos?
```

O Agente interpreta a pergunta, consulta os dados através do MCP e direciona os dados para a Skill correspondente.

---

# ▶️ Como executar o projeto

## 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
```

Depois:

```bash
cd APP-Prevencao-de-Perdas
```

---

## 2. Criar o ambiente virtual

```powershell
python -m venv .venv
```

---

## 3. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Executar o Agente

```powershell
python -m app.agente
```

---

## 5. Executar o Dashboard

```powershell
python -m streamlit run app\interface.py
```

A interface web será aberta pelo Streamlit no navegador.

---

# 🧪 Validação da V5.6

A integração MCP → Agente → Skills foi validada através de cinco perguntas principais.

### Teste 1 — Perdas

```text
Quais são as perdas?
```

Status:

```text
✅ APROVADO
```

---

### Teste 2 — Rotas

```text
Quais são as rotas?
```

Status:

```text
✅ APROVADO
```

---

### Teste 3 — Transportadoras

```text
Quais são as transportadoras?
```

Status:

```text
✅ APROVADO
```

---

### Teste 4 — Anomalias

```text
Quais são as anomalias?
```

Status:

```text
✅ APROVADO
```

---

### Teste 5 — Riscos

```text
Quais são os riscos?
```

Status:

```text
✅ APROVADO
```

---

# 🔐 Segurança e governança

O projeto adota premissas importantes para utilização em um contexto de Prevenção de Perdas.

## O agente não acusa fraude automaticamente

Uma anomalia pode representar:

* Erro operacional;
* Falha de processo;
* Divergência de informação;
* Problema logístico;
* Necessidade de investigação.

Portanto:

```text
ANOMALIA ≠ FRAUDE
```

---

## Decisão humana

O agente atua como ferramenta de apoio:

```text
DADOS
  ↓
ANÁLISE
  ↓
INDÍCIO / PONTO DE ATENÇÃO
  ↓
INVESTIGAÇÃO
  ↓
VALIDAÇÃO HUMANA
  ↓
DECISÃO
```

As informações produzidas pelo sistema não devem ser utilizadas isoladamente para decisões críticas.

---

# 🏗️ Evolução do projeto

O projeto foi desenvolvido de forma incremental.

## V1 — Agente e análises iniciais

Implementação inicial utilizando:

* Python;
* CSV;
* Análises;
* Skills;
* Agente básico;
* Geração de resultados.

---

## V1.1 — Interpretação de linguagem natural

Evolução da capacidade de interpretar diferentes formas de perguntas.

---

## V1.2 — Interpretação estruturada

Implementação do:

```text
app/interpretador.py
```

Responsável por identificar:

```text
INTENÇÃO
ENTIDADE
```

antes da execução da Skill.

---

## V2 — Persistência com SQLite

Evolução da arquitetura para utilização de banco de dados.

Foi implementado:

```text
app/database/
```

com:

* Conexão com SQLite;
* Criação das tabelas;
* Importação dos dados;
* Validação do banco;
* Consultas estruturadas.

---

## V3 — Skills + Tools

A arquitetura foi evoluída para separar a lógica de análise do acesso aos dados.

Foi criada a camada:

```text
app/tools/
```

As Skills passaram a utilizar Tools para obtenção dos dados.

Fluxo:

```text
AGENTE
   ↓
SKILL
   ↓
TOOL
   ↓
DATABASE
   ↓
SQLITE
```

---

## V4.1 — Interface e Dashboard

Foi criada uma interface web com Streamlit e o Dashboard foi separado da interface.

Arquitetura:

```text
INTERFACE
   ↓
DASHBOARD
   ↓
ANÁLISES
   ↓
DADOS
```

A etapa foi validada com:

```powershell
python -m app.dashboard
```

e:

```powershell
python -m streamlit run app\interface.py
```

---

## V5.5 — MCP, dados externos e Skills

Foi implementada a primeira estrutura de MCP.

Também foram adicionadas ferramentas para:

* Leitura de CSV;
* Validação de CSV;
* Normalização de dados;
* Importação de dados externos.

Foi criado o MCP Server com ferramentas de consulta:

```text
consultar_ocorrencias()
consultar_remessas()
consultar_rotas()
consultar_transportadoras()
```

As Skills foram adaptadas para receber dados externos mantendo compatibilidade com o funcionamento anterior.

Checkpoint:

```text
v5.5
```

---

## V5.6 — Integração MCP com o Agente

Na V5.6, o MCP passou a participar efetivamente do fluxo de execução do Agente.

Foi criado:

```text
app/mcp/cliente.py
```

O fluxo passou a ser:

```text
USUÁRIO
   ↓
AGENTE
   ↓
MCP CLIENT
   ↓
MCP SERVER
   ↓
TOOLS
   ↓
DADOS
   ↓
SKILLS
   ↓
RESULTADO
```

As cinco consultas principais foram validadas:

```text
✅ Quais são as perdas?
✅ Quais são as rotas?
✅ Quais são as transportadoras?
✅ Quais são as anomalias?
✅ Quais são os riscos?
```

Checkpoint:

```text
v5.6
```

Commit:

```text
157712d
feat: integrate MCP with agent and skills
```

---

# 📌 Checkpoints Git

O projeto possui checkpoints versionados:

```text
v3.0
│
├── Skills + Tools
│
v4.1
│
├── Interface + Dashboard
│
v5.5
│
├── MCP + dados externos + Skills
│
└── v5.6
    └── MCP integrado ao Agente
```

A branch de desenvolvimento atual é:

```text
v4-interface
```

A `main` permanece como referência do estágio V3, enquanto as evoluções posteriores estão organizadas na branch de desenvolvimento.

---

# 🎓 Conhecimentos aplicados

O desenvolvimento deste projeto permitiu aplicar conhecimentos relacionados a:

* Python;
* Estruturas de dados;
* Funções;
* Modularização;
* Importação de módulos;
* Arquitetura de software;
* Arquitetura de agentes;
* Model Context Protocol (MCP);
* Manipulação de arquivos CSV;
* Banco de dados SQLite;
* SQL;
* Análise de dados;
* Indicadores operacionais;
* Regras de negócio;
* Inteligência Artificial;
* Agentes inteligentes;
* Interpretação de linguagem natural;
* Orquestração de Skills;
* Tools;
* Prevenção de Perdas;
* Logística;
* E-commerce;
* Gestão de riscos;
* Priorização de investigações;
* Streamlit;
* Git;
* GitHub;
* VS Code;
* Ambientes virtuais Python.

---

# 👨‍💻 Contexto profissional

O projeto foi concebido a partir de situações e conceitos relacionados à área de **Prevenção de Perdas, logística e e-commerce**, transformando conhecimentos de negócio em uma aplicação tecnológica.

A proposta demonstra a aplicação de tecnologia para:

* Identificar padrões;
* Apoiar auditorias;
* Analisar rotas;
* Avaliar indicadores de transportadoras;
* Identificar pontos de atenção;
* Apoiar investigações;
* Automatizar análises;
* Transformar dados operacionais em informações para tomada de decisão.

O projeto também demonstra a evolução de conhecimentos de negócio para uma arquitetura de software composta por **Agente, Skills, Tools, MCP, banco de dados e interface web**.

---

# 🔮 Encerramento e futuras evoluções

A V5.6 representa um estágio funcional importante do projeto, com o MCP integrado efetivamente ao fluxo do Agente.

A partir deste ponto, novas funcionalidades podem ser desenvolvidas futuramente, como:

```text
Integração com APIs externas
        ↓
Alertas automáticos
        ↓
Autenticação e controle de acesso
        ↓
Monitoramento de indicadores
        ↓
Integração com sistemas corporativos
```

Essas funcionalidades não fazem parte do escopo atual do projeto.

O objetivo da versão atual é demonstrar uma arquitetura funcional de **Agente Inteligente aplicado à Prevenção de Perdas**, utilizando dados estruturados, análise de indicadores, Skills, Tools, MCP e interface web.

---

# 📌 Status do projeto

**Versão atual: V5.6 — MCP integrado ao Agente**

```text
🟢 Projeto funcional

🟢 Dados fictícios

🟢 Interpretador implementado

🟢 Agente implementado

🟢 Skills implementadas

🟢 Tools implementadas

🟢 Banco SQLite implementado

🟢 Camada de consultas implementada

🟢 Dados externos implementados

🟢 Validação e normalização de CSV

🟢 MCP Server implementado

🟢 MCP Client implementado

🟢 MCP integrado ao Agente

🟢 Interface Web implementada

🟢 Dashboard implementado

🟢 Priorização de riscos implementada

🟢 Análise de anomalias implementada

🟢 Relatório implementado

🟢 Testes das Skills aprovados

🟢 Testes de integração do Agente aprovados

🟢 Cinco consultas principais validadas

🟢 Checkpoint Git V5.6 criado

🟢 Tag v5.6 publicada no GitHub
```

---

# 📄 Licença

Projeto desenvolvido para fins de **estudo, aprendizado e portfólio profissional**.

Os dados utilizados são fictícios e não representam informações reais de empresas, clientes, transportadoras ou operações logísticas.
