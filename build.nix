with import<nixpkgs> {};
stdenv.mkDerivation rec {
    name = "venv";

    dependencies = [
        discord
        requests
        setuptools 
        wheel
        Red-DiscordBot
        sqlite-utils
        psutil
    ];

    env = buildEnv {
        name = name;
        paths = dependencies;
    };
}