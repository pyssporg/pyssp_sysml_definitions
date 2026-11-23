package PysspCore {
  
  // Role contract.  Every fact a model declares has exactly one of three
  // roles, and its carrier decides which:
  //
  //   build metadata    a typed attribute container (FmuMetadata,
  //                     SspMetadata, DefaultExperiment/Experiment).
  //                     Build-time configuration; never a connector and
  //                     never a wire field.
  //   initialization    a parameter interface (port def :> ParameterInterface,
  //                     used as `in port parameters : <PortDef>`) or a
  //                     parameter set (attribute def :> ParameterSet plus
  //                     `bind`).  Applied before initialization.
  //   runtime signal    every other port.  Propagates as an input or output.
  //
  // A parameter interface must use the reserved usage name `parameters`.
  // Rationale, examples, and anti-patterns: docs/roles.md.

  // Build-metadata role: shared base for containers that name an external
  // artifact.
  attribute def SourcedMetadata {
    attribute source : String;
  }
  
  attribute def FmuMetadata :> SourcedMetadata {
    attribute implementation : String;
  }
  
  attribute def SspMetadata :> SourcedMetadata;
  
  part def Analysis;

  // Initialization role: the interface is a port def, the set is an attribute
  // def.  Neither is a runtime signal.
  port def ParameterInterface;
  attribute def ParameterSet;
  
  part def SspModel {
    attribute ssp_meta : SspMetadata;
  }
  part def FmuModel {
    attribute fmu_meta : FmuMetadata;
  }

  // Build-metadata role: experiment containers.  ssd:DefaultExperiment
  // (SSP 2.0.1) carries only startTime and stopTime.
  attribute def DefaultExperiment {
    attribute startTime : Real;
    attribute stopTime : Real;
  }

  // fmi2:DefaultExperiment: all four are optional in the FMI 2.0.5 XSD, so
  // Experiment is the FMI superset.
  attribute def Experiment :> DefaultExperiment {
    attribute stepSize : Real;
    attribute tolerance : Real;
  }
}
