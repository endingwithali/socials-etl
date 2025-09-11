import instaloader
import logging
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

USERNAME = os.getenv('INSTAGRAM_USERNAME')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InstagramService:
    """Service for fetching Instagram account information"""
    
    def __init__(self):
        """Initialize the Instagram service with instaloader"""
        self.loader = instaloader.Instaloader()
        
        self.loader.context._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    async def get_account_metrics(self) -> dict:
        """
        Fetch Instagram account information
            
        Returns:
            Dictionary containing account information and optionally recent posts
        """
        try:
            logger.info(f"Fetching Instagram data for username: {USERNAME}")
            
            profile = instaloader.Profile.from_username(self.loader.context, USERNAME)
            
            result = {
                "success": True,
                "data": {
                    "followers": profile.followers,
                    "following": profile.followees,
                    "posts": profile.mediacount
                },
                "error": None
            }
            return result
        except instaloader.exceptions.ProfileNotExistsException:
            error_msg = f"Instagram profile '{username}' does not exist"
            logger.error(error_msg)
            return {
                "success": False,
                "data": None,
                "error": error_msg,
                "recent_posts": None
            }

        except Exception as e:
            error_msg = f"An error occurred while fetching Instagram data: {str(e)}"
            logger.error(error_msg)
            return {
                "success": False,
                "data": None,
                "error": error_msg,
                "recent_posts": None
            }


service = InstagramService()
print(asyncio.run(service.get_account_metrics()))