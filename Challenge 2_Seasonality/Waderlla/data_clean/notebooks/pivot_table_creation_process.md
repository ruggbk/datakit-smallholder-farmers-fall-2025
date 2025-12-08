# Pivot Table Creation Process  
_Data source used for further work in Tableau_

This document describes how the aggregated pivot table was created.  
The table itself is not included in the repository — only the process and structure are documented.  
The pivot table serves as the primary input for Tableau and provides a consolidated summary of the classified question dataset.

---

## 1. Starting point: input data

The process began with a processed dataset of farmer questions containing both:

- original WeFarm topic annotations, and  
- newly assigned dictionary-based categories.

The original dataset included (among others) the following fields:

- `question_id`
- `question_language`
- `question_content`
- `question_topic`
- `question_sent`
- `question_user_country_code`
- `topic_category`
- `Year`
- `Month`
- `category` (assigned by the dictionary-based pipeline)

---

## 2. Column renaming and normalization

Before constructing the pivot table, several columns were renamed to ensure clarity, consistency,  
and an unambiguous distinction between:

- dictionary-based categories,  
- simplified WeFarm categories,  
- and original WeFarm topic labels.

The following mapping was applied:

| Original column name          | New column name             | Meaning |
|-------------------------------|------------------------------|---------|
| `Year`                        | **`year`**                   | Year when the question was asked. |
| `Month`                       | **`month`**                  | Month when the question was asked. |
| `question_language`           | **`question_language`**      | Language of the question (unchanged). |
| `question_user_country_code` | **`country_code`**           | User’s country code (shortened column name). |
| `category`                    | **`dictionary_category`**    | Category assigned by the custom dictionary-based pipeline. |
| `topic_category`              | **`wefarm_topic_group`**     | Simplified, grouped version of WeFarm categories. |
| `question_topic`              | **`wefarm_question_topic`**  | Original, detailed WeFarm topic label. |

In addition to renaming, fields were normalized (lowercasing, consistent coding, etc.)  
to facilitate clean grouping and filtering.

---

## 3. Construction of the aggregated pivot table

Using the normalized dataset, an aggregated summary table was produced.  
Each row represents the *count of questions* matching a specific combination of classification, time, and language dimensions.

The grouping dimensions used were:

- `year`  
- `month`  
- `question_language`  
- `country_code`  
- `dictionary_category`  
- `wefarm_topic_group`  
- `wefarm_question_topic`

For each unique combination of these fields, a single metric was computed:

- **`count`** – number of questions (`question_id`) belonging to that group.

This resulted in a consolidated table where each row answers the question:

> “How many questions were asked in year _Y_, month _M_, language _L_,  
> from country _C_, with dictionary category _D_, WeFarm topic group _G_,  
> and detailed WeFarm topic _T_?”

---

## 4. Structure of the final aggregated table

The final pivot table contains the following columns:

- `year` – year of the question,  
- `month` – month of the question,  
- `question_language` – language code,  
- `country_code` – user country,  
- `dictionary_category` – dictionary-based category (final classification),  
- `wefarm_topic_group` – grouped WeFarm topic category,  
- `wefarm_question_topic` – original WeFarm topic label,  
- `count` – number of questions for the given combination.

This structure allows fast filtering, drilling down, and charting inside Tableau.

---

## 5. Output file

The resulting aggregated pivot table was saved as:

### **`questions_aggregated_pivot_dashboard.xlsx`**

This file serves as the **primary data source for Tableau visualizations**.  
Only the process description is included in the repository; the data itself is intentionally omitted.
