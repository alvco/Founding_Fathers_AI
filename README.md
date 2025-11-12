# AI Founding Fathers: Multi-Agent GIS Search

[![arXiv](https://img.shields.io/badge/arXiv-XXXX.XXXXX-b31b1b.svg)](https://arxiv.org/abs/XXXX.XXXXX)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A comparative study of multi-agent pipeline architectures for enhancing LLM reasoning through gradual, incremental, and sequential (GIS) search.**

> 📄 **[Read the full research paper on arXiv](https://arxiv.org/abs/XXXX.XXXXX)**

---

## Overview

This repository contains the complete implementation and experimental results for my research on multi-agent pipelines and enhancing LLM reasoning which I synthesize into a systematic framework called gradual, incremental, and sequential (GIS) search. The project assesses whether explicitly structuring a multi-agent pipeline to ensure a **gradual, incremental, and sequential (GIS)** traversal of the search space improves language model performance.

**Key Innovation:** I built two distinct multi-agent systems — a 4-agent baseline linear pipeline (simple model) and an 8-agent structured pipeline with a recursive refinement layer (complex model) — and ran a controlled experiment using RAG-powered historical personas of three US Founding Fathers (Hamilton, Jefferson, Madison) to generate responses to three contemporary political questions.

**Result:** The 8-agent GIS-structured pipeline consistently outperformed the simple model across all 9 test cases and outscored its counterpart by an average of 16.7 points (88.3 vs 71.6).

---

## Understanding The Implications

Modern LLM applications increasingly rely on multi-agent architectures, but there's limited understanding of why certain design patterns work better than others. This research:

- **Proposes a systematic framework** (GIS search) for understanding LLM optimization
- **Demonstrates empirically** that structuring a multi-agent pipeline according to GIS-search criteria improves reasoning quality
- **Provides a production-grade implementation** showing best practices in multi-agent system design
- **Bridges theory and practice** by connecting computational search-based interpretations to practical architecture

---

## The GIS Framework

**Core Thesis:** High-quality reasoning is a controlled, incremental search.

The GIS framework asserts that LLM reasoning is best enhanced by structuring pipelines to ensure that a traversal of the search space is:

- **Gradual:** Step-by-step decomposition with distinct, focused stages
- **Incremental:** Each step builds upon and refines previous outputs through feedback
- **Sequential:** Controlled progression prevents premature convergence to suboptimal solutions and local optima

This framework synthesizes why techniques like Chain-of-Thought, self-refinement, and multi-agent debate are effective. More specifically, they all impose structured, modularized, and iterative processes on LLM computation.

---

## Architecture

### Simple Model (4-Agent Baseline)
A linear pipeline representing a baseline architecture:

```
Selector → Researcher → Thinker → Communicator
```

### Complex Model (8-Agent GIS Pipeline)
Implements GIS search through a **Recursive Refinement (RR) loop**:

```
Selector → Researcher → Thinker → [Recursive Refinement Loop] → Communicator
                                    ↓
                        Validator → Red Team → Strategist → Final Judge
```

**Recursive Refinement Loop:**
1. **Validator:** Evaluates candidate arguments and selects the strongest based on internal consistency
2. **Red Team:** Engages in adversarial stress-testing to identify critical vulnerabilities
3. **Strategist:** Develops defensive counter-responses leveraging different rhetorical strategies
4. **Final Judge:** Integrates feedback into refined final argument by selecting the strongest and most resilient constructs

---

## Key Results

### Quantitative Findings
- **9/9 test cases:** Complex model outperformed simple model in every scenario
- **Average scores:** 88.3 (complex) vs 71.6 (simple) — a +23% improvement
- **Consistent across personas:** Hamilton (+22%), Jefferson (+31%), Madison (+17%)

### Qualitative Analysis
Arguments from the complex model demonstrated:
- **Greater analytical depth:** Multi-dimensional reasoning vs. monolithic positions
- **Enhanced nuance:** Qualified, balanced assessments vs. absolutist claims
- **Conceptual expansion:** Expansion and further elaboration of arguments

**Full results:** See [`data/arbiter_scores.csv`](data/arbiter_scores.csv) and [`data/model_outputs.docx`](data/model_outputs.docx)

---

## Technical Highlights

This implementation showcases production-grade engineering practices:

### 🏗️ **Modular Architecture**
- **Separation of Concerns:** Each agent has a single, well-defined responsibility
- **Dependency Injection:** RAG system and prompts injected into agents (not hardcoded)
- **Externalized Configuration:** All prompts managed in `prompts.yaml` for rapid iteration

### 🔍 **RAG System**
- **Vector Store:** ChromaDB with SentenceTransformer embeddings
- **Persona-Specific Filtering:** Metadata ensures Hamilton's agent only queries Hamilton's writings
- **Efficient Retrieval:** Semantic search over 100K+ tokens of historical texts

### 🛡️ **Robust Parsing**
- **"Reason-Then-Extract" Pattern:** Two-stage LLM calls for reliable JSON extraction
- **Fault Tolerance:** `dirtyjson` library handles minor formatting errors
- **Type Safety:** Structured outputs validated before pipeline progression

### 📊 **Evaluation Framework**
- **Dual Assessment:** Quantitative (LLM arbiter) + qualitative (human analysis)
- **Reproducible:** All prompts, data, and results version-controlled

---

## Installation

### Prerequisites
- Python 3.9 or higher
- Anthropic API key (for Claude models)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/alvco/Founding_Fathers_AI.git
cd Founding_Fathers_AI
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure API key:**

Create a `.env` file in the root directory:
```bash
ANTHROPIC_API_KEY=your-api-key-here
```

5. **Prepare RAG corpora:**

The repository includes sample corpora in `corpora/`. The RAG system will automatically:
- Load and chunk the texts
- Generate embeddings
- Create a persistent ChromaDB vector store

---

## Usage

### Running the Experiments

**1. Simple Model (4-agent baseline):**
```bash
python run_simple_model.py
```
Generates arguments using the linear pipeline. Results saved to `simple_model_results.md`.

**2. Complex Model (8-agent GIS pipeline):**
```bash
python run_complex_model.py
```
Generates arguments using recursive refinement. Results saved to `complex_model_results.md`.

**3. Comparative Analysis:**
```bash
python run_analysis.py
```
Evaluates both models using the Arbiter Agent. Outputs quantitative scores and detailed justifications.

### Quick Example

```python
from environment import DebateOrchestrator
from rag_system import RAGSystem

# Initialize system
rag = RAGSystem(corpora_dir="corpora")
orchestrator = DebateOrchestrator(rag_system=rag)

# Generate argument using complex model
result = orchestrator.run_complex_pipeline(
    persona="hamilton",
    question="Should the government prioritize reducing national debt?"
)

print(result['final_argument'])
```

---

## Project Structure

```
Founding_Fathers_AI/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── .gitignore
│
├── Chauhan_GIS_Search_2025.pdf    # Research paper (add after arXiv approval)
│
├── src/
│   ├── base_agent.py              # Core BaseAgent class with JSON parsing
│   ├── specialist_agents.py       # All 9 agent implementations
│   ├── historical_agent.py        # Pipeline orchestration logic
│   ├── rag_system.py              # ChromaDB + SentenceTransformer RAG
│   ├── environment.py             # DebateOrchestrator for experiments
│   └── prompts.yaml               # Externalized agent prompts
│
├── scripts/
│   ├── run_simple_model.py        # Execute 4-agent experiments
│   ├── run_complex_model.py       # Execute 8-agent experiments
│   └── run_analysis.py            # Run arbiter evaluation
│
├── corpora/                       # RAG source texts
│   ├── hamilton.txt               # Federalist Papers, letters, speeches
│   ├── jefferson.txt              # Writings, correspondence
│   └── madison.txt                # Federalist Papers, letters
│
└── data/                          # Experimental results
    ├── arbiter_scores.csv         # Quantitative evaluation data
    └── model_outputs.docx         # Full argument texts
```

---

## Agent Descriptions

### Core Pipeline Agents

**Selector Agent**
- Analyzes debate topic and persona
- Identifies relevant core principle, historical precedent, and ideological ally
- Outputs strategic brief for subsequent agents

**Researcher Agent**
- Queries RAG system with persona-specific filtering
- Retrieves relevant passages from historical writings
- Provides factual grounding for arguments

**Thinker Agent**
- **Simple model:** Generates single, direct evidence-based argument
- **Complex model:** Generates three distinct argument types (orthodox, unorthodox, pragmatic)

**Communicator Agent**
- Stylistic enhancement and final polishing
- Matches persona's authentic voice and rhetorical style
- Produces final publishable argument

### Recursive Refinement Agents (Complex Model Only)

**Validator Agent**
- Evaluates multiple candidate arguments
- Uses the following scoring rubric: principles consistency (60%), personality consistency (25%), intellectual strength (15%)
- Selects highest-scoring argument for stress-testing

**Red Team Agent**
- Adversarial role: identifies critical vulnerabilities
- Simulates counterarguments from opposing founders
- Finds the single most damaging attack vector

**Strategist Agent**
- Develops three defensive strategies:
  - Direct rebuttal (challenge criticism head-on)
  - Reframe & minimize (diminish importance)
  - Concede & outweigh (acknowledge but justify trade-off)

**Final Judge Agent**
- Evaluates original + three strategic variations
- Selects most persuasive and resilient argument
- Produces final integrated output

**Arbiter Agent** (Evaluation Only)
- LLM-powered judge for comparative assessment
- Uses equally weighted scoring criteria: structure, depth, support/justification, rhetoric/style
- Provides quantitative verdict with detailed justification

---

## Key Findings & Discussion

### What the Experiment Validated

The consistent outperformance of the complex model supports several hypotheses:

1. **Structured refinement works:** Iterative self-criticism, stress-testing, and critical feedback improves argument quality
2. **GIS principles generalize:** The framework successfully predicted which architecture would perform better
3. **Specialization adds value:** Dedicated agents for validation, stress-testing, and strategy outperform monolithic generation

### Interesting Edge Cases

**The Jefferson Immigration Scenario:** Both models misconstrued the nomenclature and context of the merit-based immigration question and conflating it with the maintenance of aristocratic privilege. However, the complex model still produced a more sophisticated, nuanced response despite this conceptual misinterpretation — demonstrating that GIS improves argument construction even when inheriting a flawed conceptual foudnation.

### Limitations

- **Sample size:** n=9 exploratory study; larger-scale validation needed for statistical significance
- **Single model:** Tested only on Claude 3 Sonnet; cross-model validation would strengthen findings
- **No ablations:** Cannot isolate which specific architectural features drive improvements (e.g., sequential vs. parallel architectures, number of agents vs. refinement loops, etc.)
- **Subjective evaluation:** LLM arbiter introduces potential biases; human expert evaluation would strengthen conclusions

---

## Citation

If you use this work in your research, please cite:

```bibtex
@article{chauhan2025founding,
  title={AI Founding Fathers: A Case Study of Gradual, Incremental, and Sequential (GIS) Search in Multi-Agent Pipelines},
  author={Chauhan, Alvin},
  journal={arXiv preprint arXiv:XXXX.XXXXX},
  year={2025}
}
```

---

## Future Work

Potential extensions of this research:

- **Scale validation:** Expand to n=100+ test cases with statistical significance testing
- **Ablation studies:** Systematically isolate which architectural features drive improvements (e.g., sequential vs. parallel architectures, varying agent counts, removing refinement loops, etc.)
- **Cross-model testing:** Validate GIS framework across GPT-4, Gemini, Llama models
- **Domain transfer:** Test GIS principles on mathematical reasoning, code generation, scientific analysis
- **Benchmark comparison:** Evaluate on standardized datasets (MMLU, HellaSwag, etc.)
- **Production deployment:** Optimize for latency, cost, and reliability in real-world applications

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Historical texts sourced from [Founders Online](https://founders.archives.gov)
- Built with [Anthropic Claude](https://www.anthropic.com), [ChromaDB](https://www.trychroma.com), and [Sentence Transformers](https://www.sbert.net)

---

## Contact

**Alvin Chauhan**  
📧 alvin.chauhan@gmail.com  
🔗 [LinkedIn](https://www.linkedin.com/in/alvin-chauhan-93855562)  
📄 [arXiv Paper](https://arxiv.org/abs/XXXX.XXXXX)

---

*This research was conducted independently as a portfolio project demonstrating end-to-end capabilities in AI system design, implementation, and evaluation.*