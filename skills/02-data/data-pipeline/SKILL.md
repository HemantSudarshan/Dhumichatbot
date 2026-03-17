---
name: data-pipeline
description: "Use this skill when tasked with data preprocessing, cleaning, transformation, dataset creation, model evaluation, metric computation, building evaluation harnesses, or performance/load testing of AI systems and APIs."
---

# Data Preprocessing + Evaluation + Testing

## Overview

This skill provides a complete pipeline for transforming raw data into model-ready datasets, evaluating ML/LLM models with structured metrics, and performance-testing AI APIs under load.

## Supporting References

Load only the reference file you need:
- `references/instructions.md` for execution order and validation checkpoints
- `references/debug.md` for data quality and evaluation failure handling
- `references/tests.md` for test prompts and expected outcomes

## Required Inputs

1. **Data source** — file paths, URLs, database connections, or API endpoints
2. **Data modality** — text (NLP), tabular (CSV), image, or mixed
3. **Task** — what the data is for (training, evaluation, analysis)
4. **For evaluation**: model to evaluate + test dataset + target metrics
5. **For load testing**: API endpoint URL + expected throughput

## Step-by-Step Workflow

### Phase 1 — Data Ingestion & Profiling

**Objective**: Load data and create a comprehensive quality profile.

1. Load data (auto-detect format):
   ```python
   import pandas as pd
   
   # Auto-detect format
   if filepath.endswith('.csv'):
       df = pd.read_csv(filepath, encoding='utf-8-sig')
   elif filepath.endswith('.json'):
       df = pd.read_json(filepath)
   elif filepath.endswith('.jsonl'):
       df = pd.read_json(filepath, lines=True)
   elif filepath.endswith('.parquet'):
       df = pd.read_parquet(filepath)
   ```

2. Generate data profile:
   ```python
   profile = {
       "total_rows": len(df),
       "total_columns": len(df.columns),
       "column_types": df.dtypes.to_dict(),
       "missing_values": df.isnull().sum().to_dict(),
       "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
       "duplicates": df.duplicated().sum(),
       "memory_usage_mb": df.memory_usage(deep=True).sum() / 1e6,
   }
   ```

3. Generate `data_quality_report.md` with all findings.

---

### Phase 2 — Data Cleaning & Transformation

**Objective**: Clean data based on modality.

**NLP Data Cleaning**:
```python
import re
import unicodedata

def clean_text(text):
    """Standard NLP text cleaning pipeline."""
    if pd.isna(text):
        return ""
    text = unicodedata.normalize("NFKD", str(text))
    text = re.sub(r'<[^>]+>', '', text)          # Remove HTML
    text = re.sub(r'http\S+|www.\S+', '', text)  # Remove URLs
    text = re.sub(r'\s+', ' ', text).strip()      # Normalize whitespace
    return text
```

**Tabular Data Cleaning**:
```python
def clean_tabular(df):
    """Standard tabular data cleaning."""
    # Remove constant columns
    constant_cols = [c for c in df.columns if df[c].nunique() <= 1]
    df = df.drop(columns=constant_cols)
    
    # Handle missing values
    numeric_cols = df.select_dtypes(include='number').columns
    categorical_cols = df.select_dtypes(include='object').columns
    
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    df[categorical_cols] = df[categorical_cols].fillna(df[categorical_cols].mode().iloc[0])
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    return df
```

**Decision Table — Missing Value Strategy**:

| Scenario | Strategy | Code |
|----------|----------|------|
| < 5% missing | Drop rows | `df.dropna()` |
| 5-30% missing, numeric | Impute with median | `fillna(median)` |
| 5-30% missing, categorical | Impute with mode | `fillna(mode)` |
| > 30% missing | Drop column or flag | `df.drop(columns=[col])` |
| Missing is informative | Create indicator | `df[col+'_missing'] = df[col].isna()` |

**Output**: Cleaned dataset + `preprocessing_pipeline.py`

---

### Phase 3 — Data Validation & Quality Checks

**20-Item Quality Checklist**:

| # | Check | Method | Auto |
|---|-------|--------|------|
| 1 | No null values in critical columns | `df[col].notnull().all()` | ✅ |
| 2 | No duplicate rows | `not df.duplicated().any()` | ✅ |
| 3 | Correct data types | `df.dtypes` matches schema | ✅ |
| 4 | Values within expected ranges | `df[col].between(min, max).all()` | ✅ |
| 5 | No unexpected categories | `df[col].isin(expected).all()` | ✅ |
| 6 | Text columns non-empty | `df[col].str.len() > 0` | ✅ |
| 7 | Dates are parseable | `pd.to_datetime(df[col])` | ✅ |
| 8 | No data leakage (train/test overlap) | Hash comparison | ✅ |
| 9 | Class balance within acceptable range | `value_counts(normalize=True)` | ✅ |
| 10 | Encoding is UTF-8 | `chardet.detect()` | ✅ |
| 11 | File integrity (not truncated) | Row count matches expected | ✅ |
| 12 | Consistent formatting across columns | Regex validation | ✅ |
| 13 | No PII in public datasets | PII regex scan | ✅ |
| 14 | Labels are normalized | Case-insensitive dedup | ✅ |
| 15 | Numeric columns have no string values | `pd.to_numeric()` check | ✅ |
| 16 | Timestamps are in consistent timezone | TZ check | ⚠️ |
| 17 | Foreign keys are valid | Join validation | ⚠️ |
| 18 | Sample size meets minimum requirements | Count check | ✅ |
| 19 | Feature distributions are not degenerate | Variance check | ✅ |
| 20 | Data provenance documented | Metadata review | Manual |

---

### Phase 4 — Model Evaluation & Metrics

**Objective**: Evaluate an ML/LLM model with structured metrics.

**Metrics by Task Type**:

| Task | Metric | Code |
|------|--------|------|
| Classification | Accuracy | `sklearn.metrics.accuracy_score` |
| Classification | Precision/Recall/F1 | `sklearn.metrics.classification_report` |
| Classification | AUC-ROC | `sklearn.metrics.roc_auc_score` |
| Classification | Confusion Matrix | `sklearn.metrics.confusion_matrix` |
| Regression | MSE / RMSE | `sklearn.metrics.mean_squared_error` |
| Regression | MAE | `sklearn.metrics.mean_absolute_error` |
| Regression | R² | `sklearn.metrics.r2_score` |
| Generation | BLEU | `evaluate.load("bleu")` |
| Generation | ROUGE | `evaluate.load("rouge")` |
| Generation | BERTScore | `evaluate.load("bertscore")` |
| Retrieval | Recall@K | Custom function |
| Retrieval | MRR | Custom function |
| Retrieval | nDCG | `sklearn.metrics.ndcg_score` |

**Evaluation Harness Template**:
```python
class ModelEvaluator:
    def __init__(self, model, tokenizer, metrics=None):
        self.model = model
        self.tokenizer = tokenizer
        self.metrics = metrics or ["accuracy", "f1"]
    
    def evaluate(self, test_dataset):
        predictions = []
        references = []
        
        for sample in test_dataset:
            pred = self.model.predict(sample["input"])
            predictions.append(pred)
            references.append(sample["label"])
        
        results = {}
        for metric_name in self.metrics:
            metric = evaluate.load(metric_name)
            results[metric_name] = metric.compute(
                predictions=predictions,
                references=references
            )
        
        return results
    
    def generate_report(self, results, output_path):
        # Generate markdown report with charts
        ...
```

**Output**: `eval_report.md` with metrics, charts, analysis

---

### Phase 5 — Performance & Load Testing

**Objective**: Test AI API performance under load.

**Locust Load Test Template**:
```python
from locust import HttpUser, task, between

class AIAPIUser(HttpUser):
    wait_time = between(0.5, 2)
    
    @task
    def predict(self):
        self.client.post("/predict", json={
            "text": "Sample input for prediction"
        })
    
    @task
    def health(self):
        self.client.get("/health")
```

**Metrics to collect**:
- Latency: p50, p95, p99
- Throughput: requests/second
- Error rate: % of 4xx/5xx responses
- Response time distribution

**Run**: `locust -f locustfile.py --host http://localhost:8000 --headless -u 100 -r 10 -t 60s`

**Output**: `performance_report.md` + `locustfile.py`

---

### Phase 6 — Report Generation

Compile all findings into structured reports:
- `data_quality_report.md` — from Phase 1-3
- `eval_report.md` — from Phase 4
- `performance_report.md` — from Phase 5

All reports include: findings, charts, recommendations, next steps.

---

## Anti-Patterns — DO NOT

| Anti-Pattern | Consequence | Correct Approach |
|-------------|-------------|------------------|
| Skip data profiling, go straight to cleaning | Miss critical issues | Always profile first |
| Use accuracy on imbalanced datasets | Misleading results | Use F1, precision, recall |
| Include test data in training | Data leakage, invalid evaluation | Strict split before any processing |
| Impute all missing values with mean | Lost information, biased results | Choose strategy based on % missing and context |
| Load entire large dataset into memory | OOM crash | Use chunked processing or streaming |
| Test on the same data used for validation | Overfitting undetected | Hold out a separate test set |

## Skill Coordination

- Use `ai-solution-dev` when the data workflow is part of a broader AI product delivery effort.
- Use `finetuning` when evaluation results indicate model adaptation is required.
- Use `ai-integration` when the validated model must be exposed through serving endpoints.
- Use `ai-reliability` when performance testing needs to become long-term monitoring or SLO work.
- Use `documentation` to capture data reports, evaluation reports, and test evidence.
