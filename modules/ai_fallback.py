"""
AI fallback module for complex log parsing using OpenAI
"""
import os
from typing import Dict, Optional, Tuple
import json


class AIFallback:
    """Use OpenAI API for complex log parsing when regex fails"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI fallback
        
        Args:
            api_key: OpenAI API key
        """
        self.api_key = api_key or os.environ.get('OPENAI_API_KEY')
        self.client = None
        
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("Warning: OpenAI package not installed. AI fallback disabled.")
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
    
    def is_available(self) -> bool:
        """Check if AI fallback is available"""
        return self.client is not None
    
    def extract(self, log_content: str) -> Tuple[Dict[str, str], float]:
        """
        Extract information using AI
        
        Args:
            log_content: Raw log text
            
        Returns:
            Tuple of (extracted_data, confidence)
        """
        if not self.is_available():
            return self._empty_result(), 0.0
        
        try:
            # Create prompt for extraction
            prompt = self._create_extraction_prompt(log_content)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a mainframe log analysis expert. Extract structured information from logs accurately."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse response
            result_text = response.choices[0].message.content
            extracted_data = self._parse_ai_response(result_text)
            
            # Calculate confidence based on fields found
            fields_found = sum(1 for v in extracted_data.values() if v != 'NOT FOUND')
            confidence = fields_found / len(extracted_data) if extracted_data else 0.0
            
            return extracted_data, confidence
            
        except Exception as e:
            print(f"AI extraction error: {e}")
            return self._empty_result(), 0.0
    
    def _create_extraction_prompt(self, log_content: str) -> str:
        """
        Create extraction prompt for AI
        
        Args:
            log_content: Raw log text
            
        Returns:
            Formatted prompt
        """
        prompt = f"""Analyze this mainframe log and extract the following information:

Log Content:
{log_content}

Extract these fields (use "NOT FOUND" if not present):
1. JOBNAME: The job name
2. JOBID: The job ID or number
3. STATUS: Job status (ABEND, FAILED, ERROR, COMPLETED, or SUCCESS)
4. RETURN CODE: The return/completion code (e.g., U0777, S013, S0C7)
5. STEP: The step name where error occurred
6. ERROR: Brief error description

Respond in this exact JSON format:
{{
    "jobname": "value or NOT FOUND",
    "jobid": "value or NOT FOUND",
    "status": "value or NOT FOUND",
    "return_code": "value or NOT FOUND",
    "step": "value or NOT FOUND",
    "error": "value or NOT FOUND"
}}

Important:
- If STATUS is not explicitly stated but there's an error, use "ABEND"
- Extract only what's clearly present in the log
- Do not guess or infer information
- Return ONLY the JSON, no additional text"""
        
        return prompt
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, str]:
        """
        Parse AI response to extract structured data
        
        Args:
            response_text: AI response text
            
        Returns:
            Dictionary of extracted fields
        """
        try:
            # Try to find JSON in response
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            
            if start >= 0 and end > start:
                json_str = response_text[start:end]
                data = json.loads(json_str)
                
                # Validate and normalize
                result = {}
                expected_fields = ['jobname', 'jobid', 'status', 'return_code', 'step', 'error']
                
                for field in expected_fields:
                    value = data.get(field, 'NOT FOUND')
                    # Clean up value
                    if isinstance(value, str):
                        value = value.strip()
                        if not value or value.lower() == 'not found':
                            value = 'NOT FOUND'
                    result[field] = value
                
                return result
            else:
                print("No JSON found in AI response")
                return self._empty_result()
                
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            return self._empty_result()
        except Exception as e:
            print(f"Error parsing AI response: {e}")
            return self._empty_result()
    
    def _empty_result(self) -> Dict[str, str]:
        """Return empty result with all fields as NOT FOUND"""
        return {
            'jobname': 'NOT FOUND',
            'jobid': 'NOT FOUND',
            'status': 'NOT FOUND',
            'return_code': 'NOT FOUND',
            'step': 'NOT FOUND',
            'error': 'NOT FOUND'
        }
    
    def enhance_extraction(self, regex_data: Dict[str, str], log_content: str) -> Tuple[Dict[str, str], float]:
        """
        Enhance regex extraction with AI for missing fields
        
        Args:
            regex_data: Data extracted by regex
            log_content: Original log content
            
        Returns:
            Tuple of (enhanced_data, confidence)
        """
        if not self.is_available():
            return regex_data, 0.0
        
        # Find missing fields
        missing_fields = [k for k, v in regex_data.items() if v == 'NOT FOUND']
        
        if not missing_fields:
            return regex_data, 1.0
        
        # Use AI to fill missing fields
        ai_data, ai_confidence = self.extract(log_content)
        
        # Merge results (prefer regex, use AI for missing)
        enhanced_data = regex_data.copy()
        for field in missing_fields:
            if ai_data.get(field, 'NOT FOUND') != 'NOT FOUND':
                enhanced_data[field] = ai_data[field]
        
        # Calculate combined confidence
        fields_found = sum(1 for v in enhanced_data.values() if v != 'NOT FOUND')
        confidence = fields_found / len(enhanced_data) if enhanced_data else 0.0
        
        return enhanced_data, confidence


# Example usage and testing
if __name__ == "__main__":
    sample_log = """
    Job TESTBATCH99 failed with completion code S0C7
    Step CALC001 encountered a data exception
    The numeric field AMOUNT contained invalid characters
    """
    
    ai = AIFallback()
    
    if ai.is_available():
        print("Testing AI extraction...")
        data, confidence = ai.extract(sample_log)
        
        print("\nExtracted Data:")
        for key, value in data.items():
            print(f"  {key}: {value}")
        print(f"\nConfidence: {confidence:.2%}")
    else:
        print("AI fallback not available (OpenAI API key not configured)")

# Made with Bob
