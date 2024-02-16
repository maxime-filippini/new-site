---
title: "Efficient rolling windows operations in Numpy"
emoji: ⏮️
slug: efficient-rolling-windows-ops-in-numpy
publish_date: 2023-06-08
update_date: 2023-06-08
tags: [python]
image: "/images/np-strided.png"
image_attribution: ""
draft: false
post_summary: "In this first byte-sized post, we talk about how you should and should NOT perform rolling windows operations in the Numpy library."
series: Bytesized
---

Say you have an array of $N$ elements for which you would like to compute two things:

- A rolling window sum, with a window size $W < N$; and
- A block sum, splitting the array every $B < N$ elements.

We have all seen pieces of code that look like this:

```python
import numpy as np
import math

N = 500
W = 20
B = 50

# A simple array considered for testing
arr = np.arange(N)

# My first rolling window sum
rolling_window_sum = np.zeros((N - W + 1, ))

for i in np.arange(N - W + 1):
    rolling_window_sum[i] = np.sum(arr[i:i+W])

# My first block sum
n_blocks = math.floor(N / B)
block_sum = np.zeros((n_blocks, ))

for i in np.arange(n_blocks):
    block_sum[i] = np.sum(arr[i*B:(i+1)*B])

```

What is the issue with this?

As you may know, Numpy uses C under the hood to manipulate arrays, whose underlying data are stored in contiguous [memory buffers](https://en.wikipedia.org/wiki/Data_buffer) (more on that later). This means that one should try to use methods built into Numpy when possible, and not rely on pure Python loops.

<!-- {
<Advice> -->

Never use pure Python loops when dealing with Numpy arrays. Python being much slower than C at anything, writing any kind of pure Python loop when dealing with a highly optimized library like Numpy is generally a bad idea.

<!-- </Advice>
} -->

Fortunately, there exists a very nice way to deal with these very common operations. We are going to delve into a numpy feature that may not be known to most: **stride tricks**.

## Numpy stride tricks

When we initialize an array, it has to be stored somewhere in memory. In general (that includes Python and C), the items of an array are stored in a contiguous block of memory (at least as far as our program is concerned). In Python, our Numpy arrays simply represent **views** on those memory blocks.

As is shown below, if we take a slice off an array, the memory gets shared between both arrays, and no copy is created.

```python
>>> arr = np.arange(50)
>>> arr_copy = arr[10:20]

>>> np.shares_memory(arr, arr_copy)
True
```

In addition, Numpy arrays have a single type, which means each item in the array takes the same size in memory:

```python
>>> arr.dtype
dtype('int64')

>>> arr.strides
(8,)
```

Since we are dealing with an array 64-bit integers, we need to step 8 bytes (or 64 bits) to move from one element to the next (as shown by the `strides` property).

What if we could create our own views of our array to perform our rolling window/block sum operations? This is possible, using the `stride_tricks` library.

Here's a very simple example:

```python
from numpy.lib.stride_tricks import as_strided

strided_arr = as_strided(
    arr,
    shape=(2,),
    strides=(arr.strides[0],)
)

>>> strided_arr
array([0, 1])

>>> np.shares_memory(arr, strided_arr)
True

```

What happened there?

- `arr` is the array we want to build a view on;
- The `shape` argument tells Numpy what shape do we want to have for our resulting array;
- The `strides` argument tells numpy how many bytes it has to move on the memory block to build the next item in our resulting array, on each axis. It should be read like the following:

{
<Info>
Every two successive items on the first axis of <code>strided_arr</code> are <code>arr.strides[0]</code> bytes from each other in memory, in the block where the elements of <code>arr</code> are stored.
</Info>
}

## Vectorized operations

To perform our rolling window sum operation, let us create a view on `arr`, adding a second axis to store each window. We are telling Numpy here that moving along either axis in the resulting array is like moving along the only axis in the original array (i.e. by 8 bytes).

```python
N = 500
W = 20
B = 50

arr = np.arange(500)

rolling_window_stride = as_strided(
    arr,
    shape=(N - W + 1, W),
    strides=(arr.strides[0], arr.strides[0]),
)

>>> rolling_window_stride
array([[  0,   1,   2, ...,  17,  18,  19],
       [  1,   2,   3, ...,  18,  19,  20],
       [  2,   3,   4, ...,  19,  20,  21],
       ...,
       [478, 479, 480, ..., 495, 496, 497],
       [479, 480, 481, ..., 496, 497, 498],
       [480, 481, 482, ..., 497, 498, 499]])

>>> np.shares_memory(arr, rolling_window_stride)
True
```

To compute our sum, we use the vectorized `sum` method provided by Numpy, to which we specify that we want to sum on the second axis.

```python
rolling_window_sum = rolling_window_stride.sum(axis=1)

>>> rolling_window_sum[:5]
array([190, 210, 230, 250, 270])
```

Next, to perform the block sum, we define a different shape and strides. Here, each element on the first axis of the resulting array are actually separated by $8*B$ bytes in memory, $B$ being the number of element in each block.

```python
n_blocks = math.floor(N / B)

block_stride = as_strided(
    arr,
    shape=(n_blocks, B),
    strides=(arr.strides[0]*B, arr.strides[0]),
)

>>> np.shares_memory(arr, block_stride)
True

block_sum = block_stride.sum(axis=1)

>>> block_sum[:5]
array([ 1225,  3725,  6225,  8725, 11225])
```

This technique can be generalized to more complex case, like the one described below (experienced in the wild)

<!-- {
<Exercise> -->

You need to compute the maximum volatility of the returns on an asset over a 2 years horizon. You want to perform this calculation on a rolling window, based on 5 years of data. The volatility is to be estimated using a 20-day rolling window.

<!-- <br/><br/> -->

To do so, you need to stride the 1-D array into a 3-D array, one axis for the calculation date, one for the 2-year window of returns, and one for the 20-day windows for the volatility calculations.

<!-- </Exercise>
} -->

<!-- {
<Note> -->

Be very careful when using the <code>as_strided</code> method. Using it incorrectly could cause you to point to invalid memory and crash your program/corrupt results. Please always use the strides of the original array in the <code>strides</code> argument.

<!-- </Note>
} -->

## References

Here are two useful links:

- [1] [The documentation page for the `as_strided` function](https://numpy.org/doc/stable/reference/generated/numpy.lib.stride_tricks.as_strided.html); and
- [2] [A great blog post showing the extent to which it can be used](https://towardsdatascience.com/advanced-numpy-master-stride-tricks-with-25-illustrated-exercises-923a9393ab20).
