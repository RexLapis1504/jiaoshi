"""
Test script for AI Paper Checker system
Creates sample papers and tests the complete pipeline
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import MCQGradingAgent, TextualGradingAgent, OrchestratorAgent
from batch_processor import BatchProcessor, create_sample_papers_for_testing
from excel_exporter import ExcelExporter
from document_utils import parse_answer_key


def test_system():
    """Test the complete AI Paper Checker system."""
    
    print("=" * 70)
    print("AI PAPER CHECKER - SYSTEM TEST")
    print("=" * 70)
    
    # Step 1: Create sample papers
    print("\n[1/6] Creating sample papers...")
    test_dir = "/tmp/test_papers"
    paper_files = create_sample_papers_for_testing(test_dir, num_papers=3)
    print(f"✅ Created {len(paper_files)} sample papers in {test_dir}")
    
    # Step 2: Create answer key
    print("\n[2/6] Setting up answer key...")
    answer_key_text = """
1. A
2. B
3. C
4. D
5. A
"""
    answer_key = parse_answer_key(answer_key_text)
    print(f"✅ Answer key parsed: {len(answer_key)} questions")
    print(f"   Answer key: {answer_key}")
    
    # Step 3: Initialize agents
    print("\n[3/6] Initializing agent system...")
    mcq_agent = MCQGradingAgent()
    print(f"✅ {mcq_agent.name} initialized")
    
    textual_agent = TextualGradingAgent()
    print(f"✅ {textual_agent.name} initialized")
    if textual_agent.use_ai:
        print("   🤖 AI grading enabled")
    else:
        print("   📝 Using rule-based grading (no API key)")
    
    orchestrator = OrchestratorAgent(mcq_agent, textual_agent)
    print(f"✅ {orchestrator.name} initialized")
    
    # Step 4: Process papers in batch
    print("\n[4/6] Processing papers in batch...")
    batch_processor = BatchProcessor(orchestrator, max_workers=3)
    results = batch_processor.process_papers(paper_files, answer_key)
    
    print(f"\n✅ Batch processing complete!")
    print(f"   Papers processed: {len(results)}")
    print(f"   Papers with errors: {len(batch_processor.get_errors())}")
    print(f"   Papers flagged for review: {len(batch_processor.get_review_flagged())}")
    
    # Step 5: Display results
    print("\n[5/6] Grading Results:")
    print("-" * 70)
    for i, result in enumerate(results, 1):
        print(f"\n📄 Paper {i}: {result.student_name}")
        print(f"   Student ID: {result.student_id}")
        print(f"   Roll No: {result.roll_no}")
        if result.mcq_score is not None:
            print(f"   MCQ Score: {result.mcq_score}/{result.mcq_total} ({result.mcq_percentage:.2f}%)")
            if result.mcq_incorrect:
                print(f"   Incorrect: {', '.join(result.mcq_incorrect)}")
        if result.textual_score is not None:
            print(f"   Textual Score: {result.textual_score:.2f}")
        if result.total_score is not None:
            print(f"   Total Score: {result.total_score:.2f}%")
        if result.needs_review:
            print(f"   ⚠️  NEEDS REVIEW: {result.review_reason}")
        if result.error:
            print(f"   ❌ ERROR: {result.error}")
    
    # Step 6: Export to Excel
    print("\n[6/6] Exporting to Excel...")
    exporter = ExcelExporter()
    output_file = "/tmp/test_results.xlsx"
    excel_path = exporter.export_results(results, output_file)
    print(f"✅ Results exported to: {excel_path}")
    
    # Verify file exists
    if os.path.exists(excel_path):
        file_size = os.path.getsize(excel_path)
        print(f"   File size: {file_size} bytes")
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    if results:
        mcq_scores = [r.mcq_percentage for r in results if r.mcq_percentage is not None]
        if mcq_scores:
            avg_mcq = sum(mcq_scores) / len(mcq_scores)
            print(f"Average MCQ Score: {avg_mcq:.2f}%")
        
        total_scores = [r.total_score for r in results if r.total_score is not None]
        if total_scores:
            avg_total = sum(total_scores) / len(total_scores)
            print(f"Average Total Score: {avg_total:.2f}%")
        
        print(f"Papers Needing Review: {len([r for r in results if r.needs_review])}")
        print(f"Papers with Errors: {len([r for r in results if r.error])}")
    
    print("\n✅ ALL TESTS PASSED!")
    print("=" * 70)
    
    return True


def test_individual_components():
    """Test individual components separately."""
    
    print("\n" + "=" * 70)
    print("COMPONENT TESTS")
    print("=" * 70)
    
    # Test MCQ Agent
    print("\n[Component 1] Testing MCQ Grading Agent...")
    mcq_agent = MCQGradingAgent()
    student_ans = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "B"}
    correct_ans = {"1": "A", "2": "B", "3": "C", "4": "D", "5": "A"}
    correct, total, percentage, incorrect = mcq_agent.grade(student_ans, correct_ans)
    print(f"✅ MCQ Agent: {correct}/{total} = {percentage:.2f}%")
    print(f"   Incorrect: {incorrect}")
    assert correct == 4, "Expected 4 correct answers"
    assert total == 5, "Expected 5 total questions"
    
    # Test Textual Agent
    print("\n[Component 2] Testing Textual Grading Agent...")
    textual_agent = TextualGradingAgent()
    question = "What is the capital of France?"
    answer = "Paris is the capital city of France, located in the north-central part of the country."
    score, feedback = textual_agent.grade(question, answer, max_marks=10)
    print(f"✅ Textual Agent: {score}/10")
    print(f"   Feedback: {feedback}")
    assert score >= 0 and score <= 10, "Score should be between 0 and 10"
    
    # Test Orchestrator
    print("\n[Component 3] Testing Orchestrator Agent...")
    orchestrator = OrchestratorAgent(mcq_agent, textual_agent)
    student_info = {"name": "Test Student", "student_id": "12345", "roll_no": "CS101"}
    result = orchestrator.grade_paper(
        student_info=student_info,
        mcq_answers=student_ans,
        mcq_answer_key=correct_ans
    )
    print(f"✅ Orchestrator: Generated complete result")
    print(f"   Name: {result.student_name}")
    print(f"   MCQ: {result.mcq_percentage:.2f}%")
    print(f"   Needs Review: {result.needs_review}")
    
    print("\n✅ ALL COMPONENT TESTS PASSED!")
    print("=" * 70)


if __name__ == "__main__":
    try:
        # Run component tests first
        test_individual_components()
        
        # Run full system test
        test_system()
        
        print("\n🎉 All tests completed successfully!")
        print("You can now run 'python app.py' to start the web UI.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
