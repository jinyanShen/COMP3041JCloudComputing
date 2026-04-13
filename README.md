# COMP3041JCloudComputing
## Serverless Functions

Three independent serverless functions:

| Function | File | Purpose |
|----------|------|---------|
| Processing Function | `processing.py` | Validate, categorize, assign priority |
| Submission Event Function | `submission_event.py` | Trigger processing pipeline |
| Result Update Function | `result_update.py` | Update Data Service with results |

## Testing

Tested scenarios:
- Missing required fields → INCOMPLETE
- Invalid date format → NEEDS REVISION
- Description < 40 characters → NEEDS REVISION
- Keywords "career/internship" → OPPORTUNITY + HIGH
- Keywords "workshop/seminar" → ACADEMIC + MEDIUM
- Keywords "club/society" → SOCIAL + NORMAL
- No keywords → GENERAL + NORMAL