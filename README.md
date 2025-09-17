# Instagram Analytics API

A FastAPI backend service that fetches Instagram account information including follower count, post count, and profile details using web scraping.

## Features

- 📊 **Account Analytics**: Get follower count, following count, post count, and profile information
- 📝 **Recent Posts**: Fetch recent posts with likes, comments, and engagement metrics
- 🔄 **Batch Processing**: Get information for multiple accounts in a single request
- 🛡️ **Error Handling**: Comprehensive error handling for private accounts, non-existent profiles, etc.
- 📚 **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- 🌐 **CORS Support**: Ready for frontend integration

## API Endpoints

### 1. Get Account Information
```
GET /api/instagram/{username}
```
Get basic Instagram account information.

**Parameters:**
- `username`: Instagram username (without @)
- `include_posts` (optional): Whether to include recent posts (default: false)

**Example:**
```bash
curl "http://localhost:8000/api/instagram/instagram"
```

### 2. Get Account with Recent Posts
```
GET /api/instagram/{username}/posts
```
Get Instagram account information along with recent posts.

**Parameters:**
- `username`: Instagram username (without @)
- `max_posts` (optional): Maximum number of posts to fetch (1-50, default: 10)

**Example:**
```bash
curl "http://localhost:8000/api/instagram/instagram/posts?max_posts=5"
```

### 3. Batch Account Information
```
POST /api/instagram/batch
```
Get information for multiple Instagram accounts.

**Parameters:**
- `usernames`: List of Instagram usernames (max 10 per request)

**Example:**
```bash
curl -X POST "http://localhost:8000/api/instagram/batch?usernames=instagram&usernames=natgeo"
```

### 4. Health Check
```
GET /health
```
Check if the API is running.

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### 1. Clone or Download
```bash
cd /Users/mommy/Documents/coding/socialdashboard
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the API
- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **Alternative Documentation**: http://localhost:8000/redoc

## Usage Examples

### Python Example
```python
import requests

# Get basic account info
response = requests.get("http://localhost:8000/api/instagram/instagram")
data = response.json()
print(f"Followers: {data['data']['followers_count']}")
print(f"Posts: {data['data']['posts_count']}")

# Get account with recent posts
response = requests.get("http://localhost:8000/api/instagram/instagram/posts?max_posts=3")
data = response.json()
print(f"Recent posts: {len(data['recent_posts'])}")
```

### JavaScript Example
```javascript
// Get account information
fetch('http://localhost:8000/api/instagram/instagram')
  .then(response => response.json())
  .then(data => {
    console.log('Followers:', data.data.followers_count);
    console.log('Posts:', data.data.posts_count);
  });

// Get multiple accounts
fetch('http://localhost:8000/api/instagram/batch?usernames=instagram&usernames=natgeo')
  .then(response => response.json())
  .then(data => {
    data.forEach(account => {
      if (account.success) {
        console.log(`${account.data.username}: ${account.data.followers_count} followers`);
      }
    });
  });
```

## Response Format

### Successful Response
```json
{
  "success": true,
  "data": {
    "username": "instagram",
    "full_name": "Instagram",
    "biography": "Bringing you closer to the people and things you love.",
    "followers_count": 500000000,
    "following_count": 1,
    "posts_count": 15000,
    "is_private": false,
    "is_verified": true,
    "profile_pic_url": "https://...",
    "external_url": "https://about.instagram.com/",
    "last_updated": "2024-01-15T10:30:00"
  },
  "recent_posts": [
    {
      "shortcode": "ABC123",
      "caption": "Post caption...",
      "likes_count": 1000000,
      "comments_count": 50000,
      "date": "2024-01-15T09:00:00",
      "is_video": false,
      "video_view_count": null
    }
  ],
  "error": null
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "recent_posts": null,
  "error": "Instagram profile 'nonexistent' does not exist"
}
```

## Important Notes

### Rate Limiting & Instagram Policies
- This API uses web scraping to fetch Instagram data
- Instagram may implement rate limiting or block requests if used excessively
- Use responsibly and consider implementing delays between requests
- For production use, consider Instagram's official API

### Private Accounts
- Private account information is limited to basic profile data
- Recent posts cannot be fetched for private accounts
- The API will return an error for private accounts when trying to fetch posts

### Error Handling
The API handles various error scenarios:
- Non-existent profiles
- Private accounts
- Network timeouts
- Rate limiting
- Invalid usernames

## Development

### Project Structure
```
socialdashboard/
├── main.py                 # FastAPI application
├── models.py              # Pydantic data models
├── instagram_service.py   # Instagram scraping service
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Adding New Features
1. Add new endpoints in `main.py`
2. Update data models in `models.py` if needed
3. Extend the Instagram service in `instagram_service.py`
4. Update this README with new endpoint documentation

## Troubleshooting

### Common Issues

1. **"Profile does not exist" error**
   - Verify the username is correct
   - Check if the account is still active

2. **"Private profile" error**
   - The account is private and cannot be accessed
   - Only basic profile information is available

3. **Rate limiting**
   - Instagram may temporarily block requests
   - Wait a few minutes before retrying
   - Consider implementing request delays

4. **Installation issues**
   - Make sure Python 3.8+ is installed
   - Use a virtual environment
   - Update pip: `pip install --upgrade pip`

## License

This project is for educational purposes. Please respect Instagram's Terms of Service and use responsibly.
