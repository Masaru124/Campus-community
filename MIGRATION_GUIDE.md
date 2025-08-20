# Database Migration Guide: SQLite to Neon PostgreSQL

## Steps to Complete Migration

### 1. Update Dependencies
The PostgreSQL driver has been added to requirements.txt. Install it with:
```bash
pip install -r requirements.txt
```

### 2. Configure Neon Database
1. Go to [Neon](https://neon.tech) and create an account
2. Create a new project/database
3. Get your connection string (it will look like):
   ```
   postgresql://username:password@hostname.neon.tech:5432/database_name
   ```

### 3. Update .env File
Add your Neon connection string to your .env file:
```
DATABASE_URL=postgresql://your_username:your_password@your_host.neon.tech:5432/your_database
```

### 4. Database Schema Creation
Since we're not migrating data, you'll need to create the schema in your new PostgreSQL database:

```bash
# Run this to create all tables in your new PostgreSQL database
python -c "from app.db import engine; from app.models import Base; Base.metadata.create_all(engine)"
```

### 5. Verify Connection
Test your application:
```bash
uvicorn app.main:app --reload
```

## Connection String Format
- **SQLite**: `sqlite:///./campus.db`
- **PostgreSQL/Neon**: `postgresql://username:password@hostname:port/database_name`

## Troubleshooting
- If you get connection errors, check your Neon credentials
- Ensure your Neon database allows connections from your IP address
- Check firewall settings if connection fails
