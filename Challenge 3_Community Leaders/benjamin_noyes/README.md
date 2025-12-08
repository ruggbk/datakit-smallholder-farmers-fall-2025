### Table of contents
- Introduction
  - The event
- Data preparation
  - Sample space
  - Four dimensions of leaders
- Topic analysis
- Navigating the dashboard
  - Dropdowns
  - Tabs
- Insights
- Appendix


# Introduction
##### Datakind Datakit: Smallholder Farmers
This analysis was produced for a DataKit event, hosted by DataKind, in tandem with Producers Direct.

The dataset comes from WeFarm, a farmer-to-farmer question and answer service that operated via SMS. Smallholder farmers could ask a question via SMS to the WeFarm system, the system would decide which users to send questions to, and then these users would respond to the system with answers. All responses were then forwarded to the question poster in real time via SMS. WeFarm operated primarily in East Africa from 2017-2021, but was shut down during COVID.

The data itself is very large and heavily text-based. The unmodified data has around 20 million rows. Columns include “question text”, “response text”, “timestamps”, and the various user id columns. Categories of text were included, but nulls were highly present at over 60%, and the categories that did exist varied in their usefulness. Based on this data, DataKind challenged event participants with identifying leaders in the dataset, uncovering network effects, and ultimately understanding how smallholder farmers were interacting within WeFarm.

This analysis aims to define segments of leaders in the data, create topic categories, and see which topics leaders were talking about. It defines leaders in four different ways (detailed below in the section “Four dimensions of leadership”), but generally, leaders are the “superusers” of the service, who either use the service more frequently, or over a longer period of time, or respond more quickly, etc.

More specifically, the segmentation was calculated by responses – not by questions. The thought process here was that if leaders are the ones who have the expert knowledge, and are actively using WeFarm to empower other smallholder farmers, that data will come from responses. These are the users we care about the most.

Once the segmentation was completed, this analysis drilled down to then looked at the questions those leaders produced. The ultimate goal was to examine the following: what were the leaders unsure about? Essentially, what are the most important pain points of the leader market?

This dashboard is hosted on Amazon Web Services, and is available at the domain here:
https://datakit-smallholder-farmers.com/

See the end of the document for takeaways.


# Data preparation
### Sample space

The sample space of the WeFarm dataset is English speaking users only. No translation was performed, although the pipeline allows for more data to be ingested if translation is done beforehand. 

With the current data, the vast majority of English-speaking users were based in Kenya and Uganda, so this analysis focused on those two regions, but again, the dashboard allows for more countries to be placed in the dropdowns if that data becomes available.

### Four dimensions of leaders
Leaders were defined by their responses.

Count: by user, the total number of responses each user had.
Speed: by user, the mean difference between the time questions were posted, and the time their response was sent.
Reach: by user, the number of unique question askers that the responding user reached.
Tenure: by user, the raw difference in time between his/her first response and his/her last response.

##### COUNT
- 1 (low), 2, 3, 4, 5 (high)
##### SPEED
- 1 (low), 2, 3, 4, 5 (high)
##### REACH
- 1 (low), 2, 3, 4, 5 (high)
##### TENURE
- 1 (low), 2, 3, 4, 5 (high)

Notably, each dimension is treated independently, with 1, 2, 3, 4, and 5 of each dimension summing to 100% of all users within each segmentation.

Along the same lines, Count_5 and Speed_5 are not the same subsegment – there is no connection between the numerical labels, besides donating more leadlike behavior. Count_5 is comprised of leaders as analyzed by Count, and Speed_5 is comprised of leaders as analyzed by Speed. 

From here, it is possible to take the intersection of subsegments, i.e. users who were both in Count_5 and in Speed_5. This new user group (or “custom segment”) is like a venn diagram. More information can be found on Tab 3 of the dashboard.

If you’re interested in what defines Count_1 vs Count_2 vs Count_3, and so on, the notebook for this segmentation can be found on GitHub <link [here](https://github.com/ua-chjb/datakit-smallholder-farmers-fall-2025/blob/main/Challenge%203_Community%20Leaders/benjamin_noyes/02_dashboard_pipeline/PIPE1_buckets.ipynb)>.


# Topic Analysis
Text analysis was originally relegated to LDA, with top_n=30 and with number of categories k as np.linspace(5, 30, 6), to investigate where clusters naturally appeared. Several common themes emerged, including “disease”, “crops”, and “livestock”.

Based on information from Producers Direct and DataKind, several other topics were included, such as “financial inclusion” and “diversification”.

From here, 7 broad categories were created (all categories can be found in the appendix). Within each broad category, between 5~50 terms were included for investigation. For each of these in total ~100 terms:

  - Similar terms were computed in vector space, using word2vec with min_count=1
  - Questions were tagged as “including” if they included any of those similar terms (so for example, “grow” would include “grow”, “grows”, “growing”, “increasing”, “increase”, … etc.)
  - A sparse dataframe of questions and their topics was created, with each row representing a unique question, and the columns representing the topics. These topics were not mutually exclusive, as a question could ask about both “passionfruit” and “drought” in the same question, for example.

From here, the count of mentions was summed together, and divided by the total user group, to find the % of the questions that mentioned each topic.

Additionally, Principal Component Analysis (PCA) was performed on niche topic data, to see if there were any relevant patterns amongst the topics. This can be viewed on Tab 7, Topic PCA.


# Navigating the dashboard
### Dropdowns
- Basic segments
  - Country: the country (or countries) to be analyzed
  - Segmentation: the four dimensions of leader segmentation
  - Individual segments: the subsegments 1, 2, 3, 4, 5 of each dimension
- Custom segments: the intersection of different subsegments, like Count_5 and Tenure_5.
  - Country: the country (or countries) to be analyzed
  - Count: the individual subsegments within Count
  - Speed: the individual subsegments within Speed
  - Reach: the individual subsegments within Reach
  - Tenure: the individual subsegments within Tenure
- Topic overview: an overview of how often each term occurred, and their correlations with each other.
  - Toggle: switch between the scatter plot and the correlation heatmap
- Topic drilldown: the % of the selected user segment(s) that used words similar to the given keyword in their questions.
  - Same as above, and includes…
  - Broad topic: the broad category of keywords to zoom in on
- Topics over time:
  - Same as above, and includes…
  - Time slice: the time dimension over which users talked about the topics.
  - Toggle: this changes the graph from aggregate of all keywords in that category (“broad”) to zoom in on specific keywords (“niche”)
- Topic PCA: Principal Component Analysis, a technique that finds dimensions that capture - the most variability amongst the topics.
  - Principal component: select which dimension to view.


### Tabs
1. Tab 1, Geography: 
  - the number of users in each country.
2. Tab 2, Basic segments: 
  - the distribution of each of the dimensions of leaders, among 1 (low), 2, 3, 4, and 5 (high).
3. Tab 3, Custom segments: 
  - the drilldown / venn diagram of the subsegment intersections; for example, the intersection of Tenure_5 and Reach_3 is an interesting subsegment of users who were plugged into the service over a long period of time, but didn’t post many responses.
4. Tab 4, Topic overview:
  - Scatter: How often each topic term appears in the dataset.
  - Correlation heatmap: Pearson’s correlation coefficient amongst the topic terms.
5. Tab 5: Topic drilldown: 
  - the % of the user segment(s) that used words similar to the given keywords.
  - NOTE: most insights can be found starting here. Look for differences in the bar charts between different user groups. Then, move on to Tab 6 to see how this topic was talked about over time.
6. Tab 6, Topics over time: 
  - the % of the user segment(s) that used words similar to the given keywords, over time.
7. Tab 7, Topic PCA
  - Principal Component Analysis (PCA) performed on all niche topics.
  - The top figure shows all Principal Components’ loadings with each feature (topic) on the heatmap, and each Principal Components corresponding total % of the data’s variance explained in the left hand table.
  - The bottom figure shows a zoom-in on the specific Principal Component’s loadings in the middle; on the left, it shows the segmentation breakdown of users that had extreme negative correlation with the PC (bottom 10% of users); on the right, it shows the segmentation breakdown of users that had extreme positive correlation with the PC (top 10% of users)

# Insights
Generally, this analysis organizes insights into two categories: “q&a” insights, and “social connection” insights. “Q&a” insights are insights about users who used the platform as a factual question-and-answer forum. “Social connection” insights are insights about users who used the platform as a means of social connectivity.

### Prized livestock: social connectivity
- Datapoint: 
  - leaders (as defined by count) talked more about livestock than non-leaders, and this disparity increased over time. Specifically, valuable livestock –  such as a cattle, goats, donkeys, and camel – were where this difference was centralized. Chatter about less valuable livestock topics, such as hens, chickens, and poultry did not see this difference.
- Analysis:
  - In Uganda specifically, leaders may have talked more about valuable livestock as a means of sharing their success – in the US, this could be not dissimilar to how users post on Instagram to share their success
- Insight: 
  - the emotional value of WeFarm may have added to the total value of the service in Uganda -- the data suggests this trend increased over time.
- Question:
  - what is the offline connectivity of smallholder farmers in these areas like? Are they socially isolated from other smallholder farmers, or do they interact regularly?

 
### Heat: social connectivity
- Datapoint: 
  - leaders (as defined by response count) talked more about “heat” than nonleaders. The relationship over time is a bit more subtle, but in general, the total percentage of questions that mentioned “heat” increased over time.
- Analysis:
  - Scenario 1: global warming could have led to an increase in temperatures, therefore causing people to post more about “heat” as the years went on. However, this seems unlikely, as macro data on temperatures in Uganda and Kenya were fairly consistent from 2017 – 2021.
  - Scenario 2: social currency is used everywhere, but especially in high context cultures. Both Kenya and Uganda are categorized as high context cultures. “Heat” could have been a euphemism for activity on the site, or a way of connecting with other farmers who also face the same day-to-day problems.

 
### Diversification: social connectivity / q&a
- Datapoint: 
  - several terms around diversification/expansion (“expand”, “begin”, “how” and “when”) were talked about more by specific subsets of nonleaders than by leaders (as defined by count, reach, and tenure).
- Analysis:
  - nonleaders here can generally be understood as people who didn’t use the service that much – in count: not many responses; in reach: not many unique users reached; in tenure, very new to the site.
    - Scenario 1: the differences in these values paint the picture that new users / inactive users were seeking to expand their portfolios more, using the service as a factual q&a for local knowledge.
    - Scenario 2: if we think from a different perspective, all of the terms mentioned above could be euphemisms for how to begin using the platform / polite expressions to get involved. 
- Insight: 
  - Without overreaching on the analysis, this is difficult to parse. Qualitative research would help immensely in this area. 
- Potential product idea: 
  - If scenario 2 is true, it could be useful to have an option “question=answered” that the question asker could mark, which might sway the dynamic more towards q&a.


### Financial inclusion: q&a
- Datapoint:
  - financial topics were split among leaders and nonleaders; some FI topics were talked about more by leaders, some more by nonleaders. While this difference depends somewhat on which country you are analyzing, it seems that “cost”, “price” and “market” are mentioned more by leaders (as defined by tenure), while “money”,”loan”, and “investment”, “finance” and “credit” are mentioned more by new users of the service, and in general these terms are used much less frequently.
  - Additionally, in a specific subset of users who were on the service for a long period of time (leaders in the tenure niche) intersected with users who did not reach very many unique question askers (nonleaders in the reach niche) – so veteran lurkers, essentially – this difference in topics like “cost” and “market” was accentuated.
- Analysis:
  - This larger difference in the custom subsegment would appear to zoom-in on a target market of interest: users who do not care about the social connectivity aspect, but rather only use the service when it benefits them. This could be a potential candidate for a qualitative interview.
  - The difference between leaders and nonleaders could be explained by leaders’ access to the marketplaces – they have used the marketplace, and are asking questions about what price others received.
  - Zooming out, generally, terms like “investment” and “credit” are used rarely in the WeFarm dataset, whereas “price” and “market” are used more. This could be due to a focus on the short term goal of selling a product on the market.





# General themes
  - Ethnography: this would be immensely helpful in achieving certainty around how smallholder farmers were using the service, where social connectivity potentially skewed the data, and where q&a was most valued.
    - Candidates:
      - Reach_5: the superusers who responded to many questions. This group could be categorized as potentially using the service as a means of social connectivity, as well as q&a, as we saw in the insight about “prized livestock” above.
      - Tenure_5 & Reach_3: the factual q&a subset, who were on the site for a long time but did not reach comparatively many users.
      …

    - Questions
      - q&a subset: Why did you not use the service very much? Was there any communication that discouraged you from using it, or were you just not interested?
      - q&a subset: when you did use the platform, what were your considerations in forming the question? Did you feel you had to phrase your questions a certain way to get a response, or was it easy to ask a direct question and get a direct answer?
      - Social connectivity subset: what was your favorite part about using the service?
      - Social connectivity subset: did you ever meet any of the WeFarm users offline, or was WeFarm chatted about offline with other people in your area? How did this affect your business?

  - Q&A vs social connections 
    - there seem to be two uses cases of WeFarm
    - In one use case, farmers posted about specific questions, in the classic q&a format
    - In the other use case, there seems to be a social aspect to the service

  - High-context culture
    - It’s very difficult to parse these two use cases, in part due to the fact that the cultures of Uganda and Kenya are considered “high-context”, which means that context can supersede semantic accuracy. This can prove challenging for data analysis – for example, users at one end of the extreme on various leadership dimensions asked more questions about "diversification" (“expand”, “begin”, “how”, “when”).
    - It could be that:
      - New users were the ones seeking to expand their farming portfolio…
      - Or, these terms were euphemisms for getting started with the service
    - More information on which leadership segments talked about which topic can be explored on Tab 5, Topic Analysis.
    - Because of the uncertainty in this area, this analysis recommends qualitative interviews with WeFarm users, to see what benefits they derived from the platform, and what their use cases were

  - What are the downstream effects of WeFarm?
    - Does word about who is active on WeFarm get around?
    - How does this impact the culture on the ground?

  - Is the Q&A market taken over by ChatGPT and Google?
    - What local knowledge would smallholder farmers have, that ChatGPT or Google wouldn’t have?
    - Is there a way to give a “verified blue check mark” to a specific subset of smallholder farmer experts?
    - Where could a new version of WeFarm provide the most value?

  - What are the emotional benefits of WeFarm?
    - Why did some users become more active as they talked about topics that portrayed them in a positive light? Which caused which? 
    - What are the emotional benefits of a service that connects smallholder farmers, who may not be very connected with others?
    - Could these be amplified in any way, to create a specialized network / community among smallholder farmers?









# Appendix
climate
  "season",
  "time",
  "climate",
  "water",
  "rain",
  "heat",
  "sun",
  "temperature",
  "flood",
  "drought"
crop
  "crop",
  "soil",
  "fruit",
  "plant",
  "leave",
  "fertilizer",
  "seed",
  "potatoes",
  "passion",
  "maize",
  "tomatoes",
  "banana",
  "manure",
  "layer",
  "coffee",
  "tea",
  "onions",
  "grow",
  "mulch",
  "bean",
  "type",
  "cabbage",
  "land",
  "variety",
  "yield",
  "keep",
  "rice",
  "harvest",
disease
  "disease",
  "sick",
  "unhealthy",
  "medicine",
  "treat",
  "weed",
  "control",
  "plant",
  "leave",
  "spray",
  "harvest",
  "affect",
  "prevent",
  "pests",
  "chemical",
  "rabbit",
  "care",
  "tick",
  "attack",
  "mean",
  "black",
  "space",
  "turn",
  "keep"
diversification
  "new",
  "expand",
  "begin",
  "best",
  "increase",
  "clear",
  "add",
  "diversify",
  "irrigation",
  "obtain",
  "shift",
  "acquire",
  "scale",
  "register",
  "use",
  "acreage",
  "grow"
financial inclusion
  "economy",
  "price",
  "sell",
  "market",
  "buy",
  "cost",
  "fee",
  "finance",
  "investment",
  "money",
  "sum",
  "credit",
  "loan",
  "insurance",
  "bank"
livestock
  "livestock",
  "animals",
  "sheep",
  "cattle",
  "donkey",
  "pig",
  "cow",
  "goat",
  "camel",
  "hen",
  "chicken",
  "poultry",
  "lay",
  "egg",
  "milk",
  "breed",
  "dairy",
  "bee"
question
  "who",
  "what",
  "where",
  "when",
  "how",
  "which",
  "many"



