---
title: Some tips when working with Pandas
emoji: 🐼
slug: some-tips-when-working-with-pandas
publish_date: 2023-01-21
update_date: 2023-01-22
tags: [python]
draft: false
image: http://source.unsplash.com/0wk7m5SVPsM
image_attribution: https://unsplash.com/@stonewyq
post_summary: "Most Python developers have used the Pandas library. In this post, we go over some best practices and some anti-patterns to avoid."
series: "Python"
---

Most of us working in Python do so because of the powerful set of libraries that have been built for it. One such library I would like to discuss today is the ubiquitous `pandas`.

For the two people who have not heard of `pandas`, it allows you to:

- Read tabular data from a multitude of sources (e.g. csv, Excel, databases);
- Clean up that data;
- Manipulate it to fit your need (e.g. adding columns defined by formulas, grouping and aggregations);
- Display your data as plots; and
- Export your data to any format you would like.

In this post, we are going to discuss some dos and don'ts when working with `pandas`. If any reader wants to dig deeper into these best practices, I recommend the excellent book [Effective Pandas - Patterns for Data Manipulation](https://store.metasnake.com/effective-pandas-book) by Matt Harrison, which was the inspiration for this post.

## The concept of "tidy data"

If you have worked with the [R language](https://www.r-project.org/), chance is you are familiar with the concept of tidy data, since it is the back-bone of the very popular collection of packages: the [tidyverse](https://www.tidyverse.org/).

In a [paper](https://vita.had.co.nz/papers/tidy-data.pdf) published in the Journal of Statistical Software in 2014, Hadley Wickham (creator of the tidyverse) details the main tenets of so-called "tidy data", and the benefits they bring to our data analysis work. The concept of tidy data is language-agnostic, so we can apply it in our work with the `pandas` library.

A table holds **values**, each of which belongs to an **observation** as well as a **variable**. In a given dataset, an observation contains all of the measurements for a given unit across attributes (e.g. a financial instrument), while a variable contains all measurements for the same underlying attribute (e.g. price).

We would consider a dataset "tidy" if the following is true:

- Each **variable** forms a column;
- Each **observation** forms a row; and
- Each type of observational unit forms a table.

But why should we bother having tidy data? Let us consider the example of the data retrieved from the Yahoo Finance API using the following code:

    ```python
    import yfinance as yf

    df_prices = (
        yf
        .Tickers("MSFT AAPL TSLA")
        .download(period="5d")
        .loc[:, "Close"]
    )

    print(df_prices)
    ```

<table border="1" class="dataframe" style="margin:30px auto">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AAPL</th>
      <th>MSFT</th>
      <th>TSLA</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-01-13</th>
      <td>134.76</td>
      <td>239.23</td>
      <td>122.40</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <td>135.94</td>
      <td>240.35</td>
      <td>131.49</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <td>135.21</td>
      <td>235.81</td>
      <td>128.78</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <td>135.27</td>
      <td>231.93</td>
      <td>127.17</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <td>137.87</td>
      <td>240.22</td>
      <td>133.42</td>
    </tr>
  </tbody>
</table>

Now what is wrong with that? Well first of all, the data is poorly labeled, as it is not clear at first glance what type of values are included in this table. To illustrate the second reason as to why there may be issues with this format, let us consider the following exercise:

> We want to compute the price of a portfolio made up of these three stocks, with quantities provided in a separate dataframe `df_quantities`, as shown below.

<table border="1"  style="margin:30px auto">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AAPL</th>
      <th>MSFT</th>
      <th>TSLA</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-01-13</th>
      <td>134.76</td>
      <td>239.23</td>
      <td>122.40</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <td>135.94</td>
      <td>240.35</td>
      <td>131.49</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <td>135.21</td>
      <td>235.81</td>
      <td>128.78</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <td>135.27</td>
      <td>231.93</td>
      <td>127.17</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <td>137.87</td>
      <td>240.22</td>
      <td>133.42</td>
    </tr>
  </tbody>
</table>

One way to do so would be to merge the two dataframes using suffixes...

    ```python
    df_mrg = df_prices.merge(
        df_quantities,
        left_index=True,
        right_index=True,
        suffixes=("_PX", "_QT")
    )

    print(df_mrg)
    ```

<div class="w-full overflow-x-auto">
<table border="1">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>AAPL_px</th>
      <th>MSFT_px</th>
      <th>TSLA_px</th>
      <th>AAPL_qt</th>
      <th>MSFT_qt</th>
      <th>TSLA_qt</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-01-13</th>
      <td>134.76</td>
      <td>239.23</td>
      <td>122.40</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <td>135.94</td>
      <td>240.35</td>
      <td>131.49</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <td>135.21</td>
      <td>235.81</td>
      <td>128.78</td>
      <td>2</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <td>135.27</td>
      <td>231.93</td>
      <td>127.17</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <td>137.87</td>
      <td>240.22</td>
      <td>133.42</td>
      <td>0</td>
      <td>1</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>

... and combine the columns appropriately

    ```python
    df_ptf = pd.DataFrame(
    	index=df_mrg.index,
        data={
            "value": (
                df_mrg["AAPL_PX"] * df_mrg["AAPL_QT"]
                + df_mrg["MSFT_PX"] * df_mrg["MSFT_QT"]
                + df_mrg["TSLA_PX"] * df_mrg["TSLA_QT"]
            )
        }
    )

    print(df_ptf)
    ```

<table border="1" class="dataframe" style="margin:30px auto">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-01-13</th>
      <td>257.16</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <td>507.78</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <td>763.79</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <td>621.54</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <td>507.06</td>
    </tr>
  </tbody>
</table>

But this wouldn't work very well for portfolios made up of other stocks, or that include more than 3 positions. To generalize it, one must think of the process used to build this new value column:

> For each **date/stock** pair, multiply the **quantity** and the **price **to obtain the position value. Then, for each **date**, sum these values to obtain the portfolio value.

Clearly, in this context, the **variables** of our input table are _quantity_ and *price, *while each date/stock pair forms an **observation**. To make the original dataset tidy, we use the `.melt` method:

    ```python
    df_prices_tidy = (
        pd.melt(
            df_prices.reset_index(),
            id_vars=["Date"],
            var_name="stock",
            value_name="price",
        )
        .set_index(["Date", "stock"])
    )

    print(df_prices_tidy)
    ```

<table border="1" class="dataframe" style="margin:30px auto">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>price</th>
    </tr>
    <tr>
      <th>Date</th>
      <th>stock</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-01-13</th>
      <th>AAPL</th>
      <td>134.76</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <th>AAPL</th>
      <td>135.94</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <th>AAPL</th>
      <td>135.21</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <th>AAPL</th>
      <td>135.27</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <th>AAPL</th>
      <td>137.87</td>
    </tr>
    <tr>
      <th>2023-01-13</th>
      <th>MSFT</th>
      <td>239.23</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <th>MSFT</th>
      <td>240.35</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <th>MSFT</th>
      <td>235.81</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <th>MSFT</th>
      <td>231.93</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <th>MSFT</th>
      <td>240.22</td>
    </tr>
    <tr>
      <th>2023-01-13</th>
      <th>TSLA</th>
      <td>122.40</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <th>TSLA</th>
      <td>131.49</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <th>TSLA</th>
      <td>128.78</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <th>TSLA</th>
      <td>127.17</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <th>TSLA</th>
      <td>133.42</td>
    </tr>
  </tbody>
</table>

The same can be done with the table of quantities, and the merge operation now yields:

<table border="1" class="dataframe" style="margin:30px auto">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th></th>
      <th>price</th>
      <th>quantity</th>
    </tr>
    <tr>
      <th>Date</th>
      <th>stock</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-01-13</th>
      <th>AAPL</th>
      <td>134.76</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <th>AAPL</th>
      <td>135.94</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <th>AAPL</th>
      <td>135.21</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <th>AAPL</th>
      <td>135.27</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <th>AAPL</th>
      <td>137.87</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2023-01-13</th>
      <th>MSFT</th>
      <td>239.23</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <th>MSFT</th>
      <td>240.35</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <th>MSFT</th>
      <td>235.81</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <th>MSFT</th>
      <td>231.93</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <th>MSFT</th>
      <td>240.22</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-13</th>
      <th>TSLA</th>
      <td>122.40</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <th>TSLA</th>
      <td>131.49</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <th>TSLA</th>
      <td>128.78</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <th>TSLA</th>
      <td>127.17</td>
      <td>2</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <th>TSLA</th>
      <td>133.42</td>
      <td>2</td>
    </tr>
  </tbody>
</table>

Then, the value can be calculated for each observation, and an aggregation per date can be performed via the `groupby` and `agg` methods.

    ```python
    df_values = (
        df_mrg_tidy

        # We create a new column to store the position values
        .assign(value=lambda df: df["price"] * df["quantity"])

     	# For each date, sum the "value" column and store into "ptf_value"
        .groupby("Date")
        .agg(ptf_value=("value", "sum"))
    )
    ```

<table border="1" class="dataframe" style="margin:30px auto">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>ptf_value</th>
    </tr>
    <tr>
      <th>Date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2023-01-13</th>
      <td>257.16</td>
    </tr>
    <tr>
      <th>2023-01-17</th>
      <td>507.78</td>
    </tr>
    <tr>
      <th>2023-01-18</th>
      <td>763.79</td>
    </tr>
    <tr>
      <th>2023-01-19</th>
      <td>621.54</td>
    </tr>
    <tr>
      <th>2023-01-20</th>
      <td>507.06</td>
    </tr>
  </tbody>
</table>

With tidy data, the data manipulation steps make sense from a semantic point of view. To obtain the portfolio value for each date, we first compute the value of each position at each date, using prices and quantities, and then we aggregate these values via a sum for each date in our table.

But how do we transform data to become tidy? The [paper](https://vita.had.co.nz/papers/tidy-data.pdf) shows the techniques in detail, but mostly, it is about "pivoting" (i.e. moving from a "long" table to a "wide" table) and "melting" (the opposite operation, which we used earlier). In pandas, the methods which can be used are `.pivot`, `.pivot_table`, and `.melt` (which we used above).

## Chaining

If you have worked with `pandas` code before, you may have seen data manipulation procedures that are a tad difficult to read because they are written in a procedural style, assigning values to temporary variables along the way.

Consider our example above. In most code, you may see that procedure written like below:

    ```python
    df_mrg_tidy["value"] = df_mrg_tidy["price"] * df_mrg_tidy["quantity"]
    df_grp = df_mrg_tidy.groupby("Date")
    df_values = df_grp.agg(ptf_value=("value", "sum"))
    ```

Here, we are messing with `df_mrg_tidy` by adding a column that only has value after aggregation as part of `df_values`, which is not something we want.

A better approach is to perform our data manipulation in a single step, starting from a starting dataset and producing the result we need. This style is close to the main tenet of [functional programming](https://en.wikipedia.org/wiki/Functional_programming), which is the lack of [side effects](<https://en.wikipedia.org/wiki/Side_effect_(computer_science)>).

To do so, we use the **chaining** method, which takes advantage of the fact that pandas methods usually return the modified dataframe, which means that further methods can then be called on it. Recall our previous example, which uses the `assign` method to create a column, rather than the `df[col] = ...` pattern used above.

    df_values = (
        df_mrg_tidy

        # We create a new column to store the position values
        .assign(value=lambda df: df["price"] * df["quantity"])

     	# For each date, sum the "value" column and store into "ptf_value"
        .groupby("Date")
        .agg(ptf_value=("value", "sum"))
    )

The flow is now pretty clear: we start from `df_mrg_tidy` to produce `df_values`. The steps to get there are the creation of a new column `value`, and an aggregation of that column via a sum, for each unique value in the `Date` column.

#### Ceci n'est pas une `pipe`

Consider we have access to the following function that parses the date columns of a dataframe for a given format (I have deliberately not written it as a chain so as to avoid confusion).

    ```python
    def parse_date_columns(
    	df: pd.DataFrame,
        columns: list[str],
        format: str
    ) -> pd.DataFrame:
    	df_out = df.copy()

        for col in columns:
        	df_out.loc[:, col] = pd.to_datetime(df_out[col], format=format)

        return df_out
    ```

Applying a function such as this one cannot be done directly when chaining, as... well the following does not quite look like a chain.

    ```python
    df_clean = (
    	parse_date_columns(
        	(
                df_start
                .rename(columns={"Date": "date", "Values": "value"})
                .dropna()
                .assign(squares=lambda df: df["value"] ** 2)
            ),
            columns=["date"],
            format="%Y-%m-%d",
        )
    )
    ```

It naturally becomes more convoluted when multiple functions like this one are involved in our data manipulation process.

To integrate these functions into our data processing chains, we pass them as arguments to the ever-so-handy `.pipe` method. The above code is therefore equivalent to:

    ```python
    df_clean = (
    	df_start
        .rename(columns={"Date": "date", "Values": "value"})
        .dropna()
        .assign(squares=lambda df: df["value"] ** 2)
        .pipe(parse_date_columns, columns=["date"], format="%Y-%m-%d")
    )
    ```

Note that, in some situations, we may want to use `.pipe` even when pandas methods are available to us. Consider the simple example of a simple filtering on rows:

    ```python
    df_filtered = (
    	df_start
        .loc[df_start["value"] > 3]
        .dropna()
    )
    ```

Since we refer to `df_start` in line 3, we cannot easily switch around the order of operations. Indeed, swapping line 3 and 4 will not give the same result if `.dropna()` ends up removing rows, since `df_start` refers to the starting state of our dataframe. I usually like to avoid this situation, to ensure that my pipelines are actually doing what I expect them to do, but also to make them somewhat reusable.

    ```python
    df_filtered = (
    	df_start
        .pipe(lambda df: df.loc[df["value"] > 3])
        .dropna()
    )
    ```

Now, we can flip the operations over and get the same results, and we could hypothetically copy that line 3 and paste it in another pipeline and it would work all the same, as long as a `value` column is present in that new dataframe. An alternative to this would have been the `.query` method, as shown below.

    ```python
    df_filtered = (
    	df_start
        .query("Value > 3")
        .dropna()
    )
    ```

Chaining, overall, allows for cleaner data operations that **read like a recipe**. Indeed, the sequential order makes it much more readable, and ultimately reusable. As shown in one of our previous examples, you can also add comments inside your chain to improve the readability even more.

One last advantage of chaining, is that it makes the dreaded `SettingWithCopyWarning` basically disappear, since we are not modifying existing dataframes on every line of code.

## Take advantage of vectorization

One of the main reasons for the popularity of libraries like `pandas` and `numpy` is the combination of a convenient python API and a powerful calculation engine. However, there are [anti-patterns](https://en.wikipedia.org/wiki/Anti-pattern) when working with `pandas`, some that I have seen time and time over.

First of all, while you can technically loop on `pandas` dataframes via methods such as `.iterrows` and `.itertuples`, it is incompatible with chaining and is overly slow and verbose on top of it. I have yet to find a situation where I would have to resort to using `for` loops on dataframes using these methods, especially given the existence of the `.apply` method.

`.apply` is convenient because it lets you apply python functions to elements in your dataframe, be it rows or individual values, while retaining the ability to use chaining. However, it should be a last resort and specific methods should be preferred, when those exist.

Let us see a simple example, where we try to determine the even numbers from random integers stored in a dataframe.

    ```python
    import timeit

    setup_str = """
    import pandas as pd
    import numpy as np

    df = pd.DataFrame(
        data={
            "value": np.random.random_integers(
                low=0,
                high=5000,
                size=(100_000,)
            )
        }
    )
    """

    with_apply = "df['value'].apply(lambda x: x % 2 == 0)"
    with_method = "df['value'].mod(2) == 0"

    print(timeit.timeit(with_apply, setup=setup_str, number=100))
    print(timeit.timeit(with_method, setup=setup_str, number=100))
    ```

<table style="margin:30px auto">
    <thead>
        <tr>
            <th></th>
            <th>Timing (in seconds)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Using apply</th>
            <td>0.9603517500218004</td>
        </tr>
        <tr>
            <th>Using method</th>
            <td>0.023110125097446144</td>
        </tr>
    </tbody>
</table>

The simple reason for the significantly slower execution of the approach using `.apply` is that the function **loops** over each row of the dataframe. In `pandas`, looping should be a last resort, and it is generally not required.

Let us consider a slightly less contrived example, where we want to create a column based on some criteria. Here, our alternative is `np.select`, which takes a list of arrays of booleans (i.e. True/False) and a list of outputs, and recombines them into a single array.

    ```python
    setup_str = """
    import pandas as pd
    import numpy as np

    def greatest(a, b):
        if a > b:
            return "a"
        elif b > a:
            return "b"
        return None

    df = pd.DataFrame(
        data={
            "a": np.random.random_integers(
                low=0,
                high=5000,
                size=(100_000,)
            ),
            "b": np.random.random_integers(
                low=0,
                high=5000,
                size=(100_000,)
            )
        }
    )
    """

    with_apply = """df.assign(
    	greatest=lambda df_: df_.apply(
        	lambda row: greatest(**row), axis=1))
    """

    with_method = """
    df.assign(
        odd_even=lambda df_: np.select(
            condlist=[
                df_['a'] > df_['b'],
                df_['b'] > df_['a'],
            ],
            choicelist=[
                'a',
                'b',
            ],
            default=None,
        )
    )
    """

    print(timeit.timeit(with_apply, setup=setup_str, number=100))
    print(timeit.timeit(with_method, setup=setup_str, number=100))
    ```

<table style="margin:30px auto">
    <thead>
        <tr>
            <th></th>
            <th>Timing (in seconds)</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <th>Using apply</th>
            <td>38.27637587499339</td>
        </tr>
        <tr>
            <th>Using `np.select`</th>
            <td>0.375061666010879</td>
        </tr>
    </tbody>
</table>

A good question to ask yourself when using `.apply`, is whether there is any other solution that is built around vectors/arrays rather than individual values, as those solutions would in general be more performant. These solutions can either be dataframe methods, or `numpy` functions, like `where` or `select`.

## Some snippets

Here is a couple of real-world snippets of processing pipelines below, which you may find useful.

###### Concatenation of multiple tables stored in .csv files, with some light processing.

    ```python
    from datetime import datetime

    df_loaded = (
    	pd.concat(
        	[
            	(
                    pd.read_csv(
                    	f"./data_{date}.csv",
                       	sep=";",
                        decimal=","
                    )
                    .dropna()
                    .assign(file_date=datetime.strptime(date, "%Y%m%d"))

                )
                for date in ["20220930", "20220831", "20220731"]
            ],
            axis=0
        )

    )
    ```

💡

Loading multiple tables into a single dataframe is faster using `pd.concat` rather than appending.

##### Assignment using a dictionary

What if we want to replace `NaN` values in a certain set of columns while chaining?

    ```python
    df_processed = (
    	df_start
        .pipe(lambda df: df.assign(
        	**{
            	col: df[col].fillna(value=0)
            	for col in ["price", "quantity", "dividend"]
            }
        ))
    )
    ```

Here, we unpack a dictionary which holds the columns to be assigned as keys, and the processed pandas series as values. This is necessary because the columns are defined programmatically.

If you are not aware of what dictionary unpacking does, it transforms the dictionary into keyword arguments when the function is executed. For example, `f(**{"a": 2, "b": 3})` becomes `f(a=2, b=3)`.

##### Apply functions on groups

Previously, I have mentioned that the `.apply` method should be avoided. One exception is when applied right after a `.groupby` operation. Indeed, after grouping, using `.apply` allows you to apply a function that takes a dataframe as an input and returns a dataframe to each group, which is of great use for chaining.

See the example below, where we wish to transform the `value` column into a percentage for each given `date`.

    ```python
    df_processed = (
    	df_start
        .groupby("date", group_keys=False)
        .apply(
        	lambda df: df.assign(pct=df["value"] / df["value"].sum())
        )
    )
    ```

Note that this could have been solved differently using a `merge`

    ```python
    df_processed = (
    	df_start
        .pipe(
            lambda df: df.merge(
                (
                    df_start
                    .groupby("date")
                    .agg(total=("value", "sum"))
                    .reset_index()
                ),
                on="date"
            )
        )
        .assign(pct=lambda df: df["value"] / df["total"])
    	.drop(columns=["total"])
    )
    ```

##### Debugging chains

One thing you may wonder is how do we go about debugging chains. One simple way of doing so is to implement your own diagnostic function, to call with `.pipe` along your process.

    ```python
    def show(df):
    	print(df.head())
        return df

    df_debug = (
        df_mrg_tidy

        # We create a new column to store the position values
        .assign(value=lambda df: df["price"] * df["quantity"])

        # Useful for debug
        .show()

     	# For each date, sum the "value" column and store into "ptf_value"
        .groupby("Date")
        .agg(ptf_value=("value", "sum"))
    )
    ```

## Conclusion

I hope you have found those tips useful, and that you will be able to implement them in your processing pipelines. This is of course only scratching the surface, and I would recommend you to read Matt Harrison's book.

As with everything, practice makes perfect, so I encourage you to build pipelines, and look at them critically in light of the elements mentioned.

Stay tuned for more!
