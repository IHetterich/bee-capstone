# CCD and the Recovery of American Bees
![A bee hive](images/bee_banner.jpg)
## Overview
Colony Collapse Disorder, or CCD, is a phenomenon where the majority of the worker bees in a colony will suddenly disappear. This disappearance is incredibly damaging for the hive and the grand majority do not survive. While many reports suggest that CCD has afflicted hives for well over a century (there are reports matching the description back to 1869) it has only come into the public eye in the last 20 or so years. This is mainly due to much higher observed rates in the 1990's through the mid 2000's leading up to the actual classification and naming of the disorder in 2006. To this day the actual cause of CCD is unknown, there are several theories but no concrete facts beyond its existence and devastating effects.

Bees of course play in incredibly vital role in their ecosystems as pollinators. We additionally rely on domestic hives to pollinate our crops and produce honey. So when CCD flared up and was officially classified many people sounded the alarm so to speak. Major efforts were instituted by the EPA to track and study both domestic and wild colony health. Thankfully over time the rate of CCD appeared to slow, many reports have even stated that the American Honey industry is recovering, leading to the following questions.

## Questions
- How have domestic bee populations responded after the uptick in CCD?
- If they are recovering to what extent can we see that?
- More than just the colonies, how has the honey industry been effecting in the wake of this colony die-off?

## The Data
The focus on domestic bee colonies in the questions above is due to the nature of the data we are working with. While domestic honey producers have to register their operations with the USDA wild colonies obviously don't and as such the only complete data we have is for domestic colonies.

Data was sourced at first from a [kaggle dataset](https://www.kaggle.com/jessicali9530/honey-production) for 1998-2012. I was hoping to extend this dataset to the present so I tracked down the original source, the [Annual Honey Report](https://usda.library.cornell.edu/concern/publications/hd76s004z?locale=en) published every spring by the NASS (National Agricultural Statistics Service). From there I took the corresponding tables as seen below and developed a script to automate the cleaning process.
<p align='center'>
<img src='images/raw_data.png' alt='Raw format of data' width=400>
</p>
Once cleaned the data was merged with the kaggle dataset and a new complete csv was written, it can be found in this repositories data directory.

In terms of quality the data is wonderful, all listed states in the report have values for every field so nan values were not an issue. Furthermore I was able to keep all the columns present as they covered exactly the information I was looking for. That said several states we not present in every year's report. Whichever states were omitted were bundled into a single field in order to not disclose data for individual operations. That said even the sum of these states was small and as such I omitted them from my study in order to ensure consistent data for all years from 1998-2019.

## Visualizing Bee Populations
Needs a better section title first off. Get some nice visualizations of hive population over time to show a clear trend towards growth.

## Hypothesis Testing
Run through bootstrap methodology and arrive at a p-value that doesn't allow us to reject the null hypothesis.

## The Honey Industry
Run through visualizations of honey production metrics, show the strong correlation between price and total value and the non-existent correlation elsewhere. Look into honey industry reports for some kind of explanation or elaboration.

## Conclusion
Overall hopeful outlook even without a nice p-value (maybe a graph of p values from 09 onward showing a trend?) Maybe highlight how insane ND is.

## Sources and acknowledgements
Self-explanatory