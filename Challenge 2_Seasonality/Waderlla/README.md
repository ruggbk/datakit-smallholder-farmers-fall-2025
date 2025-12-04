# README – Seasonality Analysis (WeFarm / Producers Direct)

## Overview

This directory contains the complete workflow, documentation, and final deliverables for my contribution to **DataKind DataKit Challenge 2025 – Challenge 2: Seasonality**.  
The goal of this work was to analyze seasonal patterns in farmer questions from Kenya (KE), Uganda (UG), and Tanzania (TZ), understand differences across countries and categories, and provide actionable insights for operational planning (e.g., SMS timing and advisory campaigns).

This folder includes:

- full data‑cleaning and categorization pipeline,  
- semantic dictionary and category mapping,  
- complete pivot table creation documentation,  
- the final analytical report (PDF),  
- link to the interactive Tableau dashboard.

---

## Repository Structure

```
Waderlla/
│
├── data_clean/
│   ├── data/
│   │   └── words_categories_merged.json
│   │
│   └── notebooks/
│       ├── agricultural_semantic_dictionary_builder.ipynb
│       ├── data_cleaning_and_category_pipeline.ipynb
│       └── pivot_table_creation_process.md
│
├── Seasonality_Report.pdf
└── README.md
```

---

## Files and Their Purpose

### 1. Data Cleaning & Categorization (`data_clean/`)

#### `data_clean/data/words_categories_merged.json`
A merged agricultural semantic dictionary used to assign `dictionary_category` to each farmer question.

#### `data_clean/notebooks/agricultural_semantic_dictionary_builder.ipynb`
Notebook documenting:
- extraction of multilingual agricultural terms,
- dictionary construction,
- grouping terms into unified semantic categories,
- iterative refinement of the dictionary.

#### `data_clean/notebooks/data_cleaning_and_category_pipeline.ipynb`
Notebook describing the full preprocessing workflow:
- cleaning and normalization of raw question data,
- restructuring time variables (`year`, `month`),
- merging dictionary output with WeFarm categories,
- creation of the final dataset used for pivoting.

#### `data_clean/notebooks/pivot_table_creation_process.md`
Documentation of how the aggregated pivot table was built:
- column renaming and normalization,
- grouping dimensions (year, month, country, category, topic),
- how `count` was computed,
- structure used as the primary Tableau data source.

---

## Analytical Outputs

### **1. Final Report (PDF)**

The full analytical report is available here:

📄 **PDF:**  
https://github.com/Waderlla/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%202_Seasonality/Waderlla/Seasonality_Report.pdf


The report includes:
- justification for using only years **2019–2020**,  
- category-level seasonality,  
- cross-country comparisons for KE/UG/TZ,  
- year-to-year shifts,  
- operational recommendations,  
- limitations of the data and methods.

---

### **2. Tableau Dashboard**

The interactive visualization is available here:

📊 **Tableau Dashboard:**  
https://public.tableau.com/app/profile/olga.mironczuk/viz/Book1_17641068607630/OverallSeasonality#1

The dashboard allows:
- exploration of seasonality by country, category, and month,  
- comparison across KE, UG, TZ,  
- identification of peak months for agricultural themes,  
- interactive filtering by language, topic, and category.

---

## Reproducing the Workflow

1. Start with the original WeFarm dataset (not included in this repository).  
2. Run `data_cleaning_and_category_pipeline.ipynb` to prepare and normalize the data.  
3. Build or update the semantic dictionary using `agricultural_semantic_dictionary_builder.ipynb`.  
4. Follow `pivot_table_creation_process.md` to generate the aggregated pivot table.  
5. Load the pivot table into Tableau to reproduce the dashboard.  
6. Refer to the PDF report for complete methodological documentation.

---

## Notes

- Raw data is **not** included due to challenge requirements.  
- Seasonality analysis uses **only 2019–2020**, the only complete and stable years.  
- This work covers only KE, UG, TZ — other countries were excluded due to insufficient volume.  

---

## Author & Contact

Analysis by **Olga Mirończuk**  
GitHub: https://github.com/Waderlla  
LinkedIn: https://www.linkedin.com/in/olga-mironczuk/
