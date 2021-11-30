# OFF-EP 0002 — Support vdW interactions with a hard cut-off

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

In most use cases involving force fields, vdW interactions are truncated at cutoff distance because
the size of neighbor lists increases as the number of particles squared. This stepwise change in the
potential energy function introduces an artifact that is later corrected (in part) by adding some
sort of tail correction term. There are many ways to implement this, often including polynomial
smoothing functions that are implemented in incompatible ways by different simulation engines.  The
SMIRNOFF specification currently has an option that encodes this: `long_range_dispersion`, with a
default value of `"isotropic"`. This is insufficient, but left for a future OFF-EP.  Because of
these differences in how the potential energy function is actually computed, this complexity can
make it difficult to compare the results of using SMIRNOFF force fields with different engines; the
actual result depends on more than the functional form of the 12-6 Lennard-Jones potential and the
parameter values associated with each particle. For testing the application of SMIRNOFF force fields
in different engines, the most precise way around this complexity is by not introducing tail
corrections at all. Because of a discontinuity in the force at the cutoff distance, this is
dubious for most scientific applications.

This OFF-EP adds `none` to the list of allowed values for the `long_range_dispersion` tag in the
`<vdW>` section. This option communicates that the vdW interactions should be truncated with no tail
correction, reaction field attenuation, or other modification for long-range interactions. It does
not make it the default value, so existing SMIRNOFF force fields and implementations should not be
affected by it.  Since it is strictly bad for a vast majority of force field use cases, it likely
will only be used by downstream developers while testing implementations of SMIRNOFF, not by
scientists using SMIRNOFF force fields.

## Usage and Impact

This option will make it easier to test the use of SMIRNOFF force fields in different engines. Each
engine - even if given identical parameters, particle positions, and non-bonded functional forms -
will not likely produce quantitatively similar non-bonded energies without this option being set.
With this option, there still may be some differences but a large portion of the complexity of
different implementations is sidestepped. The intent is that `long_range_dispersion="none"` will
make it more likely that differences non-bonded energy evaluations produced by different engines are
more likely due to genuinely different parameters being passed to them, not differences in how they
each implement tail corrections.

Using hard cut-offs is a non-starter for virtually all of the applications broadly targeted by the
SMIRNOFF specification. The default value (`long_range_dispersion="isotropic"`) remains unchanged
and `long_range_dispersion="none"` should seldom be used by scientists.

As a non-default value, no implementation should result in this option accidentally being used.

## Backward compatibility

This OFF-EP does not modify existing sections or options in the specification and should be fully
backwards-compatible.

## Detailed description

The `long_range_dispersion` option in the vdW section can now be `none`. This indicates that vdW
interactions should be cut off with no tail correction, reaction-field attenuation, or other
modifcation used at all. The following line is added to the `<vdW>` section:

``` Interactions can also be truncated with no long-range dispersion correction, reaction-field
attenuation, or other modification for long-range interactions. (`long_range_dispersion='none'`).
```

## Alternatives

There is no alternative route to this behavior in the current SMIRNOFF specification. It can be
achieved by modifying the resulting objects after typing and parameterization, but this is precisely
the sort of user operation that having a force field specification is meant to prevent.

## Discussion

- [Toolkit issue  #191](https://github.com/openforcefield/openff-toolkit/issues/191#issuecomment-476842873)
- [GROMACS](https://manual.gromacs.org/documentation/current/user-guide/mdp-options.html#mdp-value-vdwtype=Cut-off)  implementation (`vdwtype = Cut-off`)
- [OpenMM](http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html?highlight=cutoffnonperiodic#coulomb-interaction-with-cutoff) implementation (`CutoffPeriodic` or `CutoffNonPeriodic`)
  - Note that reaction-field attentuation [cannot be turned off](https://github.com/openmm/openmm/issues/397), so this is not currently compatible with OpenMM's `NonbondedForce`.
- [Amber21](https://ambermd.org/doc12/Amber21.pdf) implementation (`vdwmeth=0`)
- [LAMMPS](https://docs.lammps.org/pair_modify.html) implementation (`pair_modify shift no`)

## Copyright

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
