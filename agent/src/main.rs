use llm::api;
use std::collections::HashMap;
use std::error::Error;
use std::fs;
use std::path::{Path};

fn generate_directory_tree<P: AsRef<Path>>(path: P) -> Result<String, Box<dyn Error>> {
    let mut tree = String::new();
    generate_directory_tree_recursive(path.as_ref(), &mut tree, 0)?;
    Ok(tree)
}

fn generate_directory_tree_recursive(path: &Path, tree: &mut String, depth: usize) -> Result<(), Box<dyn Error>> {
    if depth > 0 {
        let prefix = if depth > 1 { "│   ".repeat(depth - 1) } else { String::new() } + "├── ";
        let file_name = path.file_name().unwrap_or_default().to_string_lossy();
        tree.push_str(&format!("{}{}\n", prefix, file_name));
    }
    if path.is_dir() {
        for entry in fs::read_dir(path)? {
            let entry = entry?;
            generate_directory_tree_recursive(&entry.path(), tree, depth + 1)?;
        }
    }
    Ok(())
}

fn pre_prompt(directory_tree: &str) -> String {
    format!("generate an index.md markdown file for the following directory structure:\n{}", directory_tree)
}

fn main() -> Result<(), Box<dyn Error>> {
    let directory_tree = generate_directory_tree("../notes")?;
    let message = pre_prompt(&directory_tree).to_owned();

    let messages: Vec<HashMap<&str, &str>> = vec![
        {
            let mut map = HashMap::new();
            map.insert("role", "system");
            map.insert("content", "imagine you are a graphic artist who plays around with markdown files.");
            map
        },
        {
            let mut map = HashMap::new();
            map.insert("role", "user");
            map.insert("content", &message);
            map
        },
    ];

    let model = "granite-code:3b";
    let response = api(messages, model); // Passing the messages vector directly

    println!("{}", response);

    Ok(())
}
