# 🌦️ Weather Conditions and Farmer Questions: Kenya & Uganda Analysis

> **Objective:** Statistically analyze how farmers' questions change based on weather conditions in East Africa (Kenya & Uganda).

## 📊 Dataset Summary

| Country | Total Questions | Date Range | Unique Topics |
|---------|-----------------|------------|---------------|
| **Kenya** | 425,291 | Nov 2017 - Oct 2018 (12 months) | 146 |
| **Uganda** | 1,268,716 | Nov 2017 - Dec 2021 (47 months) | 145 |

---

## 🔍 Research Questions

1. **Which crops/livestock are most sensitive to weather?**
2. **Are pest and disease questions weather-dependent?**
3. **Is there a lag effect?** (Does today's rain affect tomorrow's questions?)
4. **Livestock vs Crop Production: Which is more weather-sensitive?**

---

## 💡 Key Findings

### 1. Pest/Disease Questions and Rainfall Relationship

**🔑 Main Finding:** As rainfall increases, pest/disease questions increase!

> 📌 **See in notebook:** "PEST AND DISEASE QUESTION PATTERNS" section in both notebooks

---

### 2. Temperature and Maize Production

**Critical finding in Kenya:** During hot weather, maize questions rise to **10.36%** (only 6.31% during cool weather).

> 📌 **See in notebook:** "TOPIC DISTRIBUTION BY WEATHER CONDITIONS" section

---

### 3. Lag Effect - Predictive Power!

**🔑 Critical Discovery:** The effect of rainfall on pest questions is **stronger with a 1-month delay**!

> **Implication:** Using today's rainfall data, we can **predict** the increase in pest questions 1 month later!

> 📌 **See in notebook:** "LAG EFFECT ANALYSIS" section

---

### 4. Crop-Specific Rainfall Sensitivity

**Most sensitive crops (by standard deviation in question distribution):**

| Rank | Kenya | Uganda |
|------|-------|--------|
| 1 | Maize (10.4) | Kale (15.1) |
| 2 | Chicken (9.4) | Cabbage (11.6) |
| 3 | Tea (8.1) | Onion (11.3) |
| 4 | Tomato (8.0) | Tomato (9.9) |
| 5 | Cattle (8.0) | Bean (9.7) |

> 📌 **See in notebook:** "CROP-SPECIFIC WEATHER SENSITIVITY ANALYSIS" section

---

### 5. Livestock vs Crop Production

> **Finding:** Crop production generates 2x more questions about pests/diseases!

> 📌 **See in notebook:** "LIVESTOCK VS CROPS" section

---

### 6. Statistical Validation (Chi-Square Tests)

All findings are statistically **significant** (p < 0.001):

| Test | Kenya χ² | Uganda χ² |
|------|----------|-----------|
| Rainfall ↔ Pest Questions | 137.27 | 641.89 |
| Temperature ↔ Pest Questions | 93.80 | 122.02 |
| Extreme Rainfall ↔ Topic Distribution | 2565.38 | 895.63 |

> 📌 **See in notebook:** "STATISTICAL TESTS: CHI-SQUARE" section

---

## 🗂️ Notebook Structure

Both notebooks contain the following analysis steps:

1. **Data Loading & Overview** - Dataset size, columns, date range
2. **Weather Data Structure** - Monthly weather variables (temperature, precipitation, humidity)
3. **Topic Distribution** - Most popular agricultural topics
4. **Temporal Patterns** - Seasonal and monthly question volume changes
5. **Weather Categories** - Low/Moderate/High categorization
6. **Topic × Weather Analysis** - Which topics emerge under different weather conditions
7. **Pest/Disease Analysis** - Relationship between weather and disease questions
8. **Correlation Analysis** - Pearson correlations
9. **Lag Effect Analysis** - Delayed effect correlations
10. **Livestock vs Crops** - Sector comparison
11. **Statistical Tests** - Chi-square independence tests

---

## 📈 Conclusions and Recommendations

### ✅ Validated Hypotheses
- Weather conditions **significantly** affect farmer questions
- Rainfall is a strong predictor of pest/disease questions
- An **early warning system** can be built using lag effects

### 🎯 Action Recommendations
1. **After rainfall** highlight pest/disease content
2. **During hot periods** prepare specialized content for maize producers
3. **Develop a prediction model**: Predict question surges 1 month in advance

---

## 📁 Files

| File | Description |
|------|-------------|
| `kenya.ipynb` | Kenya analysis notebook (425K questions) |
| `uganda.ipynb` | Uganda analysis notebook (1.27M questions) |
| `data-sources/KEN/` | Kenya data files |
| `data-sources/UGA/` | Uganda data files |

---

*This analysis was conducted as part of the DataKind project.*
