"""
Batch Processing Engine for AI Paper Checker
Handles processing multiple papers with progress tracking and error handling
"""
import os
from pathlib import Path
from typing import List, Dict, Optional, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from document_utils import (
    extract_text_from_file,
    extract_student_info,
    extract_mcq_answers,
    parse_answer_key
)
from agents import GradingResult, OrchestratorAgent


class BatchProcessor:
    """
    Process multiple papers in batch with progress tracking and error handling.
    Supports up to 100 papers at once.
    """
    
    def __init__(self, orchestrator: OrchestratorAgent, max_workers: int = 5):
        self.orchestrator = orchestrator
        self.max_workers = max_workers
        self.results: List[GradingResult] = []
        self.errors: List[Dict] = []
    
    def process_papers(self,
                       paper_files: List[str],
                       mcq_answer_key: Optional[Dict[str, str]] = None,
                       progress_callback: Optional[Callable] = None) -> List[GradingResult]:
        """
        Process multiple papers with progress tracking.
        
        Args:
            paper_files: List of file paths to papers
            mcq_answer_key: Answer key for MCQ questions
            progress_callback: Optional callback for progress updates
        
        Returns:
            List of GradingResult objects
        """
        if len(paper_files) > 100:
            raise ValueError("Batch processing limited to 100 papers at once")
        
        self.results = []
        self.errors = []
        
        print(f"Processing {len(paper_files)} papers...")
        
        # Use tqdm for progress bar
        with tqdm(total=len(paper_files), desc="Grading papers", unit="paper") as pbar:
            # Process papers with thread pool for I/O operations
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                future_to_file = {
                    executor.submit(
                        self._process_single_paper,
                        file_path,
                        mcq_answer_key
                    ): file_path
                    for file_path in paper_files
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_file):
                    file_path = future_to_file[future]
                    try:
                        result = future.result()
                        if result:
                            self.results.append(result)
                    except Exception as e:
                        error_info = {
                            'file': file_path,
                            'error': str(e)
                        }
                        self.errors.append(error_info)
                        print(f"\nError processing {Path(file_path).name}: {e}")
                    
                    pbar.update(1)
                    if progress_callback:
                        progress_callback(pbar.n, len(paper_files))
        
        print(f"\nCompleted: {len(self.results)} papers graded successfully")
        if self.errors:
            print(f"Errors: {len(self.errors)} papers failed to process")
        
        return self.results
    
    def _process_single_paper(self,
                              file_path: str,
                              mcq_answer_key: Optional[Dict[str, str]] = None) -> Optional[GradingResult]:
        """
        Process a single paper with error handling.
        
        Returns:
            GradingResult or None if processing failed
        """
        try:
            # Extract text from document
            text = extract_text_from_file(file_path)
            
            if not text or len(text.strip()) < 10:
                raise ValueError("Could not extract text from document or document is empty")
            
            # Extract student information
            filename = Path(file_path).name
            student_info = extract_student_info(text, filename)
            
            # Extract MCQ answers if answer key provided
            mcq_answers = None
            if mcq_answer_key:
                mcq_answers = extract_mcq_answers(text, len(mcq_answer_key))
            
            # For now, we'll focus on MCQ grading
            # Textual answer extraction would require more sophisticated parsing
            # which can be added based on specific format requirements
            
            # Grade the paper
            result = self.orchestrator.grade_paper(
                student_info=student_info,
                mcq_answers=mcq_answers,
                mcq_answer_key=mcq_answer_key
            )
            
            return result
            
        except Exception as e:
            # Return error result
            return GradingResult(
                student_name=Path(file_path).stem,
                student_id="",
                roll_no="",
                error=str(e),
                needs_review=True,
                review_reason=f"Processing error: {str(e)}"
            )
    
    def get_results(self) -> List[GradingResult]:
        """Get all grading results."""
        return self.results
    
    def get_errors(self) -> List[Dict]:
        """Get all processing errors."""
        return self.errors
    
    def get_review_flagged(self) -> List[GradingResult]:
        """Get papers flagged for review."""
        return [r for r in self.results if r.needs_review]


def create_sample_papers_for_testing(output_dir: str = "/tmp/test_papers", num_papers: int = 3):
    """
    Create sample papers for testing the system.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    sample_papers = [
        {
            "name": "John Doe",
            "id": "12345",
            "roll": "CS101",
            "answers": {"1": "A", "2": "B", "3": "C", "4": "D", "5": "A"}
        },
        {
            "name": "Jane Smith",
            "id": "12346",
            "roll": "CS102",
            "answers": {"1": "A", "2": "C", "3": "C", "4": "D", "5": "B"}
        },
        {
            "name": "Bob Johnson",
            "id": "12347",
            "roll": "CS103",
            "answers": {"1": "B", "2": "B", "3": "A", "4": "D", "5": "A"}
        }
    ]
    
    created_files = []
    
    for i, paper in enumerate(sample_papers[:num_papers]):
        content = f"""Name: {paper['name']}
Student ID: {paper['id']}
Roll No: {paper['roll']}

Multiple Choice Answers:
"""
        for q_num, answer in paper['answers'].items():
            content += f"{q_num}. {answer}\n"
        
        filename = f"{paper['name'].replace(' ', '_')}_{paper['id']}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        created_files.append(filepath)
    
    return created_files
