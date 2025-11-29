"""Pure data processing logic for the TikTok Reality Check app."""

import json
import pandas as pd


def process_json(file):
    """
    Processes uploaded JSON file and returns a DataFrame.
    
    Args:
        file: File-like object containing JSON data
        
    Returns:
        pd.DataFrame or None: DataFrame with video history, or None if invalid
    """
    try:
        json_data = json.load(file)
        
        # Extract path: Activity -> Video Browsing History -> VideoList
        try:
            video_list = json_data['Activity']['Video Browsing History']['VideoList']
            
            # Create DataFrame
            df = pd.DataFrame(video_list)
            
            # Convert Date to datetime
            df['Date'] = pd.to_datetime(df['Date'])
            
            return df
            
        except (KeyError, TypeError):
            return None
    
    except json.JSONDecodeError:
        return None
    except Exception:
        return None


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
        df (pd.DataFrame): DataFrame with video history
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
    
    # Find peak period
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
    
    # Pet cat (5 minutes = 0.083 hours)
    if total_hours >= 0.083:
        pet_count = int(total_hours / 0.083)
        items.append({'icon': '🐱', 'text': f'Pet a cat {pet_count:,} times'})
    
    # Become President of Argentina (4 year term = ~35,000 hours)
    if total_hours >= 35000:
        pres_count = int(total_hours / 35000)
        items.append({'icon': '🇦🇷', 'text': f'Become President of Argentina {pres_count} times'})
    
    # Walk to the Moon (~76,880 hours round trip)
    if total_hours >= 76880:
        items.append({'icon': '🌙', 'text': 'Walk to the Moon and back'})
    elif total_hours >= 38440:
        items.append({'icon': '🌙', 'text': 'Walk to the Moon (one way)'})
    
    # Additional items
    if total_hours >= 1000:
        one_piece_count = int(total_hours / 1000)
        items.append({'icon': '🏴‍☠️', 'text': f'Watch the entire One Piece anime {one_piece_count} times'})
    
    if total_hours >= 10000:
        govt_count = int(total_hours / 10000)
        items.append({'icon': '⚔️', 'text': f'Overthrow a government {govt_count} times'})
    
    if total_hours >= 1000:
        lang_count = int(total_hours / 1000)
        items.append({'icon': '🗣️', 'text': f'Learn {lang_count} languages to fluency'})
    
    if total_hours >= 50:
        book_count = int(total_hours / 50)
        items.append({'icon': '📚', 'text': f'Read War and Peace {book_count} times'})
    
    if total_hours >= 100:
        marathon_count = int(total_hours / 100)
        items.append({'icon': '🏃', 'text': f'Train for and run {marathon_count} marathons'})
    
    if total_hours >= 2000:
        house_count = int(total_hours / 2000)
        items.append({'icon': '🏠', 'text': f'Build {house_count} houses from scratch'})
    
    return items

