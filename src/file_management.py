"""File management module for kata export."""

import os
import logging
from typing import List
from app_state import app_state
from path_validator import validate_path, validate_file_path, validate_git_repository, PathValidationError

logger = logging.getLogger(__name__)

class FileManager:
    """Class responsible for managing kata file operations."""
    
    def __init__(self, repo_path: str, file_name: str):
        """
        Initialize the FileManager.
        
        Args:
            repo_path: Path to the repository
            file_name: Name of the kata file
        """
        self.repo_path = repo_path
        self.file_name = file_name
        self.file_path = os.path.join(repo_path, file_name)
        self._language_files: Dict[str, str] = {}
        
    def _get_language_file_path(self, language: str) -> str:
        """
        Get the file path for a specific language.
        
        Args:
            language: Programming language
            
        Returns:
            str: Path to the language-specific file
        """
        if language not in self._language_files:
            base_name, ext = os.path.splitext(self.file_name)
            language_file = f"{base_name}-{language}{ext}"
            self._language_files[language] = os.path.join(self.repo_path, language_file)
        return self._language_files[language]
        
    def validate_paths(self) -> None:
        """
        Validate all required paths at startup.
        
        Raises:
            PathValidationError: If path validation fails
        """
        logger.info("Validating paths...")
        validate_path(self.repo_path)
        validate_git_repository(self.repo_path)
        validate_file_path(self.file_path, create_if_missing=True)
        logger.info("Path validation completed successfully")
        
    def add_kata(self, content: str, language: str = None) -> None:
        """
        Append a kata to the specified file using buffered write.
        
        Args:
            content: Content to write
            language: Programming language (optional)
            
        Raises:
            IOError: If there is an error writing to the file
        """
        target_path = (
            self._get_language_file_path(language)
            if app_state.different_file_depending_on_language and language
            else self.file_path
        )
        
        try:
            if app_state.different_file_depending_on_language and language:
                validate_file_path(target_path, create_if_missing=True)
                
            with open(target_path, "a", buffering=8192) as f:
                f.write(content)
        except IOError as e:
            logger.error(f"Error writing to file {target_path}: {str(e)}")
            raise
            
    def read_katas(self) -> None:
        """
        Read and process all kata files in the repository to populate already_pushed_katas.
        Uses a set for faster lookups and memory efficiency.
        
        Raises:
            FileNotFoundError: If the file does not exist
            IOError: If there is an error reading the file
        """
        kata_set: Set[str] = set()
        
        # Get all markdown files in the repository
        _, ext = os.path.splitext(self.file_name)
        for file in os.listdir(self.repo_path):
            if file.endswith(ext):
                file_path = os.path.join(self.repo_path, file)
                try:
                    with open(file_path, 'r', buffering=8192) as f:
                        for line in f:
                            if line.startswith('#') and "kyu" in line.lower():
                                kata_title = line[1:line.rfind('#')].strip().split("[")[0].strip()
                                kata_set.add(kata_title)
                                
                except FileNotFoundError:
                    if file_path == self.file_path:
                        logger.warning(f"File {file_path} not found. Creating a new file.")
                        open(file_path, 'a').close()
                except IOError as e:
                    logger.error(f"Error reading file {file_path}: {str(e)}")
                    raise
        
        for kata_name in kata_set:
            app_state.add_pushed_kata(kata_name)