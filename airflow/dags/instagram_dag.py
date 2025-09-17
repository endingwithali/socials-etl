from datetime import datetime, timedelta
import instaloader
from airflow.sdk import Variable
from airflow.decorators import task, dag
import logging

logger = logging.getLogger(__name__)
@dag(
    dag_id="instagram_dag", 
    default_args={
        "depends_on_past": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
    },
    description="A DAG to fetch Instagram data on a regular basis", 
    schedule="@hourly", 
    tags=["instagram"], 
    start_date=datetime(2025, 1, 1)
)
def instagram_to_db():
    @task 
    def extract():
        username = Variable.get('INSTAGRAM_USERNAME')
        loader = instaloader.Instaloader()
        
        loader.context._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        logger.info(f"Fetching Instagram data for username: {username}")
        try:  
            profile = instaloader.Profile.from_username(loader.context, username)
            
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
    @task
    def load(data):
        logger.info(f"Loading Instagram data to db: {data}")
        ## write to db using sql alchemy and postgres
        pass
    
    # Define task dependencies
    extract_task = extract()
    load_task = load(extract_task)
    
    return extract_task, load_task

dag = instagram_to_db()