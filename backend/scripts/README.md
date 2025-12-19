# Backend Scripts Documentation

## verify_ingestion.py

This script verifies that the ingestion pipeline has successfully stored data in both Qdrant and Neon databases.

### Usage

```bash
cd backend/scripts
python verify_ingestion.py
```

### What it does

1. **Verifies Qdrant Connection**: Checks that the Qdrant service is accessible
2. **Verifies Neon Connection**: Checks that the Neon database is accessible
3. **Reports Status**: Provides clear success/failure messages

### Prerequisites

- Environment variables must be set in `.env` file:
  ```
  COHERE_API_KEY=your_cohere_api_key_here
  QDRANT_HOST=your_qdrant_host_here
  QDRANT_API_KEY=your_qdrant_api_key_here
  NEON_DB_URL=your_neon_db_url_here
  ```

### Output

On success:
```
INFO: Starting ingestion verification...
INFO: Verifying Qdrant database...
INFO: Qdrant service initialized successfully
INFO: ✓ Qdrant verification completed - service is available
INFO: Verifying Neon database...
INFO: Neon database connection successful
INFO: ✓ Neon verification completed - database is accessible
INFO: ✓ All verifications completed successfully!
INFO: ✓ Ingestion pipeline is working correctly
```

On failure:
```
ERROR: Error verifying [service]: [error message]
```