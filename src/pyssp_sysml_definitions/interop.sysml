// Reusable interop vocabulary.  A model that imports PyfmiInterop::* gets the
// standalone FMU base and the shared deployment parameter port without
// re-authoring either type.
package PyfmiInterop {
  private import ScalarValues::*;
  private import PysspCore::*;

  // Interop identity and wire format metadata.  This is deliberately not
  // FmuMetadata: fmu_meta is the reserved FMI implementation slot and must
  // stay typed by FmuMetadata.
  attribute def InteropMetadata {
    attribute source : String;
    attribute serialization : String;
    attribute version : String;
  }

  // Deployment defaults for local development.  These are initialization
  // configuration: the master binds them as FMI parameters before
  // fmi2EnterInitializationMode, and they never become wire fields.
  port def InteropDeployment :> ParameterInterface {
    attribute transport : String = "loopback";
    attribute bind_address : String = "127.0.0.1:5000";
    attribute peer_address : String = "";
  }

  // A standalone interop FMU.  FmuModel supplies fmu_meta; do not redeclare
  // it here, because the FMI metadata slot is reserved for that type.
  part def FmuInterop :> FmuModel {
    attribute interop_meta : InteropMetadata;
    in port parameters : InteropDeployment;
  }
}
