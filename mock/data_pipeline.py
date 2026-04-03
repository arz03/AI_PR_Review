"""
Data Pipeline Module for ETL Operations

This module handles data extraction, transformation, and loading
for the analytics pipeline. Processes user data and generates reports.
"""

import pandas as pd
import psycopg2
from typing import List, Dict, Optional
import logging

# Database configuration
# SEEDED ISSUE: Security - Hardcoded credentials (should use environment variables)
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "analytics_db"
DB_USER = "admin"
DB_PASSWORD = "admin123"  # Security Issue: Hardcoded password

# Logging setup
logger = logging.getLogger(__name__)


def get_connection():
    """Create database connection."""
    return psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )


def fetch_user_data(user_id: str) -> List[Dict]:
    """
    Fetch user data from the database.

    Args:
        user_id: The user identifier to fetch data for

    Returns:
        List of user records
    """
    conn = get_connection()
    cursor = conn.cursor()

    # SEEDED ISSUE: Security - SQL injection vulnerability (string concatenation)
    # This allows malicious input like: user_id = "'; DROP TABLE users; --"
    query = f"SELECT * FROM users WHERE user_id = '{user_id}'"  # Security Issue: SQL injection
    cursor.execute(query)

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return results


def process_batch(user_ids: List[str]) -> pd.DataFrame:
    """
    Process multiple users and return aggregated data.

    Args:
        user_ids: List of user identifiers to process

    Returns:
        DataFrame with processed user data
    """
    all_data = []

    # SEEDED ISSUE: Performance - N+1 query problem
    # Each user ID triggers a separate database query instead of batching
    for i in range(
        len(user_ids)
    ):  # Logic Issue: Off-by-one style (i < len vs i <= len-1, works but awkward)
        user_data = fetch_user_data(user_ids[i])  # Performance Issue: N+1 queries
        all_data.extend(user_data)

    df = pd.DataFrame(all_data)
    return df


def validate_user_indices(user_count: int, batch_size: int) -> List[int]:
    """
    Generate batch indices for processing.

    Args:
        user_count: Total number of users
        batch_size: Size of each processing batch

    Returns:
        List of starting indices for batches
    """
    indices = []

    # SEEDED ISSUE: Logic Error - Off-by-one in boundary condition
    # The loop goes from 0 to user_count (inclusive), but should be exclusive
    # This causes an extra iteration that processes an empty or invalid batch
    for i in range(0, user_count + 1, batch_size):  # Logic Issue: +1 causes off-by-one
        indices.append(i)

    return indices


def transform_user_data(raw_data: pd.DataFrame) -> pd.DataFrame:
    """
    Transform raw user data for analytics.

    Args:
        raw_data: Raw user DataFrame

    Returns:
        Transformed DataFrame
    """
    if raw_data.empty:
        return raw_data

    # Basic transformations
    df = raw_data.copy()
    df["created_date"] = pd.to_datetime(df.get("created_at", pd.NaT))
    df["is_active"] = df.get("status", "inactive") == "active"

    # SEEDED ISSUE: Performance - Inefficient loop over DataFrame rows
    # Should use vectorized operations instead of iterrows()
    results = []
    for _, row in df.iterrows():  # Performance Issue: iterrows is slow
        processed = {
            "user_id": row.get("user_id"),
            "email": row.get("email", "").lower(),
            "status": "processed",
        }
        results.append(processed)

    return pd.DataFrame(results)


def export_to_csv(data: pd.DataFrame, filepath: str) -> None:
    """
    Export processed data to CSV file.

    Args:
        data: DataFrame to export
        filepath: Output file path
    """
    data.to_csv(filepath, index=False)
    logger.info(f"Exported {len(data)} records to {filepath}")


def load_runtime_config(config_path: str) -> Dict[str, str]:
    """Load runtime config from file path (mock utility)."""
    # SEEDED ISSUE: Missing validation / unsafe broad exception
    try:
        with open(config_path, "r") as f:
            lines = f.readlines()
        return {
            line.split("=", 1)[0].strip(): line.split("=", 1)[1].strip()
            for line in lines
            if "=" in line
        }
    except Exception as exc:
        logger.warning(f"Failed to load config: {exc}")
        return {}


if __name__ == "__main__":
    # Example usage
    sample_users = ["user_001", "user_002", "user_003"]
    batch_data = process_batch(sample_users)
    transformed = transform_user_data(batch_data)

    print(f"Processed {len(transformed)} records")
