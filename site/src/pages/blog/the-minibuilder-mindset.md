---
title: Embracing the Minibuilder mindset
emoji:
slug: embracing-the-minibuilder-mindset
tags: [mindset]
publish_date: 2022-09-26T21:07:11.000Z
update_date: 2022-10-02T14:57:32.000Z
image: http://source.unsplash.com/XJXWbfSo2f0
image_attribution: http://www.unsplash.com
draft: false
post_summary: "Software is a tool that helps us build other tools. The Minibuilder mindset is an essential part of building software pragmatically. Here is what it is all about."
series: "Unclassified"
---

Hi there 👋,

Welcome to the blog! I will be starting off easy with this first post, which will serve as an introduction to a concept that is near and dear to my heart: **_Minibuilding_**.

When I say "_Minibuilding_", I refer to the act of building small-scale software tools to help us in our job. Underlying this concept is the idea of taking ownership of processes and striving to deliver additional value, using software as a leverage.

Of course, this is going to be applicable to some professions more than it is to others, but this should be particularly relevant to anyone doing a job that makes extensive use of software-based tools.

I have worked in the financial industry for the last six years, in positions that very much relied on software-based solutions. During that time, I have grown to embrace the Minibuilder mindset, continually improving the work performed by myself and my colleagues, and after some time, the people I supervised, through technical innovation and automation.

To illustrate how Minibuilding can work for you, I will start by relating it to the idea of responsibility and ownership, then move on to concrete examples, and finally provide some ideas of what is to come for future posts.

## Minibuilding and mindset

Consider the following situation:

> You get onboarded on a recurring task that has to be performed monthly. This task deals with ingesting data stored as Excel file, enriching it using external data sources, transforming it and feeding that transformed data into a calculation engine that spits out an output.
>
> This task is largely automated, thanks to an in-house solution developed 5 years ago by someone who since left the company.
>
> Since then, the format of the Excel files have changed slightly, and new calculations need to be performed following a change in requirements.

There are two ways to look at this situation.

1. "**I accept these tasks and the work being asked of me**".
   This is a passive mindset, where all responsibility for the way the work is performed, its efficiency, its impact on morale, is delegated to your manager.

2. "**I accept the responsibility for these tasks**, and I take ownership of the work ahead\*".
   This is an active mindset. You know you will gain a deep understanding of the tasks given to you, and through that, you will be the person who is most able to plan, improve, and extend the work.

While the choice of approach is ultimately up to the individual and the way they perceive work, I believe there are many reasons why the second approach is preferrable.

First and foremost, it is paramount to understand that, along with any assignment, comes **trust**. The trust that the process has been carried out in such a way that its output is most certainly correct.

**But what would happen if an issue occured in our process described above? **

If you are in the passive mindset, you will most likely raise the issue to your manager, mention that the procedure and the tools do not work in this specific situation, maybe format it nicely in an email. This type of action does not really provide any solution to the problem experienced.

A person who accepts the responsibility of their tasks will most likely:

- Diagnose the issue at hand;
- Based on the type of issue, brainstorm a solution and determine the possible best course of action;
- If the solution is a simple patch (e.g. data override), they may carry it out and mention it at the time of the delivery of the output;
- If the solution is more involved, they may provide an action plan to their manager before continuing.

This sense of ownership, coupled with the continuous lowering of the barrier to entry to work with building software is what empowers us to become "Minibuilders".

The example above presents two clear opportunities for improvement:

- We can build a data transformation pipeline that will transform the Excel files and save those transformed files to disk for ingestion by the main tool;
- We can build a calculation pipeline that will ingest the output of the main tool, and enrich it with the required extra calculations.

These two things would be relatively simple to set up using Python thanks to the `pandas` package, or even in Visual Basic for Applications (i.e. "VBA") for those who would feel so inclined. Some steps that do not require file manipulations could even be implemented via Excel formulas, whose power has largely been unlocked thanks to the introduction of [dynamic array formulas](https://support.microsoft.com/en-us/office/dynamic-array-formulas-and-spilled-array-behavior-205c6b06-03ba-4151-89a1-87a7eb36e531).

What would the benefits be in automating these tasks? Well, most of all, you are making an investment. An investment in your own professional excellence. First, you are saving time, which means that, in the next months, you will be able to spend this time on other tasks, which will present new learning opportunities. Second, you are reducing operational risks, which will unavoidably lead to better quality outputs, and make you more trustworthy as a result. Finally, you honed your programming skills, something that will pay dividends in the future.

This basically covers my introduction to the "owner" mindset and how it relates to software development carried out by non-IT professionals.

## What can you expect from future posts?

In future posts, I will write about the various tools and framework that could help a minibuilder on their journey, as well as provide insights on how managers can fully benefit from empowering their colleagues to take ownership and embrace the Minibuilder mindset.

For those folks with whom this first post resonated, and anyone interested in software-related topics, here are some topics that I plan to cover in the following weeks and months:

- A **whole lot of Python** content. Indeed, I believe that Python has become THE language of the minibuilder, being high-level enough to make the developer experience a joy, and having all of these wonderful libraries that allow us to build specific and performant applications and tools.
- **Productivity tips**. When we talk about being a minibuilder, we talk about pushing ourselves to grow, to make an investment in ourself and our work, instead of doing the bare minimum that is asked of us. This requires adequate time and task management.
- **Projects walk-throughs**. It is no secret, for one to learn, one has to make. To illustrate the suite of tools and techniques at the disposal of the minibuilder, I will be putting them to use in sample projects, with step-by-step explanations.
- **Musings** on programming languages, features, existing tools, etc.

If there are specific things you would like to see covered, please feel free to leave them as comment on this post!

See you on the other side!
