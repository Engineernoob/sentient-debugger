# 🧠 Sentient Debugger + Adaptive Test Architect

An intelligent, offline AI coding assistant that learns and adapts to your coding style. It combines real-time code analysis with natural conversation to provide a uniquely personalized development experience - like having a senior developer who understands exactly how you work.

## 🌟 Key Features

- **Conversational AI**: Natural dialogue interface that understands context and learns from interactions
- **Self-Learning**: Adapts to your coding style and preferences over time
- **Offline & Private**: Runs completely locally - perfect for secure environments
- **Real-Time Monitoring**: Proactively identifies issues and suggests improvements
- **Multi-Model Architecture**: Combines conversational and technical models for optimal assistance

## 💡 What Makes It Special

- **Natural Interaction**: Chat naturally about your code, just like talking to a colleague
- **Context Awareness**: Understands project context and maintains conversation history
- **Proactive Assistance**: Identifies potential issues before they become problems
- **Personalized Learning**: Adapts suggestions based on your feedback and preferences
- **Privacy First**: All processing happens locally - your code never leaves your machine

## 🛠️ Technical Features

- 🗣️ **Dual Model System**
  - Conversational model for natural interaction
  - Technical model for code analysis and suggestions
  
- 🔍 **Code Analysis**
  - Real-time syntax checking
  - Code quality metrics
  - Security vulnerability scanning
  - Performance optimization suggestions
  
- 📊 **Metrics & Insights**
  - Code complexity analysis
  - Maintainability scoring
  - Bug pattern detection
  - Style consistency checking

## 🏗️ Architecture

📦 sentient-debugger
├── ai/
│ ├── local_model_runner.py # Local LLM runner (e.g. llama.cpp)
│ └── style_embedding.py # Learns your coding patterns
├── watcher/
│ ├── file_monitor.py # Monitors code changes
│ └── event_handler.py # Handles file events and triggers analysis
├── tests/
│ └── adaptive_test_writer.py # Writes and evolves test cases
├── static_analysis/
│ └── tree_sitter_parser.rs # AST parsing via Tree-sitter
├── gui/tauri-app/ # (Optional) Frontend using Tauri
├── launch.py # Entry point CLI for tool
└── requirements.txt # Python dependencies


---

## 📦 Setup Instructions

### ✅ Prerequisites

- Python 3.10+
- Local LLM model (default: CodeLlama 7B)
- Windows/Linux/MacOS
- Rust (for static analysis)

### 📥 Installation

```bash
git clone https://github.com/your-username/sentient-debugger.git
cd sentient-debugger
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cargo build --manifest-path static_analysis/Cargo.toml

🚦 Usage
Start the debugger on your project directory:

bash
Copy
Edit
python launch.py --watch ~/dev/my-cool-project
Once running, the debugger will:

Parse file changes.

Extract coding patterns.

Suggest inline improvements (via CLI or GUI).

Write test cases to tests/generated/.

🧠 Model Support
Default integration supports:

LLaMA.cpp for ultra-light local inference

ONNX runtime for pretrained transformer models

Style embedding uses sentence-transformers + FAISS for similarity search.

🧪 Test Evolution Engine
Auto-writes tests like:

python
Copy
Edit
# Generated by Sentient Debugger on 2025-05-18
def test_process_data_edge_case():
    result = process_data([])
    assert result == {}
🛡️ Security & Privacy
Entirely offline.

No data leaves your machine.

Ideal for secure coding environments.

🌐 Future Roadmap
 Auto-refactor suggestions via GUI.

 Git diff learning to track developer evolution.

 Collaborative mode for team behavior synthesis.

 ## 💬 Interactive Commands
- help - Show available commands
- suggest - Get code suggestions
- explain - Explain current code
- metrics - Show code quality metrics
- optimize - Get optimization suggestions
- security - Run security analysis
- And many more...

🤝 Contributing
Pull requests are welcome! If you’d like to plug in new models or add language support, check out the ai/ and static_analysis/ folders.

📜 License
MIT License © 2025 Taahirah Denmark