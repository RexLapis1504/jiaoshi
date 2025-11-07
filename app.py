"""
Gradio Web UI for AI Paper Checker
Main interface for the grading system
"""
import os
import gradio as gr
from pathlib import Path
from typing import List, Tuple, Optional

from agents import MCQGradingAgent, TextualGradingAgent, OrchestratorAgent
from batch_processor import BatchProcessor
from excel_exporter import ExcelExporter
from document_utils import parse_answer_key


class PaperCheckerUI:
    """Gradio UI for the AI Paper Checker system."""
    
    def __init__(self):
        self.orchestrator = None
        self.batch_processor = None
        self.excel_exporter = ExcelExporter()
        self.setup_agents()
    
    def setup_agents(self):
        """Initialize the agent system."""
        mcq_agent = MCQGradingAgent()
        
        # Try to use OpenAI API if available
        api_key = os.environ.get("OPENAI_API_KEY")
        textual_agent = TextualGradingAgent(api_key=api_key)
        
        self.orchestrator = OrchestratorAgent(mcq_agent, textual_agent)
        self.batch_processor = BatchProcessor(self.orchestrator, max_workers=5)
    
    def process_papers(self, 
                       paper_files: List[str],
                       answer_key_file: Optional[str],
                       answer_key_text: str) -> Tuple[str, str, str]:
        """
        Process uploaded papers and return results.
        
        Returns:
            Tuple of (result_message, excel_file_path, summary_message)
        """
        try:
            if not paper_files:
                return "Error: No paper files uploaded.", None, ""
            
            # Limit to 100 papers
            if len(paper_files) > 100:
                return "Error: Maximum 100 papers allowed per batch.", None, ""
            
            # Parse answer key
            mcq_answer_key = None
            if answer_key_text.strip():
                mcq_answer_key = parse_answer_key(answer_key_text)
                if not mcq_answer_key:
                    return "Error: Could not parse answer key. Please check the format.", None, ""
            elif answer_key_file:
                # Read answer key from file
                from document_utils import extract_text_from_file
                answer_key_content = extract_text_from_file(answer_key_file)
                mcq_answer_key = parse_answer_key(answer_key_content)
                if not mcq_answer_key:
                    return "Error: Could not parse answer key from file.", None, ""
            
            # Process papers
            results = self.batch_processor.process_papers(
                paper_files=[f if isinstance(f, str) else f.name for f in paper_files],
                mcq_answer_key=mcq_answer_key
            )
            
            if not results:
                return "Error: No papers were processed successfully.", None, ""
            
            # Export to Excel
            excel_path = self.excel_exporter.export_results(results)
            
            # Generate summary
            total = len(results)
            reviewed = sum(1 for r in results if r.needs_review)
            errors = sum(1 for r in results if r.error)
            
            summary = f"""
## Processing Complete! ✅

- **Total Papers Processed:** {total}
- **Papers Needing Review:** {reviewed}
- **Papers with Errors:** {errors}
- **Success Rate:** {((total - errors) / total * 100):.1f}%

### Score Distribution
"""
            
            if any(r.mcq_percentage is not None for r in results):
                mcq_scores = [r.mcq_percentage for r in results if r.mcq_percentage is not None]
                avg_mcq = sum(mcq_scores) / len(mcq_scores)
                summary += f"- **Average MCQ Score:** {avg_mcq:.2f}%\n"
            
            if any(r.total_score is not None for r in results):
                total_scores = [r.total_score for r in results if r.total_score is not None]
                avg_total = sum(total_scores) / len(total_scores)
                summary += f"- **Average Total Score:** {avg_total:.2f}%\n"
            
            result_msg = f"✅ Successfully processed {total} papers!\n\n"
            result_msg += f"📊 Results exported to: {excel_path}\n\n"
            
            if reviewed > 0:
                result_msg += f"⚠️ {reviewed} papers flagged for manual review.\n"
            
            if errors > 0:
                result_msg += f"❌ {errors} papers had processing errors.\n"
            
            return result_msg, excel_path, summary
            
        except Exception as e:
            error_msg = f"Error processing papers: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return error_msg, None, ""
    
    def create_ui(self):
        """Create and return the Gradio interface."""
        
        with gr.Blocks(title="AI Paper Checker", theme=gr.themes.Soft()) as demo:
            gr.Markdown("""
            # 📝 AI Paper Checker - Complete MVP
            
            Grade up to 100 papers at once with AI-powered evaluation!
            
            ### Features:
            - ✅ Batch Processing (up to 100 papers)
            - 📄 Multi-format Support (PDF, DOCX, TXT)
            - 🎯 Strict MCQ Grading (100% accuracy)
            - 🤖 AI-Powered Textual Answer Grading
            - 📊 Excel Export with Review Flags
            - 🔍 Automatic Student Info Extraction
            - ⚡ Real-time Progress Tracking
            - 🛡️ Robust Error Handling
            """)
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### 1️⃣ Upload Papers")
                    paper_files = gr.File(
                        label="Upload Student Papers (PDF, DOCX, TXT)",
                        file_count="multiple",
                        file_types=[".pdf", ".docx", ".txt"]
                    )
                    
                    gr.Markdown("### 2️⃣ Provide Answer Key (Optional for MCQ)")
                    
                    with gr.Tabs():
                        with gr.Tab("Text Input"):
                            answer_key_text = gr.Textbox(
                                label="Answer Key",
                                placeholder="Enter answer key:\n1. A\n2. B\n3. C\n4. D\n5. A",
                                lines=10
                            )
                        
                        with gr.Tab("File Upload"):
                            answer_key_file = gr.File(
                                label="Upload Answer Key File",
                                file_types=[".txt", ".pdf", ".docx"]
                            )
                    
                    process_btn = gr.Button("🚀 Process Papers", variant="primary", size="lg")
                
                with gr.Column():
                    gr.Markdown("### 📊 Results")
                    result_output = gr.Textbox(
                        label="Processing Status",
                        lines=8,
                        interactive=False
                    )
                    
                    summary_output = gr.Markdown()
                    
                    excel_output = gr.File(
                        label="Download Results (Excel)",
                        interactive=False
                    )
            
            gr.Markdown("""
            ---
            ### 📖 Instructions:
            
            1. **Upload Papers**: Select multiple paper files (max 100)
            2. **Answer Key**: Provide MCQ answer key in format: `1. A`, `2. B`, etc.
            3. **Process**: Click the button and wait for results
            4. **Download**: Get formatted Excel with scores and review flags
            
            ### 📋 Supported Formats:
            - **PDF**: Scanned or text-based PDFs
            - **DOCX**: Microsoft Word documents
            - **TXT**: Plain text files
            
            ### 🎯 Answer Key Format:
            ```
            1. A
            2. B
            3. C
            4. D
            5. A
            ```
            
            Or:
            ```
            Q1: A
            Q2: B
            Q3: C
            ```
            
            ### ⚠️ Notes:
            - Student info is extracted from document content or filename
            - Papers with low scores are automatically flagged for review
            - AI grading requires OpenAI API key (set OPENAI_API_KEY env variable)
            - Without API key, rule-based grading is used as fallback
            """)
            
            # Connect the button to the processing function
            process_btn.click(
                fn=self.process_papers,
                inputs=[paper_files, answer_key_file, answer_key_text],
                outputs=[result_output, excel_output, summary_output]
            )
        
        return demo
    
    def launch(self, **kwargs):
        """Launch the Gradio interface."""
        demo = self.create_ui()
        demo.launch(**kwargs)


def main():
    """Main entry point for the application."""
    print("🚀 Starting AI Paper Checker...")
    print("=" * 60)
    
    # Check for OpenAI API key
    if os.environ.get("OPENAI_API_KEY"):
        print("✅ OpenAI API key found - AI grading enabled")
    else:
        print("⚠️  No OpenAI API key found - using rule-based grading")
        print("   Set OPENAI_API_KEY environment variable for AI grading")
    
    print("=" * 60)
    
    # Create and launch UI
    ui = PaperCheckerUI()
    ui.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860
    )


if __name__ == "__main__":
    main()
