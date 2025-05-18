//! Tree-sitter parser bindings for multiple programming languages
//!
//! This crate provides safe Rust bindings for various Tree-sitter language grammars.
//! The actual language implementations are compiled from C code in the build script.

// Include the generated bindings (includes both FFI declarations and safe wrappers)
include!(concat!(env!("OUT_DIR"), "/bindings.rs"));

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_language_bindings() {
        // Test that we can call the language functions without panicking
        let languages = [
            ("python", language_python()),
            ("rust", language_rust()),
            ("typescript", language_typescript()),
            ("tsx", language_tsx()),
        ];

        for (name, lang) in &languages {
            assert!(!lang.is_null(), "Failed to load {} parser", name);
        }
    }
}
