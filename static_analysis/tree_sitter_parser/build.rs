// build.rs
fn main() {
    cc::Build::new()
        .include("vendor/tree-sitter-python/src")
        .file("vendor/tree-sitter-python/src/parser.c")
        .compile("tree_sitter_python");

    cc::Build::new()
        .include("vendor/tree-sitter-rust/src")
        .file("vendor/tree-sitter-rust/src/parser.c")
        .compile("tree_sitter_rust");

    cc::Build::new()
        .include("vendor/tree-sitter-typescript/tsx/src")
        .file("vendor/tree-sitter-typescript/tsx/src/parser.c")
        .compile("tree_sitter_tsx");
}
