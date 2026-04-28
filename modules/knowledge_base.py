"""
Knowledge base module for error code resolutions
"""
import json
import os
from typing import Dict, List, Optional


class KnowledgeBase:
    """Manage error code knowledge base"""
    
    def __init__(self, kb_path: str = 'data/error_codes.json'):
        """
        Initialize knowledge base
        
        Args:
            kb_path: Path to error codes JSON file
        """
        self.kb_path = kb_path
        self.error_codes = {}
        self.load_knowledge_base()
    
    def load_knowledge_base(self) -> bool:
        """
        Load error codes from JSON file
        
        Returns:
            True if successful
        """
        try:
            if os.path.exists(self.kb_path):
                with open(self.kb_path, 'r', encoding='utf-8') as f:
                    self.error_codes = json.load(f)
                return True
            else:
                print(f"Warning: Knowledge base file not found: {self.kb_path}")
                return False
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return False
    
    def get_error_info(self, error_code: str) -> Optional[Dict]:
        """
        Get information about an error code
        
        Args:
            error_code: Error code (e.g., 'U0777', 'S013')
            
        Returns:
            Dictionary with error information or None
        """
        if not error_code or error_code == 'NOT FOUND':
            return None
        
        # Normalize error code (uppercase, remove spaces)
        error_code = error_code.upper().strip()
        
        return self.error_codes.get(error_code)
    
    def get_resolution_steps(self, error_code: str) -> List[str]:
        """
        Get resolution steps for an error code
        
        Args:
            error_code: Error code
            
        Returns:
            List of resolution steps
        """
        error_info = self.get_error_info(error_code)
        if error_info:
            return error_info.get('resolution_steps', [])
        return []
    
    def get_common_causes(self, error_code: str) -> List[str]:
        """
        Get common causes for an error code
        
        Args:
            error_code: Error code
            
        Returns:
            List of common causes
        """
        error_info = self.get_error_info(error_code)
        if error_info:
            return error_info.get('common_causes', [])
        return []
    
    def get_prevention_tips(self, error_code: str) -> List[str]:
        """
        Get prevention tips for an error code
        
        Args:
            error_code: Error code
            
        Returns:
            List of prevention tips
        """
        error_info = self.get_error_info(error_code)
        if error_info:
            return error_info.get('prevention', [])
        return []
    
    def format_resolution(self, error_code: str) -> str:
        """
        Format resolution information for display
        
        Args:
            error_code: Error code
            
        Returns:
            Formatted resolution text
        """
        error_info = self.get_error_info(error_code)
        
        if not error_info:
            return f"No resolution information available for error code: {error_code}"
        
        output = []
        output.append("=" * 70)
        output.append(f"ERROR CODE: {error_code}")
        output.append(f"NAME: {error_info.get('name', 'Unknown')}")
        output.append("=" * 70)
        output.append("")
        
        # Description
        output.append("DESCRIPTION:")
        output.append(error_info.get('description', 'No description available'))
        output.append("")
        
        # Common Causes
        causes = error_info.get('common_causes', [])
        if causes:
            output.append("COMMON CAUSES:")
            for i, cause in enumerate(causes, 1):
                output.append(f"  {i}. {cause}")
            output.append("")
        
        # Resolution Steps
        steps = error_info.get('resolution_steps', [])
        if steps:
            output.append("RESOLUTION STEPS:")
            for i, step in enumerate(steps, 1):
                output.append(f"  {i}. {step}")
            output.append("")
        
        # Prevention
        prevention = error_info.get('prevention', [])
        if prevention:
            output.append("PREVENTION:")
            for i, tip in enumerate(prevention, 1):
                output.append(f"  {i}. {tip}")
            output.append("")
        
        output.append("=" * 70)
        
        return "\n".join(output)
    
    def search_by_keyword(self, keyword: str) -> List[str]:
        """
        Search error codes by keyword
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching error codes
        """
        keyword = keyword.lower()
        matches = []
        
        for code, info in self.error_codes.items():
            # Search in name and description
            if keyword in info.get('name', '').lower() or \
               keyword in info.get('description', '').lower():
                matches.append(code)
        
        return matches
    
    def get_all_error_codes(self) -> List[str]:
        """
        Get list of all error codes in knowledge base
        
        Returns:
            List of error codes
        """
        return list(self.error_codes.keys())
    
    def is_known_error(self, error_code: str) -> bool:
        """
        Check if error code is in knowledge base
        
        Args:
            error_code: Error code to check
            
        Returns:
            True if error code is known
        """
        if not error_code or error_code == 'NOT FOUND':
            return False
        
        error_code = error_code.upper().strip()
        return error_code in self.error_codes
    
    def get_summary(self, error_code: str) -> str:
        """
        Get brief summary of error
        
        Args:
            error_code: Error code
            
        Returns:
            Brief summary text
        """
        error_info = self.get_error_info(error_code)
        if error_info:
            return f"{error_info.get('name', 'Unknown Error')}: {error_info.get('description', '')[:100]}..."
        return f"Unknown error code: {error_code}"


# Example usage and testing
if __name__ == "__main__":
    kb = KnowledgeBase()
    
    print("Knowledge Base Test")
    print("=" * 70)
    print(f"Total error codes loaded: {len(kb.get_all_error_codes())}")
    print(f"Error codes: {', '.join(kb.get_all_error_codes())}")
    print()
    
    # Test specific error code
    test_code = "U0777"
    print(f"Testing error code: {test_code}")
    print()
    print(kb.format_resolution(test_code))
    print()
    
    # Test search
    print("Searching for 'data':")
    results = kb.search_by_keyword('data')
    print(f"Found: {', '.join(results)}")

# Made with Bob
