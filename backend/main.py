from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.architectures import ARCHITECTURE_REGISTRY
from core.architectures.debate_two import TwoAgentDebate
from core.llm_service import LLMService
from models.schemas import ArchitectureResult, TestArchitectureRequest

app = FastAPI(
    title="Agent Reliability Benchmark Lab",
    description="FutureAGI-Powered Multi-Agent Reliability Benchmark API",
    version="0.1.0",
)

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/test-architecture", response_model=ArchitectureResult)
async def test_architecture(request: TestArchitectureRequest):
    """Execute a prompt through the selected architecture and return the structured result."""

    arch_cls = ARCHITECTURE_REGISTRY.get(request.architecture)
    if arch_cls is None:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown architecture '{request.architecture}'. "
                f"Available: {list(ARCHITECTURE_REGISTRY.keys())}"
            ),
        )

    llm = LLMService()

    # Pass rounds for debate architectures
    if arch_cls is TwoAgentDebate:
        architecture = arch_cls(llm_service=llm, rounds=request.rounds)
    else:
        architecture = arch_cls(llm_service=llm)

    try:
        result = await architecture.execute(request.prompt)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Architecture execution failed: {exc}")

    return result
