# OFF-EP 0007b — Add long-range dispersion attribute in vdW section

**Status:** Draft

**Authors:** Matt Thompson, John Chodera

**Stakeholders:** Jeffrey Wagner, David Mobley, John Chodera

**Acceptance criteria:** <Unanimity>

**Created:** 2022-06-18

**Discussion:** [PR #40](https://github.com/openforcefield/standards/pull/40) [PR #44](https://github.com/openforcefield/standards/pull/44)

**Implementation:** [``openff-standards``](https://github.com/openforcefield/openff-standards)

## Abstract

This change adds an attribute to the `vdW` section of the SMIRNOFF specification to clarify how long-range vdW interactions are handled.

## Motivation and Scope

In version 0.3 of the `<vdW>` tag, there is no exposed option for specifying how long-range vdW interactions are to be handled.
Existing implementations of SMIRNOFF, to our knowledge, all presume an isotropic long-range dispersion correction is used,
but important details that determine the "correct" potential energy are omitted, and no facility to specify alternative approaches to treating
long-range interactions is provided. This proposal makes this an explicit attribute and adds specifications for the most important variants:
no long-range vdW correction (`none`),
an isotropic long-range vdW correction that integrates the vdW potential against the switching function out to infinite pair separation (`isotropic`),
and the LJPME formulation (`LJPME`).

## Usage and Impact

While existing SMIRNOFF implementations always use a long-range isotropic dispersion correction (i.e. [OpenFF
Toolkit](https://github.com/openforcefield/openff-toolkit/blob/0.10.6/openff/toolkit/typing/engines/smirnoff/parameters.py#L3695)),
following discussion in [Standards #38](https://github.com/openforcefield/standards/pull/38), it was recognized that
(1) there was no way to disable this long-range correction or specify an important alternative approach (LJPME) that leads to a different potential definition,
(2) the exact form of the long-range isotropic dispersion correction currently used was not specified as part of the SMIRNOFF standard.
Updating the specification would not impact this behavior if using the default, recommended setting.

This proposed enhancement would provide a way to disable the long-range vdW correction as well as build force fields that use LJPME,
which has been recognized as being important in treating heterogeneous systems such as [those containing lipid bilayers](https://doi.org/10.1021/ct400140n).

Most engines implement a common form of isotropic long-range vdW correction in which the pairwise vdW potential is averaged over all vdW site pairs
and integrated (numerically or analytically) alongside a surface area term (and a term to account for the switching function if one is in use) to account for the missing interactions out to infinite separation:
```
U_{correction} = [N (N-1)]^{-1} \sum_{i < j}^N \int_0^{\infty} dr [1-S(r)] [4 \pi r^2] U_{vdw}(r)
```
Here, `U_{correction}` is the long-range vdW correction, `N` is the number of vdW sites, `S(r)` is the switching function or cutoff function that assumes the value of `S(r) = 0` for `r \ge r_{cut}` and `S(r) = 1` for `r ~ 0`.

In [OpenMM](http://docs.openmm.org/latest/api-python/generated/openmm.openmm.NonbondedForce.html#openmm.openmm.NonbondedForce.setUseDispersionCorrection),
this is controlled via a method that accepts a boolean toggle. Similar options are implemented
in [GROMACS](https://manual.gromacs.org/current/user-guide/mdp-options.html#mdp-DispCorr), AMBER
(`nodisper`), [LAMMPS](https://docs.lammps.org/pair_modify.html), and likely other engines. However
unlikely, if in the future other types of corrections than the current isotropic one are developed,
this specification can be extended because the setting is a string value, not a boolean.

Many of these engines also provided the capability to use LJPME.
As with electrostatics, we do not specify the exact parameters used for PME (real-space cutoff, grid spacing, error tolerance);
the SMIRNOFF spec instead specifies the Ewald sum is the true desired potential and the simulation engine must make a faithful
approximation of this true potential, but can adjust settings or use other algorithms to achieve improved performance without introducing significant error.

## Backward compatibility

This change proposes adding an attribute to a section, so in a strict sense it is not
backwards-compatible. (A parser that only knows about version 0.3 might not understand a serialized
representation of a version 0.4 section because of this new attribute, and at very least the
information would be lost in a down-conversion.) However, the recommended
default value matches what is currently ubiquitous in SMIRNOFF implementations, so an up-converter
from section 0.3 to 0.4 should be straightforward to write and safe to use. It is recommended that
any 0.3 version section is up-converted to a 0.4 section with the only change being an added
`long_range_treatment` attribute with its default value of `"isotropic"`.

## Detailed description

A `long_range_treatment` attribute is added to the `vdW` section, which is bumped to version 0.4.

Supported values are
  * `"none"`: No long-range vdW correction is applied.
  * `"isotropic"`: An isotropic vdW correction, described below, is applied.
  * `"LJPME"`: An Ewald sum is used (commonly referred to as LJPME) to treat the vdW potential in a periodic manner [1](https://doi.org/10.1063/1.464397) [2](http://dx.doi.org/10.1063/1.465608) [3](https://doi.org/10.1021/acs.jctc.5b00726). Note that this is only compatible with certain forms of the potential that involve sums of inverse even powers of `r`.

The default value, which is recommended for general use, is `"isotropic"`.

The long-range correction would only be applied to periodic systems; it would be omitted and this attribute ignored for non-periodic systems.

For the `"isotropic"` case, the correction is computed as
```
U_{correction} = [N (N-1)]^{-1} \sum_{i < j}^N \int_0^{\infty} dr [1-S(r)] [4 \pi r^2] U_{vdw}(r)
```
Here, `U_{correction}` is the long-range vdW correction, `N` is the number of vdW sites, `S(r)` is the switching function or cutoff function that assumes the value of `S(r) = 0` for `r \ge r_{cut}` and `S(r) = 1` for `r ~ 0`.
This is described in more detail in [Shirts, 2007](https://pubs.acs.org/doi/10.1021/jp0735987) and implemented in [OpenMM](http://openmm.org) for [Lennard-Jones 12-6 potentials analytically](http://docs.openmm.org/latest/api-python/generated/openmm.openmm.NonbondedForce.html#openmm.openmm.NonbondedForce.setUseDispersionCorrection) and for other vdW potentials [numerically](http://docs.openmm.org/latest/api-python/generated/openmm.openmm.CustomNonbondedForce.html#openmm.openmm.CustomNonbondedForce.setUseLongRangeCorrection).

No other sections are updated, therefore this change is not meant to impact electrostatic interactions.

## Alternatives

No alternative proposals are under consideration or offered. If this proposal were to be rejected,
implementations would likely continue using long-range dispersion corrections, but would lack
guidance from the SMIRNOFF specification and no other values (such as turning corrections off) would
unambiguously be supported.

## Discussion

- [Standards #38](https://github.com/openforcefield/standards/pull/38): A user discovered that `long_range_dispersion` is not an attribute in version 0.3.
- [OFF-EP 00002](https://github.com/openforcefield/standards/pull/22): A naive proposal that attempted to make this change without noticing that it would be breaking.
- [OpenFF Toolkit #1351](https://github.com/openforcefield/openff-toolkit/pull/1351): A sample implementation with example behavior

## Copyright

* This was seeded from the
[OFF-EP template](https://github.com/openforcefield/standards/blob/main/docs/enhancement-proposals/off-ep-template.md),
which was is based upon the
[``numpy`` NEP template]( https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
