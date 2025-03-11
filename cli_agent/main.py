import os
from dotenv import load_dotenv
from groq import Groq
import instructor
from pydantic import BaseModel, Field
from typing import List
import subprocess
import argparse
import sys
from tavily import TavilyClient

load_dotenv()   
# Initialize Groq client
client_base = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Enable instructor patches for Groq client
client = instructor.from_groq(client_base)

class TerminalCommand(BaseModel):
    command: str = Field(description="The command to be executed in the terminal")

class TerminalCommands(BaseModel):
    commands: List[TerminalCommand] = Field(description="List of terminal commands")

class ListTools(BaseModel):
    tools: List[str] = Field(description="List of tools")
    
tools = [
    {
        "name": "commands",
        "description": "Generates and executes Windows terminal commands. Use this for system operations, file management, or when the user needs to perform actions on their computer."
    },
    {
        "name": "search",
        "description": "Searches the internet for up-to-date information. Use this when the query requires external knowledge, current events, or information not available in the system."
    }
]

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_with_tavily(query: str):
    try:
        response = tavily_client.search(query)
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def generate_commands(query: str) -> TerminalCommands:
    return client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates windows terminal commands give only direct terminal commands for the given query"},
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

def tools_selection(query: str, tools) -> ListTools:
    result = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"You are a tool selection agent that looks at the query and gives a list of tools that can be used for the given query from the existing tools : {tools} or if no tools are needed"},
            {"role": "user", "content": f"Tools needed for: {query}"}
        ],
        response_model=ListTools,
    )
    return result

def agent_with_tools(query: str, tools) -> str:
    results = ""
    for tool in tools.tools:
        if tool == "search":
            response = search_with_tavily(query)
            results += str(response)
        elif tool == "commands":
            commands = generate_commands(query)
            results += execute_commands(commands)
    return results

def chat_with_llm(query: str, results) -> str:
    return client_base.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a personalised llm that receives the query the output from the cli-agent and you need to reply taking the query and the agents output as input and give a response, and if the agents output is empty then you need to give a response based on the query"},
            {"role": "user", "content": f"Query is: {query} and the output from agent is: {results}"}
        ],
    )

def main():
    parser = argparse.ArgumentParser(description="Cli-agent is a command line tool that can run commands and search web for simple queries.")
    parser.add_argument("query", nargs="*", help="The query to process")
    parser.add_argument("-c", "--chat", action="store_true", default=True, help="Chat with the llm (default)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    
    args = parser.parse_args()

    if not args.query:
        print("Please provide a query.")
        parser.print_help()
        sys.exit(1)

    query = ' '.join(args.query)
    
    selected_tools = tools_selection(query, tools)
    result = agent_with_tools(query, selected_tools)
    
    if args.verbose:
        print("Tools selected:")
        print(selected_tools)
        print("Output from the selected tools:")
        print(result)
        
    if args.chat:
        print("Chatting with llm:")
        response = chat_with_llm(query, result)
        print(response.choices[0].message.content)

def run():
    main()

if __name__ == "__main__":
    run()
