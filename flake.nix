{
  description = "Mindclade pinned developer toolchain and system dependencies";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "aarch64-darwin" ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            bazelisk
            buf
            uv
            nodejs
            pnpm
            go
            just
            pre-commit
            git
            python312
          ];
          shellHook = ''
            export PATH="${pkgs.python312}/bin:$PATH"
          '';
        };
      });
    };
}
