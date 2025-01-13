"""Main module for the Codewars kata exporter."""

import os
import logging
from typing import List
import utils
from file_management import FileManager
from app_state import app_state
import web_scraper
from config import Configuration
from path_validator import PathValidationError
from auth import (
    Credentials,
    CredentialsValidator,
    AuthenticationError,
    ValidationError,
    ConfigurationError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def save_and_commit_kata(kata, file_manager: FileManager) -> None:
    """Save a kata to file and commit it."""
    content = f"# {kata.name} [{kata.level}] #{len(app_state.pushed_katas)}\n\n```{kata.language}\n{kata.code}\n```\n\n"
    file_manager.add_kata(content, kata.language)
    os.system(f'cd {file_manager.repo_path} && git add . && git commit -m "docs(common): add \'{kata.name}\' kata" > /dev/null 2>&1')
    logger.info(f"Le kata '{kata.name}' a été ajouté")

def main():
    """Main function to run the kata exporter."""
    try:
        # Load configuration and initialize credentials
        config = Configuration()
        credentials = Credentials(
            email=config.mail_address,
            password=config.password,
            username=config.username
        )
        
        # Set global configuration
        app_state.different_file_depending_on_language = config.different_file_depending_on_language
        
        # Initialize file manager and validate paths
        file_manager = FileManager(config.local_repo_path, config.kata_file_name)
        file_manager.validate_paths()
        file_manager.read_katas()
        
        # Start browser session and authenticate
        utils.start_browser_session()
        app_state.web_driver.get("https://www.codewars.com/users/sign_in")
        logger.info("Connecting to your Codewars account...")
        
        validator = CredentialsValidator(app_state.web_driver)
        validator.authenticate(credentials)
        
        # Navigate to completed solutions and get katas
        app_state.web_driver.get(f'https://www.codewars.com/users/{credentials.username}/completed_solutions')
        logger.info("Getting completed katas...")
        
        katas = web_scraper.get_completed_katas(config.push_step)
        for kata in katas:
            save_and_commit_kata(kata, file_manager)
            
    except (ConfigurationError, ValidationError) as e:
        logger.error(f"Configuration error: {str(e)}")
        logger.error("Please check your .env file and try again.")
        exit(1)
    except AuthenticationError as e:
        logger.error(str(e))
        logger.error("Failed to authenticate. Please check your credentials and try again.")
        exit(1)
    except PathValidationError as e:
        logger.error(str(e))
        logger.error("Path validation failed. Please check your paths and permissions.")
        exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        exit(1)
    finally:
        if app_state.web_driver:
            app_state.cleanup()

if __name__ == "__main__":
    main()