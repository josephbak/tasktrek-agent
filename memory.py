# memory.py

from datetime import datetime

class Memory:
    def __init__(self, system_prompt, recent_limit=10, important_limit=5):
        self.system_prompt = system_prompt
        self.recent_history = []      # Last N messages for immediate context
        self.important_history = []   # Key messages worth preserving longer
        self.recent_limit = recent_limit
        self.important_limit = important_limit
    
    def add_user_message(self, content):
        message = {
            "role": "user", 
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.recent_history.append(message)
        self._trim_recent()
    
    def add_agent_message(self, content):
        message = {
            "role": "assistant", 
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.recent_history.append(message)
        
        # Check if this message should be preserved as important
        if self._is_important_message(content):
            important_msg = message.copy()
            important_msg["reason"] = self._get_importance_reason(content)
            self.important_history.append(important_msg)
            self._trim_important()
        
        self._trim_recent()
    
    def _is_important_message(self, content):
        """Determine if a message should be preserved as important"""
        importance_indicators = [
            "[TOOL]" in content,           # Tool usage results
            "Error:" in content,           # Error messages
            "read_file" in content,        # File content
            "list_files" in content,       # Directory listings
            "web_search" in content,       # Search results
            len(content) > 200,            # Long, detailed responses
            "python" in content.lower(),   # Code-related content
            "file" in content.lower(),     # File operations
        ]
        return any(indicator for indicator in importance_indicators)
    
    def _get_importance_reason(self, content):
        """Get reason why message is important (for debugging)"""
        if "[TOOL]" in content:
            return "tool_result"
        elif "Error:" in content:
            return "error_message"
        elif len(content) > 200:
            return "detailed_response"
        else:
            return "general_importance"
    
    def _trim_recent(self):
        """Keep only the most recent messages"""
        if len(self.recent_history) > self.recent_limit:
            self.recent_history = self.recent_history[-self.recent_limit:]
    
    def _trim_important(self):
        """Keep only the most important messages"""
        if len(self.important_history) > self.important_limit:
            # Keep the most recent important messages
            self.important_history = self.important_history[-self.important_limit:]
    
    def get_history(self):
        """Get combined history for API calls"""
        # Start with system prompt
        history = [{"role": "system", "content": self.system_prompt}]
        
        # Add important messages (without metadata)
        for msg in self.important_history:
            history.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add recent messages (without metadata)
        for msg in self.recent_history:
            history.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Remove duplicates while preserving order
        seen = set()
        unique_history = []
        for msg in history:
            msg_key = (msg["role"], msg["content"])
            if msg_key not in seen:
                seen.add(msg_key)
                unique_history.append(msg)
        
        return unique_history
    
    def get_memory_stats(self):
        """Get memory usage statistics"""
        total_messages = len(self.recent_history) + len(self.important_history)
        history = self.get_history()
        estimated_tokens = sum(len(msg["content"].split()) for msg in history)
        
        return {
            "recent_messages": len(self.recent_history),
            "important_messages": len(self.important_history),
            "total_unique_messages": len(history) - 1,  # Exclude system prompt
            "estimated_tokens": estimated_tokens,
            "recent_limit": self.recent_limit,
            "important_limit": self.important_limit
        }
    
    def get_important_summary(self):
        """Get summary of what's stored as important (for debugging)"""
        summary = []
        for msg in self.important_history:
            preview = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
            summary.append({
                "reason": msg.get("reason", "unknown"),
                "preview": preview,
                "timestamp": msg["timestamp"]
            })
        return summary
    
    def save_conversation_to_file(self, filename=None):
        """Save the entire conversation to a text file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("TaskTrek Agent Conversation Log\n")
                f.write("=" * 40 + "\n")
                f.write(f"Session Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Get all messages (recent + important, deduplicated)
                all_messages = []
                
                # Add important messages first (chronologically)
                for msg in self.important_history:
                    all_messages.append({
                        "role": msg["role"],
                        "content": msg["content"],
                        "timestamp": msg["timestamp"],
                        "type": "important"
                    })
                
                # Add recent messages
                for msg in self.recent_history:
                    all_messages.append({
                        "role": msg["role"],
                        "content": msg["content"],
                        "timestamp": msg["timestamp"],
                        "type": "recent"
                    })
                
                # Sort by timestamp and remove duplicates
                seen_content = set()
                unique_messages = []
                for msg in sorted(all_messages, key=lambda x: x["timestamp"]):
                    content_key = (msg["role"], msg["content"])
                    if content_key not in seen_content:
                        seen_content.add(content_key)
                        unique_messages.append(msg)
                
                # Write messages to file
                for msg in unique_messages:
                    role_label = "User" if msg["role"] == "user" else "Agent"
                    f.write(f"{role_label}: {msg['content']}\n")
                    f.write("-" * 40 + "\n")
                
                # Add memory statistics at the end
                f.write("\nMemory Statistics:\n")
                stats = self.get_memory_stats()
                for key, value in stats.items():
                    f.write(f"  {key}: {value}\n")
            
            return f"Conversation saved to {filename}"
            
        except Exception as e:
            return f"Error saving conversation: {e}"
