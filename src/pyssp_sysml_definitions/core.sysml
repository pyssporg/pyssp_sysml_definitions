package PysspCore {
  
  // Shared base for containers that name an external artifact.
  attribute def SourcedMetadata {
    attribute source : String;
  }
  
  attribute def FmuMetadata :> SourcedMetadata {
    attribute implementation : String;
  }
  
  attribute def SspMetadata :> SourcedMetadata;
  
  part def Analysis;
  port def ParameterInterface;
  attribute def ParameterSet;
  
  part def SspModel {
    attribute ssp_meta : SspMetadata;
  }
  part def FmuModel {
    attribute fmu_meta : FmuMetadata;
  }

  // ssd:DefaultExperiment (SSP 2.0.1): only startTime and stopTime.
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
