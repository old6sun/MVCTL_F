# Agent Interception Prediction Analysis

This project analyzes the security trajectories of AI Agents to predict and evaluate interceptions against various malicious behaviors and vulnerabilities. It processes agent interaction logs and computes statistics based on multi-dimensional temporal properties.

## Project Structure

- **`main.py`**: The entry point of the program. It loads the trajectory data (`test.json`) and initiates the verification process.
- **`analyzer.py`**: Contains the core logic for processing agent trajectories. It extracts action sequences layer by layer and evaluates comprehensive security judgments to calculate interception and misjudgment rates.
- **`evaluator.py`**: Contains the robust regular expression rule sets (`evaluate_aps`) for detecting specific security properties across five layers (Input, Reasoning, Execution, Output, and Environment). 

## Core Properties Evaluated

The tool tracks the following multi-dimensional properties to determine if a major danger is triggered:
1. **Property 1 (Environment Layer Vulnerability)**: Un-intercepted environment poisoning.
2. **Property 2 (Input Layer Vulnerability)**: Malicious input or deep disguise.
3. **Property 3 (Cognitive Layer Vulnerability)**: Security alertness generated but not properly corrected.
4. **Property 4 (Agent Inherent Blind Faith)**: Ignoring environment quality warnings to force compliance.

## Usage

1. Ensure your data file is named `test.json` and is placed in the same directory as the scripts.
2. Run the main script via Python:

```bash
python main.py
```

## Output

The script evaluates trajectories and outputs a statistical dashboard grouped by risk sources (e.g., `direct_prompt_injection`, `malicious_tool_execution`, `inherent_agent_failures`). It provides detailed counts of correct danger interceptions versus safe misjudgments for each individual property, as well as a combined comprehensive defense score.

## MvKS_builder Module

The `MvKS_builder` directory contains an advanced verification suite based on Multi-valued Kripke Structures (MvKS). It provides tools for matrix-based temporal logic evaluation, fuzzy state transition mapping, and visual distributions of interception possibilities.

### Key Scripts in `MvKS_builder`:

1. **`mvks_builder.py`**:
   - Parses the agent evaluation logs and constructs a Multi-valued Kripke Structure (MvKS).
   - Generates State-AP matrices and transition possibility matrices (P-matrices).
   - Automatically exports state-space matrices to CSV and outputs high-resolution heatmaps.
   - **Usage**: `python mvks_builder.py`

2. **`verify-property-eventually.py`**:
   - Evaluates specific temporal properties like ♢Φ (Eventually reaching a safe rejection state) across the agent trajectory network.
   - Implements Max-Min composition (Sup-Inf) and transitive closures (P^+, P^*) for logical state-space paths.
   - Generates line charts representing the possibility measure distributions of successful interceptions across states.
   - **Usage**: `python verify-property-eventually.py`

3. **`frequency-calculate.py`**:
   - Analyzes AP property triggers to verify node/keyword coverage.
   - Used for step-size sensitivity analysis and general trajectory density measurements.
   - **Usage**: `python frequency-calculate.py`

### MvKS Execution Flow

To perform a complete formal verification run:
```bash
cd MvKS_builder
# 1. Build matrices and state spaces
python mvks_builder.py

# 2. Evaluate eventual reachability (e.g., safe termination)
python verify-property-eventually.py
```

