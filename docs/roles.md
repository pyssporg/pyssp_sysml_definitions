# Roles: build metadata, initialization configuration, runtime signal

Status: current. This is the long-form statement of the contract that
`src/pyssp_sysml_definitions/core.sysml` states in short. The two are the same
contract; if they disagree, `core.sysml` is what consumers load.

## Why a role contract

A SysML architecture mixes facts with very different lifetimes:

- a source path is needed to build the artifact and means nothing once it
  exists;
- a gain is chosen before initialization and then held, or retuned on purpose;
- a measured value changes at every communication step.

If the model does not say which fact is which, every consumer decides for
itself. That produces three familiar failures: build data ends up on the wire,
an initialization value is wired as a signal, or a runtime value is frozen into
a parameter and silently stops propagating. The fix is one classification at
the vocabulary level; an artifact family then only decides how each role lands
in its own format.

## The three roles

| role | carrier | lifetime | becomes a connector or variable? |
|---|---|---|---|
| build metadata | typed attribute container that reaches `SourcedMetadata` (`FmuMetadata`, `SspMetadata`, and family containers such as `InteropMetadata`), or an experiment container (`DefaultExperiment`/`Experiment`) | the build | never |
| initialization configuration | parameter interface (`port def :> ParameterInterface`, used as `in port parameters : <PortDef>`) and parameter sets (`attribute def :> ParameterSet` applied with `bind`) | chosen before initialization; held for the run unless the artifact declares it tunable | yes, with the parameter role |
| runtime signal | every other port | the run | yes, as input or output |

Metadata is configuration of the artifact itself: where it comes from, how it
is packaged, and the experiment defaults it carries. Initialization
configuration describes the state the artifact starts from. Runtime signals are
the information that propagates between artifacts after initialization.

## The carrier decides, not the name

Recognition is by type:

- an attribute whose `attribute def` reaches `SourcedMetadata` — directly, or
  through a family container — is build metadata, as is an experiment
  container;
- a `port def` that reaches `ParameterInterface` is an initialization
  interface;
- an `attribute def` marked `:> ParameterSet` is a parameter set;
- every other port is a runtime signal.

A name convention ("anything ending in `Metadata`") drifts silently, because a
typo is still a valid name. A supertype is checkable, and the drift test in
`pycps_sysml/tests/test_definition_markers.py` keeps the vocabulary and the
code constants in step.

## The reserved interface name

A parameter interface is typed like any port but found under the reserved usage
name `parameters`. The dialect could scan every port for the marker instead. It
does not: one reserved name means a component has exactly one parameter
interface, and every consumer agrees where its parameters live without a
tie-break.

The rule is enforced, not assumed: a `ParameterInterface` port under any other
name is a validation error. Before that check existed, exporters skipped such a
port without a word, so its parameters disappeared from the artifact.

## Worked example

```sysml
package Aircraft {
  private import PysspCore::*;

  // Build metadata: consumed by the build, never simulated.
  attribute def SensorFmu :> FmuMetadata {
    attribute source = "build/fmus/Sensor.fmu";
    attribute implementation = "CoSimulation";
  }

  // Initialization configuration: defaults chosen before initialization.
  port def SensorParameters :> ParameterInterface {
    attribute sampleRate : Real = 100.0;
    attribute noiseFloor : Real = 0.01;
  }

  // Runtime signal: a value that changes during the run.
  port def Voltage {
    attribute value : Real;
  }

  part def Sensor :> FmuModel {
    attribute fmu_meta : SensorFmu;
    in port parameters : SensorParameters;
    out port voltage : Voltage;
  }

  attribute def NominalCalibration :> ParameterSet {
    attribute sampleRate = 100.0;
    attribute noiseFloor = 0.02;
  }

  part def System {
    part sensor : Sensor;
    attribute nominal : NominalCalibration;
    bind sensor.parameters.noiseFloor = nominal.noiseFloor;
  }
}
```

Reading the example by role:

- `fmu_meta` is build metadata. It says which `.fmu` to package; no consumer
  turns it into a connector or a variable.
- `parameters` is initialization configuration. The interface declares the
  schema and the set supplies an alternative value through `bind`.
- `voltage` is a runtime signal. Member direction (`out`) decides input versus
  output; that is a wiring question, not a role question.

`src/pyssp_sysml_definitions/interop.sysml` is the shipped worked example:
`InteropDeployment` is initialization configuration bound before initialization
and never a wire field.

## Anti-patterns

- **Metadata as a plain attribute.** An untyped `attribute source = "..."` on a
  leaf is a flat parameter, and the parameter dialect rejects it. Type it with
  a container that reaches `SourcedMetadata`.
- **An interface port under another name.** `in port gains : GainParameters`
  where `GainParameters :> ParameterInterface` is an error. Use
  `in port parameters : GainParameters`.
- **A runtime value declared as a parameter.** Giving a signal a start value
  does not make it initialization configuration. Declaring it as a parameter
  removes it from propagation.
- **A build-time fact declared as a parameter.** A structural choice (source
  path, serialization backend, role) in a parameter set lands in an SSV or an
  FMI start value and invites tuning of something that is fixed by construction.

## Where this lands

This package owns the roles and the carriers. It does not own any artifact
format, so it does not say how a role is written into SSD, SSV, SSM, or FMI
XML. Each artifact family states that once for its own format and references
this contract:

- short contract: `src/pyssp_sysml_definitions/core.sysml`;
- recognition and validation: `pycps_sysml` (`docs/breakdown/02-architecture/dialect.md`);
- SSP-family landing: `pyssp_sysml` (`docs/building-on-pyssp-sysml.md`);
- FMI landing: `pyfmi_sysml` and `pyfmi_interfaces`.
