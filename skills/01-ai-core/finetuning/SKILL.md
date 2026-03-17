---
name: finetuning
description: "Use this skill when tasked with fine-tuning, adapting, or optimizing a machine learning model or LLM. Covers dataset preparation, LoRA/QLoRA/PEFT setup, training configuration, hyperparameter tuning, evaluation, and post-training optimization (quantization, export, merging adapters)."
---

# Fine-Tuning & Model Optimization

## Overview

This skill provides a complete, deterministic workflow for fine-tuning ML models and LLMs — from dataset audit through training, evaluation, and optimization for production serving.

## Supporting References

Load only the reference file you need:
- `references/instructions.md` for detailed execution steps and checklists
- `references/debug.md` for common failure modes and recovery actions
- `references/tests.md` for scenario-based validation prompts

## Pre-Check — Is Fine-Tuning Actually Needed?

Before starting, evaluate alternatives:

| Approach | When to Use | Cost | Quality |
|----------|------------|------|---------|
| Prompt Engineering | Task works with instructions + examples | Low | Good |
| RAG | Need factual recall over documents | Medium | Good-High |
| Few-Shot Prompting | < 20 examples, general-purpose model works | Low | Moderate |
| Fine-Tuning | Specific style/format/domain, 100+ examples | High | Highest |

**Rule**: If prompting or RAG can achieve > 85% of the target quality, recommend those first. Fine-tune only when customization is essential.

## Required Inputs

1. **Base model** — which model to fine-tune (e.g., Llama-3-8B, Mistral-7B, GPT-4o-mini)
2. **Training data** — format, size, quality assessment
3. **Task type** — instruction following, classification, code generation, etc.
4. **Hardware** — available GPU(s), VRAM, compute budget
5. **Target** — what quality bar must the fine-tuned model hit?

## Step-by-Step Workflow

### Phase 1 — Data Audit & Preparation

**Objective**: Ensure the training dataset is clean, well-formatted, and sufficient.

1. **Audit the raw data**:
   - Count total samples
   - Check for duplicates (exact + near-duplicate via MinHash)
   - Identify missing/null values
   - Measure text length distribution
   - Detect language and encoding issues

2. **Format the data** for the training method:

   | Training Type | Required Format |
   |--------------|----------------|
   | SFT (Supervised Fine-Tuning) | `{"instruction": "...", "input": "...", "output": "..."}` |
   | Chat Fine-Tuning | `{"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}` |
   | DPO (Direct Preference) | `{"prompt": "...", "chosen": "...", "rejected": "..."}` |
   | Classification | `{"text": "...", "label": "..."}` |

3. **Split the data**:
   - Training: 80-90%
   - Validation: 10-15%
   - Test: 5-10% (held out, NEVER seen during training)
   - Use stratified splitting for classification tasks

4. **Quality filters**:
   - Remove samples shorter than 10 tokens
   - Remove samples longer than context window
   - Remove samples with extreme formatting anomalies
   - Verify label consistency (for classification)

**Output**: `dataset_audit_report.md`, cleaned dataset files

**Validation Gate**: Data passes all quality checks before proceeding.

---

### Phase 2 — Method Selection

**Objective**: Choose the optimal fine-tuning method based on constraints.

**Decision Matrix**:

| Factor | Full Fine-Tuning | LoRA | QLoRA | Adapter Tuning |
|--------|-----------------|------|-------|----------------|
| VRAM (7B model) | ~28 GB | ~8 GB | ~6 GB | ~8 GB |
| VRAM (13B model) | ~52 GB | ~14 GB | ~10 GB | ~14 GB |
| VRAM (70B model) | ~280 GB | ~40 GB | ~24 GB | ~40 GB |
| Training Speed | Slow | Fast | Fast | Fast |
| Quality | Highest | High | High- | High |
| Parameters Updated | All | 0.1-1% | 0.1-1% | 0.5-2% |
| Recommended When | Unlimited compute | Standard case | GPU memory limited | Multiple tasks |

**Decision Rules**:
- VRAM < 8 GB and 7B model → QLoRA (4-bit)
- VRAM 16-24 GB and 7B model → LoRA (default choice)
- VRAM ≥ 48 GB and ≤ 13B model → Full fine-tuning
- Need to serve 1 base model + multiple task adapters → LoRA with separate adapters
- Consumer GPU (RTX 3090/4090) → QLoRA

**Output**: Method selection documented in `training_config.yaml`

---

### Phase 3 — Training Configuration

**Objective**: Set up all hyperparameters and training infrastructure.

**Hyperparameter Cheat Sheet**:

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| Learning Rate | 2e-4 (LoRA), 2e-5 (full FT) | Lower for larger models |
| LR Schedule | cosine with warmup | warmup_ratio: 0.03 |
| Batch Size | Largest that fits in VRAM | Use gradient accumulation |
| Gradient Accumulation | 4-8 steps | Effective batch = batch × accumulation |
| Epochs | 1-3 for LLMs | More epochs = higher overfitting risk |
| LoRA Rank (r) | 8-64 | Higher = more params = better quality |
| LoRA Alpha | 2 × rank | Standard heuristic |
| LoRA Target Modules | q_proj, v_proj, k_proj, o_proj | For attention fine-tuning |
| Weight Decay | 0.01 | Standard regularization |
| Max Seq Length | Model's context window or less | Match training data distribution |
| BF16/FP16 | Use BF16 if GPU supports it | Ampere+ GPUs support BF16 |

**Training Script Template** (HuggingFace + PEFT):
```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
from datasets import load_dataset

# Load base model and tokenizer
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3-8B-Instruct",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
tokenizer.pad_token = tokenizer.eos_token

# LoRA configuration
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./output",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    lr_scheduler_type="cosine",
    warmup_ratio=0.03,
    weight_decay=0.01,
    bf16=True,
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=50,
    save_strategy="steps",
    save_steps=100,
    save_total_limit=3,
    report_to="wandb",
)

# Load dataset
dataset = load_dataset("json", data_files="train.jsonl", split="train")

# Initialize trainer
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    peft_config=peft_config,
    args=training_args,
    max_seq_length=2048,
)

# Train
trainer.train()
trainer.save_model("./final_model")
```

**Output**: `training_config.yaml`, `train.py`

---

### Phase 4 — Training Execution & Monitoring

**Objective**: Run training and monitor for issues.

1. Launch training with logging enabled
2. Monitor these signals:
   - **Training loss**: should decrease steadily
   - **Validation loss**: should decrease, then plateau
   - **Learning rate**: should follow the configured schedule
   - **GPU memory**: should remain stable after first batch
   - **Gradient norms**: should not spike or explode

3. **Early warning signs**:
   | Signal | Problem | Action |
   |--------|---------|--------|
   | Val loss increases while train loss decreases | Overfitting | Stop training, use best checkpoint |
   | Loss is NaN or Inf | Gradient explosion | Reduce learning rate by 10x |
   | Loss doesn't decrease at all | Learning rate too low or data issue | Verify data, increase LR |
   | GPU utilization < 50% | Data loading bottleneck | Increase num_workers, prefetch |

4. Save checkpoints every N steps
5. Log to Weights & Biases for experiment tracking

---

### Phase 5 — Evaluation & Validation

**Objective**: Rigorously assess the fine-tuned model's quality.

1. **Quantitative evaluation**:
   - Perplexity on validation set
   - Task-specific metrics:
     | Task | Metrics |
     |------|---------|
     | Text classification | Accuracy, F1, Precision, Recall |
     | Text generation | BLEU, ROUGE-L, BERTScore |
     | Instruction following | MT-Bench, AlpacaEval |
     | Code generation | HumanEval pass@k |
     | Summarization | ROUGE-1, ROUGE-2, ROUGE-L |

2. **Qualitative evaluation**:
   - Test 20 representative inputs manually
   - Compare: base model output vs fine-tuned output
   - Check for regressions on general tasks

3. **Benchmark against baseline**:
   - Run evaluation on 3 benchmarks BEFORE and AFTER fine-tuning
   - If general capability drops > 10%, consider lower learning rate or LoRA

**Output**: `eval_report.md`

**Validation Gate**: Fine-tuned model must outperform baseline on target task AND not regress > 10% on general tasks.

---

### Phase 6 — Post-Training Optimization & Export

**Objective**: Prepare the model for production serving.

1. **Merge LoRA adapters** (if using LoRA/QLoRA):
   ```python
   from peft import PeftModel
   model = PeftModel.from_pretrained(base_model, "path/to/adapter")
   merged_model = model.merge_and_unload()
   merged_model.save_pretrained("merged_model")
   ```

2. **Quantize for serving**:
   - GGUF for llama.cpp: `python convert.py` + `quantize`
   - GPTQ for GPU serving: AutoGPTQ
   - AWQ for vLLM-optimized serving

3. **Inference speed benchmark**:
   - Measure tokens/second on target hardware
   - Measure time-to-first-token latency
   - Compare: full precision vs quantized

4. **Export and document**:
   - Save model card with training details
   - Upload to HuggingFace Hub (if sharing)
   - Document exact reproduction steps

**Output**: Optimized model artifacts, `experiment_log.md`

---

## Anti-Patterns — DO NOT

| Anti-Pattern | Consequence | Correct Approach |
|-------------|-------------|------------------|
| Skip data validation | Training on corrupt data wastes GPU hours | Always audit data first |
| Use excessively high learning rate | Catastrophic forgetting | Start with recommended defaults |
| Train for too many epochs | Overfitting | Use early stopping, monitor val loss |
| Fine-tune without baseline evaluation | Cannot prove improvement | Always benchmark before and after |
| Merge adapters without testing | Silent quality degradation | Test merged model before deploying |
| Store training data with model weights | Privacy/licensing violation | Keep data and model separate |

## Skill Coordination

- Use `data-pipeline` when raw dataset cleaning or evaluation harness work becomes the bottleneck.
- Use `ai-solution-dev` when fine-tuning is only one phase inside a larger solution build.
- Use `ai-integration` when the tuned model must be exposed through an API or batch interface.
- Use `ai-reliability` when benchmarking, drift checks, or production guards are required.
- Use `documentation` for experiment logs, model cards, and deployment runbooks.
- Use `research` when the right tuning method or model family is still unclear.
