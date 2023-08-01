# OFF-EP 0008 — Specifying different vdW methods for periodic and non-periodic systems and allow no-cutoff vdW interactions

**Status:** Draft

**Authors:** Matt Thompson

**Stakeholders:** All who have implemented a SMIRNOFF parser

**Acceptance criteria:** Majority of SMIRNOFF committee

**Created:** 2023-08-01

**Discussion:** Issues [#51](https://github.com/openforcefield/standards/pull/51) and
[#7](https://github.com/openforcefield/standards/issues/7)

**Implementation:** [PR #51](https://github.com/openforcefield/standards/pull/51)

## Abstract

This OFF-EP splits the current vdW `"method"` tag into separate tags for periodic and non-periodic systems and adds `"no-cutoff"` as a supported method.

## Motivation and Scope

The `"method"` tag in the vdW section specifies what sort of cut-off scheme should be used, if any, for vdW
interactions, whether or not the system is periodic. Conventionally, however, different treatments are used for
periodic systems in the condensed phase (cut-off interactions with various corrections) and non-periodic systems in the
gas phase (no cut-off). This causes an issue for existing implementations, which favor the use of a "no cut-off" scheme
in the gas phase despite not being a part of the SMIRNOFF specification.

Additionally, the current specification implies that the only supported vdW method is "cutoff" and, by extension, that vdW
interactions without a cut-off are not supported by SMIRNOFF.

## Usage and Impact

As these proposed changes bring the specification in line with existing implementations, such as how OpenFF software
implements SMIRNOFF, there is no practical impact on existing workflows. Other software that implements the SMIRNOFF
specification may need to be updated.

## Backward compatibility

Because this change expands the information content of the vdW section and adds an option that does not currently
exist, it can be understood as strictly backwards-incompatible. However, most implementations do not strictly follow
the specification in its current form and the proposed changes bring the specification in line with this implementation
and community practices more broadly.

## Detailed description

The vdW method section is updated to version 0.4.

The `method` option is removed from the vdW section and replaced with two new options: `periodic_method` and
`nonperiodic_method`. These encode the method that should be used for periodic and non-periodic simulations,
respectively.

Either `periodic_method` or `nonperiodic_method` can take the following values:

* `"cutoff"`: The vdW interaction is truncated at a distance specified by the `cutoff` argument.
* `"no-cutoff"`: The vdW interaction is not truncated.

The default values, and the implied up-conversion from `method="cutoff"`, are `periodic_method="cutoff` and `nonperiodic_method="no-cutoff"`.

Other options in the vdW section, such as `potential`, are not affected.

## Alternatives

The existing `method` section could remain but specify both periodic and non-periodic methods. The result would be
something like `method="periodic=cutoff,non-periodic=no-cutoff"`. This is unappealing, however, as it forces two
details into one setting, is non-trivial to parse, and makes future extensions to the set of supported methods more difficult.

## Discussion

* [Ambiguitiy with periodicity](https://github.com/openforcefield/standards/pull/51)
* [Lack of support for non-cut-off interactions](https://github.com/openforcefield/standards/issues/7)
* A similar change to the Electrostatics section was accepted in OFF-EP 0005

## Copyright

*This template is based upon the [``numpy`` NEP template](https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
