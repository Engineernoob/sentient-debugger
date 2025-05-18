use std::{env, fs};
use anyhow::{Result, Context, bail};
use tree_sitter::{Parser, Language};

extern "C" { fn tree_sitter_python() -> Language; }
extern "C" {
    fn tree_sitter_typescript() -> Language;
    fn tree_sitter_tsx() -> Language;
}

extern "C" { fn tree_sitter_rust() -> Language; }

fn detect_language(filename: &str) -> Option<Language> {
    if filename.ends_with(".py") {
        Some(unsafe { tree_sitter_python() })
    } else if filename.ends_with(".ts") {
        Some(unsafe { tree_sitter_typescript() })
    } else if filename.ends_with(".tsx") {
        Some(unsafe { tree_sitter_tsx() })
    } else if filename.ends_with(".rs") {
        Some(unsafe { tree_sitter_rust() })
    } else {
        None
    }
}


fn main() -> Result<()> {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        bail!("Usage: {} <source-file>", args[0]);
    }

    let file_path = &args[1];

    let code = fs::read_to_string(file_path)
        .with_context(|| format!("Failed to read file {}", file_path))?;

    let lang = detect_language(file_path)
        .ok_or_else(|| anyhow::anyhow!("Unsupported file extension: {}", file_path))?;

    let mut parser = Parser::new();
    parser.set_language(lang)
        .context("Failed to set parser language")?;

    let tree = parser.parse(&code, None)
        .ok_or_else(|| anyhow::anyhow!("Failed to parse source code"))?;

    let root_node = tree.root_node();

    println!("[AST] Root node: {}", root_node.kind());
    print_node_tree(root_node, &code, 0);

    Ok(())
}

fn print_node_tree(node: tree_sitter::Node, source_code: &str, indent: usize) {
    let indent_str = "  ".repeat(indent);
    println!("{}{} [{}:{}]", indent_str, node.kind(), node.start_position().row + 1, node.start_position().column + 1);

    for i in 0..node.child_count() {
        if let Some(child) = node.child(i) {
            print_node_tree(child, source_code, indent + 1);
        }
    }
}