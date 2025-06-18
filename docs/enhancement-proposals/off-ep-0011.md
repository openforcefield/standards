# OFF-EP 11 — Add NAGLCharges section to spec

**Status:** Draft

**Authors:** Lily Wang, Matt Thompson, Jeff Wagner

**Acceptance criteria:** Unanimity (4 approving reviews) or partial support (2 approvals and 2 week period with no reviews requesting changes)[https://openforcefield.atlassian.net/wiki/spaces/MEET/pages/2638774273/09-05-23+SMIRNOFF+Committee+Meeting]

**Created:** 2025-04-01

**Discussion:** [PR #71](https://github.com/openforcefield/standards/pull/71)

**Implementation:** https://github.com/openforcefield/openff-interchange/pull/1206 https://github.com/openforcefield/openff-toolkit/pull/2048

## Abstract

This change adds a `<NAGLCharges>` section which calls for a specific NAGL model to be used to assign atomic partial charges.

## Motivation and Scope

**Motivation:** OpenFF NAGL has built on existing work and trained a graph-convolutional neural network (GNN) that reproduces AM1-BCC ELF10 partial charges for a substantial set of chemistries. Currently, there is not a canonical method by which these GNN-provided charges can be requested in a SMIRNOFF force field. At the moment, a user can generate partial charges from a GNN and pass them to `create_interchange` or `create_openmm_system` alongside a SMIRNOFF force field as prespecified charges. To use GNNs in a flagship force field, this approach is not sufficient, and the SMIRNOFF specification must be updated to include enough information that an external developer could get the same charges themselves. 

**Who this EP would affect:** The changes described in this proposal affect any consumer of SMIRNOFF force fields that include `<NAGLCharges>`, which is likely to be the case for `openff-2.3.0` and beyond. Since it is not a required section, force field developers who choose to use other partial charge methods would not be affected. SMIRNOFF implementations must implement `<NAGLCharges>`, by definition, to use force fields that include this section. Existing force fields do not use this section, so they are not affected.

**Interaction with other sections:** This proposal does not include changes or interactions with sections that do not modify partial charges, such as `<vdW>`, `<Constraints>`, `<Bonds>`, `<Angles>`, etc.

`NAGLCharges` fits into the current charge hierarchy as follows (with methods high in the list taking priority over those lower):

- Pre-specified charges (charge_from_molecules)
- Library charges
- GNN charges
- ChargeIncrementModel charges
- ToolkitAM1BCC charges

The initial `0.3` version of the `NAGLCharges` section does have special interactions with virtual sites, though future versions of this section may include direct assignment of partial charges to virtual sites. But for the 0.3 version of this section proposed by this EP, the behavior will be that, if the `NAGLCharges` section is present in a force field with virtual sites, NAGL is used to assign initial charges to the molecule, and then virtual sites apply their charge increments on top of those initial charges. 

**Changes needed:** The contents of this proposal derive from the current structure of OpenFF NAGL and the model(s) it implements. If this proposal is accepted, OpenFF NAGL may need minor updates to properly check its GNN implementation against the details encoded in a SMIRNOFF force field, but we expect these changes will be minor because the proposed changes derive directly from this software. The OpenFF Toolkit and Interchange will need minor updates to properly support this section and some edge cases that arise from using this section in combination with other section(s) and tools (such as prespecified charges and virtual site parameters which modify charges). Similar tools which also implement the encoded GNN and/or the SMIRNOFF specification more broadly will need similar updates.

## Backward compatibility

This proposal adds a new section which does not affect backwards compatibility. While in practice the first version of the NAGLCharges section is very likely to be trained on AM1BCC ELF10 charges, we do not propose that existing force fields with the ToolkitAM1BCC section be assumed to be compatible with/automatically upgrade-able to NAGLCharges sections.

## Detailed description

This proposal adds a section named `<NAGLCharges`>. The proposed initial version of this section (0.3) is as follows, and will be added verbatim to the specification if this EP is approved:

### `<NAGLCharges>`: Use a specified NAGL model file for charge assignment

The `NAGLCharges` section-level element specifies that the force field should use a specific model file in conjunction with the `openff-nagl` software to assign partial charges. It contains the following attributes:

- `version`
- `model_file`
- `digital_object_identifier` (optional)

The attribute `model_file` is a string identifying a file that includes model weights and other information. This by convention is a PyTorch `.pt` file, extended to contain additional information about the model that is read by the `openff-nagl` software. By their nature, GNNs use many more weights than can reasonably be encoded into an XML file, so pointing to an external file is a necessary and unavoidable layer of complexity.

Because the NAGLCharges section requires loading information from a source outside the SMIRNOFF force field, the optional attribute `digital_object_identifier` is provided for ease and reproducibility of use. `digital_object_identifier` is a string that contains a [Zenodo](https://zenodo.org/) [Digital Object Identifier (DOI)](https://www.doi.org/) that can be accessed to fetch the model file. If the file can not be found locally, it may be fetched from this Zenodo entry. The Zenodo entry must have an attached file with a name matching the `model_file` string to be fetched. 

Below is an example `<NAGLCharges>` section:

```xml
<NAGLCharges model_file="openff-gnn-am1bcc-0.1.0-rc.3.pt" digital_object_identifier="10.5072/zenodo.203601" version="0.3"></NAGLCharges>
```

This section only specifies a model file name, not a version of the NAGL software. The NAGL software is responsible for only accepting model files which it can correctly interpret.

Note that atoms for which prespecified or `<LibraryCharges>` charges have already been applied are excluded from charging via `<NAGLCharges>`.

## Discussion

- [Original SMIRNOFF EP](https://github.com/openforcefield/standards/pull/71)

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
