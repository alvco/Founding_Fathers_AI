# AI Founding Fathers: Multi-Agent GIS Search

[![arXiv](https://img.shields.io/badge/arXiv-2511.09005-b31b1b.svg)](https://arxiv.org/abs/2511.09005)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A comparative study of multi-agent pipeline architectures for enhancing LLM reasoning through gradual, incremental, and sequential (GIS) search.**

> **(https://arxiv.org/abs/2511.09005)**

---

## Overview

This repository contains the complete implementation and experimental results for my research on multi-agent pipelines and enhancing LLM reasoning which I synthesize into a systematic framework called gradual, incremental, and sequential (GIS) search. The project assesses whether explicitly structuring a multi-agent pipeline to ensure a **gradual, incremental, and sequential (GIS)** traversal of the search space improves language model performance.

To test this, I built two distinct multi-agent systems — a 4-agent baseline linear pipeline (simple model) and an 8-agent structured pipeline with a recursive refinement layer (complex model) — and ran a controlled experiment using RAG-powered historical personas of three US Founding Fathers (Hamilton, Jefferson, Madison) to generate responses to three contemporary political questions.

**Result:** The 8-agent GIS-structured pipeline consistently outperformed the simple model across all 9 test cases and outscored its counterpart by an average of 16.7 points (88.3 vs 71.6).

---


## The GIS Framework

**Core Thesis:** High-quality reasoning is a controlled, incremental search.

The GIS framework asserts that LLM reasoning is best enhanced by structuring pipelines to ensure that a traversal of the search space is:

- **Gradual:** Step-by-step decomposition with distinct, focused stages
- **Incremental:** Each step builds upon and refines previous outputs through feedback
- **Sequential:** Controlled progression prevents premature convergence to suboptimal solutions and local optima


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


## Installation

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


## Key Findings & Discussion

### What the Experiment Validated

The consistent outperformance of the complex model supports several hypotheses:

1. **Structured refinement works:** Iterative self-criticism, stress-testing, and critical feedback improves argument quality
2. **GIS principles generalize:** The framework successfully predicted which architecture would perform better
3. **Specialization adds value:** Dedicated agents for validation, stress-testing, and strategy outperform monolithic generation

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
  journal={arXiv preprint arXiv:2511.09005},
  year={2025}
}
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Historical texts sourced from [Founders Online](https://founders.archives.gov)
- Built with [Anthropic Claude](https://www.anthropic.com), [ChromaDB](https://www.trychroma.com), and [Sentence Transformers](https://www.sbert.net)

---

## Contact

**Alvin Chauhan**  
alvin.chauhan@gmail.com  
[LinkedIn](https://www.linkedin.com/in/alvin-chauhan-93855562)  
[arXiv Paper](https://arxiv.org/abs/2511.09005)

---

