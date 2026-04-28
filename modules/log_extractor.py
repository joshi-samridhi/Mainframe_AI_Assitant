"""
Log extraction module for parsing mainframe logs
Uses regex patterns as primary method with AI fallback
"""
import re
from typing import Dict, Optional, Tuple


class LogExtractor:
    """Extract information from mainframe logs using regex patterns"""
    
    # Regex patterns for mainframe log fields - prioritize simple key=value format
    PATTERNS = {
        'jobname': [
            # Primary: JOBNAME=VALUE format (most common in user logs)
            r'JOBNAME\s*=\s*([A-Z0-9]+)',
            # Alternative: JOBNAME:VALUE or JOBNAME VALUE
            r'JOBNAME\s*:\s*([A-Z0-9]+)',
            # IEF236I ALLOC. FOR JOBNAME JOBID
            r'IEF236I\s+ALLOC\.\s+FOR\s+([A-Z0-9]+)',
            # IEF450I JOBNAME STEP - ABEND
            r'IEF450I\s+([A-Z0-9]+)\s+\w+',
            # JOB /JOBNAME/ format
            r'JOB\s+/([A-Z0-9]+)/',
        ],
        'jobid': [
            # Primary: JOBID=VALUE format
            r'JOBID\s*=\s*([A-Z0-9]+)',
            # Alternative formats
            r'JOB\s*ID\s*[=:]\s*([A-Z0-9]+)',
            r'JOBID\s*:\s*([A-Z0-9]+)',
            # IEF236I ALLOC. FOR JOBNAME JOBID
            r'IEF236I\s+ALLOC\.\s+FOR\s+[A-Z0-9]+\s+([A-Z0-9]+)',
            # Line starting with JOBID
            r'^\s*([A-Z0-9]{6,8})\s+',
        ],
        'status': [
            # Primary: STATUS=VALUE format
            r'STATUS\s*=\s*(ABEND|ABENDED|FAILED|ERROR|COMPLETED|SUCCESS|STARTED|TERMINATED)',
            # Alternative: STATUS:VALUE
            r'STATUS\s*:\s*(ABEND|ABENDED|FAILED|ERROR|COMPLETED|SUCCESS|STARTED|TERMINATED)',
            # Look for ABEND keyword
            r'(ABEND)\s*=',
            # Look for status keywords in text
            r'\b(ABENDED|FAILED|TERMINATED)\b',
        ],
        'return_code': [
            # Primary: RETURN_CODE=VALUE format
            r'RETURN_CODE\s*=\s*([A-Z0-9]+)',
            # Alternative: RETURN CODE=VALUE (with space)
            r'RETURN\s+CODE\s*[=:]\s*([A-Z0-9]+)',
            # RC=VALUE format
            r'RC\s*=\s*([A-Z0-9]+)',
            # IEF450I format: ABEND=S0C7
            r'IEF450I.*ABEND\s*=\s*([SU][0-9A-F]{3,4})',
            # IEF472I format: SYSTEM=0C7
            r'IEF472I.*SYSTEM\s*=\s*([0-9A-F]{3,4})',
            # CEE format: (System Completion Code=0C7)
            r'\(System\s+Completion\s+Code\s*=\s*([0-9A-F]{3,4})\)',
            # Generic ABEND= format
            r'ABEND\s*=\s*([SU][0-9A-F]{3,4})',
        ],
        'step': [
            # Primary: STEP=VALUE format
            r'STEP\s*=\s*([A-Z0-9]+)',
            # Alternative: STEP:VALUE
            r'STEP\s*:\s*([A-Z0-9]+)',
            # STEPNAME format in text
            r'STEPNAME\s*[=:]\s*([A-Z0-9]+)',
            # IEF450I JOBNAME STEPNAME - ABEND
            r'IEF450I\s+[A-Z0-9]+\s+([A-Z0-9]+)\s+-',
            # STEP /STEPNAME/ format
            r'STEP\s+/([A-Z0-9]+)\s+/',
        ],
        'error': [
            # Primary: ERROR=VALUE format
            r'ERROR\s*=\s*([A-Z0-9_]+)',
            # Alternative: ERROR:VALUE or ERROR VALUE
            r'ERROR\s*:\s*(.+?)(?:\n|$)',
            r'ERROR\s+DETECTED\s+(.+?)(?:\n|$)',
            # CEE messages
            r'(CEE\d+[A-Z]\s+.+?)(?:\n|$)',
            # IEC messages
            r'(IEC\d+[A-Z]\s+.+?)(?:\n|$)',
            # Data exception message
            r'(The system detected a .+?)(?:\n|$)',
        ]
    }
    
    def __init__(self):
        """Initialize the log extractor"""
        self.confidence_threshold = 0.7
    
    def extract(self, log_content: str) -> Tuple[Dict[str, str], float, str]:
        """
        Extract information from log content
        
        Args:
            log_content: Raw log text
            
        Returns:
            Tuple of (extracted_data, confidence, method)
            - extracted_data: Dictionary with extracted fields
            - confidence: Confidence score (0.0 to 1.0)
            - method: Extraction method used ('regex' or 'ai')
        """
        if not log_content or not log_content.strip():
            return self._empty_result(), 0.0, 'none'
        
        # Try regex extraction first
        extracted_data, confidence = self._extract_with_regex(log_content)
        
        # If confidence is high enough, return regex results
        if confidence >= self.confidence_threshold:
            return extracted_data, confidence, 'regex'
        
        # Otherwise, mark for AI fallback
        return extracted_data, confidence, 'regex_low_confidence'
    
    def _extract_with_regex(self, log_content: str) -> Tuple[Dict[str, str], float]:
        """
        Extract fields using regex patterns
        Prioritizes lines with error indicators (ABEND, FAILED, ERROR)
        
        Returns:
            Tuple of (extracted_data, confidence_score)
        """
        extracted = {}
        fields_found = 0
        total_fields = len(self.PATTERNS)
        
        # Convert to uppercase for case-insensitive matching
        log_upper = log_content.upper()
        
        # Find the error line (line with ABEND, FAILED, or ERROR status)
        error_line = None
        for line in log_content.split('\n'):
            line_upper = line.upper()
            if 'STATUS=ABEND' in line_upper or 'STATUS=FAILED' in line_upper:
                error_line = line
                break
            elif 'ABENDED' in line_upper or 'TERMINATED ABNORMALLY' in line_upper:
                error_line = line
                break
        
        # If we found an error line, prioritize extracting from it
        if error_line:
            error_line_upper = error_line.upper()
            for field, patterns in self.PATTERNS.items():
                # Try to extract from error line first
                value = self._extract_field(error_line, error_line_upper, patterns)
                if value != 'NOT FOUND':
                    extracted[field] = value
                    fields_found += 1
                else:
                    # Fall back to full log if not found in error line
                    value = self._extract_field(log_content, log_upper, patterns)
                    extracted[field] = value
                    if value != 'NOT FOUND':
                        fields_found += 1
        else:
            # No specific error line found, extract from full log
            for field, patterns in self.PATTERNS.items():
                value = self._extract_field(log_content, log_upper, patterns)
                extracted[field] = value
                if value != 'NOT FOUND':
                    fields_found += 1
        
        # Special handling for STATUS
        if extracted['status'] == 'NOT FOUND':
            # Default to ABEND if error indicators are present
            if any(keyword in log_upper for keyword in ['ABEND', 'ERROR', 'FAILED']):
                extracted['status'] = 'ABEND'
                fields_found += 1
        
        # Calculate confidence based on fields found
        confidence = fields_found / total_fields if total_fields > 0 else 0.0
        
        return extracted, confidence
    
    def _extract_field(self, log_content: str, log_upper: str, patterns: list) -> str:
        """
        Extract a single field using multiple patterns
        
        Args:
            log_content: Original log content (preserves case)
            log_upper: Uppercase version for matching
            patterns: List of regex patterns to try
            
        Returns:
            Extracted value or 'NOT FOUND'
        """
        for pattern in patterns:
            # Try case-insensitive match
            match = re.search(pattern, log_upper, re.IGNORECASE | re.MULTILINE)
            if match:
                value = match.group(1).strip()
                if value:
                    return value
        
        return 'NOT FOUND'
    
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
    
    def validate_extraction(self, extracted_data: Dict[str, str]) -> bool:
        """
        Validate extracted data
        
        Args:
            extracted_data: Dictionary of extracted fields
            
        Returns:
            True if at least some critical fields were found
        """
        critical_fields = ['return_code', 'error']
        found_critical = sum(
            1 for field in critical_fields 
            if extracted_data.get(field, 'NOT FOUND') != 'NOT FOUND'
        )
        
        return found_critical > 0
    
    def format_output(self, extracted_data: Dict[str, str]) -> str:
        """
        Format extracted data for display
        
        Args:
            extracted_data: Dictionary of extracted fields
            
        Returns:
            Formatted string
        """
        output = []
        output.append("=" * 50)
        output.append("EXTRACTED INFORMATION")
        output.append("=" * 50)
        output.append(f"JOBNAME:      {extracted_data.get('jobname', 'NOT FOUND')}")
        output.append(f"JOBID:        {extracted_data.get('jobid', 'NOT FOUND')}")
        output.append(f"STATUS:       {extracted_data.get('status', 'NOT FOUND')}")
        output.append(f"RETURN CODE:  {extracted_data.get('return_code', 'NOT FOUND')}")
        output.append(f"STEP:         {extracted_data.get('step', 'NOT FOUND')}")
        output.append(f"ERROR:        {extracted_data.get('error', 'NOT FOUND')}")
        output.append("=" * 50)
        
        return "\n".join(output)


# Example usage and testing
if __name__ == "__main__":
    # Test with sample log
    sample_log = """
    JOBNAME: DUMMYBATCH01
    JOBID: 12345
    STATUS: ABEND
    RETURN CODE: U0777
    STEP: STEP002
    ERROR: DATA VALIDATION FAILED
    
    Job Log:
    Invalid record RECORD#007, STEP002 ended abnormally
    """
    
    extractor = LogExtractor()
    data, confidence, method = extractor.extract(sample_log)
    
    print(extractor.format_output(data))
    print(f"\nConfidence: {confidence:.2%}")
    print(f"Method: {method}")

# Made with Bob
