
# cli-agent

A terminal AI assistant for Windows that runs in your terminal and can execute simple shell commands.

## 📔 Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)


## About

cli-agent is a powerful terminal-based AI assistant that helps you generate and execute Windows terminal commands. It leverages the Groq API with LLaMA 3.3 70B model to understand your queries and provide appropriate terminal commands or conversational responses.

## Features

- Generate Windows terminal commands based on natural language queries
- Execute generated commands directly in your terminal
- Chat with the AI about command results
- Support for different output modes (verbose, execute, chat)


## Installation

### Prerequisites

- Python 3.6 or higher
- pip (Python package installer)
- A Groq API key (create your free key here: https://console.groq.com/keys )


### Setup

1. Clone the repository:
```bash
git clone https://github.com/arthyism/cli-agent.git
cd cli-agent
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. open the `.env` file in the cli_agent directory and replace it with your Groq API key:
```
GROQ_API_KEY=your_groq_api_key_here
```


## Usage

After installation, you can use the cli-agent command directly from your terminal:

```bash
# Basic usage - chat mode (default)
cli-agent find all text files in current directory

# Generate and display commands without executing
cli-agent -v list all running processes

# Generate and execute commands
cli-agent -e create a new folder named test

# Combine flags
cli-agent -v -e check disk space
```


### Command Line Arguments

- `query`: The natural language query to generate commands for
- `-e, --execute`: Execute the generated commands
- `-v, --verbose`: Show the detailed output of generated commands
- `-c, --chat`: Chat with the LLM about the results (default mode)


## Environment Variables

The application requires the following environment variable:

- `GROQ_API_KEY`: Your API key for the Groq service



