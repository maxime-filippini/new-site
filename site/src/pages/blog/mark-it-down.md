---
title: Mark it down!
emoji:
slug: mark-it-down
publish_date: 2023-02-16
update_date: 2023-02-16
tags: [writing]
image: http://source.unsplash.com/0gkw_9fy0eQ
image_attribution: http://www.unsplash.com/@patrickian4
draft: false
post_summary: "How can Markdown help you for your software documentation and in your day-to-day notetaking."
series: "Unclassified"
---

This is going to be a short post on which I go over the various ways you may want to use [Markdown](https://www.markdownguide.org/) in your work or for your personal note-taking.

## What is Markdown?

Most of us are used to so-called WYSIWYG ("What You See Is What You Get") systems like Microsoft Word, where the styling and formatting is handled by the software and displayed in real time. This is, of course, an attractive feature because our files come with all the formatting necessary, and we are pretty sure it will look the same to anyone else who opens it.

Markdown is a little bit different, as all you need to start writing in it is a basic text editor. To get started, simply create a file ending in `.md`, and write some text in it.

<video src="/images/markdown_nano.webm" autoplay loop/>
    <!-- {
        <Caption>
           You can do that with nano or any other text editor
        </Caption>
    } -->

The syntax of Markdown is simple and generally does not get in the way of your writing. The basics are the following:

- `# {text}` represent headings. The number of `#`s can vary from 1 to 6, with increasing numbers indicating increasingly smaller headings.
- `*{text}*` makes the text italic, while `**{text}**` bolds it.
- `-` creates an unordered list.
- `1.` creates an ordered list.
- `[text](url)` creates a hyperlink labelled "text", which points to "url".
- `![alt text](path)` adds the image located at `path`.
- `{text}` creates an inline code block, where code gets formatted differently.

Most implementations of Markdown also includes the following syntax:

- Code blocks, which are separated by triple backticks, i.e. ```, and add information on the language being used (see the block below).

  `````markdown
  ````python
  print("Hello World!")
  \```
  ````
  `````

  ```

  {
  <Caption>
  The backward slash had to be added for the fenced block to render in its raw form.
  </Caption>
  }

  ```

- Tables, which are not the most convenient to write in a readable way, as we have to align pipes to... well, make it look like a table. But luckily, some tools exist to make it more convenient for us when writing

  ```markdown
  | Header1 | Header2 |
  | ------- | ------- |
  | A       | 1       |
  | B       | 2       |
  ```

So far, we have talked about **writing** Markdown, but what about **reading**? Well, you can choose to either read your files in plain text, which is a decent experience, or to use a Markdown reader, which will apply the necessary formatting on your files. In the next section, I show an example of an editor that can also act as a reader, and that you are most certainly familiar with.

## Why do I like Markdown?

Up to this point, you may be wondering why you should even consider Markdown when you've been used to MS Word and the likes for such a long time.

Here are the aspects of Markdown that I find have improved my workflow:

- Markdown files are portable, since they are plain-text. The content is just there, in a readable format, even without a dedicated reader to apply formatting. This means I can easily transfer my files to my phone, send them to a colleague who may not have access to the MS Office suite, etc.

- Markdown as plain-text usually retains readability

  ```
  ## Is this not readable?

  Although we are looking at a *plain-text* markdown file, it remains **readable** by humans.
  ```

- Writing in Markdown is usually faster, since it is all text, and therefore does not require any mouse action. In addition, you can edit Markdown in any text editor you like, which means you can leverage on shortcuts you've already learned instead of learning new ones (like those you'd need to learn to not use the mouse in MS Word).

  ![Working with Markdown in Visual Studio Code](../../assets/markdown_in_vscode.png)
  <!-- {
  <Caption>
  I use VSCode, which provides syntax highlighting , as well as a formatted preview that is linked to the contents of my file.
  </Caption>
  } -->

<!-- ![](__GHOST_URL__/content/images/2023/02/Screenshot-2023-02-16-at-10.11.42.png) -->

While Ghost provides a WYSISYG editor, it also accepts Markdown --> \_/}

- Markdown is quite popular and large slew of tools exist to help you expand further on the contents of your file. For example [Mermaid](https://mermaid.js.org/) lets you build nice flowcharts programmatically, you can build simple presentations with [Marp](https://marp.app/), and [Obsidian](https://obsidian.md/) lets you build full-blown personal knowledge management systems using Markdown files as back-bone.

If you want to be able to preview your Mermaid charts in VSCode, you will need the preview extension below.

<!-- ![](__GHOST_URL__/content/images/2023/02/Screenshot-2023-02-16-at-21.17.43.png) -->

- The Markdown processors I have used support LaTeX, which is convenient for the work I do.
- I am sure you know how annoying versioning can be in MS Word. Who here has not had to deal with something like `Report_v6.2_vFinal_vFinal_vRev_vFinal.docx` in the past? Well, plain text files can easily be tracked via `git`, which solves that issue.
- Markdown is used in a lot of places. For example, Ghost, the blogging platform I use, can directly take Markdown content and format it. The popular documentation system [MkDocs](https://www.mkdocs.org/) also uses Markdown as a file format.

## Conclusion

I hope that this post will encourage you to explore the possibility of using Markdown for your notes, leveraging on the great versioning capabilities that come with `git`, or the nice charts you can build thanks to Mermaid. Please feel free to share your workflows in the comments!
