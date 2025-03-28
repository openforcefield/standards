# OFF-EP X — Template

**Status:** Draft

**Authors:** Lily Wang

**Stakeholders:** &lt;list of stakeholders that would be affected by this proposal>

**Acceptance criteria:** 

**Created:** &lt;date created>

**Discussion:** &lt;link to the PR / issue where proposal is being discussed>

**Implementation:** &lt;link an example / reference implementation of the proposal>

## Abstract

A short description of the change being addressed.

## Motivation and Scope

OpenFF NAGL has built on existing work and trained a GNN that reproduced AM1-BCC partial charges for a substantial set of chemistries. Currently, there is not a canonically method by which these charges can be used in a SMIRNOFF force field. Generating partial charges from a GNN and passing them alongside a SMIRNOFF force field as prespecified charges works but is discouraged as this pathway exists only as a convenience to a user. Using an external tool to assign charges also bypasses the need to specify the contents of the GNN sufficient for somebody else to reimplement them. Developers and users for SMIRNOFF force fields would benefit from information about these GNNs being encoded directly into the force field itself.

This affects any consumer of SMIRNOFF force fields which includes `<GNNCharges>`. Since it is not a required section, force field developers who choose to use other partial charge methods would not be affected. SMIRNOFF implementations must implement `<GNNCharges>`, by definition, to use force fields that include this section. Existing force fields cannot use this section, so they are not affected.

The introduction of this section lays the groundwork for supporting future models with improved performance and scope. This may include, for example:

- support for more elements
- improved runtime performance on large and/or complex molecule(s) such as biopolymers
- modelling of charge methods other than AM1-BCC
- models employing different architecture, featurization, and/or normalization techniques

OpenFF has produced a reference implementation of this section in its package OpenFF NAGL. The contents of this proposal derive from the current structure of OpenFF NAGL and the model(s) it implements. If this proposal is accepted, OpenFF NAGL will need minor updates to properly check its GNN implementation against the details encoded in a SMIRNOFF force field, but we expect these changes will be minor because the proposed changes derive directly from this software. The OpenFF Toolkit and Interchange will need minor updates to properly support this section and some edge cases that arise from using this section in combination with other section(s) and tools, such as prespecified charges and virtual site parameter which modify charges. Similar tools which also implement the encoded GNN and/or the SMIRNOFF specification more broadly will need similar updates.

This proposal does not include changes or interactions with sections that do not modify partial charges, such as `<vdW>`, `<Constraints>`, `<Bonds>`, `<Angles>`, etc.

# TODO: Describe where in the charge method hierarchy this exists
# TODO: Describe interaction(s) with virtual sites

## Usage and Impact

This section describes how users of the ecosystem will use features 
described in this SMIRNOFF EP. It should be comprised mainly of code / file 
examples that wouldn't  be possible without acceptance and implementation 
of this proposal, as well as the impact the proposed changes would have 
on the ecosystem. 

## Backward compatibility

This adds a new section which cannot meaningfully be converted to any existing sections.

## Detailed description

This section should provide a detailed description of the proposed
change. It should include examples of how the new functionality would be
used, intended use-cases and pseudo-code illustrating its use.

## Alternatives

The first GNN trained with the intent to be shipped in SMIRNOFF force fields is one that models AM1-BCC partial
charges, so another solution could involve updating the existing `<ToolkitAM1BCC>` section instead of adding a new
section altogether. This might involve a new tag in the `<ToolkitAM1BCC>` section that distinguishes a particular GNN
from the existing QuacPac and/or `sqm`-based approach. This approach is limiting, however, since GNNs can be used to
predict other charge models than AM1-BCC; if a GNN was trained to ABCG2 or a RESP variant, it's not obvious if that
could drop in to `<ToolkitAM1BCC>`.

Another similar solution could involve not updating the SMIRNOFF specification at all and simply letting
implementations use GNNs in place of QuacPac or `sqm` as currently specified. This in principle produces the same
results, to the extent that the GNN accurately reproduces AM1-BCC charges, but is inconsistent with the philosophy that
the details of a force field must be communicated to users and not hidden from view.

The solution in this proposal makes clear to any person or tool inspecting a force field that GNNs are a different tool
than existing AM1-BCC charge providers. It attempts to provide enough detail that somebody could re-implement the same
GNN provided weights that are shipped alongside a force field. It allows for future modifications in which a different
underlying charge model is targeted.

## Discussion

This section may just be a bullet list including links to any discussions
regarding the proposal:

- This includes links to mailing list threads and / or relevant GitHub issues.

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
