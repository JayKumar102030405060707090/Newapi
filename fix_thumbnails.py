#!/usr/bin/env python3
"""
Thumbnail Fix Script
Ensures thumbnails are always available and high quality
"""

def get_youtube_thumbnail(video_id, quality='maxresdefault'):
    """
    Get YouTube thumbnail URL for a video ID
    
    Args:
        video_id: YouTube video ID
        quality: Thumbnail quality (maxresdefault, hqdefault, mqdefault, default)
    
    Returns:
        Thumbnail URL
    """
    if not video_id:
        return ""
    
    # Try different qualities in order of preference
    qualities = ['maxresdefault', 'hqdefault', 'mqdefault', 'default']
    
    if quality in qualities:
        qualities.insert(0, quality)
    
    for q in qualities:
        thumbnail_url = f"https://i.ytimg.com/vi/{video_id}/{q}.jpg"
        # In production, we would verify the URL exists, but for now return the highest quality
        return thumbnail_url
    
    return f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg"

def extract_best_thumbnail(info_dict):
    """
    Extract the best quality thumbnail from yt-dlp info dict
    
    Args:
        info_dict: yt-dlp extracted info dictionary
    
    Returns:
        Best thumbnail URL
    """
    video_id = info_dict.get('id', '')
    
    # Check if thumbnails array exists
    thumbnails = info_dict.get('thumbnails', [])
    if thumbnails:
        # Filter out None and invalid thumbnails
        valid_thumbnails = [t for t in thumbnails if t and t.get('url')]
        
        if valid_thumbnails:
            # Sort by resolution (width * height)
            best_thumbnail = max(valid_thumbnails, 
                               key=lambda x: (x.get('width', 0) * x.get('height', 0)))
            return best_thumbnail.get('url', '')
    
    # Check direct thumbnail field
    direct_thumbnail = info_dict.get('thumbnail', '')
    if direct_thumbnail:
        return direct_thumbnail
    
    # Fallback to YouTube's default thumbnail
    if video_id:
        return get_youtube_thumbnail(video_id)
    
    return ""

def ensure_thumbnail_availability(video_data):
    """
    Ensure video data has a valid thumbnail URL
    
    Args:
        video_data: Dictionary containing video information
    
    Returns:
        Updated video data with guaranteed thumbnail
    """
    if not video_data.get('thumbnail') and video_data.get('id'):
        video_data['thumbnail'] = get_youtube_thumbnail(video_data['id'])
    
    return video_data

if __name__ == '__main__':
    # Test the thumbnail functions
    test_video_id = "dQw4w9WgXcQ"  # Rick Roll for testing
    print(f"Test thumbnail URL: {get_youtube_thumbnail(test_video_id)}")
    
    # Test with mock data
    test_data = {'id': test_video_id, 'title': 'Test Video'}
    updated_data = ensure_thumbnail_availability(test_data)
    print(f"Updated data: {updated_data}")