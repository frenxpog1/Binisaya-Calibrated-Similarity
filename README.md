# Binisaya-Calibrated Similarity: A Cebuano-Parameterized Editex and Syllable-Stress Pipeline for Confusable Drug Name Detection

Research materials for the AIRLiC 2027 revision. We study how well spelling and Cebuano-aware pronunciation scores rank medicine-name pairs for pharmacist review. The Likoliko web application has a [separate source repository](https://github.com/frenzteriod-hub/confusable-drugs).

## Evaluation history

The poster reports 31,208 product records and an index of 25,167 names. The historical review workload comprised 20,000 pairs. At the poster snapshot, 696 pairs had judgments from all three reviewers. These counts describe different stages of the study. Results on the completed subset apply to that subset.

## Revision questions

1. Does the batch scorer use the same Cebuano Editex, pronunciation-path, syllable and stress calculations as the documented composite? Trace representative pairs through both implementations and record the code revision, weights, tie handling and missing-stress behavior.
2. How consistent are the reviewers? Report the three-way label distribution and agreement before collapsing labels. Document how “Needs discussion,” ties and incomplete reviews affect the denominator.
3. What does each component contribute? Compare the corrected composite, spelling and pronunciation baselines, and one-component-at-a-time ablations on identical pairs. Report average precision and precision at fixed review budgets alongside the positive-label prevalence.
4. How well does the ranking generalize? Keep the historical queue separate from newly generated candidates. Reserve an independent evaluation set before fitting any weights and document which names and pairs overlap across splits.
