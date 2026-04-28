"""Test script to verify log extraction works with user's actual log format"""
import sys
sys.path.insert(0, '.')

from modules.log_extractor import LogExtractor

# User's actual log
test_log = """LOGS.YPSM26.MAINLOG
---------------------------------------------------------------
22.10.12 JOB45872  JOB STARTED - BATCH PROCESS INITIATED

22.10.14 JOB45872  JOBNAME=PAYROLL1 JOBID=JOB45872 STEP=STEP01 STATUS=STARTED
22.10.18 JOB45872  STEP01 EXEC PGM=IKJEFT01
22.10.22 JOB45872  STEP01 COMPLETED RC=0000 STATUS=SUCCESS

22.10.25 JOB45872  JOBNAME=PAYROLL1 JOBID=JOB45872 STEP=STEP02 STATUS=STARTED
22.10.28 JOB45872  STEP02 EXEC PGM=COBOLPGM
22.10.35 JOB45872  ERROR DETECTED DURING PROCESSING INPUT RECORD

22.10.36 JOB45872  JOBNAME=PAYROLL1 JOBID=JOB45872 STEP=STEP02 STATUS=ABENDED 
                  RETURN_CODE=U0777 ERROR=USER_ABEND_INVALID_DATA

22.10.38 JOB45872  STEP02 TERMINATED ABNORMALLY
22.10.40 JOB45872  JOB TERMINATED - STATUS=FAILED RETURN_CODE=U0777

---------------------------------------------------------------
PF1=HELP  PF3=EXIT  PF5=REFRESH  PF7=UP  PF8=DOWN  PF12=CANCEL
---------------------------------------------------------------"""

# Test extraction
extractor = LogExtractor()
result, confidence, method = extractor.extract(test_log)

print("=" * 60)
print("EXTRACTION TEST RESULTS - USER'S LOG FORMAT")
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
print("JOBNAME:      PAYROLL1")
print("JOBID:        JOB45872")
print("STATUS:       ABENDED")
print("RETURN CODE:  U0777")
print("STEP:         STEP02")
print("ERROR:        USER_ABEND_INVALID_DATA")
print("=" * 60)

# Check if all fields match
all_correct = (
    result['jobname'] == 'PAYROLL1' and
    result['jobid'] == 'JOB45872' and
    result['status'] == 'ABENDED' and
    result['return_code'] == 'U0777' and
    result['step'] == 'STEP02' and
    result['error'] == 'USER_ABEND_INVALID_DATA'
)

if all_correct:
    print("\n[OK] ALL FIELDS EXTRACTED CORRECTLY!")
else:
    print("\n[FAIL] Some fields are incorrect")

# Made with Bob
