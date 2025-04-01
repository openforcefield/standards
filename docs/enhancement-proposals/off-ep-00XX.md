# OFF-EP X — Template

**Status:** Draft

**Authors:** Lily Wang

**Stakeholders:** &lt;list of stakeholders that would be affected by this proposal>

**Acceptance criteria:** 

**Created:** &lt;date created>

**Discussion:** &lt;link to the PR / issue where proposal is being discussed>

**Implementation:** &lt;link an example / reference implementation of the proposal>

## Abstract

This change adds a `<GNNCharges>` tag which describes a graph-convolutional neural network (GNN) that can be used to assign atomic partial charges.

## Motivation and Scope

OpenFF NAGL has built on existing work and trained a GNN that reproduced AM1-BCC partial charges for a substantial set of chemistries. Currently, there is not a canonical method by which these charges can be used in a SMIRNOFF force field. Generating partial charges from a GNN and passing them alongside a SMIRNOFF force field as prespecified charges works but is discouraged as this pathway exists only as a convenience to a user. Using an external tool to assign charges also bypasses the need to specify the contents of the GNN sufficient for somebody else to reimplement them. Developers and users for SMIRNOFF force fields would benefit from information about these GNNs being encoded directly into the force field itself.

The changes outlined in this proposal affect any consumer of SMIRNOFF force fields which include `<GNNCharges>`, which is likely to be the case for `openff-2.3.0` and beyond. Since it is not a required section, force field developers who choose to use other partial charge methods would not be affected. SMIRNOFF implementations must implement `<GNNCharges>`, by definition, to use force fields that include this section. Existing force fields cannot use this section, so they are not affected.

The introduction of this section lays the groundwork for supporting future models with improved performance and scope. This may include, for example:

- support for more elements
- improved runtime performance on large and/or complex molecule(s) such as biopolymers
- modelling of charge methods other than AM1-BCC
- models employing different architecture, featurization, and/or normalization techniques

OpenFF has produced a reference implementation of this section in its package OpenFF NAGL. The contents of this proposal derive from the current structure of OpenFF NAGL and the model(s) it implements. If this proposal is accepted, OpenFF NAGL will need minor updates to properly check its GNN implementation against the details encoded in a SMIRNOFF force field, but we expect these changes will be minor because the proposed changes derive directly from this software. The OpenFF Toolkit and Interchange will need minor updates to properly support this section and some edge cases that arise from using this section in combination with other section(s) and tools, such as prespecified charges and virtual site parameter which modify charges. Similar tools which also implement the encoded GNN and/or the SMIRNOFF specification more broadly will need similar updates.

This proposal does not include changes or interactions with sections that do not modify partial charges, such as `<vdW>`, `<Constraints>`, `<Bonds>`, `<Angles>`, etc.

# TODO: Describe where in the charge method hierarchy this exists
# TODO: Describe interaction(s) with virtual sites

## Usage and Impact

This section describes how users of the ecosystem will use features 
described in this SMIRNOFF EP. It should be comprised mainly of code / file 
examples that wouldn't  be possible without acceptance and implementation 
of this proposal, as well as the impact the proposed changes would have 
on the ecosystem. 

## Backward compatibility

This adds a new section which cannot meaningfully be converted to any existing sections.

## Detailed description

This proposal adds a section named `<GNNCharges`>. Version 0.1 of this section includes tags for

- a file containing model weights
- information about atom and bond features
- a description of the model architecture
- the reactions used for standardization.

The tag `weights` points to a file that includes models weights. This by convention is a PyTorch `.pt` file, but in principle could be any file that describe model weight as used by the GNN. By their nature, GNNs use many more weights than can reasonably be encoded into an XML file, so pointing to another file is an necessary and unavoidable layer of complexity.

The tag `AtomFeatures` includes a list of `AtomFeature`s, each of which describes a feature used by the model. Each feature includes descriptive a `name` attribute and other attribute-specific properties. The following attributes are supported:

- `"atomic_element"`, specifying also (in a comma-separated stringified list) the elements supported by the model, in the order in which they are one-hot encoded
- `"atom_connectivity"`, specifying also the range of values this feature can take
- `"atom_average_formal_charge"`
- `"atom_in_ring_of_size"`, specifying also an integer `"ring_size"`, the size of a ring that an atom is either in or not in

- The `AtomFeatures` tag includes an attribute `feature_size` which is a (stringified) integer of the total number of atom features. This should be redundant with the total number of atom features and serves as a consistency check.

The tag `BondFeatures` structurally mirrors the `AtomFeatures` section, but describes bond featurization with analogously-named elements.

The tag `Model` describes the model architecture of the GNN.

The tag `Standardizations` enumerates a number of reactions used for molecule standardization. Each `Reaction` contains a SMARTS string that describes a chemical reaction used in molecule standardization. This tag also has a `max_iter` attribute that specifies the maximum number of iterations used in the normalization process.

Below is an example `<GNNCharges>` section:

```xml
<GNNCharges weights="elm-v1.1.pt">
    <!-- specify precision? -->
    <!-- feature_size could be included as a check -- should sum to the total shape of feature tensor -->
    <AtomFeatures feature_size="21" >
        <!-- could include first_index, last_index as check if these are not ordered -->
        <AtomFeature name="atomic_element" categories="C,O,H,N,S,F,Br,Cl,I,P" />
        <AtomFeature name="atom_connectivity" categories="1,2,3,4,5,6" />
        <AtomFeature name="atom_average_formal_charge" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="3" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="4" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="5" />
        <AtomFeature name="atom_in_ring_of_size" ring_size="6" />
    </AtomFeatures>
    <BondFeatures>
        <BondFeature ... />
    </BondFeatures>
    <Model version="0.1">
        <!-- will stuff ever change per layer? Quite possible but also seems like overtuning -->
        <!-- how to incorporate architecture-specific arguments like aggregation_function? -->
        <!-- how to appropriately map layer weights and biases from the file to the actual layers? Just indexing? -->
        <ConvolutionModule activation_function="ReLU" n_hidden_layers="5" architecture="SAGEConv" hidden_feature_size="512" />
        <ReadoutModule activation_function="Sigmoid" n_hidden_layers="1" hidden_feature_size="128" pooling="atoms" output_features="initial_charge,electronegativity,hardness" postprocess_layer="regularized_compute_partial_charges">
        </ReadoutModule">
    </Model>
    <Standardizations max_iter="200">
        <Reaction reaction="[N,P,As,Sb;X3:1](=[O,S,Se,Te:2])=[O,S,Se,Te:3]>>[*+1:1](-[*-1:2])=[*:3]" />
        <Reaction reaction="[S+2:1]([O-:2])([O-:3])>>[S+0:1](=[O-0:2])(=[O-0:3])" />
        ...
    </Standardizations>
</GNNCharges>
```

## Alternatives

The first GNN trained with the intent to be shipped in SMIRNOFF force fields is one that models AM1-BCC partial
charges, so another solution could involve updating the existing `<ToolkitAM1BCC>` section instead of adding a new
section altogether. This might involve a new tag in the `<ToolkitAM1BCC>` section that distinguishes a particular GNN
from the existing QuacPac and/or `sqm`-based approach. This approach is limiting, however, since GNNs can be used to
predict other charge models than AM1-BCC; if a GNN was trained to ABCG2 or a RESP variant, it's not obvious if that
could drop in to `<ToolkitAM1BCC>`.

Another similar solution could involve not updating the SMIRNOFF specification at all and simply letting
implementations use GNNs in place of QuacPac or `sqm` as currently specified. This in principle produces the same
results, to the extent that the GNN accurately reproduces AM1-BCC charges, but is inconsistent with the philosophy that
the details of a force field must be communicated to users and not hidden from view.

The solution in this proposal makes clear to any person or tool inspecting a force field that GNNs are a different tool
than existing AM1-BCC charge providers. It attempts to provide enough detail that somebody could re-implement the same
GNN provided weights that are shipped alongside a force field. It allows for future modifications in which a different
underlying charge model is targeted.

## Discussion

This section may just be a bullet list including links to any discussions
regarding the proposal:

- This includes links to mailing list threads and / or relevant GitHub issues.

## Copyright

*This template is based upon the [``numpy`` NEP template](
https://github.com/numpy/numpy/blob/master/doc/neps/nep-template.rst) and the
[``conda-forge`` CFEP template.](https://github.com/conda-forge/cfep/blob/master/cfep-00.md)*

*All OFF-EPs are explicitly [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).*
