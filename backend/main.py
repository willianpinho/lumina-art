import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

app = FastAPI(title="Lumina Art API")

# Configuração de CORS para permitir que o frontend acesse o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ImageRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_image(request: ImageRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("op://"):
        raise HTTPException(
            status_code=500, 
            detail="OpenAI API Key não configurada corretamente ou ainda é uma referência op://. Use 'op run' para iniciar."
        )
    
    try:
        # Inicializa o cliente com a chave resolvida
        client = OpenAI(api_key=api_key)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=request.prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        image_url = response.data[0].url
        return {"url": image_url}
    except Exception as e:
        print(f"Erro na geração: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
