---
title: "Unit Tests Are Dead. The Unit Moved."
slug: "ai-unit-tests-unit-moved"
date: "2026-10-26"
subtitle: "Only if you think the unit is a method or a class."
description: "AI can change implementation and its tests together. Learn how to shift code review toward agreed behavior and validate AI-assisted changes with separate checks."
tags:
  - Testing
  - AI Engineering
  - Software Craftsmanship
author: "Mohamed Amine Bchir"
authorUrl: "https://tn.linkedin.com/in/mohamed-amine-bchir"
draft: false
readingTime: 7
seriesTitle: "Unit Tests Are Dead"
seriesOrder: 1
---

You probably asked an AI agent to refactor legacy code. It changed the implementation, rewrote the unit tests, and reported a green build.

You may even have asked it to follow a TDD loop: write a failing test, implement the change, then run the tests. But the same agent chose both the implementation and what the tests should expect, from the same prompt and context, perhaps with the same mistaken assumption. That is feedback, not independent verification.

Then comes the diff: implementation and tests, line by line, file by file. You try to follow it. The PR stalls, or you keep reading past the point where you can tell whether the tests still protect the behavior.

That’s review exhaustion, not confidence: the tests may agree with the code and still fail to protect what users need.

So what should a human review instead?

Not every changed line. Let an AI review agent scan the implementation and report suspicious changes, missed cases, and likely defects. Treat its findings as leads, not certification; it can share the implementation agent’s assumptions. Then review the **spec tests**: a small set of human-readable checks that say what the system must do, in terms a user or business could recognize. They give us a compact place to review the behavior a change proposes. They can change alongside the implementation; when they do, reviewers should judge the changed behavior as a product decision, not treat it as routine test maintenance.

That’s when I started asking: **do the review habits and quality checks we’ve spent years building still fit work generated this way? And if they don’t, how should they evolve?**

We automated the implementation, and we kept the verification rituals built for hand-written implementation. That’s bolting a jet engine onto a horse cart and wondering why the ride feels strange.

So here’s my claim, and I’ll defend it:

**Unit tests aren’t dead because testing died. They’re dead because the unit moved.**

## A test can protect the wrong thing

We used to organize much of our confidence around the small pieces we wrote. Now an agent chooses those pieces for a capability and reshapes them in the next pass. Tests tied to methods and mocks can fail when the design changes; worse, the same agent can write implementation and tests from the same mistaken assumption. A green result can tell us the pieces agree, not that they meet the need.

We built the test pyramid around economics: unit tests were cheap, fast, and easy to diagnose, so we wrote many. AI makes producing tests cheaper. It does not make reviewing rewritten assertions free. The cost has shifted from writing tests to keeping the evidence trustworthy.

There is a token bill, too. People are rightly looking for ways to use fewer tokens, with tools like RTK and Caveman that compress context and reduce output. But we should also ask what those tokens buy. A single method may need normal, boundary, and failure unit tests, each with setup and assertions. If agents generate all of them from the same assumptions as the implementation, we still have to review them without gaining much confidence. When we target 80% to 90% line coverage mainly through unit tests, the test code could plausibly reach 50% to 200% of production code. That is my rough estimate, not a measured benchmark; coverage says what code ran, not whether the tests are good. The question is whether the tests earn their review and maintenance cost.

## What I’m proposing

Not a ban on unit tests, but a change in where confidence rests. Generated implementation is easy to reshape; trustworthy evidence is not. Keep tests tied to behavior, and update them when requirements change. The implementation alone should not force us to rewrite what users need.

Our work shifts with that change. We become spec developers: shaping, challenging, and maintaining the executable descriptions of the behavior we expect, while agents do more of the implementation work. That is not just writing scenarios. It is deciding what matters, what evidence would demonstrate it, and how the specification should evolve when the requirement changes.

Plain language does not make a spec correct. If it says one reservation succeeds when one item is available but says nothing about two customers arriving at once, the implementation has a blind spot: it may pass every written scenario and still oversell inventory. People must decide which concurrent outcomes, edge cases, and invariants are required; an agent can help propose them, but cannot certify its own interpretation.

## Complementary evidence, chosen by risk

The change is not “run more tests” or follow a fixed sequence. These practices answer different questions and complement one another. Choose the evidence that fits the change and its risks.

**Agree on behavior and review the design.** Define what must be true, then inspect the agent’s proposed component boundaries, data ownership, and failure handling before those choices spread through code. A design that exposes a missing requirement should send us back to the spec, not quietly redefine it.

**Test behavior at the relevant boundaries.** Keep focused unit tests for algorithms and invariants, and run spec tests through the real application boundary for capability-level guarantees that should remain meaningful as internals and design evolve. When intended behavior changes, revise the spec tests deliberately. See [spec tests at real application boundaries](../articles/testing-real-service-boundaries.html).

**Check compatibility between services.** Verify API, event, database, and provider assumptions with contract and integration tests; a local mock alone may agree with the same wrong assumption as the implementation. See [contract and integration testing](../articles/contract-and-integration-testing.html).

**Make repeatable quality rules executable.** Build, format, analyze, and enforce the quality and security expectations the repository has made explicit. See [how deterministic quality gates steer AI-generated code](../articles/deterministic-quality-gates-for-ai-code.html).

**Assess operational risk.** A payment or data migration may warrant representative load, failure, compatibility, rollout, and rollback checks. A small isolated change may not. This is not a new checklist: choose evidence by the cost of a missed failure. In the conclusion, [we consider what these checks still cannot prove](../articles/what-our-tests-dont-prove.html).

## Unit tests still matter

“Unit tests are dead” is a provocation, not a deletion command.

A tricky algorithm or security invariant still deserves focused tests. But a simple capability does not need twenty tests guarding private plumbing just because that is what we have always done.

Choose tests by risk. Not by ritual.

The smallest useful unit of confidence is not always a method or class. It is the behavior we agreed to protect.

## The series

1. **Unit Tests Are Dead. The Unit Moved.** (this article)
2. [Spec Tests at the Service Boundary](../articles/testing-real-service-boundaries.html)
3. [Contract Tests for AI-Generated Service Integrations](../articles/contract-and-integration-testing.html)
4. [Deterministic Quality Gates for AI Code](../articles/deterministic-quality-gates-for-ai-code.html)
5. [What Our Tests Don't Prove](../articles/what-our-tests-dont-prove.html)
