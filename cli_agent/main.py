import os
from dotenv import load_dotenv
from groq import Groq
import instructor
from pydantic import BaseModel, Field
from typing import List
import subprocess
import argparse
import sys

load_dotenv()   
# Initialize Groq client
client_base = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Enable instructor patches for Groq client
client = instructor.from_groq(client_base)

class TerminalCommand(BaseModel):
    command: str = Field(description="The command to be executed in the terminal")

class TerminalCommands(BaseModel):
    commands: List[TerminalCommand] = Field(description="List of terminal commands")

def generate_commands(query: str) -> TerminalCommands:
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates windows terminal commands give only direct terminal commands for the given query"},
            {"role": "user", "content": f"Generate terminal commands for: {query}"}
        ],
        response_model=TerminalCommands,
    )

def generate_commands_with_ollama(query: str) -> TerminalCommands:
    return client.chat.completions.create(
        model="ollama-3.1",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates windows terminal commands. Give only direct terminal commands for the given query."},
            {"role": "user", "content": f"Generate terminal commands for: {query}"}
        ],
        response_model=TerminalCommands,
    )
    
def execute_commands(TerminalCommands):
    output = ""
    for command in TerminalCommands.commands:
        result = subprocess.run(["cmd", "/c", command.command], capture_output=True, text=True)
        output += result.stdout
    return output

def chat_with_llm(query: str,results) -> str:
    return client_base.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a personalised llm that recieves the query the output from the cli-agent and you need to reply taking the query and the agents output as input and give a response"},
            {"role": "user", "content": f"Query is :{query} and the output from agent is :{results} "}
        ],
        # response_model=str,
    )
    
def main():
    parser = argparse.ArgumentParser(description="Generate and execute Windows terminal commands.")
    parser.add_argument("query", nargs='*', help="The query to generate commands for")
    parser.add_argument("-e", "--execute", action="store_true", help="Execute the generated commands")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show generated commands")
    parser.add_argument("-c", "--chat", action="store_true", default=True, help="Chat with the llm (default)")

    args = parser.parse_args()

    # Check if any query was provided
    if not args.query:
        print("Please provide a query.")
        parser.print_help()
        sys.exit(1)

    query = ' '.join(args.query)
    result = generate_commands(query)

    # If any explicit flag is provided, turn off chat mode
    if args.execute or args.verbose:
        args.chat = False

    if args.verbose:
        print("Generated commands:")
        print(result.model_dump_json(indent=2))

    if args.execute:
        print("Executing commands:")
        output = execute_commands(result)
        print(output)
        
    if args.chat:
        print("Chatting with llm:")
        output = execute_commands(result)
        response = chat_with_llm(query, output)
        # print(response.model_dump_json(indent=2))
        print(f" result is {result} output is {output}")
        print(response.choices[0].message.content)
        
    elif not args.verbose and not args.execute and not args.chat:
        print("Generated commands:")
        for command in result.commands:
            print(command.command)

def run():
    main()

if __name__ == "__main__":
    run()
