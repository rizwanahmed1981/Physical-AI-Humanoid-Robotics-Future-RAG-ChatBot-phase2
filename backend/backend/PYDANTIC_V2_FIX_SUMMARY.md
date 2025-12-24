# Pydantic V2 Compatibility Fix Summary

## Issue
The backend was displaying a `UserWarning` about `schema_extra` being renamed to `json_schema_extra` because the project is using Pydantic V2 but the models were configured with V1 conventions.

## Changes Made

**File Modified**: `backend/app/models/schemas.py`

### Changes:
1. **QueryRequest class** (line 11): Changed `schema_extra` to `json_schema_extra`
2. **Source class** (line 28): Changed `schema_extra` to `json_schema_extra`
3. **QueryResponse class** (line 44): Changed `schema_extra` to `json_schema_extra`

## Verification

The fix has been applied consistently across all Pydantic models in the file:
- All `schema_extra` references have been replaced with `json_schema_extra`
- The functionality remains identical - the example payloads are unchanged
- No other modifications were made to preserve existing behavior

## Result

After this change:
- The Pydantic V2 compatibility warning should no longer appear
- All API examples continue to work exactly as before
- The OpenAPI/Swagger documentation will display correctly without warnings
- The backend functionality remains fully intact

## Next Steps

To verify the fix:
1. Restart the FastAPI server
2. Check that the warning no longer appears in the console output
3. Confirm that all API endpoints continue to function normally

The implementation follows the Pydantic V2 migration guide recommendations and maintains backward compatibility for all existing functionality.