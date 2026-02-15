# Quick Posting Reference

## Facebook & Instagram

### Single Image
```python
post_media(
    caption="Your text here #hashtag1 #hashtag2",
    media_urls=["https://example.com/image.jpg"],
    media_type="image",
    platforms=["facebook", "instagram"]  # or just ["facebook"] or ["instagram"]
)
```

### Carousel (Multiple Images)
```python
post_media(
    caption="Your caption #hashtags",
    media_urls=[
        "https://example.com/img1.jpg",
        "https://example.com/img2.jpg",
        "https://example.com/img3.jpg"
    ],
    media_type="carousel",
    platforms=["facebook", "instagram"]
)
```

### Video
```python
post_media(
    caption="Video caption #hashtags",
    media_urls=["https://example.com/video.mp4"],
    media_type="video",
    platforms=["facebook"]
)
```

### Reel
```python
post_media(
    caption="Reel caption #hashtags",
    media_urls=["https://example.com/reel.mp4"],
    media_type="reel",
    platforms=["instagram"]
)
```

## LinkedIn

### Text Post
```python
linkedin_create_text_post(
    text="Your professional update",
    hashtags=["business", "growth", "innovation"]
)
```

### Single Image
```python
linkedin_create_image_post(
    text="Image caption",
    image_url="https://example.com/image.jpg",
    hashtags=["professional", "success"]
)
```

### Carousel
```python
linkedin_create_carousel_post(
    text="Showcase your work",
    image_urls=[
        "https://example.com/img1.jpg",
        "https://example.com/img2.jpg"
    ],
    hashtags=["portfolio", "work"]
)
```

### Share Article/Link
```python
linkedin_create_link_post(
    text="Check out this article",
    link_url="https://example.com/article",
    hashtags=["mustread", "insights"]
)
```

## Telegram

### Text Message
```python
telegram_send_message(
    text="Your message here",
    hashtags=["telegram", "update"]
)
```

### Single Photo
```python
telegram_send_photo(
    photo_url="https://example.com/photo.jpg",
    caption="Photo caption",
    hashtags=["photo", "share"]
)
```

### Media Group (Carousel)
```python
telegram_send_media_group(
    media_urls=[
        "https://example.com/img1.jpg",
        "https://example.com/img2.jpg",
        "https://example.com/img3.jpg"
    ],
    caption="Album caption",
    hashtags=["gallery", "album"]
)
```

### Link with Preview
```python
telegram_send_link(
    text="Check this out",
    link_url="https://example.com/article",
    hashtags=["link", "share"]
)
```

## Hashtag Tips

- **LinkedIn**: Don't include # symbol, just the word (e.g., `["business", "tech"]`)
- **Facebook/Instagram**: Include in caption or use hashtags parameter
- **Telegram**: Added automatically with # symbol

## Image URLs

All platforms require **publicly accessible URLs**:
- ✅ `https://example.com/image.jpg`
- ✅ CDN links
- ✅ Direct image links
- ❌ Local file paths won't work
- ❌ Links requiring authentication

## Platform Limits

- **LinkedIn Carousel**: 2-10 images
- **Telegram Media Group**: 2-10 images
- **Facebook Carousel**: Multiple images supported
- **Instagram Carousel**: Up to 10 images

## Quick Workflow for Primes & Zooms

1. Upload images to your CDN/hosting
2. Get public URLs
3. Use the tools above with your URLs
4. Add hashtags for reach
5. Post across all platforms with one command each!
