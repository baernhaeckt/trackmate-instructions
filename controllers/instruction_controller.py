from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from models.input_model import InputModel
from services.instruction_service import InstructionService

router = APIRouter()


@router.post("/generate", tags=["instructions"], status_code=200)
async def generate_instructions(start: InputModel, end: InputModel):
    instructions_service = InstructionService()

    return StreamingResponse(instructions_service.generate(start, end), media_type="audio/mp3")
