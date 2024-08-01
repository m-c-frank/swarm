use std::collections::HashMap;
use llm::api; // Replace `my_library` with your library name

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let messages = vec![
        {
            let mut map = HashMap::new();
            map.insert("role", "system");
            map.insert("content", "You are a helpful assistant.");
            map
        },
        {
            let mut map = HashMap::new();
            map.insert("role", "user");
            map.insert("content", "Hello!");
            map
        },
    ];

    let model = "granite-code:3b";
    let response = api(messages, model)?;

    println!("{}", response);

    Ok(())
}
