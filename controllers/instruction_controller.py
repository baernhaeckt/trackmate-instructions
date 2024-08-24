from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.input_model import InputModel
from services.instruction_service import InstructionService

router = APIRouter()


@router.post("/generate_audio", tags=["instructions"], status_code=200)
async def generate_audio_instructions(start: InputModel, end: InputModel):
    instructions_service = InstructionService()

    return StreamingResponse(instructions_service.generate_audio(start, end), media_type="audio/wav")


@router.post("/generate_text", tags=["instructions"], status_code=200)
async def generate_text_instructions(start: InputModel, end: InputModel):
    instructions_service = InstructionService()

    return StreamingResponse(instructions_service.generate_text(start, end), media_type="text/event-stream")