"""Test script to verify log extraction works correctly"""
import sys
sys.path.insert(0, '.')

from modules.log_extractor import LogExtractor

# Your sample log
test_log = """IEF236I ALLOC. FOR PAYBATCH JOB12345
IEF237I JES2 ALLOCATED TO SYSOUT
IEF142I PAYBATCH STEP010 - STEP WAS EXECUTED - COND CODE 0000
IEF285I   SYS26094.T120530.RA000.PAYBATCH.R0101234   KEPT          
IEF285I   VOL SER NOS= WORK01.                            
IEF373I STEP /STEP010  / START 2026094.1205
IEF374I STEP /STEP010  / STOP  2026094.1206 CPU    0MIN 02.15SEC SRB    0MIN 00.00SEC VIRT   252K SYS   240K EXT       0K SYS       0K
CEE3204S The system detected a data exception (System Completion Code=0C7).
   From compile unit PAYROLL at entry point PAYROLL at compile unit offset +00000A3C at entry offset +00000A3C at address 0E8D0A3C.
IEF450I PAYBATCH STEP010 - ABEND=S0C7 U0000 REASON=00000000
         TIME=12.06.30
IEF472I PAYBATCH STEP010 - COMPLETION CODE - SYSTEM=0C7
IEF142I PAYBATCH STEP010 - STEP WAS NOT EXECUTED
IEF272I PAYBATCH STEP010 - STEP WAS NOT EXECUTED.
IEF373I STEP /STEP010  / START 2026094.1206
IEF374I STEP /STEP010  / STOP  2026094.1206 CPU    0MIN 00.00SEC SRB    0MIN 00.00SEC
IEF375I  JOB /PAYBATCH/ START 2026094.1205
IEF376I  JOB /PAYBATCH/ STOP  2026094.1206 CPU    0MIN 02.15SEC SRB    0MIN 00.00SEC"""

# Test extraction
extractor = LogExtractor()
result, confidence, method = extractor.extract(test_log)

print("=" * 60)
print("EXTRACTION TEST RESULTS")
print("=" * 60)
print(f"Method: {method}")
print(f"Confidence: {confidence:.2%}")
print("-" * 60)
print(f"JOBNAME:      {result['jobname']}")
print(f"JOBID:        {result['jobid']}")
print(f"STATUS:       {result['status']}")
print(f"RETURN CODE:  {result['return_code']}")
print(f"STEP:         {result['step']}")
print(f"ERROR:        {result['error']}")
print("=" * 60)

# Expected results
print("\nEXPECTED RESULTS:")
print("-" * 60)
print("JOBNAME:      PAYBATCH")
print("JOBID:        JOB12345")
print("STATUS:       ABEND")
print("RETURN CODE:  S0C7 or 0C7")
print("STEP:         STEP010")
print("ERROR:        CEE3204S The system detected a data exception...")
print("=" * 60)

# Made with Bob
