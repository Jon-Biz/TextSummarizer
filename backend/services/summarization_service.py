import uuid
from openai import OpenAI
from repository import SummaryRepository

class SummarizationService:
    """Service for handling text summarization."""

    def __init__(self, client: OpenAI, system_prompt: str):
        """
        Initialize the summarization service.
        
        Args:
            client: OpenAI client for generating summaries
            system_prompt: Prompt for guiding summary generation
        """
        self.client = client
        self.system_prompt = system_prompt

    def generate_summary(self, transcript: str):
        """
        Generate a summary for a given transcript.
        
        Args:
            transcript: Text to be summarized
        
        Returns:
            dict: A dictionary containing the summary path or error
        """
        try:
            print(f"Transcript: {transcript}")

            # Summarize transcript with OpenAI
            response = self.client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[
                    {
                    "role": "user",
                    "content": f"{self.system_prompt}\n\n{transcript}"
                    }
                ]
            )

            summary = response.choices[0].message.content
            print(f"Generated summary: {summary}")

            # Get title for summary
            title_response = self.client.chat.completions.create(
                model="openai/gpt-4o",
                messages=[
                    {
                    "role": "user",
                    "content": f"Generate a short, descriptive title for this text:\n\n{transcript}"
                    }
                ]
            )

            title = title_response.choices[0].message.content
            print(f"Generated title: {title}")

            # Sanitize title and save summary
            sanitized_title = self._sanitize_filename(title)
            try:
                summary_path = SummaryRepository.save(sanitized_title, summary, uuid.uuid4().hex)
                print(f"Summary saved to: {summary_path}")
                return {"summary_path": summary_path}
            except Exception as e:
                print(f"Error saving summary: {e}")
                return {"error": str(e)}

        except Exception as e:
            print(f"Error generating summary: {e}")
            return {"error": str(e)}

    @staticmethod
    def _sanitize_filename(filename):
        """
        Remove or replace characters that are not allowed in filenames.
        
        Args:
            filename: Original filename to sanitize
        
        Returns:
            str: Sanitized filename
        """
        import re
        sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
        return sanitized[:255]