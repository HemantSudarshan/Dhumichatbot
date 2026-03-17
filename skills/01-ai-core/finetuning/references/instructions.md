# Fine-Tuning & Model Optimization — Agent Instructions

## How This Skill Activates

1. Agent reads YAML frontmatter during skill discovery.
2. If user request matches "fine-tune," "train a model," "adapt a model," "LoRA," "PEFT," "optimize model performance," or similar, load the full SKILL.md.
3. Follow the 6-phase workflow sequentially.

## Execution Instructions

### Step 1 — Evaluate If Fine-Tuning Is Needed

Before any fine-tuning work:

1. Ask the user: "What have you tried so far? Prompting? RAG?"
2. If the user has NOT tried prompting or RAG, recommend trying those first.
3. Apply the Pre-Check table from SKILL.md.
4. Only proceed with fine-tuning if there's a clear justification:
   - Specific output style/format required
   - Consistent domain-specific behavior needed
   - Latency requirements (smaller fine-tuned model vs large general model)
   - Cost optimization (fewer tokens needed with fine-tuned model)
5. Document justification in `experiment_log.md`.

### Step 2 — Audit the Training Dataset

1. Load the dataset and run automated quality checks:
   ```python
   import pandas as pd
   
   df = pd.read_json("training_data.jsonl", lines=True)
   print(f"Total samples: {len(df)}")
   print(f"Null values:\n{df.isnull().sum()}")
   print(f"Duplicates: {df.duplicated().sum()}")
   print(f"Text length stats:\n{df['text'].str.len().describe()}")
   ```

2. Check for minimum dataset size:
   | Task | Minimum Samples | Recommended |
   |------|----------------|-------------|
   | Classification | 100 per class | 500+ per class |
   | Instruction SFT | 100 | 1,000+ |
   | Chat fine-tuning | 500 conversations | 5,000+ |
   | Code generation | 500 examples | 10,000+ |

3. If dataset is below minimum, recommend:
   - Data augmentation
   - Synthetic data generation with GPT-4
   - Few-shot learning instead

4. Verify the format matches the expected schema (see SKILL.md Phase 1).

5. Generate `dataset_audit_report.md`.

### Step 3 — Select the Fine-Tuning Method

1. Gather hardware constraints from the user:
   - GPU model and VRAM
   - Number of GPUs
   - Compute budget (hours or cost)

2. Apply the decision matrix from SKILL.md Phase 2.

3. Present recommendation to user:
   - "Based on your [GPU model] with [X GB VRAM], I recommend [method] for [model]."
   - Include VRAM usage estimate.

4. Wait for user confirmation.

### Step 4 — Configure and Launch Training

1. Generate training configuration:
   - Create `training_config.yaml` with all hyperparameters
   - Use the cheat sheet from SKILL.md Phase 3
   - Apply these rules:
     - Effective batch size = `per_device_batch_size × gradient_accumulation × num_gpus`
     - Target effective batch size of 16-32
     - Start with learning rate 2e-4 for LoRA, 2e-5 for full FT

2. Generate `train.py` based on the template in SKILL.md:
   - Include all imports
   - Configure W&B logging
   - Set up data loading
   - Configure model and tokenizer
   - Set up PEFT (if using LoRA/QLoRA)
   - Include checkpointing

3. Before launching, run a dry run:
   ```python
   # Verify 1 batch processes without error
   trainer.train(resume_from_checkpoint=False, max_steps=1)
   ```

4. If dry run passes, launch full training.

### Step 5 — Monitor Training

1. Watch the W&B dashboard (or terminal logs) for:
   - Loss curve: should decrease
   - Val loss: should decrease then plateau
   - GPU memory: should be stable

2. If val loss increases for 3 consecutive evaluations → trigger early stopping.

3. If loss is NaN → stop immediately:
   - Reduce learning rate by 10x
   - Check for data issues (NaN values, extreme outliers)
   - Try gradient clipping (`max_grad_norm=1.0`)

4. Log all observations.

### Step 6 — Evaluate the Fine-Tuned Model

1. Load the best checkpoint (lowest validation loss).

2. Run quantitative evaluation:
   ```python
   from evaluate import load
   
   # Example: text generation evaluation
   rouge = load("rouge")
   results = rouge.compute(predictions=preds, references=refs)
   print(results)
   ```

3. Run qualitative evaluation:
   - Test 20 diverse inputs
   - Compare base model vs fine-tuned model responses
   - Document any regressions

4. Run general capability benchmark:
   - Test on 3-5 standard benchmarks
   - Ensure < 10% regression on general tasks

5. Generate `eval_report.md` with all results.

### Step 7 — Optimize and Export

1. If using LoRA, merge adapters:
   ```python
   merged_model = model.merge_and_unload()
   merged_model.save_pretrained("merged_model")
   tokenizer.save_pretrained("merged_model")
   ```

2. Test the merged model:
   - Run the same 20 qualitative tests
   - Verify outputs match the adapter-based model

3. Quantize if needed:
   | Target | Quantization | Tool |
   |--------|-------------|------|
   | llama.cpp | GGUF Q4/Q5/Q8 | llama.cpp convert + quantize |
   | vLLM | AWQ | AutoAWQ |
   | GPU serving | GPTQ | AutoGPTQ |
   | CPU serving | ONNX INT8 | Optimum |

4. Benchmark inference speed on target hardware.

5. Write `experiment_log.md`:
   - Model, method, dataset used
   - All hyperparameters
   - Training curves and metrics
   - Final evaluation results
   - Time and compute cost
   - Conclusions and recommendations

### Step 8 — Document and Hand Off

1. Generate model card (trigger `documentation` skill).
2. Upload artifacts to designated storage.
3. Record experiment in experiment tracking system.

## Interaction Protocol

| Situation | Agent Behavior |
|-----------|---------------|
| User wants to fine-tune but hasn't tried prompting | Suggest trying prompting first |
| Dataset is too small | Warn user, suggest alternatives |
| GPU insufficient for chosen method | Recommend QLoRA or cloud GPU |
| Training diverges (loss NaN) | Stop training, diagnose, reduce LR |
| Model overfits | Recommend early stopping, report findings |
| Evaluation shows regression | Report with data, let user decide |

## Handoff to Other Skills

- If data cleaning needed → activate `data-pipeline` skill
- If model needs deployment → activate `ai-integration` skill
- If monitoring needed → activate `ai-reliability` skill
- If experiment docs needed → activate `documentation` skill
