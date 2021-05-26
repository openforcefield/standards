# OFF-EP 0 — Purpose and Process

**Status:** Accepted

**Authors:** Simon Boothroyd

**Acceptance criteria:** Unanimity

**Stakeholders:** Karmen Condic-Jurkic, Jeffrey Wagner, David Mobley, John Chodera

**Created:** 2020-04-01

**Discussion:** [Issue #741](https://github.com/openforcefield/openff-toolkit/issues/741)

**Implementation:** [``openff-standards``](https://github.com/openforcefield/openff-standards)

## What is an OFF-EP?

OFF-EPs (OpenFF Enhancement Proposals) are the mechanism by which the standards
employed across the Open Force Field ecosystem are drafted, accepted and updated.
OFF-EPs cover both technical and procedural standards, example of which include:

* the specification of core data models, such the ``Molecule``, ``Topology`` and 
  ``System`` models.
* the SMIRNOFF force field specification.
* the standard operating procedure for curating and adopting data sets, such as the 
  [QCA Standards](https://github.com/openforcefield/qca-dataset-submission/blob/master/STANDARDS.md).
  
Each OFF-EP should clearly and concisely outline what new standard is being introduced
or updated, and most importantly, provide a rationale for the change and get input
from relevant stakeholders.

Because the OFF-EPs are maintained as text files in a versioned repository,
their revision history is the historical record of the standards proposal.

### Types

There are three kinds of OFF-EPs:

1. **Standards Track** OFF-EPs describe a new feature or implementation
1. **Informational** OFF-EPs provide general, non-binding guidance to the community but do not propose a new feature.
1. **Process** OFF-EPs describe a change that may not be technical in nature but requires community input.

## Workflow

The OFF-EP process begins with a new idea for Open Force Field infrastructure and/or community.
It is highly recommended that a single OFF-EP contain a single key proposal or new idea with a concise scope.
Small changes often do not need to go through the OFF-EP process and can be submitted directly to as either a question to the community or a software patch.
Each OFF-EP must have a champion -- someone who writes the proposal using the template provded below, shepherds the discussions in the appropriate forums, and attempts to build community consensus around the proposal.

### Submission

Once a proposal is written, this draft should be submitted as a pull request to the [openforcefield/standards](https://github.com/openforcefield/standards) repository with the status set to `Proposed`.
It shall be merged at the earliest convenience of maintainers (note that this merge does not imply acceptance, as its status shall still be `Proposed`).
At this point, members of the Open Force Field community will review the submission.

### Review and Resolution

All OFF-EPs will be resolved as either *Rejected*, *Accepted* or *Deferred*

An OFF-EP is accepted upon approval by at least three of @SimonBoothroyd, @j-wags, @karmencj, @davidlmobley, and 
@jchodera. 

When an OFF-EP is accepted, it status shall be marked `Accepted`.

If an OFF-EP is not accepted and the community considers it unlikely to be accepted in the future, it can be rejected and its status shall be marked `Rejected`.
If an OFF-EP is not accepted and the community considers it plausible to be accepted in the future, possibly in a different form, the authors can withdraw it and its status shall be marked `Deferred`.

## Format

OFF-EPs are UTF-8 encoded text files using the Markdown format.
A template is provided in the file `off-ep-template.md`.

## Copyright

This document is based based upon the [`NEP 0`](https://github.com/numpy/numpy/blob/master/doc/neps/nep-0000.rst),  [`CFEP 01`](https://github.com/conda-forge/cfep/blob/master/cfep-01.md), and [`PEP 1`](https://www.python.org/dev/peps/pep-0001/)

This document is explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
