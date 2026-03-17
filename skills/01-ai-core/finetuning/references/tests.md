# Fine-Tuning & Model Optimization — Test Cases

## Purpose

Validate the `finetuning` skill handles diverse scenarios correctly.

---

## Test 1 — Method Selection with GPU Constraint

**Input**:
```
I have 500 instruction-response pairs and a single RTX 3090 (24GB).
I want to fine-tune Llama-3-8B for customer support.
```

**Expected Behavior**:
1. Agent checks dataset size (500 samples — sufficient for SFT).
2. Agent calculates VRAM: 8B FP16 = ~16 GB + optimizer overhead → full FT won't fit.
3. Agent recommends LoRA (fits in 24GB) or QLoRA for safety margin.
4. Agent generates training configuration with LoRA rank 16-32.
5. Agent produces complete `train.py`.

**Pass Criteria**:
- [ ] Method = LoRA (not full FT, not QLoRA unless user prefers)
- [ ] VRAM calculation is explicit
- [ ] Training script is runnable
- [ ] Hyperparameters follow cheat sheet

---

## Test 2 — Dataset Validation

**Input**:
Provide a JSON file with:
- 3 missing "output" fields
- 2 empty "instruction" strings
- 1 entry with broken UTF-8 encoding

**Expected Behavior**:
1. Agent runs dataset audit.
2. Agent detects all 6 issues.
3. Agent refuses to proceed until issues are fixed.
4. Agent provides specific fix suggestions for each issue.

**Pass Criteria**:
- [ ] All 6 issues detected
- [ ] Specific fix for each issue provided
- [ ] Agent does NOT start training with bad data

---

## Test 3 — Overfitting Detection

**Input**:
Simulate a training run where:
- Train loss: 2.5 → 0.3 (decreasing)
- Val loss: 2.4 → 1.8 → 2.1 → 2.5 (increasing after step 200)

**Expected Behavior**:
1. Agent detects val loss increase at step 200.
2. Agent recommends using checkpoint from step 200.
3. Agent suggests: fewer epochs, lower LR, or more data.

**Pass Criteria**:
- [ ] Overfitting detected automatically
- [ ] Best checkpoint identified
- [ ] Actionable recommendations provided

---

## Test 4 — Resource-Constrained Training

**Input**:
```
Fine-tune Llama-3-70B. Available hardware: laptop with 16GB RAM, no GPU.
```

**Expected Behavior**:
1. Agent calculates: 70B model needs minimum 24GB VRAM (QLoRA 4-bit).
2. Agent recognizes local training is impossible.
3. Agent recommends alternatives:
   - Cloud GPU (RunPod, Lambda Labs, Google Colab Pro)
   - API-based fine-tuning (OpenAI, Together AI)
   - Smaller model that fits constraints

**Pass Criteria**:
- [ ] Agent does NOT attempt local training
- [ ] Alternatives include cloud GPU options with cost estimates
- [ ] Agent suggests smaller model alternatives

---

## Test 5 — GGUF Export Pipeline

**Input**:
```
I've fine-tuned Mistral-7B with LoRA. Convert it to GGUF Q4_K_M
for use with llama.cpp on a CPU-only server.
```

**Expected Behavior**:
1. Agent merges LoRA adapter with base model.
2. Agent tests merged model.
3. Agent provides exact conversion commands:
   ```bash
   python convert_hf_to_gguf.py merged_model/ --outtype f16 --outfile model.gguf
   ./llama-quantize model.gguf model-q4_k_m.gguf Q4_K_M
   ```
4. Agent verifies output file exists and runs inference test.

**Pass Criteria**:
- [ ] Merge step included
- [ ] Conversion commands are correct
- [ ] Quantization method matches request
- [ ] Verification step included

---

## Test 6 — Fine-Tuning Justification Check

**Input**:
```
I want to fine-tune GPT-4o to answer FAQs about our product.
We have 30 FAQ entries.
```

**Expected Behavior**:
1. Agent flags: 30 entries is too few for effective fine-tuning.
2. Agent recommends RAG instead:
   - "With only 30 FAQ entries, RAG will give you better results at lower cost."
3. Agent presents comparison table.

**Pass Criteria**:
- [ ] Agent does NOT proceed with fine-tuning
- [ ] RAG recommended as better alternative
- [ ] Clear justification with cost/quality comparison

---

## Test 7 — Multi-GPU Training Setup

**Input**:
```
I have 4 A100 GPUs (80GB each). Fine-tune Llama-3-70B with full
fine-tuning on 50K instruction pairs.
```

**Expected Behavior**:
1. Agent verifies: 4×80GB = 320GB. Full FT of 70B (140GB FP16) + optimizer → fits with DeepSpeed ZeRO-3.
2. Agent configures multi-GPU training:
   - DeepSpeed ZeRO Stage 3
   - Distributed training with Accelerate
3. Agent produces `train.py` + `deepspeed_config.json` + `accelerate_config.yaml`

**Pass Criteria**:
- [ ] Multi-GPU training correctly configured
- [ ] DeepSpeed configuration included
- [ ] Effective batch size accounts for 4 GPUs
- [ ] All config files are consistent
