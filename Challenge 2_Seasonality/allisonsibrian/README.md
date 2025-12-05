# Allison Sibrian - Challenge 2 Analysis

## Overview
This project analyzes the seasonality of farmers' questions across Kenya, Uganda, and Tanzania. By correlating farmer question volume with ERA5 weather data and performing NLP keyword analysis on a split dataset (English vs. Local Languages), I identify distinct seasonal words for each region.

## Research Questions
- Question 1: Do farmer questions align with their countries' farming season?
- Question 2: Can we identify distinct seasonal farming words for each country based on question data? 
- Question 3: How does language (English vs. Local Languages (Swahili, Luganda, Ryunakole)) influence the types of seasonal questions asked?

## Methodology

### Data Sources
- - Producers Direct Dataset: Obtained de-duplicated farmer questions split by language (English, Swahili, Luganda, Runyankole).
- ERA5 Climate Reanalysis Data: Monthly aggregates for Total Precipitation (prcp), Maximum Temperature (tasmax), and Minimum Temperature (tasmin) for Kenya, Uganda, and Tanzania.

### Approach
1. **Step 1**: Data Splitting
                 - Created two comparison groups: The English Group (Kenya/Uganda baseline) and the Local Language Group (Stratified sample of Swahili, Luganda, Runyankole languages).
3. **Step 2**: Weather Validation
4.                - Overlayed ERA5 precipitation data against each countries and group question volume to compare farmer question volume to climate events.
5. **Step 3**: NLP & Cleaning
6. **Step 4**: Keyword Extraction
7. **Step 5**: Heatmap Visualizations

### Tools and Technologies
- **Programming Language**: Python 3.11
- **Key Libraries**: pandas, numpy, matplotlib, seaborn

## Key Findings

### Farmer Question Volume Peaks (English and Translated Group) during Harvest and Short Rains (vs. Long Rains)
Overlaying the ERA5 data with each countries' farmer questions reveals when question volume spiked up in relation to precipitation data.

For Kenya's English and Translated Group: 
- Question Volume is at its maximum peak for the Kenya English Group dataset in August, followed by November and September (aligning with the end of the first harvest and entering short rains). 
- Question Volume is at its maximum peak for the Kenya English Translated dataset in November, followed by August and September.
  
It seems that although this is the 'short rain' season, November tends to have a large amount of precipitation for the second half of the year and that most question volume aligns with the end of the first harvest period for Kenya. 

For Uganda's English and Translated Group:
- Similar to Kenya, Question Volume is at its maximum peak for the Uganda English Group dataset in August, then followed by November and September (aligning with the end of harvest and entering the second planting season).
- Question Volume is at its maximum peak for the Uganda Translated Group dataset in August, then followed by December and November.
  
However, unlike Kenya, most of Uganda's question volume tends to fall towards Uganda's second rains, where farmers are entering there second planting season. 

For Tanzania:
- Question Volume is at its maximum peak for the Tanzania dataset (only Translated data as English dataset did not obtain a significant amount of Tanzania data) in May, followed by April and November (aligning with Tanzania's Masika rains and Vuli Rains (Nov)).

It seems that question volume is most concentrated towards the end of the Masika Rains (Apr-May) and towards the end of Vuli Rains.

**Implications for Producers Direct:**
- Question volume seems to be occurring more during the second half of the year (Kenya/Uganda) rather than the first half of the year. It would be helpful to be more alert during this time and provide land preparation resources as this is the preparation phase for Kenyan and Ugandan farmers.
- Likewise for the Masika Rains period for Tanzania farmers.
- 
### The Regional HeatMap


**Implications for Producers Direct:**
- How this finding can be used
- What actions it suggests


## Visualizations

### Rainfall vs. Question Volume
![Visualization 1](http://localhost:8888/lab/tree/Challenge%202_Seasonality/allisonsibrian/Kenya_qprcp.png)
![Visualization 2](http://localhost:8888/lab/tree/Challenge%202_Seasonality/allisonsibrian/Uganda_qprcp.png)
![Visualization 3](http://localhost:8888/lab/tree/Challenge%202_Seasonality/allisonsibrian/Tanzania_qprcp.png)

**Interpretation**: 


### Regional Heatmap
![Visualization 4](http://localhost:8888/lab/tree/Challenge%202_Seasonality/allisonsibrian/word_frequencies_countries.png)

**Interpretation**: 

## Limitations and Challenges

### Data Limitations
- Missing data issues
- Data quality concerns
- Sample size or coverage limitations

### Methodological Limitations
- Assumptions made
- Simplifications required
- Alternative approaches not explored

### Technical Challenges
- Computational constraints
- Translation accuracy issues
- Other technical hurdles

## Next Steps and Recommendations

### For Further Analysis
1. **Recommendation 1**: What could be explored next
2. **Recommendation 2**: How to deepen this analysis
3. **Recommendation 3**: Related questions to investigate

### For Producers Direct
1. **Action 1**: Specific recommendation for the organization
2. **Action 2**: How to use these insights
3. **Action 3**: What additional data or resources would help

## Contact and Collaboration

**Author**: Allison Sibrian
**GitHub**: @allisonsibrian

**Collaboration Welcome**: 
- Open to feedback and suggestions
- Happy to collaborate on related analyses
- Available to answer questions about this approach

## Acknowledgments
- Built upon work by Conrad Keyclamp's heatmap visualizations in Challenge 2

---

**Last Updated**: December 4, 2025
