# REWT protected public inspection facade

REWT is an experimental persistent reasoning architecture designed to separate
a semantic reasoning engine from the system that owns identity, continuity,
state, validated consequences, and durable results.

This repository is a **protected technical inspection facade** for REWT. It
contains real, runnable software that demonstrates selected architectural
properties in a small offline form. It deliberately does not contain the
private REWT organism or its proprietary TREE reasoning methodology.

REWT is an independent project created by its Founder, Mark. It is under active
development and this repository is provided for technical inspection only.

## The problem REWT explores

A model can reason about a prompt and produce an answer. But an answer alone
does not establish which long-lived system owns the relevant identity, which
state should survive a process restart, what should be accepted before it is
stored, or how results remain tied to the correct owner and context.

REWT explores an architecture in which the semantic reasoning component is
bounded by persistent software that is responsible for those surrounding
concerns. The model is important, but it is not the complete system.

> **The model reasons. REWT governs, remembers and persists.**

The architectural intention is that a reasoning provider can be changed while
the persistent Tree remains owned by REWT. This is a design intention of the
wider project; this public facade demonstrates only the smaller structural
boundaries described below.

REWT is not an AI model. In the wider project, **Elian** is the semantic
reasoning role/component. This facade does not include Elian or the private
operational integration around it.

## TREE, at a safe high level

TREE is REWT terminology for persistent organisational reasoning state and
retained outcomes. A Tree has its own identity and owner. A retained outcome,
called a **Fruit**, can belong to that Tree rather than to the provider that
proposed it.

Trees can be stored, restored after a restart, and kept independent from one
another. That separation matters: a provider session, a process, or a model
choice should not become the owner of durable REWT state.

> **The model can change; the Tree remains.**

This is deliberately the extent of the public explanation. The private method
for reasoning with and evolving TREE state is not published here.

## What this repository is

This repository is a protected inspection facade, not a claim that the public
code is the complete REWT system. It demonstrates genuine architectural
mechanisms while preserving unpublished intellectual property.

The included provider is a deterministic offline demonstration double. It is
not Elian, does no semantic reasoning, makes no network request, and needs no
credential. Its purpose is to allow an engineer to inspect and exercise the
host-side boundaries without access to a live provider or the private reasoning
implementation.

## What the facade demonstrates

The runnable public code demonstrates these bounded properties:

- owner-bound Tree identity;
- provider/model identity separated from Tree identity;
- a provider-neutral, bounded request and consequence interface;
- host-side structural validation before durable state is accepted;
- fail-closed rejection of malformed or mismatched consequences;
- REWT-owned Fruit/result persistence;
- atomic local snapshot persistence;
- process restart and restore of an accepted snapshot;
- independent Tree storage and cross-owner isolation;
- independent local control and authorization components; and
- an offline deterministic demonstration requiring no credential.

These are architectural claims that can be independently inspected in this
repository. They do not claim that the facade performs complete REWT reasoning,
is production-ready, or supplies a complete local-model integration.

## Why this separation matters

The separation is useful wherever an answer should be more than a transient
piece of provider output. A durable system needs an accountable place for state
to live, a boundary at which proposed results can be accepted or rejected, and
a way to restore the correct state later without treating a previous model
session as the source of truth.

In this facade, those responsibilities remain on the REWT side of the provider
boundary. The provider can propose a generic consequence through a narrow
interface; REWT checks its structural identity and ownership before retaining
anything. The persisted result is then attached to a Tree and owner selected by
the host, not by the provider double.

This is not a claim that persistence alone produces good reasoning. It is a
claim about system responsibility: a reasoning component may be valuable while
the surrounding software remains responsible for continuity, validation, and
durable records. That distinction is what this inspection facade is designed to
make concrete.

## What an independent reviewer can verify

An engineer does not need access to the private project to inspect the public
claims. The public package exposes the reduced models, provider port, generic
validation boundary, persistence implementation, owner checks, and test suite.

For example, a reviewer can verify that a malformed or mismatched consequence
does not become persisted state; that an accepted public Fruit survives a fresh
process restore; and that a request for a Tree is bound to its owner. The tests
also demonstrate that one owner cannot restore another owner's Tree merely by
supplying an identifier.

The inspection is deliberately limited to these structural properties. It
cannot reveal, test, or stand in for the private semantic reasoning method.
That is an honest limitation of the repository rather than an omission hidden
behind the demonstration.

## Conceptual architecture

The following is a high-level conceptual picture of the larger architectural
separation. It does not describe the private reasoning method.

```text
User / Caller
      |
      v
     REWT
      |
      v
Persistent Tree State
      |
      v
Bounded Reasoning Interface
      |
      v
Semantic Provider
      |
      v
Structured Proposed Result
      |
      v
REWT Validation
      |
      v
Persistent Fruit / State
```

The executable public demonstration is intentionally narrower:

```text
Caller
  -> Protected REWT Facade
  -> Public TreeTurn Interface
  -> Deterministic Provider Double
  -> Generic Consequence
  -> Structural Validation
  -> Public Fruit
  -> Persistent Snapshot
```

The second diagram is what this repository actually runs. The provider double
must not be mistaken for the private REWT reasoning engine.

## What is deliberately not included

The facade intentionally excludes the private REWT organism, including its
proprietary reasoning engine and semantic methodology; private prompts and
instructions; complete governing materials; internal reasoning and lifecycle
logic; private state structures; private research capabilities; and operational
private REWT materials.

Those boundaries are intentional. The purpose of this repository is to permit
meaningful technical inspection of selected architecture claims without
publishing the unpublished method that sits behind the wider project.

Nothing here should be read as a specification for reconstructing the private
reasoning system.

## Run and inspect the demonstration

The package requires Python 3.11 or newer. The runtime package has no external
dependencies. Install the optional development dependency if `pytest` is not
already available:

```powershell
python -m pip install -e ".[dev]"
```

Run the offline test suite:

```powershell
python -m pytest -q
```

The tests show that the provider boundary is replaceable, malformed
consequences are rejected, accepted results persist, restart restores state,
and Trees remain owner-isolated. They also check that the public package does
not import the private `rewt` package.

Run the small offline demonstration:

```powershell
python -m rewt_public
```

It uses the deterministic provider double, validates one generic result, saves
it as a public Fruit, and restores the resulting snapshot locally. It does not
contact a provider or require an API key.

## Current development status

REWT is under active development. This protected facade records selected,
implemented architectural boundaries, not the complete private organism. The
wider project uses and develops Elian as its semantic reasoning component while REWT remains the
governing and persistent architecture around that component.

Local inference work and the complete operational Elian integration are
separate from this repository and are not represented as included here.

## Rights and review

The source is proprietary and provided for inspection only. It is not an
open-source release. See [LICENSE](LICENSE) for the current draft terms and
[SECURITY.md](SECURITY.md) for the current security-reporting draft.

Publication, licensing, security review, and intellectual-property review
remain Founder decisions. This local facade is **not authorised for public
publication**.
