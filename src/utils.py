import numpy as np
import pandas as pd

def convert_ip_to_int(ip_address):
    """
    Convert an IP address string to an integer by removing dots.
    
    Args:
    - ip_address: IP address as a string
    
    Returns:
    - int: Integer representation of the IP address
    """
    try:
        # Ensure IP address is a valid string before conversion
        if isinstance(ip_address, str):
            return int(ip_address.replace('.', ''))
        else:
            # Handle missing or invalid IP addresses
            return None  # or you could return 0 if that's more suitable
    except Exception as e:
        print(f"Error converting IP address {ip_address}: {e}")
        return None


def merge_ip_country(df, ip_data):
    """
    Merge the fraud data with the IP address-to-country data using IP ranges.
    
    Args:
    - df: DataFrame containing fraud data with IP addresses
    - ip_data: DataFrame containing IP-to-country mapping
    
    Returns:
    - merged_df: DataFrame merged based on whether the fraud IP falls within the IP range in the IP-to-country data.
    """
    # Ensure 'ip_address' is treated as a string to handle missing values
    df['ip_address'] = df['ip_address'].astype(str)
    
    # Convert IP addresses to integer format, handling errors
    df['ip_address_int'] = df['ip_address'].apply(lambda x: convert_ip_to_int(x) if x != 'nan' else None)

    # Ensure both 'lower_bound_ip_address' and 'upper_bound_ip_address' in ip_data are strings
    ip_data['lower_bound_ip_address'] = ip_data['lower_bound_ip_address'].astype(str)
    ip_data['upper_bound_ip_address'] = ip_data['upper_bound_ip_address'].astype(str)

    # Convert the IP addresses in the IP-to-country dataset to integer format
    ip_data['ip_from_int'] = ip_data['lower_bound_ip_address'].apply(lambda x: convert_ip_to_int(x) if x != 'nan' else None)
    ip_data['ip_to_int'] = ip_data['upper_bound_ip_address'].apply(lambda x: convert_ip_to_int(x) if x != 'nan' else None)

    # Ensure columns are of numeric types before merging
    df['ip_address_int'] = pd.to_numeric(df['ip_address_int'], errors='coerce')
    ip_data['ip_from_int'] = pd.to_numeric(ip_data['ip_from_int'], errors='coerce')
    ip_data['ip_to_int'] = pd.to_numeric(ip_data['ip_to_int'], errors='coerce')

    # Drop any rows with missing IP address conversions
    df = df.dropna(subset=['ip_address_int'])
    ip_data = ip_data.dropna(subset=['ip_from_int', 'ip_to_int'])

    # Merge fraud data with IP-country data based on IP address range
    merged_df = pd.merge_asof(
        df.sort_values('ip_address_int'),
        ip_data.sort_values('ip_from_int'),
        left_on='ip_address_int',
        right_on='ip_from_int',
        direction='backward'
    )

    # Now filter rows where 'ip_address_int' falls within the specified range of 'ip_from_int' and 'ip_to_int'
    merged_df = merged_df[(merged_df['ip_address_int'] >= merged_df['ip_from_int']) & 
                          (merged_df['ip_address_int'] <= merged_df['ip_to_int'])]

    return merged_df

