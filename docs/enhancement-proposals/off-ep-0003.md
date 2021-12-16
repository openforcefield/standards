# OFF-EP 0003 — Allow fractional bond order interpolation between arbitrary fractional bond order interpolation points

**Status:** Proposed

**Authors:** Matt Thompson, matt.thompson@openforcefield.org

**Stakeholders:** David Mobley, John Chodera, Jeffrey Wagner, Simon Boothroyd

**Acceptance criteria:** Unanimity

**Created:** 2021-11-23

**Discussion:** [Issue #8](https://github.com/openforcefield/standards/issues/8)

**Implementation:** [PR #23](https://github.com/openforcefield/standards/pull/23)

## Abstract

This OFF-EP explicitly documents that non-integer bond orders can be used for interpolating parameters.

## Motivation and Scope

The SMIRNOFF specification describes a process by which fractional bond orders can be used to
interpolate parameters for
[bond](https://openforcefield.github.io/standards/standards/smirnoff/#fractional-bond-orders) and
[proper
torsion](https://openforcefield.github.io/standards/standards/smirnoff/#fractional-torsion-bond-orders)
forces. The examples provided use bond orders of 1 and 2 as the basis of interpolation between
their associated parameters. Work by the Open Force Field Initiative has suggested cases in which it
would be useful to have non-integer bond orders such that i.e. parameters are interpolated between
bond orders of 1.0 and 1.2 in a different way than they may be between bond orders of 1.2 and 2.0.
The current specification does not explicitly forbid non-integer bond orders, but the section
describes the process of parameter interpolation using an example that does. Also, the current
implementation in the OpenFF Toolkit does not support non-integer bond orders.

## Usage and Impact

In practice, most bonds in molecules have bond orders very near 1.0 or 2.0 and values such as 1.5
are much less common. This results in training data being clumped near 1.0 and 2.0 and often the
slopes of each cluster are not identical. For example, the slope associated with a cluster at 1.0 -
1.2 might be different from a cluster at 1.8-2.0. @pavankum describes this in more detail in
[issue #8](https://github.com/openforcefield/standards/issues/8). Being able to have different
slopes associated with each cluster, i.e. by using 1.0, 1.5, and 2.0 instead of just 1 and 2, would
enable a force field to account for these differences. Such a parameter may look like

```
<Bonds version="0.3" potential="harmonic" fractional_bondorder_method="AM1-Wiberg" fractional_bondorder_interpolation="linear">
    <Bond
        smirks="[#6X3:1]!#[#6X3:2]"
        k1="820.0*kilocalories_per_mole/angstrom**2"
        k2="1000.0*kilocalories_per_mole/angstrom**2"
        k3="1098*kilocalories_per_mole/angstrom**2"
        length1="1.45*angstrom"
        length2="1.43*angstrom"
        length3="1.35*angstrom"
        bondorder1="1.0"
        bondorder2="1.5"
        bondorder3="2.0"

    />
/>
```

## Backward compatibility

This OFF-EP adds an attribute to the `<Bonds/>` and `<ProperTorsions/>` sections that is required in
order to use parameter interpolation. No functionality is removed, so forwards compatibility could
be provided with a converter. Functionality is added, however, so backwards compatbility cannot be
guaranteed.

## Detailed description

This section should provide a detailed description of the proposed
change. It should include examples of how the new functionality would be
used, intended use-cases and pseudo-code illustrating its use.

The following is added to the `Fractional torsion bond orders` subsection of the
`<ProperTorsions>` section.

## Alternatives

There is no alternative route to this behavior in the current SMIRNOFF specification.

## Discussion

- [Issue #8](https://github.com/openforcefield/standards/issues/8)

## Copyright

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
