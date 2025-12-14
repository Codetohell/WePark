# WePark/testing/backend/app/utils/helper.py
"""
Backward Compatibility Helper Module
Imports all helper functions from specialized modules for backward compatibility
"""

# Import validators
from .validators import (
    validate_email_format,
    validate_username_format,
    validate_password_strength,
    validate_pincode,
    validate_phone_number,
    check_email_format,  # Backward compatibility
    check_username_format,  # Backward compatibility
)

# Import decorators
from .decorators import (
    role_required,
    roles_required,
    admin_required,
    user_required,
)

# Import datetime helpers
from .datetime_helpers import (
    get_ist_time,
    get_utc_time,
    convert_to_ist,
    get_past_months,
    get_month_name,
    format_datetime_ist,
    calculate_duration_hours,
)

# Import business helpers
from .business_helpers import (
    can_delete_lot,
    calculate_parking_cost,
    format_currency,
    calculate_occupancy_rate,
    lot_can_delete,  # Backward compatibility
)

__all__ = [
    # Validators
    'validate_email_format',
    'validate_username_format',
    'validate_password_strength',
    'validate_pincode',
    'validate_phone_number',
    'check_email_format',
    'check_username_format',
    
    # Decorators
    'role_required',
    'roles_required',
    'admin_required',
    'user_required',
    
    # DateTime helpers
    'get_ist_time',
    'get_utc_time',
    'convert_to_ist',
    'get_past_months',
    'get_month_name',
    'format_datetime_ist',
    'calculate_duration_hours',
    
    # Business helpers
    'can_delete_lot',
    'calculate_parking_cost',
    'format_currency',
    'calculate_occupancy_rate',
    'lot_can_delete',
]