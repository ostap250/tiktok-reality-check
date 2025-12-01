"""Pure data processing logic for the TikTok Reality Check app."""

import json
import pandas as pd
import datetime


def _find_by_known_paths(data):
    """
    Strategy 1: Check common known paths for video history.
    
    Args:
        data: JSON dictionary
        
    Returns:
        list or None: Video list if found, None otherwise
    """
    known_paths = [
        ['Activity', 'Video Browsing History', 'VideoList'],
        ['Activity', 'Favorite Videos', 'FavoriteVideoList'],
        ['Video Browsing History', 'VideoList']
    ]
    
    for path in known_paths:
        try:
            current = data
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    break
            else:
                # Successfully traversed the path
                if isinstance(current, list) and len(current) > 0:
                    return current
        except (KeyError, TypeError):
            continue
    
    return None


def _find_by_key_name(data, target_key='VideoList'):
    """
    Strategy 2: Recursively search for any key named 'VideoList'.
    
    Args:
        data: Dictionary or list to search recursively
        target_key: Key name to search for (default: 'VideoList')
        
    Returns:
        list or None: Video list if found, None otherwise
    """
    if isinstance(data, dict):
        # Check if target_key exists in this dict
        if target_key in data:
            value = data[target_key]
            if isinstance(value, list) and len(value) > 0:
                return value
        
        # Recurse into values
        for value in data.values():
            result = _find_by_key_name(value, target_key)
            if result is not None:
                return result
    
    elif isinstance(data, list):
        # Recurse into items
        for item in data:
            if isinstance(item, (dict, list)):
                result = _find_by_key_name(item, target_key)
                if result is not None:
                    return result
    
    return None


def _find_by_content_inspection(data):
    """
    Strategy 3: Recursively search for ANY list where the first item is a dictionary
    containing both "Date" (or "date") and "Link" (or "link" or "VideoLink") keys.
    
    Args:
        data: Dictionary or list to search recursively
        
    Returns:
        list or None: Video list if found, None otherwise
    """
    # If input is Dict: iterate values -> recurse
    if isinstance(data, dict):
        for value in data.values():
            result = _find_by_content_inspection(value)
            if result is not None:
                return result
    
    # If input is List: check item [0] against heuristic
    elif isinstance(data, list):
        # Check first item if list is not empty
        if len(data) > 0:
            first_item = data[0]
            # Heuristic: Check if first item is a dict with Date/date AND (Link/link OR VideoLink/videolink)
            if isinstance(first_item, dict):
                # Check for date key (case-insensitive)
                has_date = 'Date' in first_item or 'date' in first_item
                # Check for link key (case-insensitive)
                has_link = ('Link' in first_item or 'link' in first_item or 
                           'VideoLink' in first_item or 'videolink' in first_item)
                if has_date and has_link:
                    # Matches heuristic - return this list immediately
                    return data
        
        # If heuristic doesn't match, recurse into items
        for item in data:
            if isinstance(item, (dict, list)):
                result = _find_by_content_inspection(item)
                if result is not None:
                    return result
    
    return None


def find_video_history(data):
    """
    Main Smart Finder: Searches JSON for video history using multiple strategies.
    
    Strategy 1: Check common known paths
    Strategy 2: Recursively search for key 'VideoList'
    Strategy 3: Content inspection (find list with Date + Link keys)
    
    Args:
        data: JSON dictionary or list
        
    Returns:
        list or None: Video history list if found, None otherwise
    """
    # Strategy 1: Known paths
    result = _find_by_known_paths(data)
    if result is not None:
        return result
    
    # Strategy 2: Search for 'VideoList' key
    result = _find_by_key_name(data, 'VideoList')
    if result is not None:
        return result
    
    # Strategy 3: Content inspection (recursive search for Date + Link pattern)
    result = _find_by_content_inspection(data)
    if result is not None:
        return result
    
    return None


def find_video_list(data):
    """
    Alias for find_video_history for backward compatibility.
    Uses content inspection (Strategy 3) as the primary method.
    
    Args:
        data: Dictionary or list to search recursively
        
    Returns:
        list or None: List of video records if found, None otherwise
    """
    return _find_by_content_inspection(data)


def process_json(file_obj):
    """
    Processes uploaded JSON file and returns a normalized DataFrame.
    
    Args:
        file_obj: File-like object containing JSON data
        
    Returns:
        pd.DataFrame: Normalized DataFrame with video history
        
    Raises:
        ValueError: If video history cannot be found or JSON is invalid
    """
    # Load JSON with error handling
    try:
        json_data = json.load(file_obj)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON file. Please upload a valid JSON file.")
    except Exception as e:
        raise ValueError(f"Error reading JSON file: {str(e)}")
    
    # Check if file is empty
    if not json_data:
        raise ValueError("JSON file is empty.")
    
    # Call find_video_history(data)
    video_list = find_video_history(json_data)
    
    # Validation: If None, raise ValueError
    if video_list is None:
        raise ValueError("Video history not found. Looked for Date + Link/VideoLink.")
    
    # Create DataFrame
    try:
        df = pd.DataFrame(video_list)
    except Exception as e:
        raise ValueError(f"Error creating DataFrame: {str(e)}")
    
    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("Video history list is empty.")
    
    # Normalization (CRITICAL): Handle case-insensitive keys
    # First, normalize lowercase keys to uppercase
    column_mapping = {}
    if 'date' in df.columns and 'Date' not in df.columns:
        column_mapping['date'] = 'Date'
    if 'link' in df.columns and 'Link' not in df.columns:
        column_mapping['link'] = 'Link'
    if 'videolink' in df.columns and 'VideoLink' not in df.columns:
        column_mapping['videolink'] = 'VideoLink'
    
    if column_mapping:
        df = df.rename(columns=column_mapping)
    
    # Normalization (CRITICAL): Rename "Link" to "VideoLink" immediately when creating DataFrame
    # This ensures compatibility with the rest of the app
    if 'Link' in df.columns and 'VideoLink' not in df.columns:
        df = df.rename(columns={'Link': 'VideoLink'})
    
    # Normalize: Convert "Date" to datetime using pd.to_datetime(..., errors='coerce')
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        # Drop rows where Date is NaT
        df = df.dropna(subset=['Date'])
    
    # Return the clean DataFrame
    return df


def calculate_stats(df, avg_duration):
    """
    Calculates statistics from the DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame with video history
        avg_duration (int): Average video duration in seconds
        
    Returns:
        dict: Dictionary with total_videos, total_hours, total_days
    """
    total_videos = len(df)
    total_seconds = total_videos * avg_duration
    total_hours = total_seconds / 3600
    total_days = total_hours / 24
    
    return {
        'total_videos': total_videos,
        'total_hours': total_hours,
        'total_days': total_days
    }


def get_persona(df, guilt_mode):
    """
    Determines user persona based on peak viewing hour.
    
    Args:
        df (pd.DataFrame): DataFrame with video history (must have 'Date' column)
        guilt_mode (bool): Whether to use guilt trip mode
        
    Returns:
        dict: Dictionary with title, desc, hour
    """
    df['Hour'] = df['Date'].dt.hour
    hourly_counts = df.groupby('Hour').size().reset_index(name='Views')
    
    # Define time periods
    def get_period(hour):
        if 23 <= hour or hour <= 5:
            return "Night"
        elif 6 <= hour <= 11:
            return "Morning"
        elif 12 <= hour <= 17:
            return "Afternoon"
        else:  # 18-22
            return "Evening"
    
    # Add period to hourly counts
    hourly_counts['Period'] = hourly_counts['Hour'].apply(get_period)
    period_counts = hourly_counts.groupby('Period')['Views'].sum()
    
    # Find peak period (mode)
    peak_period = period_counts.idxmax()
    
    # Determine persona based on peak period and guilt trip mode
    if guilt_mode:
        personas = {
            "Night": ("🧟 Sleep Deprived Zombie", "You're sacrificing your health for late-night scrolling. Your future self will thank you for stopping."),
            "Morning": ("☕ Caffeine-Dependent Scroller", "Starting your day with TikTok instead of purpose. What a way to set the tone."),
            "Afternoon": ("😴 Productivity Killer", "The middle of the day, prime time for getting things done. But here you are, scrolling."),
            "Evening": ("🌙 Mindless Binger", "Winding down? More like winding up your dopamine receptors. Sleep quality? What's that?")
        }
    else:
        personas = {
            "Night": ("🦉 The Night Owl", "You spend your night hours trapped in the scroll loop."),
            "Morning": ("☀️ The Early Bird", "You spend your morning hours trapped in the scroll loop."),
            "Afternoon": ("☕ The Lunchtime Scroller", "You spend your afternoon hours trapped in the scroll loop."),
            "Evening": ("🌇 The Evening Binger", "You spend your evening hours trapped in the scroll loop.")
        }
    
    title, desc = personas[peak_period]
    
    return {
        'title': title,
        'desc': desc,
        'hour': peak_period
    }


def get_absurd_items(total_hours):
    """
    Generates list of absurd comparisons based on total hours.
    
    Args:
        total_hours (float): Total hours wasted
        
    Returns:
        list: List of dictionaries with icon and text keys
    """
    items = []
    
    # Cook instant noodles (3 minutes per pack = 0.05 hours)
    if total_hours >= 0.05:
        noodle_count = int(total_hours / 0.05)
        items.append({'icon': '🍜', 'text': f'Cook {noodle_count:,} packs of instant noodles'})
    
    # Blinks (average 1200 blinks per hour)
    if total_hours >= 0.00083:  # At least 3 seconds
        blink_count = int(total_hours * 1200)
        items.append({'icon': '👁️', 'text': f'Blink {blink_count:,} times'})
    
    # Climb Mt. Everest (approx 60 hours to summit from base camp)
    if total_hours >= 60:
        everest_count = int(total_hours / 60)
        items.append({'icon': '⛰️', 'text': f'Climb Mt. Everest {everest_count} times'})
    
    # Watch Titanic (3 hours 14 minutes = 3.233 hours)
    if total_hours >= 3.233:
        titanic_count = int(total_hours / 3.233)
        items.append({'icon': '🚢', 'text': f'Watch "Titanic" {titanic_count} times'})
    
    # Walk from London to Paris (approx 90 hours walking)
    if total_hours >= 90:
        walk_count = int(total_hours / 90)
        items.append({'icon': '🚶', 'text': f'Walk from London to Paris {walk_count} times'})
    
    # Heartbeats (average 80 bpm = 4800 beats per hour)
    if total_hours >= 0.00021:  # At least 0.75 seconds
        heartbeat_count = int(total_hours * 4800)
        items.append({'icon': '❤️', 'text': f'Your heart beat {heartbeat_count:,} times'})
    
    # Thumb scroll (1 hour scrolling = 300 meters of thumb travel)
    if total_hours >= 0.0033:  # At least 12 seconds
        scroll_meters = int(total_hours * 300)
        burj_height = 828  # Burj Khalifa height in meters
        burj_count = int(scroll_meters / burj_height)
        if burj_count > 0:
            items.append({'icon': '📱', 'text': f'Scroll the height of the Burj Khalifa {burj_count:,} times'})
    
    return items
