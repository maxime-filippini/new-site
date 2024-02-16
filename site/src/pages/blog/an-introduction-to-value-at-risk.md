---
title: An introduction to Value-at-Risk
emoji: 📈
slug: an-introduction-to-value-at-risk
publish_date: 2023-06-05
update_date: 2023-06-05
tags: ["risk_management"]
image: http://source.unsplash.com/uKlneQRwaxY
image_attribution: https://unsplash.com/fr/@edge2edgemedia
draft: false
post_summary: "Value-at-Risk is by far the most infamous measures of financial risk. This first post kicks of a new series in which we dive into its definition, how it can be implemented, and how its performance can be assessed."
series: Value-At-Risk
template: blog_post.html
---

Everyone has, in their life, learned about the notion of risk. When undertaking any activity, we expose ourselves to uncertain outcomes, which may be detrimental to our success or our wellbeing.

While everyone has a different tolerance for risk, there is a process we all go through, which is to determine whether the risk we may be facing is acceptable with respect to that tolerance. This process, called **risk assessment**, is performed in a systematic manner when it comes any money investment.

In this new series of posts, we are going to delve into the concepts of risk management, with a particular subset of the risk assessment process, called **risk measurement**, which is quantitative in nature. For now, we are going to focus on the most (in)famous method for measuring the risk of a financial portfolio: **Value-at-Risk**.

## Table of Contents

## Risk, uncertainty, and measurement

### Risk vs Uncertainty

We often see the terms "Risk" and "Uncertainty" conflated, both referring to possible uncertain outcomes, i.e. that we could not possibly know in advance. However, it is important to disambiguate between events to which we can assign a probability of occurrence, and those to which we cannot.

The latter type is often referred to as "unknowable unknowns" or "Knightian uncertainty", the former type is what we commonly classify as "risk": unwanted outcomes that we can measure, both in terms of the outcome itself, and in terms of its probability of occurring within a certain time frame.

This separation between uncertainty and risk was first introduced by Frank Knight in his seminal book: ["_Risk, Uncertainty and Profit_"](https://archive.org/details/riskuncertaintyp00knigrich).

To perform this process of "probability quantification", we start by introducing the concept of **Probability distribution**.

### Probability distributions

In the field of probability theory, a probability distribution represents a mathematical function that converts a certain outcome to a probability of occurrence. We distinguish two forms of distributions:

- those whose outcomes are "**discrete**", e.g. if our event is the roll of a six-sided die, whose outcomes are fully described by the set of numbers $\{1,2,3,4,5,6\}$; and
- those whose outcomes are "**continuous**", e.g. the amount of rain on a given day.

In the most general sense, we define the **cumulative distribution function** (also known as "cdf") as:

$$
    F_X(x) = P(X \leq x)
$$

i.e. $F_X(x)$ is the probability that the outcome of $X$ is below $x$. Here, $X$ can be the roll of a die, or the amount of rain in a day, or any other outcome that can be defined as "random".

For discrete distributions, we can rewrite this quantity as:

$$
    F_X(x) = \sum_{k \leq x} P(X = k)
$$

and in the case of our die roll, we have

$$
    F_X(3) = P(X=1)+P(X=2)+P(X=3) = \frac{3}{6} = \frac{1}{2}
$$

For continuous distributions, it is a bit more complicated. Consider our rainfall example from above, how could we define $P(X=x)$?

If we take $x = 50\text{mm}$, what is the probability that we observe exactly that amount of rain in a given day? How can we be sure that it is **exactly** this amount? We can never be certain that it is $50\text{mm}$ that we observe and not $50.00000001\text{mm}$. Our measurement tools cannot possibly be that precise.

Effectively, $P(X=x) = 0$ for all values of $x$.

However, $P(X\leq x)$ still makes sense in this context, and for most values of $x$, this value will not be 0.

For those more mathematically inclined, the transition from discrete to continuous distribution requires us to change our discrete sum of probabilities, into a continuous one, known as **integral**.

We write the cumulative distribution function for this type of outcome as:

$$
    F_X(x) = \int_{-\infty}^{x} f_X(t)dt
$$

Where the function $f_X$ effectively determines how probabilities should be assigned for very small ranges of outcomes (e.g. that our recorded rainfall ends up being very close to 50mm).

Since the probability of all outcomes taken together is equal to 1, we can easily determine that:

$$
    \begin{aligned}
        &P(X \leq x) + P(X > x) = 1\\
        \Rightarrow \text{   } &F_X(x) + P(X > x) = 1\\
        \Rightarrow \text{   } &P(X > x) = 1 - F_X(x)
    \end{aligned}
$$

"<span className="text-cgreen">Why all the math?</span>", I can hear you asking. Well, now let us define $L$ as the possible losses of a given investment. Defining the risk of loss for this investment, is akin to determining $F_L(l)$, or rather $P(L>l)$, for different levels of loss $l$ (i.e. "_how likely is it that it will get worse than that?!_").

In the next chapter, we are going to talk about **Value-at-Risk**, which is directly related to this idea.

## Value-at-Risk as a risk measure

We saw that the assignment of a probability to a given outcome can be done via the cumulative distribution function. But what if we could perform this assignment in reverse, i.e. start from a probability, and get an outcome? This is what Value-at-Risk does.

For a given confidence $\alpha$ and a time horizon $T$, we write:

$$
    P\left(L > VaR(\alpha, T)\right) = 1 - \alpha
$$

In plain English, we would say:

> The probability of observing a loss over a time horizon of $T$ that is higher than $VaR(\alpha, T)$ is equal to $1-\alpha$

In practice, $\alpha$ is set to be close to 1, e.g. 99%, so that $VaR(\alpha, T)$ represents an unlikely loss.

This definition is effectively the inverse of $F_L$, i.e. we can read VaR on a chart by finding $\alpha$ on the y-axis, as shown below. This inverse of the cdf is called the **quantile function** associated with $L$.

<div id="chart">![](../../assets/cdf.png)</div>

<!-- {<Caption>With the cdf plotted, here is where we read alpha and VaR</Caption>} -->

### Risk measures

There exists a mathematical formalism used to define risk measures. At the very least, a risk measure has to have the following properties:

- When applied to a portfolio that holds no asset, the risk has to be 0.
- If we add a quantity of cash to our portfolio (a "riskless" asset), the risk of our portfolio has to be the risk of our risky assets, minus the amount of cash added.
- If we have two portfolios $A$ and $B$, and $B$ **cannot possibly** give losses higher than $A$, then the risk of $B$ has to be lower than the risk of $A$.

This all makes sense right? For our second property, you can think of the cash as a cushion that will dampen the losses experienced in all cases, since its value cannot change.

Does VaR satisfy these properties? **Yes!**

- If our portfolio has no asset, then all possible losses are 0. By definition, under this circumstance, the VaR has to be 0. (Note: this cannot be shown using the definition I have provided above. Under the possibility of non-continuous distribution, which is the case here since only a single event is possible, the definition would have to be amended.)

- If we add cash to our portfolio, we are basically shifting the curve of $F_L$ shown above to the left by the amount of cash, since all possible losses are dampened by the cash. This effectively shifts the VaR by the same amount.

- If portfolio $B$ cannot possibly lose more portfolio $A$, under any circumstance, it means that the $F_L$ curve for $B$ is fully on the left of that of $A$, and therefore, $B$'s VaR will be lower than $A$'s.

### Coherent risk measures

For a risk measure to be **coherent**, it has to satisfy one additional property:

- If we combine two portfolios, the risk of the combined portfolio can, at the most, be equal to the sum of risks of the individual portfolios.

This property means that the risk measure appropriately represents the **diversification benefit** that comes from combining portfolio.

While you may have heard that VaR is **not** a coherent risk measure, one should note that it can be, under certain circumstances.

## Value-at-Risk methodologies

As we previously mentioned, computing VaR is equivalent to determining the inverse of the cumulative distribution function for a certain value $\alpha$. Doing so means we need to be able to associate loss outcomes and probabilities.

To do so, we are going to leverage historical loss data, to some extent, and make some assumptions along the way.

Let us assume that we have observed a sample of losses of length $N$, written $\{l_1, l_2, ..., l_N\}$, where the index represents the time at which the loss was observed. (Note: any negative $l_i$ would represent a gain of $-l_i$.)

### The Historical Simulations methodology

The Historical Simulations methodology makes the following assumption:

> $S_L = \{l_1, l_2, ..., l_N\}$ accurately represents the possible values of future loss over the next time horizon.

Under this assumption, the cumulative distribution function gets approximated by the **empirical cumulative distribution function**, which is basically equivalent to the way we work with discrete distributions, i.e.

$$
    F_L^{emp}(l) = \frac{\#\{l_i \in S_L , l_i \leq l \}}{\#S_L}
$$

This means that the empirical cdf calculated at $l$ simply represents the proportion of the sample that is below $l$.

Armed with this knowledge, how do we compute VaR for our sample $S_L$?

- First, we rank $S_L$ from the worst loss, to the best gain. We write the ordered losses as $l_{(1)}, ..., l_{(N)}$.
- Then, the VaR is defined as $l_{(i)}$, $i$ being the largest index so that $\frac{i}{N} < 1-\alpha$.

This methodology is by far the easiest to put in place, and it has the nice property that it makes no assumption on the distribution of losses. However, one should ensure that the main assumption behind the methodology holds in light of the observed losses.

### The Parametric methodology

Quite opposite to the Historical Simulations methodology, the Parametric family of methodologies is simply based on making an assumption on the distribution of losses $L$, for which we would have a known functional form for the inverse of the cdf $F_L$.

For example, a common assumption is that losses follow a certain [Gaussian distribution](https://en.wikipedia.org/wiki/Normal_distribution) (with parameters $\mu$ and $\sigma$), for which VaR can be computed using a programming language, or even Excel. Unfortunately, it cannot be calculated directly on paper, since the quantile function of that distribution does not have a [closed-form expression](https://en.wikipedia.org/wiki/Closed-form_expression).

The estimation of the distribution parameters is the whole exercise when it comes to Parametric approaches. For most sub-categories of methodologies, methods can be devises to derive these parameters for the loss sample $S_L$ defined above.

## To be continued...

This post is the first in a series on Value-at-Risk, in which we will build up to implementing various methodologies and compare their performance.

You can expect the following:

- A deep dive into all of the commonly used methodologies and how they can be implemented in Python;
- How to back-test Value-at-Risk models; and
- A comparison of the performance of these models on various asset classes.

Stay tuned! 📻
