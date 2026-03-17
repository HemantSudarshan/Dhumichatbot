# AI Reliability — Debug Protocol

---

## Failure 1 — Model Drift Detected, No Retraining Pipeline

**Symptom**: Drift detection flags significant data drift but there's no automated retraining.

**Diagnostic Steps**:
1. Confirm drift is real (not a monitoring artifact):
   - Check if data collection changed recently
   - Verify reference data is still valid
2. Assess severity: how much has accuracy dropped?
3. Evaluate: can the model tolerate this drift temporarily?

**Fix**:
1. Short-term: monitor accuracy closely on recent data.
2. Medium-term: scaffold a retraining pipeline:
   - Data collection → Validation → Training → Evaluation → Deployment
   - Set up trigger: retrain when accuracy drops > 5%
3. Long-term: automate end-to-end with CI/CD for ML.

---

## Failure 2 — Latency Spikes (p99 > 10s)

**Symptom**: Sudden increase in response time under load.

**Diagnostic Steps**:
1. **Is it model inference?**
   ```python
   # Profile inference time in isolation
   import time
   start = time.time()
   model.predict(sample_input)
   print(f"Inference: {time.time()-start:.3f}s")
   ```
2. **Is it data loading/preprocessing?**
   - Profile each pipeline stage separately.
3. **Is it network/infrastructure?**
   - Check pod/container resource usage.
   - Check if auto-scaler is lagging.
4. **Is it a specific request type?**
   - Check if long inputs cause timeout.

**Fix Ladder**:
1. Enable response caching for repeated queries
2. Implement dynamic batching (batch inference)
3. Optimize model (quantization, TensorRT)
4. Scale horizontally (add replicas)
5. Increase hardware (bigger GPU, more memory)

---

## Failure 3 — Auto-Scaler Creates Pods but Model Fails to Load

**Symptom**: New pods start but become un-ready. Health checks fail. Requests queue.

**Diagnostic Steps**:
1. Check pod logs: `kubectl logs <pod> --tail=100`
2. Common causes:
   - OOM kill (model too large for pod memory limit)
   - Model download timeout (pulling from remote storage)
   - GPU not available for new pods
   - Missing environment variables in new pods

**Fix**:
- Set resource limits correctly:
  ```yaml
  resources:
    requests:
      memory: "4Gi"
      nvidia.com/gpu: "1"
    limits:
      memory: "8Gi"
      nvidia.com/gpu: "1"
  ```
- Pre-download models to a shared volume (PVC)
- Configure startup probe with generous timeout
- Test scaling by manually scaling up: `kubectl scale deployment/api --replicas=3`

---

## Failure 4 — Monitoring Blind Spots

**Symptom**: System crashes or degrades but no alert fires.

**Diagnostic Steps**:
1. Map all critical paths in the system.
2. For each path, verify an alert exists:
   | Critical Path | Alert Exists? |
   |--------------|---------------|
   | API health | ? |
   | Model inference latency | ? |
   | Error rate | ? |
   | GPU memory | ? |
   | Disk space | ? |
   | Model accuracy | ? |
   | Data pipeline | ? |
3. Identify gaps.

**Fix**:
- Add alerts for every uncovered critical path.
- Test each alert by triggering it manually.
- Set up a monthly alert audit.

---

## Failure 5 — Silent Model Degradation

**Symptom**: Accuracy drops 15% over 2 weeks but nobody notices because there's no quality monitoring in production.

**Diagnostic Steps**:
1. Check if ground truth labels are available for production data.
2. If yes: compute accuracy/F1 on recent data vs baseline.
3. If no: use proxy metrics:
   - Model confidence distribution shift
   - User feedback (thumbs up/down)
   - Downstream business metrics correlation

**Fix**:
- Implement automated quality gates:
  ```python
  def check_model_quality():
      recent_accuracy = compute_accuracy(recent_data, recent_labels)
      if recent_accuracy < THRESHOLD:
          send_alert(f"Model accuracy {recent_accuracy} below threshold {THRESHOLD}")
  ```
- Run quality checks daily.
- Set up a monthly model review meeting.

---

## Failure 6 — Data Pipeline Corruption

**Symptom**: Training data silently changes, new model trains on corrupt data.

**Diagnostic Steps**:
1. Check data checksums:
   ```python
   import hashlib
   def file_checksum(path):
       with open(path, 'rb') as f:
           return hashlib.sha256(f.read()).hexdigest()
   ```
2. Compare current checksum with stored baseline.
3. Check data lineage: who/what modified the data?

**Fix**:
- Version all datasets (DVC, Git LFS, or manual tagging).
- Add schema validation before any training run.
- Store checksums and verify before pipeline execution.
- Add data integrity checks to CI/CD.
