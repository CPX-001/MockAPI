from fastapi import APIRouter, Request

router = APIRouter(prefix = "endpoint", tags = ["endpoint"])

@router.post("/")
async def recieve_endpoint