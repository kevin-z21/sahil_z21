from datetime import datetime
from core.logger import Logger

logger = Logger()

def _parse_timestamp(timestamp_str):
        """Try multiple datetime formats"""
        formats = [
            "%m/%d/%Y %H:%M:%S",     # 02/04/2025 15:57:32 - NC 
            "%m/%d/%Y %I:%M:%S %p",  # 02/04/2025 03:57:32 PM - Nifty Index
            "%Y-%m-%d %H:%M:%S"      # 2025-02-04 15:57:32 - NF
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str, fmt)
            except ValueError:
                continue
                
        logger.error(f"Failed to parse timestamp: {timestamp_str}")
        return None

def _convert_to_postgres_timestamp(datetime_str):
        """Convert datetime string to PostgreSQL timestamp format"""
        try:
            # Parse input datetime string
            parsed_date = _parse_timestamp(datetime_str)
            if not parsed_date:
                return None
                
            # Format for PostgreSQL timestamp (YYYY-MM-DD HH:MM:SS)
            postgres_timestamp = parsed_date.strftime('%Y-%m-%d %H:%M:%S')
            return postgres_timestamp
            
        except Exception as e:
            logger.error(f"Error converting to PostgreSQL timestamp: {str(e)}")
            return None
        