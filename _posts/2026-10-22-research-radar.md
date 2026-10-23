---
title: "Cache Engineering for Agents: letting LLM agents manage their own KV cache"
date: 2026-10-22
excerpt: "Agents directly control their KV cache with drop and reposition operations, avoiding costly re-prefill while retaining more useful context."
tags:
  - paper-dive
  - kv-cache
  - llm-agents
  - inference-efficiency
header:
  teaser: radar/2026-10-22-card.png
  image: radar/2026-10-22-card.png
lang: en
translated_url: /blog/2026-10-22-research-radar-ko/
---

[EN](/blog/2026-10-22-research-radar/) · [한국어](/blog/2026-10-22-research-radar-ko/)

*Agents can directly drop and reposition entries in their KV cache — no text rewriting, no re-prefill — improving both accuracy and cost over conventional context summarization.*

## The problem

LLM agents tackle complex tasks by building up long trajectories of reasoning steps, tool calls, and observations. Each new step conditions on the full history via the key-value (KV) cache — the data structure that stores previous tokens' representations so the model doesn't recompute them from scratch.

As trajectories grow, the KV cache becomes expensive. According to the paper, KV cache reads account for 82.4% of total API cost in their agent workload analysis. Beyond cost, when the number of cached states or their positional range exceeds what the LLM handles reliably, task accuracy degrades.

The standard fix is *context engineering*: trim or summarize older messages to shrink the context. But editing any earlier part of the trajectory invalidates all KV states computed after that point. The serving system must re-prefill — recompute — the retained suffix, and the earlier the edit, the more recomputation is needed.

In practice, agent harnesses defer context reduction until a threshold is hit, then aggressively cut most history, keeping only a few recent rounds. This creates a dilemma: retain too much and pay for re-prefill, retain too little and lose information the agent needs.

On the BrowseComp-Plus benchmark with GPT-OSS-120B, summary-based context engineering at a 48K-token threshold reduced cost by about 7% but dropped accuracy by 5 percentage points compared to full-context inference.

## The core idea

Cache engineering flips the approach. Instead of editing the *text* of the trajectory and recomputing downstream cache, the agent edits the *cache itself* — marking certain KV entries as invisible to future attention — while leaving the text trajectory untouched.

Here is an analogy (mine, not the authors'): imagine you're in a long meeting with detailed minutes being kept. Context engineering is like going back and crossing out paragraphs in the minutes, then asking everyone to re-read from the edit point to get back on track. Cache engineering is more like putting on selective noise-canceling headphones: the minutes stay intact, but you stop listening to certain earlier speakers. Everyone's prior responses still carry traces of what those speakers said — they just no longer get direct attention going forward.

This matters because retained KV states can still carry information from dropped history, since they were originally computed with attention to it. The paper cites prior work (Xiao et al., 2024; Fu et al., 2026; Zou et al., 2025) supporting this residual-information property. Dropping a cache entry is less destructive than deleting the text that produced it.

The paper introduces three cache operations — **append**, **drop**, and **repos** (reposition) — and co-designs a serving engine called **AKV** that makes this scheme practical.

## How it works

### The three cache operations

**Append** is the standard operation: process a new token, compute its KV entry conditioned on the active cache, and concatenate it to the cache. Every LLM serving system already does this.

**Drop** removes selected KV entries from future attention. It does *not* change retained entries' states or position encodings, and it does *not* modify the logical token sequence. The text history stays the same; only the cache visible to subsequent attention shrinks.

**Repos** (reposition) updates the position encodings stored in cached keys. After dropping entries, position indices can have gaps or grow large enough to hit the model's context limit even though the actual cache is small. Repos compacts them: with $$ r $$ entries remaining, their position indices become 0 through $$ r-1 $$, and the next appended token uses index $$ r $$. For models using Rotary Position Embeddings (RoPE), this is achieved by rotating cached keys without recomputing hidden states.

### The history dependence problem

With standard KV caching, the token prefix fully determines the cache state — if two requests share the same token prefix, they share the same cache. Cache engineering breaks this property.

An analogy (mine, not the authors'): think of two chefs following the same recipe with the same final ingredient list, but one added salt before sautéing the onions while the other added it after. The final dishes share the same ingredients on paper, but taste different because the salt changed how earlier steps proceeded. Similarly, two trajectories can retain the same tokens at the same positions, yet have different cache states because drop and append operations occurred in different orders.

The paper illustrates this concretely (see Figure 5 in the paper): three trajectories all retain tokens B and C. In trajectory 1, C is computed while A is still in the cache. In trajectory 2, A is dropped before C is appended. In trajectory 3, B is computed without A entirely. C's KV states differ in all three cases because the attention context during C's computation differed.

Prefix matching — the standard technique for cache reuse in serving systems — is therefore no longer sufficient.

### The AKV serving engine

AKV follows a principle the authors call *stateless interface, stateful serving*. The agent submits requests in a familiar format — a messages array plus an optional cache field specifying drop and repos operations — without tracking what the server has physically cached. The server handles all the complexity internally.

AKV addresses three challenges:

**Correct reuse** via an extended radix tree. Standard radix trees index cache by token prefix. AKV inserts *drop nodes* at points where drop operations occur, branching the tree so that trajectories with different operation histories maintain distinct cache states.

**Safe eviction** with drop-awareness. When a request drops a cache entry, other requests sharing the same prefix might still need it. AKV frees physical storage only when no ongoing request needs the entry, and prioritizes evicting dropped cache over cache from completed requests (which is more likely to be reused in the next round).

**Efficient restoration** via segment-batch attention. When evicted cache must be restored, AKV reconstructs it in a single forward pass by splitting queries at operation boundaries. Each segment attends causally to its own tokens and to active cache from earlier segments, respecting the history of drops and repositions. Only attention is segmented; the FFN processes the full sequence as one batch, avoiding redundant weight reads.

## The math

The drop operation on the active cache is defined as:

$$\operatorname{drop}(P): \quad \mathcal{C} \leftarrow \mathcal{C} \setminus \{C_i : i \in P\}$$

Here $$ \mathcal{C} $$ is the active cache — the ordered set of KV entries available to future attention. $$ P $$ is the set of logical token indices selected for removal. $$ C_i $$ is the cache entry for the token at index $$ i $$. The backslash ($$ \setminus $$) denotes set removal: take the active cache and discard every entry whose index is in $$ P $$, preserving the order of what remains. After this operation, subsequent tokens cannot attend to the dropped entries, but the dropped entries' influence persists indirectly in retained entries that were computed while those entries were still active.

The repos operation adjusts position encodings via RoPE rotation:

$$K \leftarrow R(q) \, R(p)^{-1} \, K$$

$$ K $$ is a cached key vector. $$ p $$ is its current position encoding index. $$ q $$ is the target position index. $$ R(p) $$ is the RoPE rotation matrix at position $$ p $$ — the matrix that encodes positional information into keys during the original computation. $$ R(p)^{-1} $$ undoes the original rotation, and $$ R(q) $$ applies the new one. The whole expression moves the key from position $$ p $$ to position $$ q $$ without recomputing the hidden state that produced it. Cached values remain unchanged since RoPE applies only to keys and queries, not values.

## Results

The authors evaluate across three LLMs — MiniMax-M2.7 (230B total, 10B active parameters), GPT-OSS-120B (5.1B active), and MiroThinker-1.7-Mini (30B total, 3B active) — on four benchmarks: BrowseComp-Plus (deep research), GAIA-Text (general QA), SWE-bench Verified (software engineering), and xbench-DeepSearch-2510 (deep search).

**Accuracy.** AKV's tool-response rolling-drop policy (retaining the 12 most recent tool responses' KV) improves the average benchmark score by 1.7 points over the Standard baseline and by 0.9 to 8.7 points over Text Engineering, depending on the model. Gains are most pronounced on longer trajectories: on BrowseComp-Plus with GPT-OSS-120B, AKV scores 61.9% versus Standard's 57.5% and Text Engineering's 52.7%.

**Cost.** AKV reduces average per-task cost by 27.7% relative to Standard and 21.9% relative to Text Engineering, across all models and benchmarks. For GPT-OSS-120B specifically, the average per-task cost drops from 11.2 cents (Standard) to 7.3 cents (AKV).

**Serving efficiency.** On the top-80 SWE-bench Verified tasks with GPT-OSS-120B, AKV at concurrency 14 achieves a 1.51x speedup in P95 request latency over Standard at its peak concurrency of 12 (28.49s vs 43.16s). Output throughput reaches 369 tokens/s versus Standard's 313 tokens/s (1.18x), and input throughput is 1.53x higher. The advantage widens at higher concurrency as KV-cache pressure increases Standard's re-prefill work.

**Ablations.** Tool-response drop with repos achieves the highest pass rates. On BrowseComp-Plus with GPT-OSS-120B, adding repos raises pass rate from 55% to 62%, allowing exploration beyond the position limit. Dropping reasoning cache hurts more than dropping tool-response cache — consistent with the attention analysis showing older tool responses receive less attention than assistant messages at comparable positions.

**Recursive self-improvement (RSI).** Using MiniMax-M2.7 to refine cache policies on 20 BrowseComp-Plus tasks, then evaluating on 100 held-out tasks, RSI iterations 3 and 6 reduce per-task cost by 15.6% and 17.8% over Standard while maintaining accuracy.

**Cache-as-tool.** Exposing cache operations as agent tools allows the agent to proactively decide when and what to drop. On a 100-task BrowseComp-Plus subset, this achieves the highest pass rates: 61.0% for GPT-OSS-120B and 64.0% for MiniMax-M2.7.

## Limitations & what's not covered

The authors identify three directions as future work: further exploration of cache engineering strategies, training agents under this scheme (current experiments use inference-time policies only), and extending serving support to linear attention models, which use different state representations than standard KV caches.

This explainer focuses on the core mechanism and benchmark results. The paper includes detailed serving implementation specifics (segment-batch attention internals, reposition-aware radix tree matching rules, the full API grammar), cost accounting methodology, and per-layer attention-pattern analyses — see Appendices A.1 through A.4 in the paper for those details.

## Why it matters

Cache engineering reframes a systems problem — KV cache management — as an agent-level decision, giving models direct control over what they attend to without the destructive rewrite-and-recompute cycle of context engineering. In my view, the idea that agents should manage their own memory at the cache level, not just the text level, is a natural and likely durable shift in how we build long-horizon agent infrastructure.

## Source

Tianyu Fu, Ruoxi Wang, Zihan Min, Zhongqi Ren, Zhihao Li, Tengxuan Liu, Shengxu Mu, Hanling Zhang, Yu Wang. *Cache Engineering for Agents.* arXiv:2610.28577, October 2026. [Paper link](https://arxiv.org/abs/2610.28577). Code: [https://github.com/thu-nics/AKV](https://github.com/thu-nics/AKV).
