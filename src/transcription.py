from pathlib import Path

supported_audio_format = {
    ".mp3", ".mp4", ".mpeg", 
    ".mpga", ".m4a", ".wav", 
    ".webm"
}

def validate_audio(audio_path):
    """
    Validate audio file is provided, exists, and has supported format.
    """
    if not audio_path:
        raise ValueError("No audio file provided")
    
    audio_path = Path(audio_path)

    if not audio_path.exists():
        raise FileNotFoundError(
            f"Audio file not found: {audio_path}")
    
    if audio_path.suffix.lower() not in supported_audio_format:
        raise ValueError(
            f"Unsupported audio format: {audio_path.suffix}"
        )
    
    return audio_path


def format_timestamp(seconds):
    """
    Convert seconds to HH:MM:SS format.
    """
    seconds = int(seconds)

    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02}:{minutes:02}:{seconds:02}"


def transcribe_audio(
    client,
    audio_path,
    model="gpt-4o-transcribe-diarize", #performs automatic speech recognition with built-in speaker diarization
    language="en" #expects audio in english
    ):
    """
    Validate audio file, send to OpenAI for transcription and speaker 
    diarization, and return the structured transcription results.
    """
    audio_path = validate_audio(audio_path)

    with audio_path.open("rb") as audio_file: #read audio file as binary data
        transcription = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            language=language,
            response_format="diarized_json",#expects structured diarized response
            chunking_strategy="auto", #allows the transcription system to automatically address how longer audio is divided into manageable portions for transcription
        )

    segments = []

    for segment in transcription.segments:
        segments.append(
            {
                "speaker": segment.speaker,
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip()
            }
        )
    
    return {
        "text": transcription.text,
        "duration": transcription.duration,
        "segments": segments
    }


def format_diarized_transcript(transcription):
    lines = []

    for segment in transcription["segments"]:
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])

        lines.append(
            f"[{start} - {end}] "
            f"speaker {segment['speaker']}: "
            f"{segment['text']}"
        )

    return "\n".join(lines)