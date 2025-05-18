use tree_sitter::{Language, Parser};
use std::path::PathBuf;
use libloading::{Library, Symbol};

pub struct LoadedLanguage {
    pub name: &'static str,
    pub language: Language,
}

pub fn load_language(lib_path: PathBuf, lang_name: &'static str) -> Result<LoadedLanguage, Box<dyn std::error::Error>> {
    unsafe {
        let lib = Library::new(lib_path)?;
        let func: Symbol<unsafe extern "C" fn() -> Language> = lib.get(b"tree_sitter_language")?;
        Ok(LoadedLanguage {
            name: lang_name,
            language: func(),
        })
    }
}
