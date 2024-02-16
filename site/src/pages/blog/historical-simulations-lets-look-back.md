---
title: "Historical Simulations VaR: Let's look back!"
emoji: ⏮️
slug: historical-simulations-var-lets-look-back
publish_date: 2023-06-07
update_date: 2023-06-07
tags: [risk_management]
image: http://source.unsplash.com/fD3L5wxiEoo
image_attribution: https://unsplash.com/fr/@jontyson
draft: false
post_summary: "The Historical Simulations approach is one of the simplest methodologies for computing Value-at-Risk. In this post, we go over the entire process of this computation, from the sourcing of market data, to the various manipulation steps required to obtain our risk measure."
series: Value-At-Risk
---

We have talked about the concept of Value-at-Risk, but how is it applied in practice? In this post, we are going to consider a simple investment situation, and run through the entire process, from the collection of data to the risk measurement.

Let us get started by considering the following:

<blockquote className="flex flex-col">
Today is June 6th 2023. We have a (modest) portfolio made up of 15 shares of an exchange-traded-fund ("ETF") [tracking the S&P500 index](https://markets.ft.com/data/etfs/tearsheet/summary?s=500:PAR:EUR).
<br/>   
We wish to gain exposure to the European credit markets by purchasing 5 shares of [a bond ETF](https://markets.ft.com/data/etfs/tearsheet/summary?s=AHYE:PAR:EUR).
<br/>   
What is the current risk of our portfolio (via Value-at-Risk)? What would that level of risk be if we were to make that investment?
</blockquote>

We will be measuring risk using a Value-at-Risk, with $\alpha = 99\%$ and $T=1 \text{ day}$. While looking at risk over a 1-day horizon may seem contrived and reductive, we do so to keep things simple for now, and we will explore the question of longer time horizons in future posts.

## Table of Contents

## Getting some data

To assess the levels of risk related to changes in the prices of our investments (also called "**price risk**", or "**market risk**"), we need to determine possible values for our investments, as held today, based on past data.

There are a lot of market data providers out there. You may have access to a [Bloomberg Terminal](https://www.bloomberg.com/professional/solution/bloomberg-terminal/), or have a [Refinitiv](https://www.refinitiv.com/en) license, but for our little analysis here, I am going to use the free version of the [Alpha Vantage API](https://www.alphavantage.co/).

To get your own API key, simply claim it by completing [this form](https://www.alphavantage.co/support/#api-key).

To measure our market risk, we are looking to retrieve two years of market prices for the following two symbols:

- <a href="https://markets.ft.com/data/etfs/tearsheet/summary?s=500:PAR:EUR"><span className="text-cgreen">**500.PAR**</span></a> (our current asset); and
- <a href="https://markets.ft.com/data/etfs/tearsheet/summary?s=AHYE:PAR:EUR"><span className="text-cgreen">**AHYE.PAR**</span></a> (our potential new investment).

Most market data provide multiple types of daily prices: Open, High, Low, and Close. We use **Close prices** (also known as "end of day" prices), which is standard practice, as they allow for day-to-day comparisons. Actually, we are going to make use of so-called **Adjusted close prices**, which are Close prices that have been adjusted for dividend payments.

<!-- {
<Finance> -->

A dividend, after being announced, is fully priced within a company's share price. After the <span className="font-bold">ex-dividend date</span>, i.e. the date after which an investor is not eligible for the dividend, the share price corrects <span className="font-bold">downwards</span>, since new investors will not be willing to pay for a dividend they will not be getting.

<!-- <br/><br/> -->

For risk measurement, we will generally assume any dividend is reinvested fully, which means we are not concerned by these price corrections, and that is why we make use of Adjusted Close Prices. <span className="italic">This is an assumption and may not match reality</span>

<!-- </Finance>
} -->

As per Alpha Vantage's documentation, historical price information is available via the [TIME_SERIES_DAILY_ADJUSTED](https://www.alphavantage.co/documentation/#dailyadj) function, with the following example of URL:

```
https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&outputsize=full&apikey=demo
```

Using the `requests` package in Python, we can build this URL for our symbols, and retrieve our data using a "[GET](https://www.w3schools.com/tags/ref_httpmethods.asp)" request, as such:

```python
import requests

API_KEY = ...

def get_price_time_series(symbol: str) -> None:
    response = requests.get(
        url="https://www.alphavantage.co/query",
        params={
            "function": "TIME_SERIES_DAILY_ADJUSTED",
            "symbol": symbol,
            "outputsize": "full",
            "apikey": API_KEY,
        }
    )

    return response.json()
```

Let's try to see what we get back:

```python
>>> sp500_etf = get_price_time_series("500.PAR")

>>> type(sp500_etf)
dict

>>> sp500_etf.keys()
dict_keys(['Meta Data', 'Time Series (Daily)'])

>>> len(sp500_etf["Time Series (Daily)"])
3275

>>> sp500_etf["Time Series (Daily)"].get("2023-06-06")
{'1. open': '76.7749',
 '2. high': '77.3015',
 '3. low': '76.7443',
 '4. close': '77.117',
 '5. adjusted close': '77.117',
 '6. volume': '4106',
 '7. dividend amount': '0.0000',
 '8. split coefficient': '1.0'}

```

The next step will be to take that dictionary, and make it a dataset we can work with. For that, we will use `pandas`.

For an explanation as to why I write `pandas` code this way, check out my previous article: [Some tips when working with Pandas 🐼](/blog/some-tips-when-working-with-pandas/).

```python
import pandas as pd

def make_time_series_dataframe(raw_ts_data):
    return (
        pd.DataFrame(raw_ts_data)

        # Transpose, to have each date on a row
        # rather than a column
        .T

        # Fix the dates, which are in US format, stored as strings
        .assign(
            date=lambda df: pd.to_datetime(
                df.index,
                format="%Y-%m-%d"
            )
        )

        # Fix the prices, stored as string
        .assign(
            adj_close=lambda df: (
                df
                .loc[:, "5. adjusted close"]
                .astype(float)
            )
        )

        .sort_values(by="date", ascending=True)
        .set_index("date")

        # We only keep the last two years of data
        .pipe(lambda df: df.loc[df["date"] >= "20210605"])

        # We limit ourselves to the field we want
        .loc[:, ["adj_close"]]
    )
```

By using this function on our time series data, we get:

```python
>>> df_sp500 = make_time_series_dataframe(sp500_etf["Time Series (Daily)"])
>>> df_sp500.head()

```

<div className="overflow-x-auto">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adj_close</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-06-07</th>
      <td>64.7549</td>
    </tr>
    <tr>
      <th>2021-06-08</th>
      <td>64.8084</td>
    </tr>
    <tr>
      <th>2021-06-09</th>
      <td>65.0239</td>
    </tr>
    <tr>
      <th>2021-06-10</th>
      <td>65.1916</td>
    </tr>
    <tr>
      <th>2021-06-11</th>
      <td>65.5966</td>
    </tr>
  </tbody>
</table>
</div>
<br/>

<!-- {
<Exercise> -->

Try to use this process to obtain the same time series dataframe for our current investment, whose symbol is AHYE.PAR.

<!-- </Exercise>
} -->

## Building our loss sample

We want to compute Value-at-Risk (via Historical Simulations) for two distinct portfolios:

- Our current portfolio ($\mathcal{P}_1$), which holds 15 shares of 500.PAR (and enough cash to buy the new shares); and
- Our potential new portfolio ($\mathcal{P}_2$), which will hold 15 shares of 500.PAR and 5 shares of AHYE.PAR.

Since Value-at-Risk is a measure that represents the level of an unlikely loss, we need to build a sample of possible 1-day losses for these portfolios.

If we write the adjusted close price of an investment $I$ at time $t$ as $P_I(t)$, then the loss experienced over day $t+1$ can be written:

$$
    l_I(t+1) = P_I(t) - P_I(t+1)
$$

_(Note: A negative loss represents a monetary gain)_

Given the number of shares held in our portfolios, we write the possible loss of each portfolio during day $t+1$ as

$$
    \begin{cases}
        l_{\mathcal{P}_1}(t+1) &= 15*l_{500.PAR}(t+1)\\
        l_{\mathcal{P}_2}(t+1) &= 15*l_{500.PAR}(t+1) + 5*l_{AHYE.PAR}(t+1)\\
    \end{cases}
$$

From those formulas, we define all of the possible losses of our portfolio, here implemented in Python:

```python
df_combined = (
    df_sp500_etf

    # We align the prices of 500.PAR and AHYE.PAR
    .merge(
        df_hye_etf, # Built in the same way as df_sp500_etf
        left_index=True,
        right_index=True,
        suffixes=("_500", "_AHYE")
    )

    # We build the losses for each day as P_T - P_{T+1}
    .assign(
        loss_500=lambda df: -df["adj_close_500"].diff(),
        loss_AHYE=lambda df: -df["adj_close_AHYE"].diff()
    )

    # We build the possible portfolio losses
    .assign(
        loss_ptf_1=lambda df: 15*df["loss_500"],
        loss_ptf_2=lambda df: (
            15*df["loss_500"] + 5*df["loss_AHYE"]
        )
    )

    .dropna()
)

>>> df_combined.head()
```

<div className="overflow-x-auto">
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>adj_close_500</th>
      <th>adj_close_AHYE</th>
      <th>loss_500</th>
      <th>loss_AHYE</th>
      <th>loss_ptf_1</th>
      <th>loss_ptf_2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2021-06-09</th>
      <td>65.0239</td>
      <td>244.5550</td>
      <td>-0.2155</td>
      <td>-0.4836</td>
      <td>-3.2325</td>
      <td>-5.6505</td>
    </tr>
    <tr>
      <th>2021-06-10</th>
      <td>65.1916</td>
      <td>244.5256</td>
      <td>-0.1677</td>
      <td>0.0294</td>
      <td>-2.5155</td>
      <td>-2.3685</td>
    </tr>
    <tr>
      <th>2021-06-11</th>
      <td>65.5966</td>
      <td>245.0070</td>
      <td>-0.4050</td>
      <td>-0.4814</td>
      <td>-6.0750</td>
      <td>-8.4820</td>
    </tr>
    <tr>
      <th>2021-06-14</th>
      <td>65.4213</td>
      <td>245.0489</td>
      <td>0.1753</td>
      <td>-0.0419</td>
      <td>2.6295</td>
      <td>2.4200</td>
    </tr>
    <tr>
      <th>2021-06-15</th>
      <td>65.5091</td>
      <td>244.8629</td>
      <td>-0.0878</td>
      <td>0.1860</td>
      <td>-1.3170</td>
      <td>-0.3870</td>
    </tr>
  </tbody>
</table>

</div>

<!-- {
<Note> -->

Here, we have assumed that both calendars are complete, and that joining the two datasets will not create <span className="font-bold">stale prices</span> for either asset.

<!-- <br/> -->

In practice, this should be checked systematically.

<!-- </Note>
} -->

We are now equipped with our loss samples for both $\mathcal{P}_1$ and $\mathcal{P}_2$ (respectively in columns `loss_ptf_1` and `loss_ptf_2`), which means we are ready for our Value-at-Risk calculations!

## Distribution function and Value-at-Risk

Now that we have our loss samples, which we will write as $S_L(\mathcal{P}_1)$ and $S_L(\mathcal{P}_2)$, we can determine our Historical Simulations VaR by ranking each of these losses and finding the highest loss amount so that no more than 1% of the losses in our sample is greater than it.

```python
import math
import numpy as np

sorted_losses_ptf_1 = np.sort(
    df_combined["loss_ptf_1"]
    .to_numpy()
)

n_losses = sorted_losses_ptf_1.size
cutoff = math.ceil(0.99 * n_losses)

>>> n_losses
482

>>> cutoff
478
```

Therefore, our VaR computed by Historical Simulation is the 478th smallest loss in our sample (or 5th greatest loss). We have:

```python
var_ptf_1 = sorted_losses_ptf_1[cutoff]

>>> var_ptf_1
39.639
```

As of June 6th 2023, the 1-day Value-at-Risk of our portfolio $\mathcal{P}_1$, with 99% confidence level (i.e. $\alpha$), is equal to **39.64 EUR**.

The same can be done for $\mathcal{P}_2$, for which we obtain a VaR of **53.69 EUR**.

We can draw the conclusion that the addition of the 5 shares of the AHYE.PAR ETF would add a total of **14.05 EUR** to our VaR.

## Portfolio VaR

When computing the VaR of a portfolio, we will be looking to decompose this VaR into position-level VaR measures, of which there exists multiple kinds:

- The <span className="font-bold text-cgreen">Independent VaR</span>, which is the VaR of the position in a vacuum (i.e. without considering other positions in our portfolio);
- The <span className="font-bold text-cgreen">Incremental VaR</span>, which is the difference between the VaR of the portfolio and the VaR of the hypothetical portfolio where the position has been removed;
- The <span className="font-bold text-cgreen">Marginal VaR</span>, which is the change in portfolio VaR incurred by a "small" change in the size of the position.

The difference in VaR previously calculated is the **Incremental VaR** of the position in AHYE.PAR. Note that, in some cases, the definitions of Incremental VaR and Marginal VaR can be flipped (e.g. MSCI RiskMetrics).

<br/>

<!-- {
<Future> -->

The calculation methodologies for these position-level Value-at-Risk estimates will depend on the type of VaR approach being used. We will dedicate a future post to this specific topic.

<!-- </Future>
} -->

## A variant on the Historical Simulations approach

One of the core assumptions behind the Historical Simulations methodology is that our loss sample $S_L$ is a set of possible loss values for our portfolio, with each value having the same probability of occurring on the next day (i.e. $1/N$, $N$ being the number of elements in $S_L$).

This can be a pretty strong assumption, as one could intuit that data from last month should be more relevant than that of 2 years ago. In fact, many studies have shown that price volatility tends to come clustered, i.e. that there exists periods of high volatility and periods of low volatility. As such, if we currently are in a high-volatility period, we should be looking to minimize the impact of losses that have occurred in low-volatility periods on our VaR estimate.

To achieve this, Boudoukh, Richardson and Whitelaw introduced a hybrid approach in their [1998 paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=51420), which relies on a different scheme to assign probabilities to the loss events in our sample. This approach is generally referred to as **BRW VaR** (after the authors) or **Time-weighted Historical Simulations VaR**.

The crux of the approach is the following:

<blockquote className="flex flex-col">
The more recent the observation, the higher the probability assigned to it. If we compute Value-at-Risk at time $T+1$, and we write $p_t$ as the probability of the loss $l_t$ occurring over the next day, then we have, for any given $t<T+1$:

$$
    p_t = \lambda p_{t-1},\quad \lambda \in ]0,1[
$$

Where $\lambda$ is the <span className="font-bold text-cgreen">decay factor</span> parameter, usually set at a very high value, e.g. 0.99.

</blockquote>

Since probabilities are related to each other using the geometric scheme above, one needs to set the value of the last observation, i.e. $p_{T}$, which will then dictate all of the other values of $p_t$.

Since we still assume that our sample $S_L$ covers all of the possible losses one could observe, it is required that the sum of all $p_t$ is equal to 1.

We are dealing with a [geometric sequence](https://en.wikipedia.org/wiki/Geometric_progression) here, and therefore, the sum of its first $T$ elements is written:

$$
    \sum_{t=1}^{T} p_t = p_{T} \frac{1-\lambda^{T}}{1-\lambda} \quad ( = 1),
$$

which leads to:

$$
    \forall t < T+1, \quad p_t = \lambda^{T-t} \frac{1-\lambda}{1-\lambda^{T}}
$$

Armed with our probabilities and our loss sample $S_L$, the process becomes the following:

- We assign each loss $l_t$ in our loss sample with the probability $p_t$ described above.
- Similar to the Historical Simulations methodology, we rank losses from the smallest to the largest. After sorting, we obtain two sequences:
  - $\{l_{(1)}, ..., l_{(T)}\}$, which are our ranked losses; and
  - $\{p_{(1)}, ..., p_{(T)}\}$, which are the associated probabilities.
- We define VaR as the largest loss $l_{(i)}$ so that the sum of probabilities for losses above it is smaller than $1-\alpha$, in our case 1%.

$$
    \sum_{j>i} p_{(j)} < 1 - \alpha
$$

To do this in Python, we do the following:

```python
# We get the unsorted losses from our dataframe
losses_ptf_1 = df_combined["loss_ptf_1"].to_numpy()

lambda_ = 0.99          # Decay factor
T = losses_ptf_1.size   # Size of sample

ts = np.arange(T) + 1 # 1, 2, ..., T

# Our formula above, applied for all values of t
prob_losses_ptf_1 = (
    (lambda_ ** (T-ts))
    * (1 - lambda_)
    / (1 - lambda_ ** T)
)

# We get the ordering of the losses
ix_sorted_losses_ptf_1 = np.argsort(losses_ptf_1)

# l_(i) and p_(i)
sorted_losses = losses_ptf_1[ix_sorted_losses_ptf_1]
sorted_probs = prob_losses_ptf_1[ix_sorted_losses_ptf_1]

# This is the running sum of probabilities (after sorting)
cum_probs = np.cumsum(sorted_probs)

# VaR is the largest loss so that the total probability
# of observing a larger loss is less than 1 - alpha
ix_var = np.argmax(cum_probs > 0.99)
var_brw = sorted_losses[ix_var_brw]

>>> var_brw
28.1145
```

We note that this VaR is significantly lower than the one we obtained using Historical Simulations, which means that many large 1-day losses occurred relatively far in the past.

## Conclusion

we have gone over the implementation of the Historical Simulation and BRW methodologies for a simple case, starting from the collection of price data. In the next post, we will focus on another major family of approaches to Value-at-Risk, the **Parametric** approaches.

As we introduce more approaches, we will also discuss of the advantages and disadvantages of each of them, in order to make our choice of methodology easier.
