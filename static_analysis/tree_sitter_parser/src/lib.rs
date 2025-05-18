use tree_sitter::Language;

extern "C" {
    fn tree_sitter_rust() -> Language;
    fn tree_sitter_python() -> Language;
    fn tree_sitter_typescript() -> Language;
    fn tree_sitter_tsx() -> Language;
}

/// Returns the Tree-sitter language for Rust
pub fn language_rust() -> Language {
    unsafe { tree_sitter_rust() }
}

/// Returns the Tree-sitter language for Python
pub fn language_python() -> Language {
    unsafe { tree_sitter_python() }
}

/// Returns the Tree-sitter language for TypeScript
pub fn language_typescript() -> Language {
    unsafe { tree_sitter_typescript() }
}

/// Returns the Tree-sitter language for TSX
pub fn language_tsx() -> Language {
    unsafe { tree_sitter_tsx() }
}
