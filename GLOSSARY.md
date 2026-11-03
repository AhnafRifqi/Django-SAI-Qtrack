# SAI-Qtrack

A digital quality control and scrap tracking system tailored for automotive wiring harness manufacturing at PT. Surabaya Autocomp Indonesia. It captures real-time shopfloor defect logs and provides traceable quality analytics.

## Language

**Line**:
A designated physical production line within the manufacturing plant where wiring harnesses or sub-assemblies are processed.
_Avoid_: Department, section, workshop, station

**Harness Part**:
A specific wiring harness assembly identified by an OEM automotive part number.
_Avoid_: Product, SKU, item, component

**Defect Category**:
A standardized classification for an electrical or mechanical fault occurring during harness manufacturing (e.g., Crimp Deformed, Wire Core Cut, Continuity Fail).
_Avoid_: Issue, problem, bug, error

**Defect Log**:
An immutable record capturing a detected defect occurrence on a specific line, shift, and harness part.
_Avoid_: Ticket, transaction, defect report

**Shift**:
A designated production operational work shift (Shift 1, Shift 2, Shift 3) under which output and defects are logged.
_Avoid_: Working hours, schedule, session

**Action Taken**:
The physical disposition applied to a defective unit, classified strictly into Scrap or Rework.
_Avoid_: Resolution, fix, disposition status
