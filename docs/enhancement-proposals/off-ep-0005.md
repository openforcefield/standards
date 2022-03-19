# OFF-EP 0005 — Allow different electrostatics methods to be used on period and non-periodic systems

**Status:** Proposed

**Authors:** Matt Thompson and John Chodera

**Stakeholders:** Simon Boothroyd, Jeffrey Wagner, David Mobley, John Chodera

**Acceptance criteria:** Unanimity

**Created:** 2020-03-15

**Discussion:** [Issue #29](https://github.com/openforcefield/standards/issues/29)

**Implementation:** [``openff-standards``](https://github.com/openforcefield/openff-standards)

## Abstract

This change refines the way the `<Electrostatics>` tag defines behavior in periodic
(i.e., condensed-phase) and non-periodic (i.e., gas phase) systems to clarify the
intended true electrostatics models in each case. Implementations are permitted
to make approximations to these specified models---e.g. Particle-Mesh Ewald (PME)---
as a controlled approximation to Ewald) provided the approximation accuracy is controlled.

## Motivation and Scope

In version 0.3 of the `<Electrostatics>` tag, the default electrostatics method is
`method="PME"`, with `reaction-field` also a permitted choice.

These definitions present several issues that this OFF-EP attempts to solve:
* `PME` is intended to be a permissible approximation to the true electrostatics model, Ewald
* The boundary conditions (e.g. dielectric at infinity) for the Ewald sum are not specified
* The Ewald method is only intended for periodic systems; unmodified vacuum electrostatics are intended for non-periodic systems
* The treatment of intramolecular electrostatics exceptions is unspecified
* The choice `reaction-field` does not uniquely specify the functional form for the true reaction-field model intended; many variants are available
* The solvent dielectric constant was not specified.
* Cutoffs were not specified
* The physical constants used to compute the potential were unspecified

To solve these issues, this OFF-EP proposes:
* The `method` attribute is replaced with `periodic_potential` in analogy to other parameters that use the `potential` term to specify the functional form or a common choice
* The `periodic_potential` attribute defaults to `Ewald3D-ConductingBoundary` as a valid keyword that states that the Ewald periodic sum with conducting boundary conditions should be the true potential used for periodic systems
* PME (and other methods) are permissible approximations to Ewald as long as they are controlled.
* For reaction field or other methods, the `periodic_potential` can specify the exact functional form used for the periodic potential or a keyword denoting a common choice, along with the optional `cutoff` and `solvent_dielectric` attributes
* The `nonperiodic_potential` attribute defaults to `Coulomb` indicating the Coulomb potential is to be used in non-periodic systems, though other functional forms are accepted.
* The `exception_potential` attribute defaults to `Coulomb`, indicating the Coulomb potential is to be used for exceptions, though other functional forms are accepted.
* We explicitly specify which self-consistent physical constants should be used.

We leave these to future extensions:
* We reserve the possibility of adding a `nonperiodic_potential` keyword at a future date should it become necessary to permit different choices for non-periodic systems
* We reserve the possibility of adding specific keywords to specify reaction field potentials for `periodic_potential`

## Usage and Impact

Since most force fields use some flavor of PME for periodic systems and something similar to
`nonperiodic_potential="Coulomb"` for non-periodic systems, the default attributes for this tag will
likely be the most commonly-used. Splitting `method` out into explicit attributes to specify periodic,
nonperiodic, and exception potential energy terms, however, makes it less
ambiguous how electrostatics should be handled in each case and decouples the method used in each
case.

Users are recommended to consider upgrading from the default attribute values of 0.3 to 0.4 to avoid
continuing to use this ambiguity. Implementations may wish to execute this up-conversion automatically (see below).

If backward-compatibility is provided as specified below, users of old force fields will not need to update their force field definitions.

## Backward compatibility

To minimize pain in implementations, we can allow implementations continue to accept `method="PME"` as a synonym for `periodic_potential="Ewald3D-ConductingBoundary"` for a few releases,
issuing a warning that the spec has changed and this behavior may be removed in a future release.

Implementations may wish to add up-converters from old versions. An up-converter could convert the following tag header
```
<Electrostatics version="0.3" method="PME" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```
to a less ambiguous header using version 0.4, which for this case could be
```
<Electrostatics version="0.4" periodic_potential="Ewald3D-ConductingBoundary" nonperiodic_potential="Coulomb" exception_potential="Coulomb" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```

## Detailed description

[CODATA 2018](https://physics.nist.gov/cuu/Constants/index.html) physical constants are used.
Future OFF-EPs may migrate the specification of which self-consistent physical constants are used to a higher-level attribute.

The `method` tag attribute is **removed** and replaced with `periodic_potential`, `nonperiodic_potential`, and `exception_potential`.

The optional `cutoff` tag attribute is added to specify the cutoff used for `periodic_potential` if applicable, defaulting to `None`.
No value of `cutoff` is allowed for Ewald methods---only finite-ranged methods.

The optional `solvent_dielectric` tag attribute is added to specify the solvent dielectric used with finite-ranged potentials, defaulting to `78.5`.

For `periodic_potential`:
* `Ewald3D-ConductingBoundary` denotes that the Ewald potential with conducting (dielectric 0) boundary conditions are used
* `Coulomb` denotes that the standard Coulomb potential is used with specified cutoff `cutoff`
* A function denotes that the specified function is used with specified cutoff `cutoff` and optionally `solvent_dielectric`
* Future OFF-EPs may add specific keywords for common choices of reaction field electrostatics

For `nonperiodic_potential`:
* `Coulomb` denotes that the standard Coulomb potential is used (without reaction field attenuation) with optional specified cutoff `cutoff`
* A function denotes that the specified function is used with optional specified cutoff `cutoff` and optionally `solvent_dielectric`

For `exception_potential`:
* `Coulomb` denotes that the standard Coulomb potential is used with no cutoff
* A function denotes that the specified function is used with no cutoff and optionally `solvent_dielectric`

## Examples

Ewald electrostatics (permitting PME to be used) are used for periodic systems; Coulomb used for non-periodic:
```
<Electrostatics version="0.4" cutoff="None" periodic_potential="Ewald3D-ConductingBoundary" nonperiodic_potential="Coulomb" exception_potential="Coulomb" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```

Shifted reaction field electrostatics (e.g. from [OpenMM](http://docs.openmm.org/7.6.0/userguide/theory/02_standard_forces.html#coulomb-interaction-with-cutoff)) are used for periodic systems; Coulomb used for non-periodic:
```
<Electrostatics version="0.4" periodic_potential="charge1*charge2/(4*pi*epsilon0)*(1/r + k_rf*r^2 - c_rf); k_rf=(cutoff^(-3))*(solvent_dielectric-1)/(2*solvent_dielectric+1); c_rf=cutoff^(-1)*(3*solvent_dielectric)/(2*solvent_dielectric+1)" solvent_dielectric="78.5" cutoff="12*angstroms" nonperiodic_potential="Coulomb" exception_potential="Coulomb" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```

## Alternatives

See [OFF-EP 0005](https://github.com/openforcefield/standards/pull/30).

## Discussion

- Toolkit [#1084](https://github.com/openforcefield/openff-toolkit/issues/1084)
- Standards [#29](https://github.com/openforcefield/standards/issues/29)
- Alternatives: [OFF-EP 0005](https://github.com/openforcefield/standards/pull/30)

## Copyright

This template is based upon the
[OFF-EP template](https://openforcefield.github.io/standards/enhancement-proposals/off-ep-template/).

This document is explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
