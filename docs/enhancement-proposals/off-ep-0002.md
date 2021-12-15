# OFF-EP 0002 — Support vdW interactions without long-range disperson corrections

**Status:** Proposed

**Authors:** Matt Thompson

**Stakeholders:** David Mobley, John Chodera, Jeffrey Wagner, Simon Boothroyd

**Acceptance criteria:** <Unanimity>

**Created:** 2021-11-23

**Discussion:** [Issue #7](https://github.com/openforcefield/standards/issues/7)

**Implementation:** [PR #22](https://github.com/openforcefield/standards/pull/22)

## Abstract

This OFF-EP adds a `none` option in the `long_range_dispersion` option in the vdW section of the
SMIRNOFF specification.

## Motivation and Scope

In most use cases involving force fields, vdW interactions are truncated at cutoff distance and have
no effect past that cutoff. There [are ways](https://pubs.acs.org/doi/10.1021/jp980939v) to
approximately correct for this, known as long-range dispersion corrections, that can improve the
accuracy and/or speed of simulations. The SMIRNOFF specification currently has an option that
encodes this: `long_range_dispersion`, with a default value of `"isotropic"`. There are no other
supported values and no way to bypass adding this correction. While potentially dubious for use in
scientific applications, users may wish to not include this correction. This would also make it
easier to validate implementations of SMIRNOFF-style force fields by making the vdW interactions
simpler to compute, since the long-range dispersion correction adds complexity not included in
conventional 12-6 Lennard-Jones potential implied by `potential="Lennard-Jones-12-6"`.

This OFF-EP adds `none` to the list of allowed values for the `long_range_dispersion` tag in the
`<vdW>` section. This option communicates that there should be no correction term added to the vdW interactions
to account for long-range dispersion forces. It does not make it the default value, so existing
SMIRNOFF force fields and implementations should not be affected. It leaves unresolved questions
around if a switching function or other tail correction method should be applied.

## Usage and Impact

This option can be used by including `long_range_dispersion="none"` in the header of the `<vdW>`
section of a SMIRNOFF force field file. Implementations of the SMIRNOFF specification should account
for this optional behavior. This option can be toggled by OpenMM, GROMACS, Amber, and likely other
simulation engines.

Given that long-range dispersion corrections are generally beneficial to turn on and are commonly
used, `long_range_dispersion="none"` will likely not be turned on by most users. This proposal does
not change the default value (`long_range_dispersion="isotropic"`). Therefore, the impact on most
users should be none because the usage should be low. This option may make it easier for users to
develop force fields if they desire to not include the long-range dispersion correction, which is
currently required. Because the correction, however small, is applied over the entire range `0 < r <
r_cutoff`, it may enable more accurate testing of different SMIRNOFF implementations.

## Backward compatibility

This OFF-EP does not modify any default behavior and is fully backwards-compatible.

## Detailed description

The `long_range_dispersion` option in the vdW section can now be `none`. This indicates that vdW
interactions no long-range dispersion correction term should be added to the vdW interactions.

The following line is added to the `<vdW>` section:

```
The long-range dispersion correction can optionally be ommitted (`long_range_dispersion="none"`).
```

## Alternatives

There is no alternative route to this behavior in the current SMIRNOFF specification. It can be
achieved by modifying the resulting objects after typing and parameterization, but this is precisely
the sort of user operation that having a force field specification is meant to prevent.

## Discussion

- [Shirts 2007](https://pubs.acs.org/doi/10.1021/jp0735987)
- [GROMACS option](https://manual.gromacs.org/documentation/current/user-guide/mdp-options.html#mdp-DispCorr)
- [OpenMM option](http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#lennard-jones-interaction)
- [Amber21 option](https://ambermd.org/doc12/Amber21.pdf) (`nodisper` ?)
- [LAMMPS option](https://docs.lammps.org/pair_modify.html) (`pair_modify tail yes`) - though this
  may have a [different form](https://pubs.acs.org/doi/10.1021/jp980939v)

## Copyright

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
