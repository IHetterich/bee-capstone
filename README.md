# CCD and the Recovery of American Bees
![A bee hive](images/bee_banner.jpg)
## Overview
Colony Collapse Disorder, or CCD, is a phenomenon where the majority of the worker bees in a colony will suddenly disappear. This disappearance is incredibly damaging for the hive and the vast majority do not survive. While many reports suggest that CCD has afflicted hives for well over a century (there are reports matching the description back to 1869) it has only come into the public eye in the last 20 or so years. This is mainly due to much higher observed rates in the 1990's through the mid 2000's leading up to the actual classification and naming of the disorder in 2006. To this day the actual cause of CCD is unknown, there are several theories but no concrete facts beyond its existence and devastating effects.

Bees of course play in incredibly vital role in wild ecosystems as pollinators. We additionally rely on domestic hives to pollinate our crops and produce honey. So when CCD flared up and was officially classified many people sounded the alarm so to speak. Major efforts were instituted by the EPA to track and study both domestic and wild colony health. Thankfully over time the rate of CCD appeared to slow, many reports have even stated that the American Honey industry is recovering, leading to the following questions.

## Questions
- How have domestic bee populations responded after the uptick in CCD?
- If they are recovering to what extent can we see that?

## The Data
The focus on domestic bee colonies in the questions above is due to the nature of the data we are working with. While domestic honey producers have to register their operations with the USDA wild colonies obviously don't and as such the only complete data we have is for domestic colonies.

Data was sourced at first from a [kaggle dataset](https://www.kaggle.com/jessicali9530/honey-production) for 1998-2012. I was hoping to extend this dataset to the present so I tracked down the original source, the [Annual Honey Report](https://usda.library.cornell.edu/concern/publications/hd76s004z?locale=en) published every spring by the NASS (National Agricultural Statistics Service). From there I took the corresponding tables as seen below and developed a script to automate the cleaning process.
<p align='center'>
<img src='images/raw_data.png' alt='Raw format of data' width=600>
</p>
Once cleaned the data was merged with the kaggle dataset and a new complete csv was written, it can be found in this repository's data directory.

In terms of quality the data is wonderful, all listed states in the report have values for every field so nan values were not an issue. Furthermore I was able to simply keep all the columns present as they covered exactly the information I was looking for. That said several states we not present in every year's report. Whichever states were omitted were bundled into a single field in order to not disclose data for individual operations. That said even the sum of these states was small and as such I omitted them from my study in order to ensure consistent data for all years from 1998-2019.

## Visualizing Bee Populations
Our first question of how bee populations have responded in the wake of CCD is an easy one to dive into. A great place to start is in looking at our national average across our time span of 1998 - 2020.
<p align='center'>
<img src='images/avg_cols.png' alt='Average colonies'>
</p>

Now right off the bat I for one was surprised at this rate of loss in 2004-2008. While it's clear to see I was expecting something a lot more drastic based on what I knew about CCD. While this dip does represent a loss of tens of thousands of hives I expected more severity. As for the recovery of colonies it appears that we have not only returned to but surpassed colony levels from before CCD. But this is afterall an average, so maybe the picture will be clearer if we break it down by state.

<p align='center'>
<img src='images/map_2008.png' alt='Map of colonies in 2008', width=800, height=400>
<img src='images/map_2019.png' alt='Map of colonies in 2019', width=800, height=400>
</p>

Looking at these a few things caught my attention. Firstly while there does seem to be a definite increase in hives it doesn't appear that dramatic. Secondly there seems to be no change in North Dakota, South Dakota, and California. In fact they seem to have had plentiful hives even at the lowest point nationally in the past 21 years. I was curious how their numbers looked compared to the national trend.

<p align='center'>
<img src='images/avg_vs_large.png' alt='Map of colonies in 2008'>
</p>

And we can immediately see that they are outliers to put it mildly. At its lowest point South Dakota still had roughly 3 times as many colonies as the national average. While good news on whole, knowing that CCD hasn't been more than a speed bump to the growth in ND and SD and only a slight contributor to the general decline in CA, these incredibly high numbers are going to pose a challenge in trying to see if the rest of the country has recovered.

## Hypothesis Testing
Well our first step, as always with hypothesis testing, is to come up with some hypotheses. In particular our null and alternative:

<p align='center'>
<b>H<sub>0</sub>: &mu; of 2008 = &mu; of 2019<br>
H<sub>A</sub>: &mu; of 2008 < &mu; of 2019</b>
</p>

To quickly summarize we're starting with a null hypothesis that the mean of our current population is actually the same as it was in 2008, at our lowest point in the dataset. Our alternative is that our current population average is actually higher. Our next two steps before we actually start doing math are settling on a test and selecting an alpha value. Since we're testing whether two samples are drawn from the same population or not the obvious answer is a [Student's t-test](https://en.wikipedia.org/wiki/Student%27s_t-test) which was developed for this exact purpose. As for our alpha, how certain we want to be that they are in fact different, we'll go for the standard value of .05.

The final consideration before running our test is whether we want to include ND, CA, and SD for the reasons discussed earlier. Since they represent such outliers both in terms of size and behavior we are discounting them for the moment. When we run our test using `scipy.stats.ttest_ind()` and feed in our samples from 2008 and 2019 the results are less than exciting to put it plainly. We arrive at a p-value of .40, very much above our threshold of rejection. As such we've failed to reject our null hypothesis and we can't say that there's statistical evidence that bee populations have substantively recovered since 2008.

## Conclusion and Further Steps
So where does this leave us? While it seems like the population is recovering when we look at the population trends we can't confirm that through hypothesis testing. So what good is a hunch without proof? How much longer do I have to lose sleep thinking about the threat that CCD poses to bee colonies?

Well as it turns out even though we can't reject our null hypothesis currently I'm fairly hopeful about recovery being true. Whenever testing a hypothesis over time it's important to view the p-values of many points in time. The latest date may be the most immediately interesting but in order to really be confident that a change has happened you have to protect yourself from fluke years. For instance if bees had one fantastic year and their population skyrocketed you could get a p-value under .05, but if that population falls right back down the next year that's no kind of real recovery. As such the key is to look at the trend of p-values, if real recovery is occuring they'll start trending towards 0, just like it's suggested in the graph below.
<p align='center'> 
<img src='images/p_value_trend.png' alt='Bootstrapping results'>
</p>
While we don't have that many data points yet it does seem like a trend is emerging. So while it may not be time to open a bottle of champagne just yet, it looks like that day is on the way. We just have to wait and see where further data leads us.

While we wait for that data, however, there is plenty of other things to dig into. In fact we haven't touched the majority of the data in our dataset that pertains to actual honey production. My next steps on this analysis are going to focus on how the honey industry has responded to the CCD crisis. Another point of interest moving forward will be bringing in another report the NASS releases yearly which has information on rates of colony survivorship through winter. With that data it may be possible to see how much of this population behavior is due to lower rates of CCD and how much is due to more aggressive beekeeping strategies of propgating colonies.

## Citations
I would like to close out with just one more mention on the source of this data, and to thank the curators of both these sources for their work and diligence.

1998 - 2012 https://www.kaggle.com/jessicali9530/honey-production

2013 - 2019 https://usda.library.cornell.edu/concern/publications/hd76s004z?locale=en