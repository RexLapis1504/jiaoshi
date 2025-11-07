"""
AI Agents for Paper Grading System
"""
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class GradingResult:
    """Result from grading a paper"""
    student_name: str
    student_id: str
    roll_no: str
    mcq_score: Optional[int] = None
    mcq_total: Optional[int] = None
    mcq_percentage: Optional[float] = None
    mcq_incorrect: Optional[List[str]] = None
    textual_score: Optional[float] = None
    textual_feedback: Optional[str] = None
    total_score: Optional[float] = None
    needs_review: bool = False
    review_reason: Optional[str] = None
    error: Optional[str] = None


class MCQGradingAgent:
    """
    Agent for grading Multiple Choice Questions with 100% accuracy.
    Uses strict comparison against answer key.
    """
    
    def __init__(self):
        self.name = "MCQ Grading Agent"
    
    def grade(self, student_answers: Dict[str, str], 
              answer_key: Dict[str, str]) -> Tuple[int, int, float, List[str]]:
        """
        Grade MCQ answers with strict comparison.
        
        Returns: (correct_count, total_questions, percentage, incorrect_questions)
        """
        correct = 0
        incorrect = []
        total = len(answer_key)
        
        for q_num, correct_answer in answer_key.items():
            student_answer = student_answers.get(q_num, '').upper().strip()
            correct_answer_upper = correct_answer.upper().strip()
            
            if student_answer == correct_answer_upper:
                correct += 1
            else:
                incorrect.append(q_num)
        
        percentage = (correct / total * 100) if total > 0 else 0
        
        return correct, total, percentage, incorrect


class TextualGradingAgent:
    """
    Agent for grading textual/subjective answers using AI.
    Provides scores and detailed feedback.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.name = "Textual Grading Agent"
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model
        self.use_ai = bool(self.api_key)
    
    def grade(self, question: str, student_answer: str, 
              reference_answer: Optional[str] = None,
              max_marks: int = 10) -> Tuple[float, str]:
        """
        Grade a textual answer using AI or rule-based approach.
        
        Returns: (score, feedback)
        """
        if not student_answer or not student_answer.strip():
            return 0.0, "No answer provided."
        
        if self.use_ai:
            return self._grade_with_ai(question, student_answer, reference_answer, max_marks)
        else:
            return self._grade_rule_based(student_answer, max_marks)
    
    def _grade_with_ai(self, question: str, student_answer: str,
                       reference_answer: Optional[str], max_marks: int) -> Tuple[float, str]:
        """Grade using OpenAI API."""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.api_key)
            
            prompt = f"""You are an expert teacher grading student answers. Grade the following answer objectively.

Question: {question}

Student Answer: {student_answer}

{f"Reference Answer: {reference_answer}" if reference_answer else ""}

Maximum Marks: {max_marks}

Provide:
1. A score out of {max_marks}
2. Constructive feedback (2-3 sentences)

Format your response as:
Score: X/{max_marks}
Feedback: [Your feedback here]
"""
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert teacher grading student answers."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = response.choices[0].message.content.strip()
            
            # Parse score and feedback
            score = 0.0
            feedback = result
            
            lines = result.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('Score:'):
                    # Extract score
                    import re
                    match = re.search(r'(\d+\.?\d*)', line)
                    if match:
                        score = float(match.group(1))
                    # Get feedback from remaining lines
                    feedback_lines = [l for l in lines[i+1:] if l.strip()]
                    if feedback_lines:
                        feedback = '\n'.join(feedback_lines)
                        # Remove "Feedback:" prefix if present
                        feedback = re.sub(r'^Feedback:\s*', '', feedback, flags=re.IGNORECASE)
                    break
            
            return min(score, max_marks), feedback
            
        except Exception as e:
            print(f"AI grading failed: {e}")
            return self._grade_rule_based(student_answer, max_marks)
    
    def _grade_rule_based(self, student_answer: str, max_marks: int) -> Tuple[float, str]:
        """Simple rule-based grading fallback."""
        word_count = len(student_answer.split())
        
        if word_count == 0:
            return 0.0, "No answer provided."
        elif word_count < 10:
            score = max_marks * 0.3
            feedback = "Answer is too brief. Please provide more detail."
        elif word_count < 30:
            score = max_marks * 0.5
            feedback = "Answer shows basic understanding but lacks detail."
        elif word_count < 100:
            score = max_marks * 0.7
            feedback = "Good answer with adequate detail."
        else:
            score = max_marks * 0.85
            feedback = "Comprehensive answer with good detail."
        
        return score, feedback


class OrchestratorAgent:
    """
    Orchestrator agent that coordinates the grading workflow.
    Manages MCQ and textual grading, combines results, and flags papers for review.
    """
    
    def __init__(self, mcq_agent: MCQGradingAgent, textual_agent: TextualGradingAgent):
        self.name = "Orchestrator Agent"
        self.mcq_agent = mcq_agent
        self.textual_agent = textual_agent
    
    def grade_paper(self,
                    student_info: Dict[str, str],
                    mcq_answers: Optional[Dict[str, str]] = None,
                    mcq_answer_key: Optional[Dict[str, str]] = None,
                    textual_answers: Optional[List[Tuple[str, str]]] = None,
                    textual_questions: Optional[List[str]] = None) -> GradingResult:
        """
        Grade a complete paper with both MCQ and textual components.
        
        Args:
            student_info: Dict with name, student_id, roll_no
            mcq_answers: Student's MCQ answers
            mcq_answer_key: Correct MCQ answers
            textual_answers: List of (question, answer) tuples
            textual_questions: List of questions for textual grading
        
        Returns:
            GradingResult object
        """
        result = GradingResult(
            student_name=student_info.get('name', 'Unknown'),
            student_id=student_info.get('student_id', ''),
            roll_no=student_info.get('roll_no', '')
        )
        
        try:
            # Grade MCQ section if present
            if mcq_answers and mcq_answer_key:
                correct, total, percentage, incorrect = self.mcq_agent.grade(
                    mcq_answers, mcq_answer_key
                )
                result.mcq_score = correct
                result.mcq_total = total
                result.mcq_percentage = percentage
                result.mcq_incorrect = incorrect
                
                # Flag for review if MCQ score is very low
                if percentage < 40:
                    result.needs_review = True
                    result.review_reason = "MCQ score below 40%"
            
            # Grade textual section if present
            if textual_answers:
                total_textual_score = 0.0
                total_textual_marks = 0.0
                feedbacks = []
                
                for i, (question, answer) in enumerate(textual_answers):
                    max_marks = 10  # Default marks per question
                    score, feedback = self.textual_agent.grade(
                        question, answer, max_marks=max_marks
                    )
                    total_textual_score += score
                    total_textual_marks += max_marks
                    feedbacks.append(f"Q{i+1}: {score}/{max_marks} - {feedback}")
                
                result.textual_score = total_textual_score
                result.textual_feedback = "\n".join(feedbacks)
                
                # Flag for review if textual answers seem suspicious
                if total_textual_marks > 0:
                    textual_percentage = (total_textual_score / total_textual_marks) * 100
                    if textual_percentage < 30:
                        result.needs_review = True
                        result.review_reason = "Low textual score (possible plagiarism/irrelevant answers)"
            
            # Calculate total score
            if result.mcq_score is not None and result.textual_score is not None:
                # Weighted combination (50% MCQ, 50% Textual)
                mcq_normalized = (result.mcq_score / result.mcq_total) * 50 if result.mcq_total > 0 else 0
                textual_normalized = (result.textual_score / (len(textual_answers) * 10)) * 50 if textual_answers else 0
                result.total_score = mcq_normalized + textual_normalized
            elif result.mcq_score is not None:
                result.total_score = result.mcq_percentage
            elif result.textual_score is not None:
                result.total_score = (result.textual_score / (len(textual_answers) * 10)) * 100 if textual_answers else 0
            
        except Exception as e:
            result.error = str(e)
            result.needs_review = True
            result.review_reason = f"Grading error: {str(e)}"
        
        return result
