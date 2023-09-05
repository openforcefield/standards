# OFF-EP 0008 — Specifying different vdW methods for periodic and non-periodic systems and allow "no-cutoff" vdW interactions

**Status:** Draft

**Authors:** Matt Thompson

**Stakeholders:** All who have implemented a SMIRNOFF parser

**Acceptance criteria:** Majority of SMIRNOFF committee

**Created:** 2023-08-01

**Discussion:** Issues [#51](https://github.com/openforcefield/standards/pull/51) and
[#7](https://github.com/openforcefield/standards/issues/7)

**Implementation:** [PR #53](https://github.com/openforcefield/standards/pull/53)

## Abstract

This OFF-EP splits the current `method` attribute in the vdW section into separate attributes for periodic and non-periodic systems. It also adds `"no-cutoff"` as a supported method.

## Motivation and Scope

The `method` attribute in the vdW section specifies what sort of cut-off scheme should be used, if any, for vdW
interactions. It does this without consideration for whether or not the system is periodic. Conventionally, however,
different schemes are used for periodic systems (cut-off interactions with various corrections) and non-periodic
systems (no cut-off). This causes an issue for existing implementations, which favor the use of a "no cut-off" scheme
for non-periodic systems despite not being a part of the SMIRNOFF specification.

Additionally, the current specification implies that the only supported vdW method is `"cutoff"` and, by extension, that vdW
interactions without a cut-off are not supported by SMIRNOFF despite its common use.

## Usage and Impact

As these proposed changes bring the specification in line with existing implementations, such as how OpenFF software
implements the SMIRNOFF specification, there should be no practical impact on existing workflows and simulations.
Software that implements the SMIRNOFF specification will need to be updated to support new attributes. Additionally,
developers may choose to implement an up-converter from older versions of the vdW section.

## Backward compatibility

Because this change expands the information content of the vdW section and adds attributes that do not currently exist,
it can be understood as strictly backwards-incompatible. However, most implementations do not strictly follow the
specification in its current form and the proposed changes bring the specification in line with this implementation and
community practices more broadly.

## Detailed description

The vdW method section is updated to version 0.4.

The `method` attribute is removed from the vdW section and replaced with two new attributes: `periodic_method` and
`nonperiodic_method`. These encode the method that should be used for periodic and non-periodic systems,
respectively.

Either `periodic_method` or `nonperiodic_method` can take the following values:

* `"cutoff"`: The vdW interaction is truncated at a distance specified by the `cutoff` attribute.
* `"no-cutoff"`: The vdW interaction is not truncated.

The default values, and the implied up-conversion from `method="cutoff"` of version 0.3, are `periodic_method="cutoff"`
and `nonperiodic_method="no-cutoff"`.

Other attributes in the vdW section, such as `potential`, are not affected.

## Alternatives

The existing `method` section could remain but specify both periodic and non-periodic methods. The result would be
something like `method="periodic=cutoff,non-periodic=no-cutoff"`. This is unappealing, however, as it forces two
details into one setting, is non-trivial to parse, and makes future extensions to the set of supported methods more difficult.

## Discussion

* [Ambiguity with periodicity](https://github.com/openforcefield/standards/pull/51)
* [Lack of (explicit) support for non-cut-off interactions](https://github.com/openforcefield/standards/issues/7)
* A similar change to the Electrostatics section was accepted in OFF-EP 0005

## Copyright

*This template is based upon the [``numpy`` NEP template](https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
