import json

from src.schemas import MeetingAnalysis
from src.prompts import (
    meeting_analysis_system_prompt,
    meeting_verification_system_prompt
)

def call_structured_model(
    client,
    model,
    system_prompt,
    user_prompt,
):
    """
    Generates JSON output from transcript and validate against JSON schema expected from meeting analysis
    """
    schema = MeetingAnalysis.model_json_schema()

    response = client.responses.create(
        model=model,
        instructions=system_prompt,
        input=user_prompt,
        text={
            "format": {
                "type": "json_schema",
                "name": "meeting_analysis",
                "schema": schema,
                "strict": True,
            }
        },
    )

    return MeetingAnalysis.model_validate_json(
        response.output_text
    )


def analyze_meeting( #accepts meeting transcript and instructs model to produce structured Meeting Analysis
    client,   #Take this transcript, construct an analysis request, 
    transcript, #send it to the model using my meeting-analysis instructions, require the response to follow MeetingAnalysis, and return the validated result.
    model):

    """
    Analyze the meeting transcript
    """
    user_prompt = f"""
    Analyze the meeting transcript below.

    TRANSCRIPT
    ---------
    {transcript}
    """

    return call_structured_model(
        client=client,
        model=model,
        system_prompt=meeting_analysis_system_prompt,
        user_prompt=user_prompt)


def verify_meeting_analysis( #audits and corrects the proposed analysis by comparing it against the original transcript and return corrected completed MeetingAnalysis object
    client,
    transcript,
    analysis,
    model):

    """
    Check structured meeting analysus against original meeting transcript
    and correct unsupported claims
    """

    analysis_json = analysis.model_dump_json(indent=2) #converts the MeetingAnalysis objects into JSON string and indent=2 just makes introduces indentation to make the JSON easier to read

    user_prompt = f"""
Verify the proposed analysis against the original transcript.

ORIGINAL TRANSCRIPT
-------------------
{transcript}

PROPOSED ANALYSIS
-----------------
{analysis_json}
"""

    return call_structured_model(
        client=client,
        model=model,
        system_prompt=meeting_verification_system_prompt,
        user_prompt=user_prompt
        )