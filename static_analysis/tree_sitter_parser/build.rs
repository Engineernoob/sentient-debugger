use std::env;
use std::fs;
use std::path::PathBuf;

fn main() {
    let out_dir = PathBuf::from(env::var("OUT_DIR").unwrap());
    let manifest_dir = PathBuf::from(env::var("CARGO_MANIFEST_DIR").unwrap());
    
    // Define the grammars we want to build
    let grammars = vec![
        ("python", manifest_dir.join("vendor/tree-sitter-python/src")),
        ("rust", manifest_dir.join("vendor/tree-sitter-rust/src")),
        ("typescript", manifest_dir.join("vendor/tree-sitter-typescript/typescript/src")),
        ("tsx", manifest_dir.join("vendor/tree-sitter-typescript/tsx/src")),
    ];

    // Tell Cargo to link the runtime library
    println!("cargo:rustc-link-lib=static=tree-sitter");

    // Build each language parser
    for (lang, src_dir) in &grammars {
        let parser_c = src_dir.join("parser.c");
        let scanner_c = src_dir.join("scanner.c");
        let scanner_cc = src_dir.join("scanner.cc");

        println!("cargo:rerun-if-changed={}", src_dir.display());
        
        // Configure the build
        let mut build = cc::Build::new();
        build
            .include(src_dir)
            .include(&manifest_dir.join("vendor"))
            .warnings(false)
            .flag_if_supported("-std=c11")
            .file(parser_c);

        // Add scanner if it exists
        if scanner_c.exists() {
            build.file(&scanner_c);
        } else if scanner_cc.exists() {
            build.cpp(true).file(&scanner_cc);
        }

        // Compile the parser
        let lib_name = format!("tree_sitter_{}", lang);
        build.compile(&lib_name);
        
        // Tell Cargo to link the generated static library
        println!("cargo:rustc-link-lib=static={}", lib_name);
    }

    // Generate bindings for the language functions
    let mut bindings = String::new();
    bindings.push_str("use tree_sitter::Language;\n\n");
    
    for (lang, _) in &grammars {
        bindings.push_str(&format!(
            "extern \"C\" {{\n    pub fn tree_sitter_{}() -> Language;\n}}\n\n",
            lang
        ));
    }
    
    // Add safe wrapper functions
    for (lang, _) in &grammars {
        bindings.push_str(&format!(
            "/// Returns the Tree-sitter language for {}\n\
///\n\
/// # Safety\n\
/// This function is safe to call as long as the tree-sitter-{} library is properly linked.\n\
pub fn language_{}() -> Language {{\n\
    unsafe {{ tree_sitter_{}() }}\n\
}}\n\n",
            lang, lang, lang, lang
        ));
    }

    // Write the bindings to a file
    let bindings_file = out_dir.join("bindings.rs");
    fs::write(&bindings_file, bindings).unwrap();
    
    // Tell Cargo to re-run if any of the source files change
    println!("cargo:rerun-if-changed=build.rs");
}
