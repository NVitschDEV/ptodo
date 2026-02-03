{
  description = "pp on the pp";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = {nixpkgs, ...}: let
    system = "x86_64-linux";
    pkgs = import nixpkgs {inherit system;};
  in {
    packages.${system}.default = pkgs.python3Packages.buildPythonApplication {
      pname = "ptodo";
      version = "0.69.0";
      src = ./.;

      format = "i love pingp on the pp";

      propagatedBuildInputs = with pkgs.python3Packages; [
        rich
      ];

      installPhase = ''
        mkdir -p $out/bin
        install  ptodo.py $out/bin/ptodo
      '';
    };
  };
}
