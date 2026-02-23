# Software Requirements Specification
## For To-Do List

Version 0.1  
Prepared by Osvaldo, Jake, Kyle  
Spring CS-2450, Utah Valley University
02/22/2026

## Table of Contents
<!-- TOC -->
* [1. Introduction](#1-introduction)
    * [1.1 Document Purpose](#11-document-purpose)
    * [1.2 Product Scope](#12-product-scope)
    * [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
    * [1.4 References](#14-references)
    * [1.5 Document Overview](#15-document-overview)
* [2. Product Overview](#2-product-overview)
    * [2.1 Product Perspective](#21-product-perspective)
    * [2.2 Product Functions](#22-product-functions)
    * [2.3 Product Constraints](#23-product-constraints)
    * [2.4 User Characteristics](#24-user-characteristics)
    * [2.5 Assumptions and Dependencies](#25-assumptions-and-dependencies)
    * [2.6 Apportioning of Requirements](#26-apportioning-of-requirements)
* [3. Requirements](#3-requirements)
    * [3.1 External Interfaces](#31-external-interfaces)
    * [3.2 Functional](#32-functional)
    * [3.3 Quality of Service](#33-quality-of-service)
    * [3.4 Compliance](#34-compliance)
    * [3.5 Design and Implementation](#35-design-and-implementation)
    * [3.6 AI/ML](#36-aiml)
* [4. Verification](#4-verification)
* [5. Appendixes](#5-appendixes)
<!-- TOC -->

## Revision History

| Name | Date | Reason For Changes | Version |
|------|------|--------------------|---------|
|      |      |                    |         |
|      |      |                    |         |

## 1. Introduction
  This Software Requirements Specification (SRS) defines the requirements for the To-Do List System designed for local college students. The purpose of this document is described in Section 1.1 (Document Purpose) and establishes this SRS as the formal agreement between stakeholders and developers regarding system functionality and constraints. The overall scope and objectives of the To-Do List System are summarized in Section 1.2 (Product Scope). This document is intended for developers, project managers, testers, and stakeholders who require a clear understanding of system requirements. Relevant terminology and references are provided in Section 1.3 (Definitions, Acronyms, and Abbreviations) and Section 1.4 (References).

The remainder of this document is organized as follows:

- Section 2 (Product Overview) provides a high-level description of the system.
- Section 3 (Requirements) details the system’s functional and non-functional requirements.
- Section 4 (Verification) describes how requirements will be validated.
- Section 5 (Appendixes) contains supporting and supplementary information.

A more detailed explanation of the document structure is provided in Section 1.5 (Document Overview).

### 1.1 Document Purpose
  This Software Requirements Specification (SRS) defines the requirements for a web-based To-Do List System designed for local college students. The system provides a centralized, internet-accessible platform that enables students to create, manage, prioritize, and track academic and personal tasks.

  The purpose of this document is to clearly specify the system’s functional and non-functional requirements. It ensures a shared understanding of system objectives, expected behavior, and constraints among all stakeholders.

  The primary audiences for this document include product managers, software engineers, quality assurance (QA) teams, security and compliance reviewers, and operations personnel. Throughout the software development lifecycle, this SRS serves as a formal reference for design, implementation, testing, validation, deployment, and maintenance. It may be used in conjunction with related documents such as the project vision and scope statement, system architecture documentation, development roadmap, and contractual agreements.

### 1.2 Product Scope
💬 _Defines the software product’s purpose, boundaries, and relationship to business goals._

➥ Identify the product by name and version/release. In 3–5 sentences, describe its primary purpose, key capabilities, and intended outcomes. Clearly list inclusions and exclusions when this SRS covers part of a larger system. Focus on the “what” and “why.”

💡 Tips:
- Connect capabilities to business objectives and reference a separate vision/scope document if relevant.
- Include a simple diagram if it clarifies boundaries within a larger system.

### 1.3 Definitions, Acronyms, and Abbreviations
➥ Help readers understand specialized terms and notation by providing a glossary of domain terms, acronyms, and abbreviations used in the SRS.

💡 Tips:
- Include terms that impact interpretation of requirements (e.g., “user,” “tenant,” “near real-time”).
- Keep entries alphabetized and consistent across the document set.

| Term | Definition                                                                                                                   |
|------|------------------------------------------------------------------------------------------------------------------------------|
| API  | Application Programming Interface - A set of definitions and protocols for building and integrating application software     |
| SRS  | Software Requirements Specification - A document that describes the intended purpose, requirements, and nature of a software |
| UI   | User Interface - The visual part of computer application through which a user interacts with a software                      |

### 1.4 References
💬 _Lists external sources that are normative or informative for this SRS._

➥ Cite standards, contracts, policies, interface specs, UX style guides, use-case docs, architectural decisions, or a vision/scope document. For each reference, include title, author/owner, version, date, and location/URL. Indicate whether each reference is normative (binding) or informative (guidance).

💡 Tips:
- Prefer stable links or repository paths over volatile URLs.

### 1.5 Document Overview
💬 _Brief guide to the structure of the SRS so readers can quickly find what they need._

➥ Summarize what each major section covers (Product Overview, Requirements, Verification, Appendixes), note any document conventions, and mention how updates and revision history are managed.

💡 Tips:
- Keep to 3–5 sentences focusing on navigation and conventions.

## 2. Product Overview
College students frequently manage assignments across multiple platforms, including learning management systems, email, physical planners, and messaging applications. This fragmentation increases the risk of missed deadlines and academic stress.

The To-Do List System is designed to provide a centralized, web-based task management platform that consolidates academic and personal responsibilities into a single focus point. The system’s requirements are influenced by the high workload variability in academic environments, limited student time, and the need for mobile accessibility.

### 2.1 Product Perspective
💬 _Places the product within a larger ecosystem or lineage._

➥ Describe context and origin of the product, whether this is a new product, replacement, or member of a family. If part of a larger system, briefly explain relationships, external interfaces, and key dependencies. Include details on ownership, service level agreements (SLAs), and support models.

💡 Tips:
- Highlight upstream/downstream systems and ownership boundaries.
- A high-level context diagram may help to orient the reader.

### 2.2 Product Functions
The Task Manager is designed to organize, track, and manage tasks based on the following areas.
-Task creation: Users can create new tasks with a title, description, due date, and priority level.
-Task options: Users can delete, read, update, and complete tasks.
- Advanced options: Users can perform bulk actions, undo actions, add notes and files, and oragnize tasks/subtasks by several categories.
- Dashboard: Users can access a homepage displaying urgent tasks, visual analytics, and task completion.
- Data portability: CSV files can be imported and exported to populate data or keep a copy.

[UML Diagram](UML.pdf)

💡 Tips:
- 5–10 bullets are often sufficient at this level, grouping related functions logically.
- Include a top-level data flow or use case diagram if helpful.

### 2.3 Product Constraints
- The MVP must operate on a Python CLI using data from the local file tasks.json.
- To support collaboration functions across devices, local JSON storage must migrate to a central database.
- The system should restrict file size (including attachments) to 10MB to control database management and high transfer speeds.
- The UI must implement standard web design principles to be utilized across multiple browsers and screen sizes.

➥ Describe constraints such as mandated interfaces, technology stacks, regulatory obligations, QoS baselines, hardware limitations, AI/ML model families, and organizational policies.

💡 Tips:
- State constraints as verifiable "must" statements (e.g., “must use FIPS 140–3 validated crypto modules”).
- Distinguish external/internal and mandatory/preferred constraints.
- Avoid design decisions unless truly binding.

📝 Note:
Requirements (Section 3) defines verifiable system obligations—specific behaviors or qualities the system shall exhibit in order to satisfy limits described in this section.

### 2.4 User Characteristics
💬 _Defines the user groups and the attributes that affect requirements._

➥ Identify user classes, roles, and personas, noting expertise, access levels, frequency of use, accessibility needs, and goals.

💡 Tips:
- Define user classes by behavior, not just titles.
- Note localization and accessibility considerations that affect UI/UX requirements.

### 2.5 Assumptions and Dependencies
#### 2.5.1 Assumptions
Users will import tasks via a CSV file formatted to the standardized template of the application.
Time sensitive analytics like due dates and progress bars assume the users date and time settings are accurate.

### 2.5.2 Dependencies
For the MVP, the application depends on local file permissions to tasks.json.

### 2.6 Apportioning of Requirements
💬 _Allocation of requirements across components or increments._

➥ Map major requirements to subsystems, services, or releases/iterations. Use a cross-reference table to show allocation and to clearly identify deferred requirements.

💡 Tips:
- Note unknown allocations explicitly and track as follow-ups.

## 3. Requirements
💬 _This section specifies **verifiable** requirements of the software product to enable design and testing._

➥ State requirements to a level of detail sufficient for design and verification. Use unique identifiers, consistent keywords (shall/should/may), and clear conditions. Describe inputs, processing in response, and outputs where applicable. Reference the relevant 2.3 Product Constraints that the requirement addresses.

📃 Template (applies to **all** requirements):
```markdown
- ID: REQ-FUNC-001
- Title: Short title, representative of the requirement...
- Statement: The system shall...
- Rationale: ...
- Acceptance Criteria: ...
- Verification Method: Test | Analysis | Inspection | Demonstration | Other
- More Information: Additional context. Links to related artifacts.
```

Requirement ID schema and traceability:
- ID format: REQ-[AREA]-[NNN]-[VER] (optional -[VER] if versioned), where AREA ∈ {FUNC, INT, PERF, SEC, REL, AVAIL, OBS, COMP, INST, BUILD, DIST, MAINT, REUSE, PORT, COST, DEAD, POC, CM, ML}.
- Uniqueness: IDs must be unique and immutable; changes increment -[VER] and are recorded in Revision History.
- Traceability: Each test artifact may reference the requirement ID.

💡 Tips:
- Make each requirement testable and unambiguous, using standard metrics and avoiding vague terms (e.g., “user-friendly,” “fast”).

### 3.1 External Interfaces
💬 _Specifies all external inputs and outputs, covering both required and provided interfaces._

➥ Provide interface definitions sufficient for implementation and test.

💡 Tips:
- Use interface control documents or schemas where appropriate and reference them here.

#### 3.1.1 User Interfaces
💬 _Describes how users interact with the system at a logical level._

➥ Define UI elements, flows, and standards to be followed (style guides, accessibility guidelines). Include layout constraints, common controls (e.g., help, search), keyboard shortcuts, error/empty-state behavior, and localization. Keep visual designs in a separate UI specification and reference them.

- ID: REQ-INT-001
- Title: Web-based responsive UI
- Statement: The website will be able to be used with common web browsers 
- Rationale: We want anyone to be able to use our website no matter what web browser they use
- Acceptance Criteria: Website loads on firefox, safari, internet explorer, google chrome
- Verification Method: Inspection
- More Information:

- ID: REQ-INT-002
- Title: Intuitive homepage
- Statement: The website will have a basic homepage where it is easy to understand what is going on and what everything means
- Rationale: If people don't understand how the homepage works, they won't be able to get to any other pages
- Acceptance Criteria: Visually looks nice and every button is simple and intuitive
- Verification Method: Inspection
- More Information:

- ID: REQ-INT-003
- Title: Simple add task page
- Statement: The website will have an add task page with simple variables that will add tasks to your database
- Rationale: Having tasks is the whole point of this project, and if we can't add tasks, it defeats the whole point of the website.
- Acceptance Criteria: Visually looks nice and is simple and understandable
- Verification Method: Inspection
- More Information:


💡 Tips:
- Reference accessibility standards (e.g., WCAG) and platform-specific guidelines.
- Consider organizing into subcategories for clarity: Usability/Accessibility (inputs/outputs and dialogs to fit user abstractions, abilities, and expectations), and Convenience.

#### 3.1.2 Hardware Interfaces
💬 _Details interactions with physical devices and platforms._

➥ Specify (un)supported device types, data/control signals, electrical or mechanical characteristics if relevant, and communication protocols. Include timing, throughput, and reliability expectations.
- ID: REQ-INT-004
- Title: Supports desktops/laptops and mobile devices with keyboards or touch input
- Statement: The website will be able to read input inputted by either a keyboard or mouse and display to both desktops and mobile devices
- Rationale: We want our website to be convenient; if we don't have our website available on mobile it will be hard to see, add or complete tasks from anywhere outside of the office
- Acceptance Criteria: Accepts inputs and properly displays to mobile
- Verification Method: Inspection
- More Information: 
💡 Tips:
- Reference applicable hardware specs and certification requirements.

#### 3.1.3 Software Interfaces
💬 _Defines integrations with other software components and services._
- ID: REQ-INT-005
- Title: Saving data to be able to reload if the website ever crashes.
- Statement: The website will save data to a database, making it so that it will be able to load the data from the previous time opened
- Rationale: We don't want tasks to disappear randomly
- Acceptance Criteria: Saves data and is able to load data on start up
- Verification Method: Test | Inspection
- More Information:
➥ List connected systems (name and version), required or provided services/APIs, data items/messages exchanged, communication styles/protocols, and limit/error/timeout semantics. Identify shared data and ownership.

💡 Tips:
- Capture versioning and backward compatibility policies.
- Define authentication/authorization expectations for each integration.

### 3.2 Functional
💬 _Specifies the externally observable behaviors and functions the software shall provide._

➥ Organize functional requirements by feature, use case, or service. For each, describe triggers/inputs, processing/logic (at a black-box level), outputs, and error conditions. For AI behaviors, define determinism bounds (e.g., temperature), refusal criteria, safety rules, and human review points.

- ID: REQ-FUNC-001
- Title: Loads tasks that were added based on the user who logs in
- Statement: The website will load the proper tasks based on the user that is logged in
- Rationale: We need to display the right tasks for the proper user.
- Acceptance Criteria: Loads different data based off of different users
- Verification Method: Test
- More Information:

- ID: REQ-FUNC-002
- Title: Create task
- Statement: The website will be able to create new tasks with all of the required requirements for a task.
- Rationale: We need tasks to be able to populate our website
- Acceptance Criteria: tasks are created and added to our database
- Verification Method: Test
- More Information:

- ID: REQ-FUNC-003
- Title: Edit tasks
- Statement: Once a task is created, you will be able to edit it to change any and all variables on the task.
- Rationale: Sometimes the task changes. We want to be able to change the info so that it matches what is actually needed.
- Acceptance Criteria: Once a task is changed, it will have different variables
- Verification Method: Test
- More Information:

- ID: REQ-FUNC-004
- Title: filter display
- Statement: The website can be filtered based on variables in the tasks. 
- Rationale: We want to be able to simplify our tasks so that it is a little simpler and easier to see specific tasks
- Acceptance Criteria: Changes the display of tasks
- Verification Method: Inspection
- More Information:

- ID: REQ-FUNC-005
- Title: Sort display
- Statement: The Website will be able to sort and display the tasks based on certain varaibles
- Rationale: This will help make it easier to decide what task you need to work on
- Acceptance Criteria: Changes the order of the tasks that are displayed.
- Verification Method: Inspection
- More Information:

- ID: REQ-FUNC-006
- Title: Mark task complete
- Statement: The website will be able to mark a task as completed, and will then hide the task unless prompted to show completed tasks.
- Rationale: Once a task is done we need to be able to mark it as completed
- Acceptance Criteria: Checks that it is completed and then hides
- Verification Method: Test | Inspection
- More Information:

- ID: REQ-FUNC-007
- Title: Delete task
- Statement: The website will be able to remove tasks
- Rationale: Sometimes tasks don't get finished but are no longer needed
- Acceptance Criteria: Task is removed from the database
- Verification Method: Test | Inspection
- More Information:
💡 Tips:
- Include edge cases and negative scenarios for completeness.
- For AI features, include fallback behaviors and thresholds for abstention.

### 3.3 Quality of Service
💬 _Quality attributes that constrain or qualify functional behavior._

➥ Use specific metrics, ranges, and conditions.

💡 Tips:
- When a quality applies only to a subset of functions, reference the related requirement IDs.
- Provide rationale when targets cut across functions to aid trade-off decisions.

#### 3.3.1 Performance
💬 _Response time, throughput, and resource usage expectations._
- ID: REQ-PERF-001
- Title: Website loads fast
- Statement: The website will load in a timely manner(< 15 Seconds)
- Rationale: We don't want our task manager website to take too much time to load
- Acceptance Criteria: Loads quickly enough
- Verification Method: Test | Inspection
- More Information:

➥ Specify timing relationships, peak/steady-state loads, and performance targets under expected conditions. Include measurement methods, environments, and acceptance thresholds. Note any real-time constraints.

💡 Tips:
- Include scalability targets and capacity planning assumptions.
- Consider organizing into subcategories for clarity: Time (latency, throughput, etc.) and Space (memory, storage, bandwidth, etc.).

#### 3.3.2 Security
💬 _Defines the protection of data, identities, and operations._
- ID: REQ-SEC-001
- Title: The passwords are secure
- Statement: The passwords will either be hashed or outsourced to a to a service that securely stores passwords
- Rationale: We don't want our clients passwords to be leaked
- Acceptance Criteria: Passwords are hashed
- Verification Method: Inspection
- More Information:

- ID: REQ-SEC-002
- Title: Task privacy
- Statement: The website will make sure that you are only able to view and edit tasks that you are supposed to be able to
- Rationale: We want people to view other people's tasks
- Acceptance Criteria: Can only see tasks for which you have permissions.
- Verification Method: Inspection
- More Information:
➥ Define authentication, authorization, data protection (in transit/at rest), auditing, and privacy requirements. Address abuse/misuse and external attacks (e.g., injection, data exfiltration, or service compromise), and include secure defaults and incident response requirements.

💡 Tips:
- Distinguish mandatory controls vs. recommended practices.
- Consider organizing into subcategories for clarity: Safety (harmful external outcomes), Confidentiality (disclose data to unauthorized parties), Privacy (private data disclosed without consent), Integrity (data modified without authorization), and Availability (authorized data or resources made available when requested).

📝 Note:
Place generic security controls here (3.3.2), and cross-reference from supported controls as necessary:
- Use 3.1 External Interfaces for interface-level validation and secure protocols.
- Use 3.4 Compliance for regulatory/contractual obligations and audit evidence.
- Use 3.6 AI/ML for model-specific runtime protections and data governance.

#### 3.3.3 Reliability
💬 _Ability to consistently perform as specified._
- ID: REQ-REL-001
- Title: Data is saved
- Statement: The website will save data to our database, so that in case of a crash, it will be able to load previous tasks.
- Rationale: We want to be able to have all of the previous tasks reload if the service is ever shut down.
- Acceptance Criteria: On server shutdown, the tasks can be reloaded after
- Verification Method: Inspection
- More Information:
➥ Specify reliability metrics and techniques (e.g., MTBF, error budgets, retry/backoff, idempotency, redundancy). Define conditions under which reliability is assessed and any failover behaviors. Define graceful degradation (e.g., fallback components, cached results, AI/ML deterministic heuristics), timeout/abstain policies, and rollback to previous versions.

#### 3.3.4 Availability
💬 _System uptime and readiness to deliver service._

➥ Define availability targets, maintenance windows, and mechanisms like checkpointing, recovery, and restart. Include geographical/zone redundancy if applicable.
- ID: REQ-AVAIL-001
- Title: The server will have an uptime of 90%
- Statement: The website will be available 90% of the time while we are testing it.
- Rationale: We want our clients to be able to use our website at almost anytime of the day
- Acceptance Criteria: Measured monthly, the website is available 90%
- Verification Method: Inspection
- More Information:
💡 Tips:
- Express availability in terms meaningful to users (e.g., downtime per month) and tie to SLAs/SLOs.
- Capture scale-out/in behavior affecting availability (e.g., max failover time, quorum constraints).

#### 3.3.5 Observability
💬 _Ability to understand system state and behavior in production through telemetry._
- ID: REQ-OBS-001
- Title: Error handling
- Statement: The website will be able to give out errors when stuff goes wrong
- Rationale: We want to have errors in case anything goes wrong.
- Acceptance Criteria: If anything crashes, it gives an error.
- Verification Method: Inspection
- More Information:
➥ Define requirements for logs, metrics, traces, and profiling: events/fields, cardinality limits, sampling, retention, and privacy/PII handling in telemetry. Specify standard labels (e.g., service, version, tenant), correlation/trace IDs propagation, and redaction policies. State SLO-aligned alert rules, dashboards, and ownership.

💡 Tips:
- Avoid maintenance-process details (keep runbooks and on-call policies in 3.5.4 Maintainability).

### 3.4 Compliance
💬 _Requirements derived to satisfy external standards, regulations, or contracts._

➥ Specify mandated formats, naming conventions, accounting procedures, provider/user rights and agreements, licensing agreements, audit tracing, records retention, and reporting. For each compliance item, reference 2.3 Product Constraints if applicable, or cite the authoritative source directly.

### 3.5 Design and Implementation
💬 _Constraints or mandates affecting how the solution is designed, deployed, and maintained._

#### 3.5.1 Installation
💬 _Ensures the software runs smoothly in its target environments._

➥ Define (un)supported platforms/environments, prerequisites, installation methods, environment configuration (e.g., env vars, secrets), and rollback/uninstall procedures.

💡 Tips:
- Detail automation expectations (e.g., IaC, installer scripts, container images).
- Keep scaling mechanics (topology, multi-region) in 3.5.3 Distribution; keep scaling targets in 3.3 QoS.

#### 3.5.2 Build and Delivery
💬 _Defines the controls for building, packaging, and delivering software artifacts to ensure integrity, traceability, and reproducibility._

➥ Define how source code is transformed into deployable artifacts and moved through environments. Describe expectations for build reproducibility, dependency management, licensing, configuration management, artifact verification, and release promotion.

💡 Tips:
- Cross-reference 3.5.1 Installation and 3.5.10 Change Management for environment setup, versioning, and release traceability.
- Avoid operational topology details (those belong in 3.5.3 Distribution).

#### 3.5.3 Distribution
💬 _Addresses geographically or organizationally distributed deployments, data, and devices._

➥ Specify deployment topologies, component and data distribution/replication approaches and scale-out runbooks, and constraints imposed by organizational or network structure.

#### 3.5.4 Maintainability
💬 _Attributes that make the software easier to modify, fix, and evolve._

➥ Define expectations for modularity, code complexity, interfaces, coding standards, developer oriented observability, documentation, software delivery performance, and technical debt management.

#### 3.5.5 Reusability
💬 _Encourages leveraging components across products or contexts when appropriate._

➥ Identify components intended for reuse and any constraints on their dependencies or technology choices. Specify modularization, API stability, packaging, and documentation to enable reuse.

#### 3.5.6 Portability
💬 _Ability to run on multiple platforms or environments with minimal changes._

➥ Specify (un)supported operating systems, hardware architectures, cloud providers, or container runtimes. Define abstraction layers, configuration policies, and externalization of environment-specific settings.

#### 3.5.7 Cost
💬 _Financial considerations or cost targets._

➥ State budgetary limits, cost-per-transaction targets, licensing constraints, or cloud spend envelopes that influence design decisions.

💡 Tips:
- Keep costs high-level unless contractually defined.
- Link to a cost model or TCO assumptions where available.
- Note variable vs. fixed cost expectations impacting scaling strategies.

#### 3.5.8 Deadline
💬 _Schedule expectations that affect scope and prioritization._

➥ Specify key milestones, delivery dates, or phases/increments. Indicate dependencies between milestones and required readiness criteria.

💡 Tips:
- Use deadlines to guide apportioning of requirements (Section 2.6).

#### 3.5.9 Proof of Concept
💬 _Validates feasibility and de-risks critical assumptions before full-scale delivery._

➥ Define the objectives, scope, success criteria, and timebox for any POCs. Describe what will be validated (technical, usability, performance) and how results will influence requirements or design.

💡 Tips:
- Keep POCs narrowly focused and measurable. Focus on validation goals, not implementation details.

#### 3.5.10 Change Management
💬 _Controls how changes are introduced and communicated._

➥ Define change categories (breaking, additive, bugfix), approval workflow, and required artifacts (changelogs, evaluation summaries, migration guides, release notes). Specify backward/forward compatibility guarantees, client communication plans, deprecation timelines, and rollout/rollback procedures.

### 3.6 AI/ML
💬 _This section defines requirements unique to systems incorporating machine learning or data-driven components at their core. These requirements complement functional, quality, and design aspects in preceding sections but address ML-specific lifecycle, data, and ethical considerations._

#### 3.6.1 Model Specification
💬 _Defines what each model is intended to do and the measurable criteria for acceptable performance._

➥ Describe model(s) purpose, scope, expected behavior, key inputs and outputs, and measurable performance objectives. Note any validation datasets, benchmarks, or versioning practices used to ensure reproducibility.

💡 Tips:
- Distinguish baseline targets from aspirational improvements and define acceptable tolerance for drift.

#### 3.6.2 Data Management
💬 _Ensures integrity, traceability, and ethical lifecycle of data used in model training, validation, and operation._

➥ Specify dataset origin, ownership, consent conditions; labeling processes and quality controls; data lineage, versioning, and reproducibility (training → validation → inference); storage, access controls, and anonymization/pseudonymization standards; handling of missing, synthetic, or augmented data.

#### 3.6.3 Guardrails
💬 _Ensure that the AI system operates safely, predictably, and within approved boundaries._

➥ Specify how the system validates inputs, filters or constrains outputs, and limits available actions to prevent harm, misuse, or unintended consequences. Include mechanisms to detect and respond to malicious inputs or unsafe operational conditions.

💡 Tips:
- Treat “guardrails” across input, output, and action layers.
- Define escalation, logging, and rollback procedures when safety constraints are triggered.
- Cross-reference 3.3.2 Security for system-level protections and 3.6.4 Ethics for normative expectations.

#### 3.6.4 Ethics
💬 _Addresses fairness, transparency, and accountability in model behavior and outcomes._

➥ Define how ethical considerations will be identified, measured, and managed throughout development and operation. Include fairness objectives, explainability expectations, and documentation or review requirements.

💡 Tips:
- Use fairness metrics appropriate to context (e.g., demographic parity, equal opportunity).
- Consider organizing into subcategories for clarity: Fairness (societal bias in outcomes), Interpretability (can inspect the model and understand outputs), and Explainability (can explain an output for a given input).
- Coordinate with 3.6.3 Guardrails for enforcement mechanisms and 3.6.5 Human-in-the-Loop for human oversight.

#### 3.6.5 Human-in-the-Loop
💬 _Specifies the role of human oversight in decisions influenced or made by machine learning models._

➥ Describe where and how human review, approval, or intervention is required. Clarify review latency or throughput expectations, escalation paths, feedback mechanisms, traceability, and auditability of human actions.

💡 Tips:
- Link to applicable roles defined in 2.4 User Characteristics.

#### 3.6.6 Model Lifecycle and Operations
💬 _Defines requirements for deploying, monitoring, retraining, and retiring models in production._

➥ Outline how models transition from development to production, how their performance and data quality are monitored, and how retraining or rollback is triggered and managed. Include expectations for versioning and archival.

## 4. Verification
💬 _Describes how each requirement will be verified to provide objective evidence of compliance._

➥ Outline verification methods (test, canary metrics, analysis, inspection, demonstration) and test evidence preferably in a matrix paralleling Section 3. Consider adding environment details, tools, and test data requirements.

| Requirement ID | Verification Method | Test/Artifact Link | Status | Evidence           |
|----------------|---------------------|--------------------|--------|--------------------|
| REQ-FUNC-001   | test                | tests/UC01.md      | Passed | reports/tuc01.html |
| REQ-SEC-003    | analysis            | threat-model.md    | WIP    |                    |

💡 Tips:
- Include both positive and negative tests and include non-functional verification (performance, security, reliability).
- Verification artifacts may be versioned and linked to CI/CD.
- For AI, reference Model Cards and track eval datasets’ versions and ensure reproducibility of results.

## 5. Appendixes
💬 _Optional supporting material that aids understanding without being normative._

➥ Include glossaries, data dictionaries, models/diagrams, sample datasets, or change-impact analyses that support the main sections. Reference rather than duplicate content when possible.

💡 Tips:
- Keep appendixes organized and referenced from the main text.
