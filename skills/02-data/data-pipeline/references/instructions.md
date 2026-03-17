# Data Pipeline — Agent Instructions

## How This Skill Activates

1. Agent reads YAML frontmatter during skill discovery.
2. If user request matches "clean data," "preprocess," "evaluate model," "run metrics," "load test," "data quality," or similar, load the full SKILL.md.

## Execution Instructions

### Step 1 — Identify Data Modality

1. Examine the input data format:
   - `.csv`, `.tsv` → Tabular
   - `.json`, `.jsonl` → Structured text
   - `.txt`, `.md` → Unstructured text
   - `.jpg`, `.png`, `.webp` → Image
   - `.parquet`, `.arrow` → Columnar
2. Select the appropriate preprocessing pipeline.
3. If modality is unclear, ask the user.

### Step 2 — Profile the Data

1. Load data using appropriate reader.
2. Run profiling:
   ```python
   print(f"Shape: {df.shape}")
   print(f"Types:\n{df.dtypes}")
   print(f"Missing:\n{df.isnull().sum()}")
   print(f"Duplicates: {df.duplicated().sum()}")
   print(f"Stats:\n{df.describe()}")
   ```
3. Generate `data_quality_report.md` containing:
   - Row/column counts
   - Missing value percentages
   - Duplicate count
   - Type mismatches
   - Distribution summaries

### Step 3 — Clean the Data

1. Apply the cleaning pipeline for the identified modality.
2. Use the Missing Value Strategy decision table from SKILL.md.
3. Log every transformation:
   - "Dropped 150 duplicate rows"
   - "Imputed 45 missing values in 'price' column with median (29.99)"
   - "Removed 12 rows with invalid dates"
4. Save cleaning pipeline as reusable `preprocessing_pipeline.py`.

### Step 4 — Validate Data Quality

1. Run the 20-item quality checklist from SKILL.md Phase 3.
2. Mark each item as PASS/FAIL/WARNING.
3. If ANY critical check fails (items 1-8), STOP and report.
4. Present results to user.

### Step 5 — Split Data (If for Training)

1. Determine split ratios:
   - Default: 80/10/10 (train/val/test)
   - Small dataset (<1000): 60/20/20
2. Use stratified splitting for classification:
   ```python
   from sklearn.model_selection import train_test_split
   train, temp = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)
   val, test = train_test_split(temp, test_size=0.5, stratify=temp['label'], random_state=42)
   ```
3. Verify no overlap between splits (hash check).

### Step 6 — Evaluate Model (If Requested)

1. Determine task type from user context.
2. Select metrics from the task-metric table in SKILL.md Phase 4.
3. Run evaluation:
   ```python
   from sklearn.metrics import classification_report, confusion_matrix
   
   report = classification_report(y_true, y_pred, output_dict=True)
   cm = confusion_matrix(y_true, y_pred)
   ```
4. Generate visualizations:
   - Confusion matrix heatmap
   - ROC curve (for binary classification)
   - Precision-recall curve
5. Write `eval_report.md` with all metrics and charts.

### Step 7 — Run Load Tests (If Requested)

1. Generate `locustfile.py` from the template.
2. Configure test parameters:
   - Number of users
   - Spawn rate
   - Duration
   - Target endpoint
3. Run the load test.
4. Collect latency percentiles and throughput.
5. Write `performance_report.md`.

### Step 8 — Generate Final Report

Compile all outputs into a summary:
- Data quality findings
- Cleaning transformations applied
- Evaluation results (if applicable)
- Performance results (if applicable)
- Recommendations for next steps

## Interaction Protocol

| Situation | Agent Behavior |
|-----------|---------------|
| Data format unclear | Ask user to confirm modality |
| Data too large for memory | Recommend chunked processing, proceed with sampling |
| Quality check fails | Report failure, ask user how to handle |
| Evaluation metric unclear | Present options, let user choose |
| Load test target unavailable | Report connection error, suggest local setup |

## Handoff to Other Skills

- If data needs fine-tuning preparation → `finetuning` skill
- If evaluation reveals model needs retraining → `finetuning` skill
- If API latency is unacceptable → `ai-reliability` skill
- If documentation needed → `documentation` skill
