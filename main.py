from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from threat_engine import calculate_scores

app = FastAPI(title="AegisAI - Behavioral Threat Intelligence API")

class TextInput(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(input: TextInput):
    result = calculate_scores(input.text)
    result["deepfake_suspicion"] = "N/A"
    result["transcript"] = "N/A"
    return result

@app.post("/analyze-audio")
async def analyze_audio(file: UploadFile = File(...)):
    # Simulated transcription for stable prototype demo
    simulated_transcript = "Your bank account will be suspended immediately. Transfer OTP now."

    threat_result = calculate_scores(simulated_transcript)

    threat_result["transcript"] = simulated_transcript
    threat_result["deepfake_suspicion"] = "Moderate (Heuristic Simulation)"

    return threat_result

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")