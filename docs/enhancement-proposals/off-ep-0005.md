# OFF-EP 0005 — Allow different electrostatics methods to be used on period and non-periodic systems

**Status:** Proposed

**Authors:** Matt Thompson

**Stakeholders:** Karmen Condic-Jurkic, Jeffrey Wagner, David Mobley, John Chodera

**Acceptance criteria:** Unanimity

**Created:** 2020-02-18

**Discussion:** [Issue #29](https://github.com/openforcefield/standards/issues/29)

**Implementation:** [``openff-standards``](https://github.com/openforcefield/openff-standards)

## Abstract

This change allows for the `<Electrostatics>` tag to optionally specify that different methods
shouuld be used for periodic (i.e. condensed-phase) and non-periodic (i.e. gas phase) systems. This
in particular enables a force field to specify that PME should be used for periodic systems and no
cutoff should be used for non-periodic systems.

## Motivation and Scope

In version 0.3 of the `<Electrostatics>` tag, the default and most commonly-used electrostatics
method is PME (`method="PME")`. It is, however, not compatible with non-periodic systems, such as
gas-phase and/or single-molecule systems. In practice, force fields defined with PME are modified by
users in ways that make them compatible with non-periodic systems, such as the
[``NoCutoff``](http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html?highlight=nocutoff#coulomb-interaction-without-cutoff)
option provided by OpenMM's ``NonbondedForce``.

Given that is it not tractable to use (much less train) a force field that can only be applied to
periodic OR non-periodic systems, this OFF-EP proposes that the `<Electrostatics>` tag may specify
that different methods should be used for each kinda of systems.

This OFF-EP
* does not propose changes any detail of the `<vdW>` section
* does not alter the intended meaning of `method="PME"`
* does not add allowed methods for non-periodic systems (still only `Coulomb`), but does require
  explicitly specifying what is used for non-periodic systems

Each of the above points are important and worthy of consideration but should be scoped to separate OFF-EPs.

## Usage and Impact

Since most force fields use some flavor of PME for periodic systems and something similar to
`method_nonperiodic="Coulomb"` for non-periodic systems, the default attributes for this tag will
likely be the most commonly-used. Splitting `method` out into two attributes, however, makes it less
ambiguous how electrostatics should be handled in each case and decouples the method used in each
case. Users are recommended to consider upgrading from the default attribute values of 0.3 to 0.4 to avoid
continuing to use this ambiguity. Implementations may wish to execute this up-conversion
automatically (see below).

The impact to a vast majority of users should be limited to needing to modify this line in their
force field files. Non-standard electrostatics settings are not generally covered here and should be
the focus of future OFF-EPs.

## Backward compatibility

Version 0.4 of this tag is backwards-incompatible with older versions because the information
content is different. It is ambiguous how to map both `method_periodic` and `method_nonperiodic`
back down to a single `method` and it is not recommended to try doing so.

Implementations may wish to add up-converters from old versions. A common up-converter could convert the
following tag header

```
<Electrostatics version="0.3" method="PME" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```

to the equivalent of reading

```
<Electrostatics version="0.4" method_periodic="PME" method_nonperiodic="Coulomb" scale12="0.0" scale13="0.0" scale14="0.833333" scale15="1.0"/>
```

This is likely desirable for implementations such as the OpenFF Toolkit in which the information
content of the version 0.4 snippet represents what is it currently does.

## Detailed description

The `method` tag attribute is **removed** and replaced with `method_periodic` and `method_nonperiodic`.
The deault values of each are `"PME"` and `"Coulomb"`, respectively. The following section is added
to justify and describe these new methods:

```
Some methods for computing electrostatics interactions are not valid for periodic systems, so
separate methods must be specified for periodic (`method_periodic`) and non-periodic
(`method_nonperiodic`) systems.
```

It is clarified that the allowed values of `method_periodic` are `PME` and `reaction-field` and that the only
allowed value of `mehtod_nonperiodic` is `Coulomb`.

A clause is added to the description of the `Coulomb` method that makes it clear how it can be
implemented in engines like GROMACS that do not support an equivalent of OpenMM's
[``NonbondedForce.NoCutoff``](http://docs.openmm.org/latest/userguide/theory/02_standard_forces.html?highlight=nocutoff#coulomb-interaction-without-cutoff):

```
* `Coulomb` - direct electrostatics interactions should be used without reaction-field attenuation and
  no cut-off (or with a cutoff that is larger than any intermolecular distance).
```

## Alternatives

Resolving this incompatibility could be left to implementation, as it has been for years. This is not
desirable as a general principle of maintaining specifications.

This could be resolved by mandating that separaate force fields should be used for periodic and
non-periodic systems. This would be a clunky user experience and should be avoided.

## Discussion

- Toolkit [#1084](https://github.com/openforcefield/openff-toolkit/issues/1084)
- Standards [#29](https://github.com/openforcefield/standards/issues/29)

## Copyright

This template is based upon the
[OFF-EP template](https://openforcefield.github.io/standards/enhancement-proposals/off-ep-template/).

This document is explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
