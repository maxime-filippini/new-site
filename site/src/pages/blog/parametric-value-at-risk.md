---
title: "The Parametric methodology for Value-at-Risk"
emoji: 🎛️
slug: the-parametric-methodology-for-value-at-risk
publish_date: 2023-06-11
update_date: 2023-06-11
tags: [risk_management]
image: "/images/covers/chartguy.png"
image_attribution: ""
draft: false
post_summary: "While the Historical Simulations approaches do not make assumptions on the behavior of financial losses, the Parametric methodology is built around it! In this post, we start by defining the crux of the methodology and end by building an understanding of its two main models."
series: Value-At-Risk
---

In the last post, we have gone over the basics of the Historical Simulations methodology for computing Value-at-Risk, whose core value proposition is that it does not require us to make assumptions about the behavior of financial losses.

Today, we are going to shine a light on a second type of methodology, which is the complete opposite, as it fully relies on behavior assumptions to derive Value-at-Risk figures.

Strap in, because there is a lot to cover on this topic!

## A methodology based on models

In the wild, you may hear about "VaR models", when referring to one of the largest categories of methodologies (e.g. Historical Simulations or Parametric).

While one could qualify the Historical Simulations methodology (and its time-weighted counterpart) as a model, **there is no such thing as a "Parametric VaR model"**.

Instead the Parametric methodology is built around the definition of a **model** that describes the behavior of financial losses, from which a Value-at-Risk can be derived.

In the next sections, we go over some key concepts that are crucial in the determination of behavior models for financial variables, before we jump into the various types of Parametric Value-at-Risk models used in practice.

## Random variables and probabilities

In our [first post](/blog/an-introduction-to-value-at-risk), we talked about how the assignment of probabilities to events is one of the cornerstone of risk measurement, and how this is done using a **probability distribution**. For this post, we need to write things a little bit more formally, so we can build upon it when we define our behavior models.

To represent outcomes that are random in nature, we use **random variables**, commonly written in capital letters, such as $L$ (e.g. to represent losses). Simply put, these random variables represent a mapping between elements of a [sample space](https://en.wikipedia.org/wiki/Sample_space) into something whose probability can be measured.

For our use case, we are going to focus onto the (more complex) case of **continuous random variables**, i.e. those whose outcomes are "without gap". For example, we can choose to represent the financial loss of an investment over the next day as a continuous random variable, in which case there will exist an infinity of possible losses between any pair of loss events $l_1$ and $l_2$.

### Outcomes and events

If we consider the case of **relative losses**, i.e. the percentage of our portfolio value that is lost over a given day, which we will write $L$. **What are the possible outcomes for this variable?**

Given this definition, the loss outcomes can take values from $\Omega = [-\infty, 100\%]$.

(Note: While we cannot lose more than 100% of our portfolio, gains are technically not bounded.)

Now, in terms of these outcomes, how do we define all of the possible **events** to which a probability can be assigned?

One can intuit that we can technically measure probability for an infinity of loss intervals.

For example, the event $]0, 10\%[$, represents losses up to 10% of our portfolio, and this event will have a certain probability. Similarly, the event $]VaR, 100\%]$ represents the case where the loss would exceed a certain value $VaR$, and we can also assign a certain probability to that.

In the same vein, we could consider **unions** of such intervals, like the event where we have a gain **or** a loss that exceeds 10% of our portfolio, i.e. $]-\infty, -10\%[ \cup  ]10\%, 100\%]$.

Finally, the **complement** of our union, i.e. the cases where our change in value is less than 10%, written $[-10\%, 10\%]$, can also be assigned a probability, and we know that this probability, when summed to the probability of the union defined above, will be equal to 1.

We call the space made up of all of these elements, i.e. all intervals and unions of intervals contained within $\Omega$ as our **event space**.

We are now missing a single element to define our random variable formally, our **probability measure**, i.e. the function that determines the probability of each event in our event space. In our case, we are going to define that assignment of probabilities to event using the **cumulative distribution function** (also known as "cdf").

### Probabilities in terms of cumulative distribution function

We recall that if we write the cdf that defines the distribution of $L$ as $F_L$ , and our probability measure as $P$ , then it is defined as:

$$
	\forall x \in \mathbb{R}, \quad F_L(x) = P(L \leq x)
$$

To this, we add some axioms of probability measures:

- $P(\Omega) = 1$ and $P(\emptyset) = 0$
- For two disjoint intervals, i.e. $I_A$ and $I_B$ where $I_A \cap I_B = \emptyset$, $P(L \in I_A \cup I_B) =P(L \in I_A) + P(L \in I_B)$.

From these three axioms, we derive that if we write $I^C$ the complement of an interval $I$, i.e. $I \cap I^C = \emptyset$ and $I \cup I^C = \Omega$, then we have

$$
\begin{align*}
	P(L \in \Omega) = P(L \in I \cup I^C) = P(L \in I) + P(L \in I^C) &= 1 \\
	\Rightarrow P(L \in I^C) &= 1-P(L \in I)
\end{align*}
$$

Thus, we obtain the following:

$$
	\begin{align*}
	P(L \in ]0\%, 10\%[) &= 1 - P(L \in ]-\infty, 0] \cup [10\%, 1])\\
	&= 1- \left(P(L \in ]-\infty, 0\%]) + P(L \in [10\%, 100\%])\right)\\
	&= 1 - \left(P(L \leq 0\%) + (1-P(L\leq10\%))\right)\\
	&= F_L(10\%) - F_L(0\%)
	\end{align*}
$$

## Distributions and Data Generating Process

Consider a concrete case of Value-at-Risk calculation, starting from loss observations gathered into a loss sample $S_L = \{l_1, ..., l_T\}$. Where did those loss observations come from?

Since we consider our losses to be random, then each $l_i$ has to be the **realization** (or **measurement**) of a certain random variable. This random variable can, but does not have to, be dependent of the time of observatio, and may also include deterministic (i.e. non random) components that are either constant, or known at the time of measurement.

For most practical applications, we write the random loss which can be observed at time $t$, $L_t$, in terms of a model that approximates the so-called **data-generating process**, i.e. a function which depends on $t$, and defines the dependency between $L_t$ and past data (endogenous and exogenous).

Consider the case of a fair coin being tossed once a day, and for which the total number of Heads is being tallied over time. If we write that total as the random variable $X_t$, then the data generating process could be written:

$$
	\forall t,\quad X_t = X_{t-1} + Z_t
$$

Where $Z_t$ represents the random value of a single fair coin toss, and therefore follows a [Bernoulli distribution](https://en.wikipedia.org/wiki/Bernoulli_distribution) with parameter $p=0.5$.

At time $t-1$, we already know the realized value of $X_{t-1}$, which we write $x_{t-1}$. Therefore, we can determine the distribution of $X_t$ **conditional on $X_{t-1}$ being equal to $x_{t-1}$** as:

$$
	\begin{cases}
	P(X_t = x_{t-1}|X_{t-1}=x_{t-1})&= 0.5\\
	P(X_t = x_{t-1} + 1|X_{t-1}=x_{t-1})&= 0.5\\
	\end{cases}
$$

For our Value-at-Risk calculation, made at time $T$, we are concerned about what, $L_{T+1}$ could be, knowing the past realizations, i.e. $L_1 = l_1$, $L_2 = l_2$, ..., $L_t = l_t$. It is usual to write this set of conditions as $\mathcal{F}_{t}$, as it is formally known as a [filtration](<https://en.wikipedia.org/wiki/Filtration_(probability_theory)>).

Here are the general steps applied for the computation of VaR using the parametric method.

- First, we define a model that will approximate the data-generating process for our losses;
- Based on this model, we determine the distribution of $L_{T+1}$ (or of a region of interest) conditional on $\mathcal{F}_T$;
- From this distribution, we derive the wanted quantile $F_L^{-1}(\alpha)$, which is none but our Value-at-Risk.

In the next sections, we delve into a couple of specific approaches, most used in practiced.

## The most basic model - Assumption of Gaussian-distributed losses

A common assumption is that relative losses follow a Gaussian (or Normal distribution).

The model for the data-generating process is the following:

$$
	\forall t, \quad \begin{cases}
	L_t = \mu+\sigma Z\\
	Z \sim \mathcal{N}(0,1)
	\end{cases},
$$

where $\mu$ and $\sigma$ are the parameters model, respectively representing the mean relative loss and the standard deviation of relative losses (also called "**volatility**"), and $Z$ is a random variable that has a Standard-Normal distribution (i.e. $\mathcal{N}(0,1)$).

This equation leads to the fact that, for all $t$, $L_t$ follows a Gaussian distribution with parameters $\mu$ and $\sigma$, written $\mathcal{N}(\mu, \sigma)$. Here, we note that $L_t$ has no dependency with any previous loss, since neither $\mu$, $\sigma$ or $Z$ depend on $t$.

$\mu$ and $\sigma$ are estimated using the loss sample $S_L = \{l_1, ..., l_T\}$, in a way that yields the distribution $\mathcal{N}(\mu, \sigma)$ that is the most likely to have generated $S_L$ (see [Maximum Likelihood Estimation](https://en.wikipedia.org/wiki/Maximum_likelihood_estimation)).

(Note: For a time horizon of 1 day, it is often difficult to estimate a value for $\mu$ that is statistically different from 0. As such, it is often assumed that $\mu=0$.)

Conditional on $\mathcal{F}_T$ (and even unconditionally in this case), $L_{T+1}$ follows a $\mathcal{N}(\mu, \sigma)$ distribution, and therefore, we can compute $F_L^{-1}(\alpha)$ numerically, using Excel or Python.

## Relaxing assumptions - Autoregressive models

The Gaussian model described above presents one glaring issue: it does not account for the well-known [stylized fact](http://rama.cont.perso.math.cnrs.fr/pdf/empirical.pdf) that the volatility of financial returns (and therefore losses) tends to come **clustered in time**, i.e. that periods of high (or low) volatility can be defined.

To try to remedy this, we make a change to the model:

$$
	\forall t, \quad \begin{cases}
	L_t = \mu_t + \sigma_t Z\\
	Z \sim \mathcal{N}(0,1)
	\end{cases}
$$

This change may be small in notation, but it is large in meaning. Indeed, we are now saying that each loss $l_t$ in our sample is a realization of $L_t$, which has a distribution of $\mathcal{N}(\mu_t, \sigma_t)$, which may be different for all $t$.

We start by making the usual assumption that, for all $t$, $\mu_t = 0$. We now have:

$$
	\forall t, \quad \begin{cases}
	L_t = \sigma_t Z\\
	Z \sim \mathcal{N}(0,1)
	\end{cases}
$$

As is, this model is incomplete, as we still to define the behavior of $\sigma_t$ over time. Guess how? **More models!**

We provide the definition of two common models that somewhat account for the clustering of volatility below:

$$
	\begin{cases}
		\forall t, \quad \sigma_t^2 = \lambda \sigma_{t-1}^2 + (1-\lambda) l_{t-1}^2 & \text{(EWMA)}\\
		\forall t, \quad \sigma_t^2 = \omega + \beta \sigma_{t-1}^2 + \alpha l_{t-1}^2 & \text{(GARCH(1,1))}
	\end{cases}
$$

As you can see, the **variance** (i.e. the squared volatility) at time $t$ directly depends on the previous variance as well as on the previous squared relative loss.

One thing that is needed for both these models is a "seed variance", i.e. a value for $\sigma_0^2$, so that all other $\sigma_t$ can be defined. In practice, this is usually done by reserving the first chunk of our loss sample for the estimation of this seed variance, via a sample estimation.

This dependence on past losses means that our volatility/variance process is also random, but not when considered **conditionally** on $\mathcal{F}_{t-1}$!

Let's say we opted for the GARCH(1,1) model for our $\sigma_t$ term. Now our loss model becomes:

$$
	\forall t, \quad \begin{cases}
	L_t = \sigma_t Z\\
	\sigma_t^2 = \omega + \beta \sigma_{t-1}^2 + \alpha l_{t-1}^2\\
	Z \sim \mathcal{N}(0,1)
	\end{cases}
$$

This model has 3 parameters, $\theta = (\omega, \alpha, \beta)$, which can be estimated by way of [Maximum Likelihood Estimation], since we are aiming to find all of the $Z_t \sim \mathcal{N}(0, \sigma_t(\omega, \alpha, \beta))$ which are the most likely to have generated our lost sample $S_L = \{l_1, ..., l_T\}$ (again, via the Maximum Likelihood Estimation method).

The theory behind this estimation process will not be covered in this post, but might be a topic we explore in the future.

Had we opted for the EWMA model, we have a single parameter to estimate, i.e. $\theta = (\lambda)$, and in many cases, this value is set to the "standard" set by the RiskMetrics methodology, i.e. $\lambda=0.94$ for daily data, or $\lambda=0.97$ for monthly data.

Once our parameters are estimated (or assumed), obtaining a Value-at-Risk figure is almost as simple as in the Gaussian case. We start from our loss sample $S_L$, and define all volatility values $\sigma_t$ using our model (EWMA or GARCH(1,1)), up to $\sigma_{T+1}$. Since we have assumed that $L_{T+1}$ can be written as $\sigma_{T+1}Z$, our VaR will be equal to:

$$
    VaR(\alpha) = \sigma_{T+1} F_Z^{-1}(\alpha),
$$

and $F_Z^{-1}(\alpha)$ is the $\alpha$-quantile of the Standard-Normal distribution, which can be computed numerically (e.g. via `NORM.S.INV` in Excel).

## What is to come

In this post, we have gone over the foundation of the Parametric approach for the computation of Value-at-Risk, covering the Gaussian approach as well as its extension to autoregressive models for volatility.

In the next couple of posts, we will delve into the implementation of these approaches, as well as derive some idea of their performance against the Historical Simulations methods defined in the previous post.

We will then discuss of a semi-parametric approach, that should yield the "best of both worlds".
