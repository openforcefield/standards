# OFF-EP 0005 — Allow different electrostatics methods to be used on period and non-periodic systems

**Status:** Accepted

**Authors:** Matt Thompson and John Chodera, Jeffrey Wagner, Simon Boothroyd

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
as a controlled approximation to Ewald provided the approximation accuracy is controlled.

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

Implementations may wish to add up-converters from old versions. An up-converter could convert the following tag header
```
<Electrostatics version="0.3" method="PME" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```
to a header using version 0.4, which for this case could be
```
<Electrostatics version="0.4" periodic_potential="Ewald3D-ConductingBoundary" nonperiodic_potential="Coulomb" exception_potential="Coulomb" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```

Concretely, the following conversions should be performed:

|  0.3 `method`    |  0.4 `periodic_potential`    |  0.4 `nonperiodic_potential`  |  0.4 `exception_potential`  |
|------------------|------------------------------|-------------------------------|-----------------------------|
|  `PME`           | `Ewald3D-ConductingBoundary` | `Coulomb`                     | `Coulomb`                   |
| `reaction-field` | `charge1*charge2/(4*pi*epsilon0)*(1/r + k_rf*r^2 - c_rf); k_rf=(cutoff^(-3))*(solvent_dielectric-1)/(2*solvent_dielectric+1); c_rf=cutoff^(-1)*(3*solvent_dielectric)/(2*solvent_dielectric+1)`             | `Coulomb`                     | `Coulomb`                   |
|  `Coulomb`       | `Coulomb`                    | `Coulomb`                     | `Coulomb`                   |

If the 0.3 section's `method` does not actually involve the use of a `cutoff` or `switch_width` (such as is the case if `method="PME"`), those values may be set to their defaults in the 0.4 `Electrostatics` section.

The value of the 0.4 `Electrostatics` section's `solvent_dielectric` should be set to `none`.

## Detailed description

### In the general SMIRNOFF spec description

A section is added stating that [CODATA 2018](https://physics.nist.gov/cuu/Constants/index.html) physical constants are used in all released SMIRNOFF versions to date.
Future OFF-EPs may migrate the specification of which self-consistent physical constants are used to a higher-level attribute.

### In the `Electrostatics` section

The `method` tag attribute is **removed** and replaced with `periodic_potential`, `nonperiodic_potential`, and `exception_potential`.

The optional `solvent_dielectric` tag attribute is added to specify the solvent dielectric used with finite-ranged potentials, defaulting to `none`.

For `periodic_potential`:

* `Ewald3D-ConductingBoundary` (default) denotes that the Ewald potential with conducting (dielectric 0) boundary conditions are used
* `Coulomb` denotes that the standard Coulomb potential should be used with specified cutoff `cutoff` and optionally switch width `switch_width`
* A function denotes that the specified function should be used, which may make use of `cutoff`, `switch_width`, and/or `solvent_dielectric` terms
* Future OFF-EPs may add specific keywords for common choices of reaction field electrostatics

For `nonperiodic_potential`:

* `Coulomb` (default) denotes that the standard Coulomb potential should be used with no cutoff or reaction-field attenuation
* A function denotes that the specified function should be used, which may make use of `cutoff`, `switch_width`, and/or `solvent_dielectric` terms

For `exception_potential`:

* `Coulomb` (default) denotes that the standard Coulomb potential should be used with no cutoff or reaction-field attenuation
* A function denotes that the specified function should be used, which may make use of `cutoff`, `switch_width`, and/or `solvent_dielectric` terms

## Examples

Ewald electrostatics (permitting PME to be used) are used for periodic systems; Coulomb used for non-periodic:
```
<Electrostatics version="0.4" periodic_cutoff="None" periodic_potential="Ewald3D-ConductingBoundary" nonperiodic_potential="Coulomb" exception_potential="Coulomb" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```

Shifted reaction field electrostatics (e.g. from [OpenMM](http://docs.openmm.org/7.6.0/userguide/theory/02_standard_forces.html#coulomb-interaction-with-cutoff)) are used for periodic systems; Coulomb used for non-periodic:
```
<Electrostatics version="0.4" periodic_potential="charge1*charge2/(4*pi*epsilon0)*(1/r + k_rf*r^2 - c_rf); k_rf=(cutoff^(-3))*(solvent_dielectric-1)/(2*solvent_dielectric+1); c_rf=cutoff^(-1)*(3*solvent_dielectric)/(2*solvent_dielectric+1)" solvent_dielectric="78.5" periodic_cutoff="12*angstroms" nonperiodic_potential="Coulomb" exception_potential="Coulomb" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
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
