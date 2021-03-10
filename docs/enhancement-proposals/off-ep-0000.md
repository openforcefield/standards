# OFF-EP 0 — Purpose and Process

**Status:** Draft

**Authors:** Simon Boothroyd

**Stakeholders:** ...

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

[comment]: <> (There are three kinds of OFF-EPs:)

[comment]: <> (1.  A **Standards Track** NEP describes a new feature or implementation)

[comment]: <> (    for NumPy.)

[comment]: <> (2.  An **Informational** NEP describes a NumPy design issue, or provides)

[comment]: <> (    general guidelines or information to the Python community, but does)

[comment]: <> (    not propose a new feature. Informational NEPs do not necessarily)

[comment]: <> (    represent a NumPy community consensus or recommendation, so users)

[comment]: <> (    and implementers are free to ignore Informational NEPs or follow)

[comment]: <> (    their advice.)

[comment]: <> (3.  A **Process** NEP describes a process surrounding NumPy, or proposes)

[comment]: <> (    a change to &#40;or an event in&#41; a process. Process NEPs are like)

[comment]: <> (    Standards Track NEPs but apply to areas other than the NumPy)

[comment]: <> (    language itself. They may propose an implementation, but not to)

[comment]: <> (    NumPy's codebase; they require community consensus. Examples include)

[comment]: <> (    procedures, guidelines, changes to the decision-making process, and)

[comment]: <> (    changes to the tools or environment used in NumPy development. Any)

[comment]: <> (    meta-NEP is also considered a Process NEP.)

[comment]: <> (## NEP Workflow)

[comment]: <> (The NEP process begins with a new idea for NumPy. It is highly)

[comment]: <> (recommended that a single NEP contain a single key proposal or new idea.)

[comment]: <> (Small enhancements or patches often don't need a NEP and can be injected)

[comment]: <> (into the NumPy development workflow with a pull request to the NumPy)

[comment]: <> ([repo][]. The more focused the NEP, the more successful it tends to be.)

[comment]: <> (If in doubt, split your NEP into several well-focused ones.)

[comment]: <> (Each NEP must have a champion---someone who writes the NEP using the)

[comment]: <> (style and format described below, shepherds the discussions in the)

[comment]: <> (appropriate forums, and attempts to build community consensus around the)

[comment]: <> (idea. The NEP champion &#40;a.k.a. Author&#41; should first attempt to ascertain)

[comment]: <> (whether the idea is suitable for a NEP. Posting to the numpy-discussion)

[comment]: <> ([mailing list][repo] is the best way to go about doing this.)

[comment]: <> (The proposal should be submitted as a draft NEP via a [GitHub pull)

[comment]: <> (request][repo] to the `doc/neps` directory with the name `nep-<n>.rst`)

[comment]: <> (where \`)

[comment]: <> (  [repo]:)