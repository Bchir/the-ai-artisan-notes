---
title: "Spec Tests at the Service Boundary"
slug: "testing-real-service-boundaries"
date: "2026-10-27"
description: "Spec tests capture agreed service behavior in readable scenarios and run against the real application boundary, with examples and tooling across languages."
tags:
  - Testing
  - Software Architecture
  - AI Engineering
author: "Mohamed Amine Bchir"
authorUrl: "https://tn.linkedin.com/in/mohamed-amine-bchir"
draft: false
readingTime: 6
seriesTitle: "Unit Tests Are Dead"
seriesOrder: 2
---

Readable, executable scenarios for expected behavior are not new. I’ll call them **spec tests** here: BDD-style, black-box component tests. BDD describes how behavior is expressed using Gherkin and tools such as Reqnroll, while component testing describes what is tested and at which boundary. A spec test typically targets one microservice through its public boundary, using real internal dependencies where their behavior matters. It is not an end-to-end (E2E) test of a complete business journey across multiple services. Make spec tests primary evidence for capability-level behavior, while keeping focused unit tests for algorithms and invariants.

Imagine an agent is asked to add reservations. Before debating classes or methods, agree on the behavior: a customer can reserve available stock, an over-capacity request is rejected without changing inventory, and two customers competing for the last unit cannot both succeed. Make the specification, not the implementation, the first artifact.

Those promises can be written as readable, executable scenarios:

```gherkin
@inventory
Feature: Reserving available inventory

  Rule: A reservation cannot exceed available stock

    @hot_path
    Scenario: Reserve fewer units than are available
      Given a product has 2 units available
      When a customer reserves 1 unit
      Then the reservation is accepted
      And the available inventory is 1 unit

    @edge_case @expected_failure
    Scenario Outline: Reject a reservation above available inventory
      Given a product has <available> units available
      When a customer attempts to reserve <requested> units
      Then the request is rejected
      And the available inventory remains <available> units

      Examples:
        | available | requested |
        | 2         | 3         |
        | 1         | 2         |

    @edge_case
    Scenario: Reserve the exact available quantity
      Given a product has 2 units available
      When a customer reserves 2 units
      Then the reservation is accepted
      And the available inventory is 0 units

    @edge_case @concurrency
    Scenario: Two customers compete for the last unit
      Given a product has 1 unit available
      When two customers concurrently attempt to reserve 1 unit
      Then exactly one reservation is accepted
      And the other reservation is rejected
      And the available inventory is 0 units
```

Use the same BDD framework for component and E2E specifications. In .NET, Reqnroll can run scenarios written in Gherkin, but neither tool is a requirement. This approach is not specific to .NET: Cucumber supports languages including Java, JavaScript, and Ruby; Behave and pytest-bdd are options in Python; and godog brings Gherkin scenarios to Go. Choose the framework that fits the stack; the useful property is that people can review the promise and the test runner can execute it.

The tags classify the evidence: `@hot_path` marks the ordinary flow, `@edge_case` marks boundary conditions, `@expected_failure` marks rejected requests, and `@concurrency` identifies the race-condition check. They can help a team filter runs and see which kinds of behavior the suite covers. Reqnroll can map tags to test categories ([Gherkin reference](https://docs.reqnroll.net/latest/gherkin/gherkin-reference.html), [executing specific scenarios](https://docs.reqnroll.net/latest/execution/executing-specific-scenarios.html)).

The workflow is simple: **Requirement → Runnable spec-test changes → Review → Implementation → Run spec tests.** This is a practical application of specification-driven development, not a new SDD method: before coding, compare the requirement with existing specs, identify impacted scenarios, and propose new or updated ones. Review that expected behavior with stakeholders, then implement against the agreed tests. Especially with AI, writing tests after implementation risks validating the agent’s interpretation instead of the behavior people intended.

## Run the spec through the service

Run each scenario as a real caller would: through HTTP, a message endpoint, or another supported application boundary. For the rejection case, prepare a product with two units, send a request for three, check that the service rejects it, and verify that inventory remains at two. If the promise includes publishing an event, inspect it through a test broker or an observable outbox. A mock that verifies a method call does not prove the event was delivered or persisted.

Concurrency must be exercised, not just mentioned in a scenario: coordinate the two requests so they overlap, then verify both responses and the persisted inventory. Sequential requests would not expose the race. If the spec omits this guarantee, a passing suite leaves a black hole where the implementation can oversell.

Treat the service as a black box. Assert public behavior and relevant durable effects, not private class names, SQL text, or call order. The implementation can then change without making the capability or the spec that describes it meaningless.

To run scenarios against a separately hosted service, start the service and relevant dependencies as an environment before the test run. Aspire or Docker Compose can define and orchestrate it:

![An executable spec test exercises a real service in an orchestrated environment with dependencies and diagnostics.](../assets/Spec-test.png)

Use real dependencies when their behavior matters to the guarantee, such as a database, broker, or Redis. Use controlled mock servers for external systems that are not the subject of the scenario. The goal is not to recreate all of production; it is to exercise the capability across the boundary the spec claims to protect.

## Make failures diagnosable

Boundary tests have often been hard to work with: a bespoke harness could be fragile, and a failure might not reveal whether the problem was in the service, database, broker, or an external dependency. Unit tests are cheaper to run and give more localized feedback, which is why teams often favored them.

Orchestration tools such as Aspire and Docker Compose make it easier to start the service and dependencies together, wait for readiness, and exercise the running service as a black box. When a scenario fails, OpenTelemetry logs, metrics, and traces give the agent evidence to investigate, potentially through an MCP server. The same diagnostic path can help an SRE investigate an incident; in development, it can help an agent investigate a failing spec.

## A bonus: context for the next spec

The readable suite can also help an agent shape future work. If it already describes stock limits, retry behavior, and authorization, an agent asked to add bulk reservations can read those scenarios first. They show existing guarantees and help surface gaps or conflicts before the new behavior is proposed.

The agent can get that context from the feature files without tracing the implementation. Unlike a separate design document that may be superseded without being archived, the scenarios are executable checks the team expects to pass against the service. They are not correct or complete by themselves; people still need to decide whether the proposed behavior is intended.

The suite records the behavior we agreed to protect; it cannot prove that we agreed on the right or complete behavior. Keep scenarios focused, free of implementation details, and runnable with isolated test data. And when mock servers stand in for external services, how do we know their assumptions match the real services? That is the question for [contract testing across service boundaries](../articles/contract-and-integration-testing.html).

## The series

1. [Unit Tests Are Dead. The Unit Moved.](../articles/ai-unit-tests-unit-moved.html)
2. **Spec Tests at the Service Boundary** (this article)
3. [Contract Tests for AI-Generated Service Integrations](../articles/contract-and-integration-testing.html)
4. [Deterministic Quality Gates for AI Code](../articles/deterministic-quality-gates-for-ai-code.html)
5. [What Our Tests Don't Prove](../articles/what-our-tests-dont-prove.html)
