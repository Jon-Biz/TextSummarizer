import uuid
from faster_whisper import WhisperModel
from repository import TranscriptRepository

class TranscriptionService:
    """Service for handling audio transcription."""

    @staticmethod
    def transcribe(file):
        """
        Transcribe an audio file using Whisper.
        
        Args:
            file: The uploaded audio file to transcribe.
        
        Returns:
            dict: A dictionary containing the transcript and file path.
        """
        try:
            print(f"Transcribing audio: {file.filename}")

            # Alternate models:
            # model = WhisperModel("medium", device="cpu")
            # model = WhisperModel("small", device="cpu")
            # model = WhisperModel("distil-large-v3", device="cpu")
            # model = WhisperModel("large-v3-turbo", device="cpu")

            model = WhisperModel("distil-large-v3", device="cpu", compute_type="float32")
            segments, info = model.transcribe(file.file, initial_prompt=None, word_timestamps=False)

            print(f"Transcription info: {info}")
            print(f"Transcription segments: {segments}")

            transcript = ""
            for segment in segments:
                print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
                transcript += segment.text + "\n"

            # Save transcript using repository
            file_id = uuid.uuid4().hex
            file_extension = file.filename.split('.')[-1]
            file_path = TranscriptRepository.save(file_id, transcript, f".{file_extension}")

            print(f"Transcript saved to: {file_path}")
            print(f"Transcript: {transcript}")

            return {"transcript": transcript, "transcript_path": file_path}

        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return {"error": str(e)}