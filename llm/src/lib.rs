use std::collections::HashMap;
use std::io::{Read, Write};
use std::net::TcpStream;

pub fn api(messages: Vec<HashMap<&str, &str>>, model: &str) -> Result<String, Box<dyn std::error::Error>> {
    let host = "localhost:11434";
    let path = "/v1/chat/completions";

    let mut stream = TcpStream::connect(host)?;

    let request_body = create_json_body(messages, model);

    let request = format!(
        "POST {} HTTP/1.1\r\n\
        Host: {}\r\n\
        Content-Type: application/json\r\n\
        Content-Length: {}\r\n\
        Connection: close\r\n\
        \r\n\
        {}",
        path,
        host,
        request_body.len(),
        request_body
    );

    stream.write_all(request.as_bytes())?;

    let mut response = String::new();
    stream.read_to_string(&mut response)?;

    if let Some(body) = response.split("\r\n\r\n").nth(1) {
        Ok(body.to_string())
    } else {
        Err("Failed to get response body".into())
    }
}

pub fn create_json_body(messages: Vec<HashMap<&str, &str>>, model: &str) -> String {
    let mut json_body = String::from("{\"model\":\"");
    json_body.push_str(model);
    json_body.push_str("\",\"messages\":[");

    for (i, message) in messages.iter().enumerate() {
        if i > 0 {
            json_body.push_str(",");
        }
        json_body.push_str("{");

        let mut first = true;
        for (key, value) in message {
            if !first {
                json_body.push_str(",");
            }
            first = false;

            json_body.push_str("\"");
            json_body.push_str(key);
            json_body.push_str("\":\"");
            json_body.push_str(value);
            json_body.push_str("\"");
        }

        json_body.push_str("}");
    }

    json_body.push_str("]}");
    json_body
}