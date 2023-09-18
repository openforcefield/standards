# OFF-EP 0009 — Add LJPME

**Status:** Submitted

**Authors:** Matt Thompson, John Chodera

**Acceptance criteria:** Unanimity (4 approving reviews) or partial support (2 approvals and 2 week period with no reviews requesting changes)[https://openforcefield.atlassian.net/wiki/spaces/MEET/pages/2638774273/09-05-23+SMIRNOFF+Committee+Meeting]

**Stakeholders:**

**Created:** 2023-09-05

**Discussion:** [PR #40](https://github.com/openforcefield/standards/pull/40), [PR #44](https://github.com/openforcefield/standards/pull/44), [Issue #11](https://github.com/openforcefield/standards/issues/11), [Toolkit issue #989](https://github.com/openforcefield/openff-toolkit/issues/989#issuecomment-862792421), [OFF-EP-0008](https://github.com/openforcefield/standards/pull/53#issuecomment-1661316600)

**Implementation:** [``openff-standards``](https://github.com/openforcefield/openff-standards)

## Abstract

This change adds `periodic_method="Ewald3D"` as a supported attribute value in the `<vdW>` tag.

## Motivation and Scope

There are compelling reasons for force fields to handle long-range vdW interactions with an Ewald sum (so-called LJPME, used here synonymously) analogously to how electrostatics are conventionally handled, despite the increased computational cost. While tail corrections largely mediate the errors introduced by cutting off vdW interactions before they naturally decay to zero, they do so imperfectly, particularly in nonisotropic systems. These differences, even if small, also imply that a force field fitted with cut-off vdW interactions would not likely perform as well if LJPME is used. Additionally, without LJPME, some observables may have substantially different values depending on the user-selected cutoff.

LJPME is only valid for periodic systems, so the `nonperiodic_method` attribute is unaffected.

LJPME does not involve a tail correction or long-range dispersion correction, as these are only relevant with cut-off vdW interactions. These attributes should be ignored if LJPME is used.

There are many details and user-provided options in various PME implementations that might affect results; this proposal does not attempt to resolve them and instead suggests that a future OFF-EP should handle these questions (i.e. [Issue #50](https://github.com/openforcefield/standards/issues/50)).

## Usage and Impact

LJPME is widely implemented in modern molecular simulation engines including [OpenMM](http://docs.openmm.org/8.0.0/api-python/generated/openmm.openmm.NonbondedForce.html?highlight=ljpme), [GROMACS](https://manual.gromacs.org/current/reference-manual/functions/long-range-vdw.html#lennard-jones-pme), Amber, CHARMM, and [LAMMPS](https://docs.lammps.org/pair_lj_long.html). Each implementation may differ slightly in its details; this proposal treats LJPME identically to PME for Coulombic interactions and leaves these differences unresolved.

Some implementations may use the following approximations:

- Used with the 12-6 Lennard-Jones potential, where $r^12$ is short-range and the $r^6$ term is long-range, the $r^12$ term is excluded from the reciprocal space calculations.
- In reciprocal space, only geometric mixing rules are supported.

While engine support for LJPME is strong, there may be compatibility issues in downstream methods such as free energy calculations or the use of non-Lennard-Jones potentials. We estimate these to be relatively rare and that a vast majority of use cases will be able to use LJPME in a general force field without major hindrance.

Users may themselves wish to tinker with options specified in a SMIRNOFF force field, such as not using LJPME even if `periodic_method="Ewald3D"` is specified. There is nothing a force field specification can do to prevent modifications like this, identically to other potentially-disruptive user modifications such as changing the cut-off distance.

This proposal only adds a non-default option and does not make recommendations of which option is best.

In this first iteration, `periodic_method="Ewald3D"` is only compatible with `potential="Lennard-Jones-12-6"`, which is currently the only supported value. Future changes to the `potential` attribute should discuss compatibility with LJPME, if any, including which terms can be ignored in reciprocal space.

## Backward compatibility

This proposal only *adds a new supported value* for one attribute and makes no other changes, so it should be backwards-compatible with all current and compliant implementations. Conversion from version 0.4 should not change the information content of an OFFXML file or in-memory representation.

This proposal bumps the version of the vdW section from 0.4 to 0.5 with only the being that `"Ewald3D"` is a supported value for `periodic_potential`.

## Detailed description

This change adds `"Ewald3D"` as a supported value of the `periodic_method` attribute in the `<vdW>` tag:

```
* `Ewald3D`: a method like [particle mesh Ewald](https://docs.openmm.org/latest/userguide/theory.html#coulomb-interaction-with-particle-mesh-ewald) should be used. This is only compatible with `potential="Lennard-Jones-12-6"`.
```

The description is nearly identical to how the `periodic_potential` attribute of the `<Electrostatics>` section is described.

This change corresponds to a bump in the vdW version from 0.4 to 0.5. All other aspects of the vdW section remain unchanged, including the default `"periodic_method="cutoff"`.

## Alternatives

[OFF-EP-0007b](https://github.com/openforcefield/standards/pull/44) includes this change as part of a larger overhaul with long-range dispersion corrections. That was introduced before [OFF-EP-0008](https://github.com/openforcefield/standards/pull/53) split the `method` attribute into `periodic_method` and `nonperiodic_method` attributes and it placed the LJPME option within a new `long_range_treatment` attribute. This might lead to confusing and self-inconsistent combinations of attribute values such as

```XML
<vdW ... periodic_method="cutoff" nonperiodic_method="no-cutoff" long_range_treatment="Ewald3D-ConductingBoundary" </vdW>
```

This proposal suggests that `nonperiodic_method` is a more natural place to specify the use of LJPME.

This proposal does not attempt to generally resolve current ambiguities in long-range disperson treatment or how cut-off vdW interactions are handled.

## Discussion

Several details were brought up in a [SMIRNOFF meeting](https://openforcefield.atlassian.net/wiki/spaces/MEET/pages/2638774273/09-05-23+SMIRNOFF+Committee+Meeting), including:

- Ewald summation can be efficiently implemented via [PME](https://doi.org/10.1063/1.464397).
- The use of PME for electrostatics interactions usually relies on a conducting periodic boundary (so-called "tin foil" boundary condiditions). There might be an analogous boundary condition used in LJPME implementations, but it's not obvious and there is nothing in LJ/vdW interactions that makes a clear analogy to the dielectric constant.
- Implementations with 12-6 Lennard Jones potentials are generally restricted to the $1/r^6$ term since the $1/r^{12}$ term is short-ranged only and ignoring it introduces no or negligible error.
  - Modified Lennard-Jones with stronger repulsive terms (i.e. 14-6) should be feasible, still ignoring the repulsive term, but engines may not (yet) support this.
  - Whether or not this assumption holds well for non-LJ potentials (such as a [double exponential potential](https://doi.org/10.1039/d3dd00070b)) is not yet explored.
- Switching from Lorentz–Berthelot to geometric mixing rules in reciprocal space (long distance, past the cutoff or direct/reciprocal space transition) has been claimed to introduce [only a small error](https://doi.org/10.1021/acs.jctc.5b00726). The authors emphasize that non-LJPME methods wouldn't include any interactions at these distances anyway.
- The Ewald3D solution can technically be extended to support any $1/r^{2n}$ powers, but we are not considering this for now.

## Copyright

* This was seeded from the
[OFF-EP template](https://github.com/openforcefield/standards/blob/main/docs/enhancement-proposals/off-ep-template.md),
which was is based upon the
[``numpy`` NEP template]( https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
