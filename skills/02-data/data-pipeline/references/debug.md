# Data Pipeline — Debug Protocol

## Purpose

Deterministic troubleshooting for data preprocessing, evaluation, and testing failures.

---

## Failure 1 — Excessive Missing Values

**Symptom**: 60%+ of a critical column is NaN.

**Diagnostic Steps**:
1. Check if missingness is random (MCAR) or systematic (MNAR):
   ```python
   # Check if missingness correlates with other columns
   df['col_missing'] = df['critical_col'].isna()
   correlations = df.corr()['col_missing']
   ```
2. Assess if the column is essential for the task.

**Decision Tree**:
- If column is non-essential → Drop column
- If missingness is random and < 70% → Impute based on type (median/mode)
- If missingness is systematic → Create a binary "missing" indicator feature
- If missingness > 70% and column is essential → **Flag for human review**
  - "Column 'field_name' has 68% missing values. Cannot proceed without guidance."

---

## Failure 2 — Data Leakage Detected

**Symptom**: Test data contains samples from the training set. Model evaluation metrics are suspiciously high.

**Diagnostic Steps**:
1. Hash all rows:
   ```python
   import hashlib
   def hash_row(row):
       return hashlib.md5(str(row.values).encode()).hexdigest()
   
   train_hashes = set(train_df.apply(hash_row, axis=1))
   test_hashes = set(test_df.apply(hash_row, axis=1))
   overlap = train_hashes & test_hashes
   print(f"Leaked samples: {len(overlap)}")
   ```
2. Check for temporal leakage (future data in training set).
3. Check for group leakage (same entity in both splits).

**Fix**:
- Remove overlapping rows from test set.
- Re-split using proper strategy (stratified, group-aware, temporal).
- Re-run evaluation.

---

## Failure 3 — Imbalanced Dataset

**Symptom**: One class has 99% of samples. Accuracy is 99% but model is useless.

**Diagnostic Steps**:
1. Check class distribution:
   ```python
   print(df['label'].value_counts(normalize=True))
   ```
2. Confirm if accuracy metric is misleading.

**Fix Options**:
| Strategy | When to Use | Code |
|----------|------------|------|
| Class weights | Always first try | `class_weight='balanced'` in sklearn |
| SMOTE | Moderate imbalance (10:1) | `imblearn.over_sampling.SMOTE` |
| Undersampling majority | Abundant data | `RandomUnderSampler` |
| Stratified splitting | Preserving distribution | `train_test_split(stratify=y)` |
| Focal loss | Deep learning | Custom loss function |
| Change metric | Always | Use F1-macro instead of accuracy |

**Prevention**: ALWAYS check class balance before training or evaluation.

---

## Failure 4 — Encoding Errors

**Symptom**: `UnicodeDecodeError`, garbled text, or `???` characters.

**Diagnostic Steps**:
1. Detect encoding:
   ```python
   import chardet
   with open(filepath, 'rb') as f:
       result = chardet.detect(f.read(10000))
   print(f"Detected encoding: {result['encoding']} ({result['confidence']:.0%})")
   ```
2. Try reading with detected encoding.
3. If mixed encodings, process file line-by-line.

**Fix**:
```python
# Try common encodings
for enc in ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']:
    try:
        df = pd.read_csv(filepath, encoding=enc)
        print(f"Successfully read with {enc}")
        break
    except UnicodeDecodeError:
        continue
```

---

## Failure 5 — Corrupt or Truncated Files

**Symptom**: File loads partially, unexpected EOF, or parsing errors.

**Diagnostic Steps**:
1. Check file size: `os.path.getsize(filepath)`
2. Try loading with `error_bad_lines=False`:
   ```python
   df = pd.read_csv(filepath, on_bad_lines='skip')
   ```
3. Count lines vs expected:
   ```python
   with open(filepath) as f:
       actual_lines = sum(1 for _ in f)
   ```
4. For JSON: validate with `json.loads()`
5. For images: check with PIL:
   ```python
   try:
       img = Image.open(path)
       img.verify()
   except:
       print(f"Corrupt image: {path}")
   ```

**Fix**: Report corrupt entries, skip them, and document what was lost.

---

## Failure 6 — Wrong Metric Selection

**Symptom**: Agent computes accuracy on a regression task, or uses BLEU on classification.

**Diagnostic Steps**:
1. Verify task type:
   - Discrete labels → Classification
   - Continuous values → Regression
   - Text output → Generation
   - Ranked results → Retrieval

2. Cross-reference with the metrics table in SKILL.md Phase 4.

**Fix**: Select the appropriate metric set. If unsure, ask the user:
- "Your model produces [output type]. I recommend [metric set]. Does this align with your goals?"

**Prevention**: ALWAYS determine task type before computing any metric.
