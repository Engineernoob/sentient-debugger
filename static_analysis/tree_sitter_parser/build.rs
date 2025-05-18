use std::fs;

fn main() {
    let grammars = vec![
        ("tree_sitter_python", "vendor/tree-sitter-python/src"),
        ("tree_sitter_rust", "vendor/tree-sitter-rust/src"),
        ("tree_sitter_typescript", "vendor/tree-sitter-typescript/typescript/src"),
        ("tree_sitter_tsx", "vendor/tree-sitter-typescript/tsx/src"),
    ];

    for (name, path) in grammars {
        let mut build = cc::Build::new();
        build.include(path).file(format!("{}/parser.c", path));

        // Optional scanner.c or scanner.cc
        let scanner_c = format!("{}/scanner.c", path);
        let scanner_cc = format!("{}/scanner.cc", path);

        if fs::metadata(&scanner_c).is_ok() {
            build.file(scanner_c);
        } else if fs::metadata(&scanner_cc).is_ok() {
            build.cpp(true).file(scanner_cc);
        }

        build.compile(name);
    }
}
