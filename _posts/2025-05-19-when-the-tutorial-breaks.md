---
layout: post
title: "When the Tutorial Breaks, Keep Building Anyway"
date: 2025-05-19
categories: [lab diary, ad lab, troubleshooting]
tags: [Active Directory, VirtualBox, netplan, chatgpt, rebuild, ubuntu, yaml]
---

Today I hit a wall.

The plan was simple: boot the VMs, follow the tutorial, and bring AD Lab 1.0 online. But everything broke the second I tried to follow it. The VirtualBox UI was different. Ubuntu's netplan config had changed. The internet was dead. The commands shown in the video? Outdated or outright missing. 

> This tutorial is only a year old — and parts of it are already unusable.

I checked the comments:  
- “Thanks! Worked first try.”  
- “Super helpful!”  
- “Got it up and running in no time!”

And I couldn’t help but wonder…  
**Did these people actually build the lab, or just watch the video and click 'like'?**

Because what I went through wasn’t that.

---

## The Real Breakpoint

The tutorial designs the lab as a **fully isolated network** — no internet access by default.

Great for realism. Terrible for practicality.

If you don’t *plan ahead* to allow temporary external access:
- You can’t download updates  
- You can’t install tools (like Splunk Forwarder)  
- And when you finally realize it... it’s **too late to patch anything**  
- You’re rebuilding the entire VM from scratch

And that's exactly what happened.

---

## How I Fought Back

Instead of quitting, I did what any tired but stubborn cyber student would do:

> **I invoked the power of ChatGPT.**

I dumped YAML files into it. I asked it to explain deprecated syntax. I walked through network configs line by line — and it helped me keep going when nothing made sense.

Then, after everything was “correct” —  
> I stared at a broken CLI output for over an hour.

The config looked fine. The commands were clean. The logic checked out.  
And then… I saw it:  
> I had misspelled the interface name.  
> Twice.

That’s what learning in this field looks like sometimes: debugging typos while barely awake at 2AM.

---

## What I Actually Did

- Rebuilt the entire lab from scratch  
- Modified VirtualBox to use a NAT adapter alongside internal ones  
- Verified connectivity for updates before isolating the network  
- Used ChatGPT to troubleshoot netplan and CLI errors  
- Documented every config change that diverged from the video  

---

## What I Learned

You can't treat tutorials like gospel.  
You have to *understand* the logic.  
You have to break things, fix them, break them again, and **document the chaos**.

And most of all:  
> **Hackers don’t sleep. And neither do students who want to catch up.**

---

**Written by Steven Loucks — cybersecurity student, veteran, and lab builder**
