<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# 

---

# cli-agent

A terminal AI assistant for Windows that runs in your terminal, executes shell commands, and searches the web for information.

## 📔 Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)


## About

cli-agent is a powerful terminal-based AI assistant that helps you generate and execute Windows terminal commands while also providing web search capabilities. It leverages the Groq API with LLaMA 3.3 70B model to understand your queries and intelligently select the appropriate tools to respond to your needs.

## Features

- **Intelligent Tool Selection**: Automatically decides whether to use terminal commands or web search based on your query
- **Web Search Integration**: Searches the internet for up-to-date information using Tavily API
- **Command Generation**: Creates Windows terminal commands based on natural language queries
- **Command Execution**: Runs generated commands directly in your terminal
- **Conversational Interface**: Chat with the AI about command results and search findings
- **Verbose Mode**: See detailed information about tool selection and execution


## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- A Groq API key (create your free key here: https://console.groq.com/keys)
- A Tavily API key (sign up at https://tavily.com)


### Setup

1. Clone the repository:
```
git clone https://github.com/arthyism/cli-agent.git
cd cli-agent
```

2. Install the package in development mode:
```
pip install -e .
```

3. Open the .env file in the cli_agent directory and add your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```


## Usage

After installation, you can use the cli-agent command directly from your terminal:

```
# Basic usage - chat mode (default)
cli-agent find all text files in current directory

# Show verbose output with tool selection details
cli-agent -v what is the weather in New York

# Ask for information that requires web search
cli-agent what are the latest news about AI
```


### Command Line Arguments

- `query`: The natural language query to process
- `-v`, `--verbose`: Show detailed information about tool selection and execution
- `-c`, `--chat`: Chat with the LLM about the results (default mode)


## Environment Variables

The application requires the following environment variables:

- `GROQ_API_KEY`: Your API key for the Groq service
- `TAVILY_API_KEY`: Your API key for the Tavily search service

