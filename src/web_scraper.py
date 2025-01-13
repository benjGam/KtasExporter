"""Module for web scraping Codewars solutions."""

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from typing import Optional, List
import logging
from kata import Kata
from gvars import app_state

logger = logging.getLogger(__name__)

def get_kata_code(element) -> str:
    """Extract code from a kata solution element."""
    return BeautifulSoup(
        element.find_element(By.TAG_NAME, 'code').get_attribute('innerHTML'),
        'html.parser'
    ).get_text()

def get_kata_name(element) -> str:
    """Extract name from a kata solution element."""
    return element.find_element(By.TAG_NAME, 'a').text

def get_kata_level(element) -> str:
    """Extract difficulty level from a kata solution element."""
    return element.find_element(By.TAG_NAME, 'span').text

def get_kata_language(element) -> str:
    """Extract programming language from a kata solution element."""
    return element.find_element(By.TAG_NAME, 'code').get_attribute('data-language').lower()

def load_more_solutions() -> bool:
    """
    Load more solutions by scrolling to the infinite marker.
    
    Returns:
        bool: True if more solutions were loaded, False otherwise
    """
    try:
        element = app_state.web_driver.find_element(By.CLASS_NAME, 'js-infinite-marker')
        app_state.web_driver.execute_script("arguments[0].scrollIntoView();", element)
        return True
    except NoSuchElementException:
        return False

def extract_kata_from_solution(solution) -> Optional[Kata]:
    """
    Extract kata information from a solution element.
    
    Args:
        solution: The web element containing the solution
        
    Returns:
        Optional[Kata]: A Kata object if valid, None otherwise
    """
    try:
        kata_name = get_kata_name(solution.find_element(By.CLASS_NAME, 'item-title'))
        
        if app_state.is_kata_pushed(kata_name):
            return None
            
        kata_level = get_kata_level(solution.find_element(By.CLASS_NAME, 'item-title'))
        if "kyu" not in kata_level:
            return None
            
        markdown_elements = solution.find_elements(By.CLASS_NAME, 'markdown')
        if not markdown_elements:
            return None
            
        kata_language = get_kata_language(markdown_elements[0])
        kata_code = get_kata_code(markdown_elements[0])
        
        return Kata(kata_name, kata_level, kata_language, kata_code)
        
    except NoSuchElementException as e:
        logger.warning(f"Failed to extract kata from solution: {str(e)}")
        return None

def get_completed_katas(push_step: int) -> List[Kata]:
    """
    Retrieve completed katas from Codewars.
    
    Args:
        push_step: Number of katas to retrieve before stopping
        
    Returns:
        List[Kata]: List of retrieved katas
    """
    katas = []
    while len(katas) < push_step:
        solutions = app_state.web_driver.find_elements(By.CLASS_NAME, "list-item-solutions")
        
        for solution in solutions:
            if len(katas) >= push_step:
                break
                
            kata = extract_kata_from_solution(solution)
            if kata:
                katas.append(kata)
                app_state.add_completed_kata(kata.name)
                app_state.add_pushed_kata(kata.name)
        
        if not load_more_solutions():
            break
            
    return katas