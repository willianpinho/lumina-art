import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

MAX_PROMPT_LENGTH = 1000

app = FastAPI(title="Lumina Art API")

# CORS so the frontend can reach the backend. This API uses no cookies or
# credentials, so credentials stay disabled — a wildcard origin combined with
# allow_credentials=True is rejected by browsers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ImageRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=MAX_PROMPT_LENGTH)


@app.post("/generate")
async def generate_image(request: ImageRequest):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key.startswith("op://"):
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key is not configured correctly or is still an op:// reference. Start the server with 'op run'.",
        )

    try:
        # Initialize the client with the resolved key
        client = OpenAI(api_key=api_key)

        # gpt-image-1 (current canonical, April 2025+) replaces deprecated dall-e-3.
        # Returns base64 by default (no URL response). We expose it as a data URL so
        # the existing frontend contract ({url: string}) stays unchanged — <img src>
        # accepts data URLs natively.
        response = client.images.generate(
            model="gpt-image-1",
            prompt=request.prompt,
            size="1024x1024",
            quality="medium",  # gpt-image-1 quality enum: low | medium | high | auto
            n=1,
        )

        b64 = response.data[0].b64_json
        if not b64:
            raise HTTPException(
                status_code=502, detail="OpenAI returned no image payload."
            )

        data_url = f"data:image/png;base64,{b64}"
        return {"url": data_url}
    except HTTPException:
        raise
    except Exception as e:
        # Log the real error server-side, but never leak it to the client —
        # OpenAI SDK exceptions can echo back request details.
        print(f"Generation error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Image generation failed. Please try again."
        )


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
