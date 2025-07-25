import json
from datetime import datetime
import requests
from urllib.parse import quote
from bs4 import BeautifulSoup
import os
import stat

function_defs = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression like '2 + 3 * (4 ** 2)'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "days_between",
            "description": "Calculate the number of days between two dates",
            "parameters": {
                "type": "object",
                "properties": {
                    "date1": {
                        "type": "string",
                        "description": "First date in YYYY-MM-DD format"
                    },
                    "date2": {
                        "type": "string",
                        "description": "Second date in YYYY-MM-DD format"
                    }
                },
                "required": ["date1", "date2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_words",
            "description": "Count the number of words in text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to count words in"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_characters",
            "description": "Count the number of characters in text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to count characters in"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "count_lines",
            "description": "Count the number of lines in text",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "The text to count lines in"
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web using DuckDuckGo API",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name to get weather for"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "url_content",
            "description": "Fetch and summarize webpage content",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch content from"
                    }
                },
                "required": ["url"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files and directories in a given path",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "The directory path to list (default: current directory)",
                        "default": "."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read and return contents of a text file",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The path to the file to read"
                    }
                },
                "required": ["filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "file_info",
            "description": "Get file information including size, modified date, and type",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The path to the file to get information about"
                    }
                },
                "required": ["filename"]
            }
        }
    }
    # Add more tool definitions here
]

def calculate(expression: str) -> str:
    allowed_names = {
        "__builtins__": None,
        "abs": abs,
        "pow": pow,
        "round": round,
    }
    try:
        result = eval(expression, allowed_names, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"

def get_current_time() -> str:
    """Get current date and time"""
    try:
        current_time = datetime.now()
        return current_time.strftime("%Y-%m-%d %H:%M:%S (%A)")
    except Exception as e:
        return f"Error getting time: {e}"

def days_between(date1: str, date2: str) -> str:
    """Calculate days between two dates (YYYY-MM-DD format)"""
    try:
        d1 = datetime.strptime(date1, "%Y-%m-%d")
        d2 = datetime.strptime(date2, "%Y-%m-%d")
        diff = abs((d2 - d1).days)
        return f"{diff} days between {date1} and {date2}"
    except Exception as e:
        return f"Error: {e}. Please use YYYY-MM-DD format (e.g., 2025-01-23)"

def count_words(text: str) -> str:
    """Count the number of words in text"""
    try:
        words = len(text.split())
        return f"{words} words"
    except Exception as e:
        return f"Error counting words: {e}"

def count_characters(text: str) -> str:
    """Count the number of characters in text"""
    try:
        chars = len(text)
        return f"{chars} characters"
    except Exception as e:
        return f"Error counting characters: {e}"

def count_lines(text: str) -> str:
    """Count the number of lines in text"""
    try:
        lines = len(text.splitlines())
        return f"{lines} lines"
    except Exception as e:
        return f"Error counting lines: {e}"

def web_search(query: str) -> str:
    """Search the web using DuckDuckGo API"""
    try:
        # Using DuckDuckGo Instant Answer API (free, no API key needed)
        encoded_query = quote(query)
        url = f"https://api.duckduckgo.com/?q={encoded_query}&format=json&no_html=1&skip_disambig=1"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Try to get instant answer first
        if data.get('AbstractText'):
            return f"Search result for '{query}': {data['AbstractText'][:500]}..."
        elif data.get('Answer'):
            return f"Answer for '{query}': {data['Answer']}"
        elif data.get('Definition'):
            return f"Definition of '{query}': {data['Definition']}"
        else:
            return f"No detailed results found for '{query}'. Try a more specific search."
            
    except Exception as e:
        return f"Error searching web: {e}"

def get_weather(city: str) -> str:
    """Get current weather for a city"""
    try:
        # Using wttr.in API (free, no API key needed)
        url = f"https://wttr.in/{quote(city)}?format=j1"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        current = data['current_condition'][0]
        
        temp_c = current['temp_C']
        temp_f = current['temp_F']
        desc = current['weatherDesc'][0]['value']
        humidity = current['humidity']
        
        return f"Weather in {city}: {desc}, {temp_c}°C ({temp_f}°F), Humidity: {humidity}%"
        
    except Exception as e:
        return f"Error getting weather for {city}: {e}"

def url_content(url: str) -> str:
    """Fetch and summarize webpage content using BeautifulSoup for clean extraction"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Parse HTML with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove unwanted elements (scripts, styles, navigation, ads, etc.)
        for element in soup(['script', 'style', 'nav', 'footer', 'aside', 'header', 'noscript']):
            element.decompose()
        
        # Remove common ad/tracking classes and IDs
        for element in soup.find_all(attrs={'class': ['ad', 'advertisement', 'sidebar', 'menu', 'navigation']}):
            element.decompose()
        
        # Try to find main content area (prioritize semantic HTML)
        main_content = (
            soup.find('article') or 
            soup.find('main') or 
            soup.find('div', {'class': ['content', 'main-content', 'post-content']}) or
            soup.find('body')
        )
        
        if not main_content:
            return f"Error: Could not find main content in {url}"
        
        # Extract clean text with proper spacing
        text_content = main_content.get_text(separator=' ', strip=True)
        
        # Clean up extra whitespace
        import re
        text_content = re.sub(r'\s+', ' ', text_content).strip()
        
        # Return summary
        if len(text_content) > 500:
            return f"Content from {url}: {text_content[:500]}..."
        else:
            return f"Content from {url}: {text_content}"
            
    except Exception as e:
        return f"Error fetching content from {url}: {e}"

def list_files(directory: str = ".") -> str:
    """List files and directories in a given path"""
    try:
        # Security: Resolve path and check if it exists
        abs_path = os.path.abspath(directory)
        if not os.path.exists(abs_path):
            return f"Error: Directory '{directory}' does not exist"
        
        if not os.path.isdir(abs_path):
            return f"Error: '{directory}' is not a directory"
        
        # Get directory contents
        items = []
        for item in sorted(os.listdir(abs_path)):
            item_path = os.path.join(abs_path, item)
            if os.path.isdir(item_path):
                items.append(f"📁 {item}/")
            else:
                # Get file size
                size = os.path.getsize(item_path)
                if size < 1024:
                    size_str = f"{size}B"
                elif size < 1024 * 1024:
                    size_str = f"{size//1024}KB"
                else:
                    size_str = f"{size//(1024*1024)}MB"
                items.append(f"📄 {item} ({size_str})")
        
        if not items:
            return f"Directory '{directory}' is empty"
        
        return f"Contents of '{directory}':\n" + "\n".join(items)
        
    except PermissionError:
        return f"Error: Permission denied accessing '{directory}'"
    except Exception as e:
        return f"Error listing files in '{directory}': {e}"

def read_file(filename: str) -> str:
    """Read and return contents of a text file"""
    try:
        # Security: Resolve path and check if it exists
        abs_path = os.path.abspath(filename)
        if not os.path.exists(abs_path):
            return f"Error: File '{filename}' does not exist"
        
        if not os.path.isfile(abs_path):
            return f"Error: '{filename}' is not a file"
        
        # Check file size (limit to 10KB for safety)
        file_size = os.path.getsize(abs_path)
        if file_size > 10 * 1024:  # 10KB limit
            return f"Error: File '{filename}' is too large ({file_size} bytes). Maximum size is 10KB."
        
        # Try to read as text file
        with open(abs_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Truncate if too long for display
        if len(content) > 1000:
            return f"Content of '{filename}' (first 1000 characters):\n{content[:1000]}..."
        else:
            return f"Content of '{filename}':\n{content}"
            
    except UnicodeDecodeError:
        return f"Error: '{filename}' appears to be a binary file, not a text file"
    except PermissionError:
        return f"Error: Permission denied reading '{filename}'"
    except Exception as e:
        return f"Error reading file '{filename}': {e}"

def file_info(filename: str) -> str:
    """Get file information including size, modified date, and type"""
    try:
        # Security: Resolve path and check if it exists
        abs_path = os.path.abspath(filename)
        if not os.path.exists(abs_path):
            return f"Error: '{filename}' does not exist"
        
        # Get file stats
        file_stat = os.stat(abs_path)
        
        # Determine type
        if os.path.isdir(abs_path):
            file_type = "Directory"
        elif os.path.isfile(abs_path):
            file_type = "File"
        elif os.path.islink(abs_path):
            file_type = "Symbolic Link"
        else:
            file_type = "Other"
        
        # Format size
        size = file_stat.st_size
        if size < 1024:
            size_str = f"{size} bytes"
        elif size < 1024 * 1024:
            size_str = f"{size/1024:.1f} KB"
        elif size < 1024 * 1024 * 1024:
            size_str = f"{size/(1024*1024):.1f} MB"
        else:
            size_str = f"{size/(1024*1024*1024):.1f} GB"
        
        # Format dates
        modified_time = datetime.fromtimestamp(file_stat.st_mtime)
        modified_str = modified_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Get permissions (Unix-style)
        permissions = stat.filemode(file_stat.st_mode)
        
        info = f"Information for '{filename}':\n"
        info += f"Type: {file_type}\n"
        info += f"Size: {size_str}\n"
        info += f"Modified: {modified_str}\n"
        info += f"Permissions: {permissions}"
        
        return info
        
    except PermissionError:
        return f"Error: Permission denied accessing '{filename}'"
    except Exception as e:
        return f"Error getting info for '{filename}': {e}"

def handle_tool_call(tool_call):
    name = tool_call["function"]["name"]
    args = json.loads(tool_call["function"]["arguments"])
    
    if name == "calculate":
        return calculate(args["expression"])
    
    if name == "get_current_time":
        return get_current_time()
    
    if name == "days_between":
        return days_between(args["date1"], args["date2"])
    
    if name == "count_words":
        return count_words(args["text"])
    
    if name == "count_characters":
        return count_characters(args["text"])
    
    if name == "count_lines":
        return count_lines(args["text"])
    
    if name == "web_search":
        return web_search(args["query"])
    
    if name == "get_weather":
        return get_weather(args["city"])
    
    if name == "url_content":
        return url_content(args["url"])
    
    if name == "list_files":
        directory = args.get("directory", ".")
        return list_files(directory)
    
    if name == "read_file":
        return read_file(args["filename"])
    
    if name == "file_info":
        return file_info(args["filename"])
    
    # Add dispatch for more tools here
    return f"Unknown tool: {name}"