# DataKind - Smallholder Farmers DataKit - Clustering Analysis
**Author:** Brandon Rugg  
**Date:** November 2025

## Introduction
Producers Direct is a nonprofit organization that supports a 1M+ network of smallholder farmers in efforts to build more sustainable and profitable farms in South America and Africa. Previously, producers Direct acquired a large dataset from WeFarm, an SMS-based platform that operated for 7 years before going bankrupt in 2022. This 7GB dataset consists of over 5M questions, 16.2M responses, and extensive metadata for each message.

In November 2025, DataKind launched a month-long initiative to help Producers Direct determine what actionable information can be obtained from these farmer-to-farmer SMS messages. Insights gathered will hopefully aid Producers Direct in reestablishing a peer-to-peer network for smallholder farmers.

Main Project Repo: https://github.com/datakind/datakit-smallholder-farmers-fall-2025  
Project Brief: https://docs.google.com/document/d/1jKTmb8R5GlM9uqQkB5fXd37o2bdX17JKB36mK-NqWFE/edit?tab=t.0

## Project Goal
This subset of the November 2025 DataKit focuses on learning how the platform was used-- in other words, what were the farmers asking? There are already approximately 150 topic tags included in the data, but all of them are related to specific types of crops or livestock, as shown in this bar plot of the top 20 most common question tags:

![Bar plot of top 20 question tags](figures/topic_tags.png)

There is undoubtedly a lot of structure that these tags aren't covering.
* The top 3 tags account for 24% of the questions, and 1,537,291 questions (another 28% of the data) are not tagged at all.
* Questions have at most one tag.
* There are no tags for things like finance, planning, farm equipment, or questions about how the WeFarm platform worked.

I performed a clustering analysis to see if I could uncover common topics the farmers were asking about, so that Producers Direct could make sure the needs of the farmers are being met moving forward. More in depth topic labeling may also help uncover patterns in seasonality, recognize domain experts, and identify common financial inclusion related topics.

## Clustering Pipeline Description

Early attempts at a global analysis of questions were not very successful. I eventually settled on a pipeline to cluster three topics independently: questions tagged with 'None' (unlabeled), 'chicken', and 'maize'. The latter two were chosen because they are the two most common topic tags for English questions, and represent an example of a crop and livestock (all question tags in the dataset appear to be one or the other).

The pipeline begins with minimal text cleaning, removing some common prefixes (e.g., `"Q:"`) and normalizing whitespace. Sentence embeddings are generated using the `all-MiniLM-L6-v2` model.

For clustering, UMAP reduces the embeddings to 5 dimensions, which are then fed into HDBSCAN to identify clusters. To better classify questions initially labeled as noise (`-1`), a second HDBSCAN pass is applied to the noise cluster, and the resulting clusters are manually verified and reintegrated.

This analysis typically resulted in over 100 clusters. Adjusting the parameters, I would either see even more clusters, or only a few very large ones (usually less than 5) that did not seem very cohesive. So, to make the results more understandable, I came up with about 10 metacluster topics and submitted short summaries of the clusters (including TF-IDF based keywords and 5 example questions) in batches to be evaluated and labeled by ChatGPT. These batches were about 40-50 questions at a time, and prefaced with the prompts found in `/notes/LLM_prompts.txt`.

Finally, a 2D UMAP projection is generated solely for visualization of the clusters. 2D projections of the clusters along with metacluster topic counts and previews of the clusters are generated in `/notebooks/final_analysis.ipynb`. This notebook will also reassemble the clustered data from the original 7GB dataset and a set of files (18MB) contained in `/data`.







