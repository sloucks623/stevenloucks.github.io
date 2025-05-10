---
layout: post
title: "Markdown, CSS, and AI: Building My GitHub Portfolio from Scratch"
date: 2025-05-10
---

When I started building my personal cybersecurity portfolio, I had no coding background. None. What I *did* have was motivation, curiosity, and access to free tools — GitHub, Jekyll, and a powerful assistant named ChatGPT. That’s how [stevenloucks.tech](https://stevenloucks.tech) was born.

But it wasn’t easy. It still isn’t. This post is a breakdown of the tools I’ve been learning — Markdown, CSS, Liquid, and more — and the real journey of making it all work (and sometimes break) with a lot of help from AI.

---

## Markdown (`.md`): My Starting Point

Markdown is a plain-text writing format that turns into HTML when the site is built. It’s how I write blog posts like this, document labs, and structure content for my GitHub Pages site.

It’s beginner-friendly, but that doesn’t mean I didn’t mess it up repeatedly. I’d forget headers, miss brackets on links, or leave off front matter — and wonder why the page wouldn’t render.

---

## CSS (`.css`): Making It Not Look Like 1999

CSS handles all the styling — fonts, colors, banners, buttons, cards, shadows. If Markdown is the skeleton, CSS is the wardrobe and makeup.

I wanted a clean, modern look with bold visuals, so I:
- Created section headers with angled mustard-orange banners
- Styled lab projects as floating cards with hover effects
- Customized buttons and fonts for a tech-forward aesthetic

Getting that styling to cooperate across browsers (or even devices) was **way harder** than I expected.

---

## The Frustration of Broken Links and Image Files

One of the most painful parts was chasing down broken things — especially image icons. Half the time it was something like:

- I used `.jpg` instead of `.png`
- A file was in the wrong folder
- The file name had a capital letter, and GitHub is case-sensitive
- The path worked locally but broke on GitHub Pages

I would spend **hours** trying to fix a badge icon that just wouldn’t show up, only to find I’d written `SecurityPlus.JPG` instead of `securityplus.png`.

---

## What Else I Had to Learn (Still Learning...)

### HTML  
I didn’t plan to write HTML, but I had to. Jekyll mixes Markdown with embedded HTML. Now I can write a basic layout, link to sections, and even customize div structures.

### YAML (`.yml`)  
This one surprised me. YAML is used for structured data in Jekyll. I store my certifications and lab metadata in `_data/certifications.yml`, which lets me reuse content across the site.

### Liquid  
Liquid is Jekyll’s templating language — I still don’t fully understand it, but I’ve figured out how to loop through YAML files and conditionally render content like my lab cards and Credly badges.

### Git and Branching  
Branching and merging repositories is still a work in progress. I’ve created protected branches like `stable-v1` and `working-copy`, and I’m learning to test changes without breaking my live site. It’s not always graceful, but I’m getting there.

---

## AI Was My Secret Weapon

I built this site in partnership with **AI (ChatGPT)**. Without it, I would’ve been lost. I asked questions like:
- “Why isn’t my badge showing?”
- “Write me a collapsible grid in HTML.”
- “Make this blog look better.”

Sometimes I didn’t even know the *right question* — just pasted my broken code and asked for help. And every time, the response helped me move forward.

But let’s be honest: **AI didn’t build the site for me**. I still had to learn it. I still had to:
- Rebuild sections I broke
- Copy and paste code a hundred times
- Manually fix filenames and file paths
- Choose a theme, then customize it line-by-line

Using AI wasn’t a shortcut. It was a **learning partner** — and a lifeline during late nights of trial-and-error.

---

## Still Not Done — But Proud of What’s Here

The truth is, my site still isn’t exactly how I want it. I’m still:
- Tweaking the layout
- Refining colors and fonts
- Fixing things that look off on mobile
- Reorganizing labs and blog sections

But I’m proud of how far it’s come. It started as a blank GitHub repo, and now it’s a working portfolio at [stevenloucks.tech](https://stevenloucks.tech), with working links, real projects, custom styling, and growing content.

---

## If You’re Just Starting Out

Here’s what I’ve learned:
- **Start with Markdown** — it’s easy, and powerful.
- **Don’t fear CSS** — small changes make big visual impacts.
- **You will break things** — that’s normal.
- **Use AI smartly** — it’s a teacher, not a crutch.
- **Track your progress** — you’ll be amazed at how much you learn.

Thanks for reading. If you're also trying to build a portfolio, feel free to reach out or follow along — I'm still figuring it out too.
