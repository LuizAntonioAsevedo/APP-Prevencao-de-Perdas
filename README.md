# 🤖 Agente Inteligente de Prevenção de Perdas

Sistema desenvolvido em **Python** para apoiar processos de **Prevenção de Perdas em operações de e-commerce e logística**, utilizando análise de dados, interpretação de perguntas em linguagem natural e uma arquitetura modular de agente inteligente.

> **Projeto de portfólio — os dados utilizados são fictícios e destinados exclusivamente para fins educacionais e demonstrativos.**

---

## 📌 Sobre o projeto

O **Agente Inteligente de Prevenção de Perdas** foi criado para demonstrar como conceitos de **Inteligência Artificial, análise de dados, automação e arquitetura de agentes** podem ser aplicados a problemas relacionados a operações logísticas.

O sistema trabalha com dados fictícios de:

* Remessas;
* Ocorrências;
* Rotas;
* Transportadoras;
* Valores de perdas;
* Status das ocorrências.

A partir desses dados, o agente consegue interpretar perguntas em linguagem natural, identificar a intenção do usuário e direcionar a solicitação para a **Skill** responsável pela análise.

Exemplos de perguntas:

* "Onde estão concentradas as perdas?"
* "Qual rota merece mais atenção?"
* "Qual transportadora apresenta maior risco?"
* "Existe algum comportamento anormal?"
* "Qual deveria ser minha prioridade de investigação?"
* "Faça um relatório completo."

---

# 🎯 Finalidade

O principal objetivo do projeto é desenvolver uma solução que possa **apoiar profissionais de Prevenção de Perdas na identificação de pontos de atenção e priorização de investigações**.

O agente não substitui a análise humana.

Sua função é:

1. Receber uma pergunta;
2. Interpretar a intenção do usuário;
3. Identificar a entidade envolvida;
4. Direcionar a solicitação para a Skill adequada;
5. Utilizar as Tools responsáveis pelo acesso aos dados;
6. Analisar os indicadores disponíveis;
7. Apresentar os resultados;
8. Apoiar a tomada de decisão humana.

## ⚠️ Regra de controle

Os indicadores apresentados pelo sistema representam **pontos de atenção, anomalias ou riscos identificados**.

Uma anomalia não constitui, isoladamente, evidência de fraude ou irregularidade.

Decisões críticas devem ser avaliadas e validadas pela equipe responsável.

---

# 🧠 Arquitetura

A arquitetura atual utiliza uma separação entre **Agente, Skills, Tools e acesso ao banco de dados**.

O fluxo principal é:

```text
                         USUÁRIO
                            │
                            ▼
                  PERGUNTA EM LINGUAGEM
                       NATURAL
                            │
                            ▼
                     INTERPRETADOR
                  app/interpretador.py
                            │
                     ┌──────┴──────┐
                     │             │
                  INTENÇÃO      ENTIDADE
                     │             │
                     └──────┬──────┘
                            ▼
                         AGENTE
                    app/agente.py
                            │
                            ▼
                         SKILL
                            │
                            ▼
                          TOOL
                            │
                            ▼
                    DATABASE / CONSULTAS
                            │
                            ▼
                         SQLite
                            │
                            ▼
                         DADOS
                            │
                            ▼
                       RESULTADO
                            │
                            ▼
                    DECISÃO HUMANA
```

Essa separação permite que cada camada tenha uma responsabilidade específica.

### Agente

Responsável pela interação com o usuário e pela orquestração da execução.

### Interpretador

Identifica a intenção e a entidade presentes na pergunta.

### Skill

Representa uma capacidade especializada do agente.

### Tool

Responsável por executar operações específicas, como obtenção de dados.

### Database

Centraliza o acesso aos dados armazenados no SQLite.

---

# 🔎 Interpretação de perguntas

O projeto possui um interpretador responsável por separar a interpretação da pergunta da execução da análise.

Arquivo:

```text
app/interpretador.py
```

O fluxo é:

```text
PERGUNTA
   ↓
INTENÇÃO
   ↓
ENTIDADE
   ↓
SKILL
   ↓
TOOL
   ↓
DADOS
```

Por exemplo:

```text
"Qual transportadora apresenta maior risco?"
```

é interpretado como:

```text
intenção: priorizar
entidade: transportadora
```

O agente então direciona a solicitação para a análise correspondente.

Essa separação torna a arquitetura mais organizada e facilita futuras evoluções.

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

As rotas são classificadas em níveis:

* BAIXO;
* MÉDIO;
* ALTO;
* CRÍTICO.

A classificação considera os critérios definidos na lógica da Skill, combinando frequência das ocorrências e impacto financeiro.

---

## 6. `gerar_relatorio`

Consolida as principais informações do sistema em um relatório de Prevenção de Perdas.

O relatório apresenta:

* Resumo executivo;
* Rotas prioritárias;
* Pontos de atenção;
* Análise das transportadoras;
* Recomendações;
* Observações de controle.

---

# 🛠️ Tools

A partir da **V3**, o projeto passou a utilizar uma camada específica de Tools.

Arquivo principal:

```text
app/tools/dados.py
```

A Tool de dados disponibiliza funções para obtenção das informações utilizadas pelas Skills:

```text
obter_remessas()
obter_ocorrencias()
obter_rotas()
obter_transportadoras()
```

As Skills não precisam acessar diretamente o banco de dados.

O fluxo passou a ser:

```text
SKILL
  ↓
TOOL
  ↓
DATABASE
  ↓
SQLITE
```

Essa separação reduz o acoplamento entre a lógica de análise e a camada de acesso aos dados.

---

# 🗄️ Banco de dados

A partir da **V2**, o projeto passou a utilizar **SQLite** como banco de dados.

Banco:

```text
dados/prevencao_perdas.db
```

O banco possui as seguintes tabelas:

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

### Fluxo de dados

Os dados fictícios inicialmente são mantidos em arquivos CSV e podem ser importados para o banco SQLite.

```text
CSV
 │
 ▼
IMPORTAÇÃO
 │
 ▼
SQLite
 │
 ▼
CONSULTAS
 │
 ▼
TOOLS
 │
 ▼
SKILLS
 │
 ▼
AGENTE
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
* Geração dos relatórios.

---

## SQLite

Banco de dados relacional utilizado para armazenar os dados da aplicação.

Permite evoluir o projeto além da utilização direta de arquivos CSV.

---

## CSV

Os arquivos CSV são utilizados como fonte de dados fictícios para a aplicação.

Arquivos:

```text
dados/
├── remessas.csv
├── ocorrencias.csv
├── rotas.csv
└── transportadoras.csv
```

---

## Python Virtual Environment — `.venv`

O projeto utiliza um ambiente virtual Python para isolamento do ambiente de desenvolvimento.

```text
.venv/
```

Ativação no Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## Visual Studio Code

O projeto foi desenvolvido utilizando o **Visual Studio Code**.

Recursos utilizados:

* Editor de código;
* Terminal integrado;
* Organização dos arquivos;
* Execução do Python;
* Testes e validações;
* Desenvolvimento incremental.

---

## Git

Utilizado para controle de versões.

Permite:

* Registrar alterações;
* Criar histórico do desenvolvimento;
* Recuperar versões anteriores;
* Organizar a evolução do projeto.

---

## GitHub

Utilizado como plataforma para versionamento e apresentação do projeto como portfólio profissional.

---

# 🗂️ Estrutura atual do projeto

```text
APP-Prevencao-de-Perdas/
│
├── app/
│   │
│   ├── agente.py
│   ├── interpretador.py
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
│       └── dados.py
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

Os dados são fictícios e foram criados para simular uma operação de logística e e-commerce.

## Remessas

Arquivo:

```text
dados/remessas.csv
```

Contém informações como:

* ID da remessa;
* Data;
* Origem;
* Destino;
* Rota;
* Transportadora;
* Valor da mercadoria;
* Status.

---

## Ocorrências

Arquivo:

```text
dados/ocorrencias.csv
```

Contém:

* ID da ocorrência;
* ID da remessa;
* Data;
* Tipo de ocorrência;
* Rota;
* Transportadora;
* Valor da perda;
* Status;
* Descrição.

Tipos utilizados:

```text
EXTRAVIO
AVARIA
DIVERGENCIA
FURTO
DEVOLUCAO
```

---

## Rotas

Arquivo:

```text
dados/rotas.csv
```

Contém:

* ID da rota;
* Origem;
* Destino;
* Distância;
* Região.

---

## Transportadoras

Arquivo:

```text
dados/transportadoras.csv
```

Contém:

* ID da transportadora;
* Nome;
* Tipo de operação;
* Região.

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

Permite avaliar o impacto financeiro médio das ocorrências.

### Classificação de risco

As rotas podem ser classificadas de acordo com os critérios definidos na lógica da Skill `priorizar_riscos`.

---

# 📌 Resultados dos dados utilizados

A base fictícia atualmente utilizada possui:

```text
30 remessas
18 ocorrências
4 rotas
2 transportadoras
```

Valor total registrado nas ocorrências:

```text
R$ 28.360,00
```

Tipos de ocorrência registrados:

```text
EXTRAVIO       6
AVARIA         5
DIVERGENCIA    3
FURTO          2
DEVOLUCAO      2
```

Os indicadores permitem analisar tanto a **frequência** quanto o **impacto financeiro** das ocorrências.

---

# 💡 Exemplo de utilização

Após iniciar o agente, o sistema apresenta:

```text
=== AGENTE DE PREVENÇÃO DE PERDAS ===

Digite uma pergunta para o agente.

Digite 'sair' para encerrar.
```

O usuário pode perguntar:

```text
Qual transportadora apresenta maior risco?
```

O agente interpreta a pergunta e direciona a solicitação para a Skill correspondente.

Exemplo de resultado:

```text
Análise das transportadoras:

- RapLog: 10 ocorrências em 15 remessas;
  índice de ocorrência de 66.67%;
  perdas de R$ 15.730,00.

- TransLog: 8 ocorrências em 15 remessas;
  índice de ocorrência de 53.33%;
  perdas de R$ 12.630,00.
```

---

# ▶️ Como executar o projeto

## 1. Clonar o projeto

```bash
git clone <URL_DO_REPOSITORIO>
```

Depois entre na pasta:

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

## 4. Executar o agente

Com o ambiente virtual ativado:

```powershell
python -m app.agente
```

> A execução com `python -m app.agente` é importante porque o projeto utiliza a estrutura de pacotes `app`, `app.skills`, `app.tools` e `app.database`.

---

# 🧪 Testes realizados

A aplicação foi validada progressivamente durante sua evolução.

## Teste 1 — Transportadora

Pergunta:

```text
Qual transportadora apresenta maior risco?
```

Resultado:

```text
Análise das transportadoras
```

Status:

```text
✅ APROVADO
```

---

## Teste 2 — Rota

Pergunta:

```text
Qual rota merece mais atenção?
```

Resultado:

```text
Priorização das rotas
```

Status:

```text
✅ APROVADO
```

---

## Teste 3 — Relatório

Pergunta:

```text
Faça um relatório completo.
```

Resultado:

```text
RELATÓRIO DE PREVENÇÃO DE PERDAS
```

Status:

```text
✅ APROVADO
```

---

# 🏗️ Evolução do projeto

O projeto foi desenvolvido de forma incremental.

## V1.0 — Agente básico

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

Exemplos:

```text
Onde estão concentradas as perdas?

Qual rota merece mais atenção?

Qual transportadora apresenta maior risco?

Existe algum comportamento anormal?

Qual deveria ser minha prioridade de investigação?
```

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

A versão foi validada com perguntas em linguagem natural.

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

Banco:

```text
dados/prevencao_perdas.db
```

---

## V3 — Skills + Tools

A arquitetura foi evoluída para separar a lógica de análise do acesso aos dados.

Foi criada a camada:

```text
app/tools/
```

com a Tool:

```text
app/tools/dados.py
```

As Skills passaram a utilizar as Tools para obter os dados.

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

As seis Skills foram validadas:

```text
✅ analisar_perdas
✅ analisar_rotas
✅ analisar_transportadoras
✅ analisar_anomalias
✅ priorizar_riscos
✅ gerar_relatorio
```

Além disso, o agente completo foi testado novamente após a evolução arquitetural.

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

# 🎓 Conhecimentos aplicados

O desenvolvimento deste projeto permitiu aplicar conhecimentos relacionados a:

* Python;
* Estruturas de dados;
* Funções;
* Modularização;
* Importação de módulos;
* Arquitetura de software;
* Arquitetura de agentes;
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
* Priorizar rotas;
* Avaliar indicadores de transportadoras;
* Identificar pontos de atenção;
* Apoiar investigações;
* Automatizar análises;
* Transformar dados operacionais em informações para tomada de decisão.

---

# 🔮 Próximas evoluções

A arquitetura atual permite futuras evoluções, como:

```text
V4
└── Interface Web com Streamlit

V5
└── Integração com MCP

V6
└── Dashboard e alertas

V7
└── Integração com APIs externas

V8
└── Alertas e análises avançadas
```

Essas funcionalidades **não fazem parte da V3 atual** e representam possibilidades de evolução do projeto.

---

# 📌 Status do projeto

**Versão atual: V3 — Skills + Tools**

```text
🟢 Projeto funcional
🟢 Dados fictícios
🟢 Interpretador implementado
🟢 Agente implementado
🟢 Skills implementadas
🟢 Tools implementadas
🟢 Banco SQLite implementado
🟢 Camada de consultas implementada
🟢 Relatório implementado
🟢 Priorização de riscos implementada
🟢 Testes das Skills aprovados
🟢 Testes de integração do agente aprovados
```

---

# 📄 Licença

Projeto desenvolvido para fins de **estudo, aprendizado e portfólio profissional**.

Os dados utilizados são fictícios e não representam informações reais de empresas, clientes, transportadoras ou operações logísticas.
