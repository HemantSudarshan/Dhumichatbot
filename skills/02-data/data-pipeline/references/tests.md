# Data Pipeline — Test Cases

---

## Test 1 — CSV Cleaning

**Input**:
```
Clean this CSV with 10K rows, 15% missing values across 3 columns,
2 datetime columns with mixed formats, and 200 duplicate rows.
```

**Expected Behavior**:
1. Agent loads and profiles the CSV.
2. Detects: 15% missing, mixed datetime formats, 200 duplicates.
3. Applies appropriate imputation per column type.
4. Normalizes datetime formats.
5. Removes duplicates.
6. Generates `data_quality_report.md` + cleaned dataset.

**Pass Criteria**:
- [ ] All missing values handled with documented strategy
- [ ] Datetime formats normalized
- [ ] Duplicates removed
- [ ] Quality report generated
- [ ] Reusable `preprocessing_pipeline.py` saved

---

## Test 2 — Model Evaluation

**Input**:
```
Evaluate my text classifier on this test set of 500 labeled samples.
Classes: positive, negative, neutral.
```

**Expected Behavior**:
1. Agent identifies: multi-class classification.
2. Computes: accuracy, precision, recall, F1 (macro + per-class).
3. Generates confusion matrix visualization.
4. Identifies worst-performing class.
5. Provides actionable insights.

**Pass Criteria**:
- [ ] All classification metrics computed
- [ ] Per-class breakdown included
- [ ] Confusion matrix generated
- [ ] Insights about weak classes provided
- [ ] `eval_report.md` complete

---

## Test 3 — Load Testing

**Input**:
```
Load test my FastAPI model API at /predict with 100 concurrent users
for 60 seconds.
```

**Expected Behavior**:
1. Agent generates `locustfile.py` with prediction endpoint test.
2. Configures: 100 users, 10 spawn rate, 60s duration.
3. Runs the test.
4. Reports: p50, p95, p99 latency, RPS, error rate.

**Pass Criteria**:
- [ ] `locustfile.py` is runnable
- [ ] All latency percentiles reported
- [ ] Throughput measured
- [ ] Error rate documented
- [ ] `performance_report.md` generated

---

## Test 4 — Data Leakage Detection

**Input**:
```
Check my train.csv and test.csv for data leakage.
```

**Expected Behavior**:
1. Agent hashes all rows in both files.
2. Computes overlap.
3. Reports: number of leaked samples, percentage.
4. Recommends: remove from test set and re-split.

**Pass Criteria**:
- [ ] Overlap detection runs correctly
- [ ] Exact count of overlapping samples reported
- [ ] Fix recommendation provided

---

## Test 5 — Imbalanced Dataset Handling

**Input**:
```
My fraud detection dataset has 99.5% legitimate and 0.5% fraud.
Prepare it for training.
```

**Expected Behavior**:
1. Agent detects extreme imbalance (199:1 ratio).
2. Warns: accuracy metric will be misleading.
3. Recommends: F1-macro, precision-recall, AUPRC.
4. Applies: class weighting or SMOTE.
5. Verifies: stratified train/test split.

**Pass Criteria**:
- [ ] Imbalance detected and flagged
- [ ] Appropriate resampling strategy applied
- [ ] Correct metrics recommended
- [ ] Stratified splitting used

---

## Test 6 — Mixed-Format Data

**Input**:
A JSON file where:
- Some "price" values are strings ("29.99"), some are floats (29.99)
- "date" column has 3 different formats (ISO, US, European)
- "status" column has typos ("active", "Active", "ACTIVE", "avtive")

**Expected Behavior**:
1. Agent detects type inconsistencies in "price".
2. Agent detects mixed date formats.
3. Agent detects label typos via case normalization + fuzzy matching.
4. Fixes all issues and documents each transformation.

**Pass Criteria**:
- [ ] All type inconsistencies resolved
- [ ] All dates parsed to consistent format
- [ ] Label typos detected and corrected
- [ ] Transformation log documented
