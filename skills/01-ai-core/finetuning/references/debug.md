# Fine-Tuning & Model Optimization — Debug Protocol

## Purpose

This file provides deterministic troubleshooting procedures for fine-tuning failures. **When a training error occurs, STOP and follow this protocol.**

---

## Failure 1 — CUDA Out of Memory (OOM)

**Symptom**: `RuntimeError: CUDA out of memory. Tried to allocate X MiB`

**Root Cause**: Model + optimizer states + activations exceed GPU VRAM.

**Diagnostic Steps**:
1. Check current GPU memory usage: `nvidia-smi`
2. Calculate required VRAM:
   - FP16: `num_params × 2 bytes`
   - INT4: `num_params × 0.5 bytes`
   - Optimizer (AdamW): `num_params × 8 bytes` (for trainable params only)
   - Activations: depends on batch size and sequence length

**Fix Ladder** (apply in order until resolved):
1. Reduce `per_device_train_batch_size` by 50%
2. Increase `gradient_accumulation_steps` to maintain effective batch size
3. Enable gradient checkpointing:
   ```python
   model.gradient_checkpointing_enable()
   ```
4. Reduce `max_seq_length`
5. Switch from LoRA to QLoRA (4-bit base model)
6. Reduce LoRA rank from 64 → 16 → 8
7. Use DeepSpeed ZeRO Stage 2 or 3
8. Switch to a smaller base model

**Test**: After fix, run 10 training steps successfully before full training.

---

## Failure 2 — Bad Dataset Formatting

**Symptom**: `KeyError`, `ValueError`, or model produces empty/garbage outputs after training.

**Root Cause**: Dataset schema doesn't match expected format for the training method.

**Diagnostic Steps**:
1. Print the first 3 samples:
   ```python
   for i, sample in enumerate(dataset):
       print(f"Sample {i}: {sample}")
       if i >= 2: break
   ```
2. Verify required keys exist:
   - SFT: `instruction`, `output` (or `messages` for chat)
   - DPO: `prompt`, `chosen`, `rejected`
3. Check for empty strings or null values
4. Check encoding: `chardet.detect(raw_bytes)`
5. Verify JSON is properly escaped (no unescaped quotes inside strings)

**Fix**:
```python
# Validation script
def validate_dataset(dataset, format_type="sft"):
    required_keys = {
        "sft": ["instruction", "output"],
        "chat": ["messages"],
        "dpo": ["prompt", "chosen", "rejected"],
    }
    errors = []
    for i, sample in enumerate(dataset):
        for key in required_keys[format_type]:
            if key not in sample:
                errors.append(f"Sample {i}: missing key '{key}'")
            elif not sample[key] or (isinstance(sample[key], str) and not sample[key].strip()):
                errors.append(f"Sample {i}: empty value for '{key}'")
    return errors
```

**Prevention**: ALWAYS run dataset validation before training.

---

## Failure 3 — Tokenization Errors

**Symptom**: Model generates strange tokens, repetitive output, or [UNK] tokens.

**Root Cause**: Tokenizer mismatch, missing special tokens, or wrong chat template.

**Diagnostic Steps**:
1. Verify tokenizer matches the base model:
   ```python
   print(f"Vocab size: {tokenizer.vocab_size}")
   print(f"Special tokens: {tokenizer.special_tokens_map}")
   print(f"Pad token: {tokenizer.pad_token}")
   ```
2. Test tokenization on a sample:
   ```python
   sample = "Hello, how are you?"
   tokens = tokenizer(sample)
   decoded = tokenizer.decode(tokens["input_ids"])
   assert decoded.strip() == sample, f"Tokenization mismatch: {decoded}"
   ```
3. For chat models, verify the chat template:
   ```python
   messages = [{"role": "user", "content": "Hello"}]
   formatted = tokenizer.apply_chat_template(messages, tokenize=False)
   print(formatted)  # Should include proper special tokens
   ```

**Common Fixes**:
- Set pad token: `tokenizer.pad_token = tokenizer.eos_token`
- Set padding side: `tokenizer.padding_side = "right"` (for training)
- Use correct chat template for the model family
- Ensure `add_special_tokens=True` during tokenization

---

## Failure 4 — Overfitting

**Symptom**: Training loss continues to drop but validation loss increases. Model memorizes training data instead of generalizing.

**Root Cause**: Too many epochs, too high learning rate, or insufficient data diversity.

**Diagnostic Steps**:
1. Plot training loss vs validation loss over steps.
2. Check if val loss starts increasing after epoch N.
3. Test the model on completely unseen inputs:
   - If outputs look like copy-paste from training data → overfitting confirmed.

**Fix Ladder**:
1. Stop training, use the checkpoint with lowest val loss
2. Reduce epochs: try 1-2 epochs instead of 3+
3. Reduce learning rate by 50%
4. Increase `lora_dropout` to 0.1
5. Add weight decay: `weight_decay=0.01`
6. Increase dataset size or add data augmentation
7. Reduce LoRA rank (fewer trainable parameters)

**Prevention**: ALWAYS use `eval_strategy="steps"` with `eval_steps≤100`.

---

## Failure 5 — Catastrophic Forgetting

**Symptom**: Fine-tuned model gains task-specific ability but loses general capabilities (can't follow basic instructions, generates incoherent text).

**Root Cause**: Training overwrites base model knowledge too aggressively.

**Diagnostic Steps**:
1. Run 10 general-purpose prompts on both base and fine-tuned model.
2. Score quality 1-5 for each response.
3. If average difference > 1.5 points → catastrophic forgetting confirmed.

**Fix Ladder**:
1. Use LoRA instead of full fine-tuning (isolates changes)
2. Reduce learning rate by 5-10x
3. Reduce number of epochs to 1
4. Reduce LoRA rank (8 instead of 64)
5. Use a replay buffer: mix 10-20% general instruction data into training set
6. Try higher LoRA alpha (2x rank)

**Prevention**: ALWAYS benchmark general capabilities before AND after training.

---

## Failure 6 — Adapter Merge Corruption

**Symptom**: Model works fine with adapter loaded separately, but produces garbage after merging LoRA weights into base model.

**Root Cause**: Base model version mismatch, dtype mismatch, or corruption during merge.

**Diagnostic Steps**:
1. Verify base model version:
   ```python
   # Must use EXACT same base model as training
   print(model.config._name_or_path)
   ```
2. Check dtypes:
   ```python
   for name, param in model.named_parameters():
       print(f"{name}: {param.dtype}")
   # All should be consistent (all bf16 or all fp16)
   ```
3. Test adapter-loaded model (without merging):
   ```python
   model = PeftModel.from_pretrained(base_model, adapter_path)
   output = model.generate(...)  # Should work correctly
   ```
4. Test merged model:
   ```python
   merged = model.merge_and_unload()
   output = merged.generate(...)  # Compare with adapter output
   ```

**Fix**:
- Ensure base model ID exactly matches the one used during training
- Convert dtypes before merge:
  ```python
  model = model.to(torch.float32)  # Convert to FP32 for merge
  merged = model.merge_and_unload()
  merged = merged.to(torch.bfloat16)  # Convert back after merge
  ```
- Re-download base model if corruption suspected

---

## Failure 7 — Training Loss is NaN or Inf

**Symptom**: Loss becomes `NaN` or `Inf` after a few steps.

**Root Cause**: Learning rate too high, data contains extreme values, or numerical instability.

**Diagnostic Steps**:
1. Check the exact step where loss became NaN.
2. Inspect the batch at that step for anomalies.
3. Check gradient norms: are they exploding?

**Fix**:
1. Enable gradient clipping: `max_grad_norm=1.0`
2. Reduce learning rate by 10x
3. Switch from FP16 to BF16 (better numerical stability)
4. Check for NaN/Inf values in training data
5. Try a smaller initial warmup: `warmup_ratio=0.1`
