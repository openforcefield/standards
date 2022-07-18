# OFF-EP 0007 — Add long-range dispersion attribute in vdW section

**Status:** Draft

**Authors:** Matt Thompson

**Stakeholders:**

**Acceptance criteria:** <Unanimity>

**Created:** 2022-06-18

**Discussion:** [PR #40](https://github.com/openforcefield/standards/pull/40)

**Implementation:** [``openff-standards``](https://github.com/openforcefield/openff-standards)

## Abstract

This change exposes long-range dispersion corrections as a toggleable option in the vdW section of
the SMIRNOFF specification.

## Motivation and Scope

In version 0.3 of the `<vdW>` tag, there is no exposed option for turning on or off long-range
dispersion corrections. Existing implementaions of SMIRNOFF, to our knowldge, all use an isotropic
correction, but in some use cases it may be desired to turn this off or use a different type of
correction. This proposal makes this explicit and also adds a non-default value that enables users
to turn this correction off. It does not attempt to modify other non-bonded settings (cut-off
distance and method, switching function, mixing rule, or long-range electrostatics treatment).

## Usage and Impact

Existing SMIRNOFF implementations currently turn on a long-range dispersion correction (i.e. [OpenFF
Toolkit](https://github.com/openforcefield/openff-toolkit/blob/0.10.6/openff/toolkit/typing/engines/smirnoff/parameters.py#L3695)).
Updating the specification would not impact this behavior if using default and recommended settings.
Users wishing to turn this correction off, for whatever reason, would now be able to do so while
still following the SMIRNOFF specifications.

Most engines implement some form of isotropic long-range dispersion correction. In
[OpenMM](http://docs.openmm.org/latest/api-python/generated/openmm.openmm.NonbondedForce.html#openmm.openmm.NonbondedForce.setUseDispersionCorrection),
this is controlled via a method that accepts a boolean toggle. Similar options are implemented
in [GROMACS](https://manual.gromacs.org/current/user-guide/mdp-options.html#mdp-DispCorr), AMBER
(`nodisper`), [LAMMPS](https://docs.lammps.org/pair_modify.html) and likely other engines. However
unlikely, if in the future other types of corrections than the current isotropic one are developerd,
this specification can be extended because the setting is a string value, not a boolean.

## Backward compatibility

This change proposes adding an attribute to a section, so in a strict sense it is not
backwards-comptaible. (A parser that only knows about version 0.3 might not understand a serialized
representation of a version 0.4 section because of this new attribute.) However, the recommended
default value matches what is currently ubiquituous in SMIRNOFF implementations, so an up-converter
from section 0.3 to 0.4 should be straightforward to write and safe to use. It is recommended that
any 0.3 version section is up-converted to a 0.4 section with the only change being an added
`long_range_dispersion` attribute with its default value of `"isotropic"`.

## Detailed description

A `long_range_dispersion` attribute is added to the `vdW` section, which is bumped to 0.4.
Supported values are
  * `"isotropic"`: Isotropic dispersion corrections described in
    [Shirts, 2007](https://pubs.acs.org/doi/10.1021/jp0735987) should be used.
  * `"none"`: No dispersion corrections should be used.

The default value, which is recommended for general use, is `"isotropic"`.

These options only sensibly apply to periodic systems and only to vdW interactions. For non-periodic
systems, this attribute should be ignored.

No other sections are updated, therefore this change is not meant to impact electrostatic interactions.

## Alternatives

No alternative proposals are under consideration or offered. If this proposal were to be rejected,
implementations would likely continue using long-range dispersion corrections, but would lack
guidance from the SMIRNOFF specification and no other values (such as turning corrections off) would
be unamiguously supported.

## Discussion

- [Standards #38](https://github.com/openforcefield/standards/pull/38): A user discovered that `long_range_dispersion` is not an attribute in version 0.3.
- [OFF-EP 00002](https://github.com/openforcefield/standards/pull/22): A naive proposal that attempted to make this change without noticing that it would be breaking.

## Copyright

* This was seeded from the
[OFF-EP template](https://github.com/openforcefield/standards/blob/main/docs/enhancement-proposals/off-ep-template.md),
which was is based upon the
[``numpy`` NEP template]( https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
