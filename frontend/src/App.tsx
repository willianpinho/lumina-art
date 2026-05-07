import { useState } from 'react';
import { Sparkles, Download, Loader2 } from 'lucide-react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    if (!prompt) return;
    
    setLoading(true);
    setError('');
    setImageUrl('');

    // Detecta se está rodando em produção ou local
    const API_URL = window.location.hostname === 'localhost' 
      ? 'http://localhost:8000' 
      : 'https://lumina-api.willianpinho.com';

    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Failed to generate image. Please check your prompt or API status.');
      }

      const data = await response.json();
      setImageUrl(data.url);
    } catch (err: any) {
      setError(err.message || 'Ocorreu um erro inesperado.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header>
        <div className="logo">
          <Sparkles className="icon-sparkle" />
          <h1>Lumina Art</h1>
        </div>
        <p>Transform your imagination into breathtaking visuals with the power of DALL-E 3.</p>
      </header>

      <main>
        <div className="input-section">
          <div className="input-group">
            <textarea
              placeholder="Describe your vision... (e.g., A cinematic shot of a futuristic neon city in the clouds, high detail, 8k)"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              disabled={loading}
            />
            <button 
              onClick={handleGenerate} 
              disabled={loading || !prompt}
              className="generate-btn"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" />
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <Sparkles size={20} />
                  <span>Generate Masterpiece</span>
                </>
              )}
            </button>
          </div>

          {error && (
            <div className="error-message">
              <span>⚠️</span>
              <p>{error}</p>
            </div>
          )}
        </div>

        <div className="display-area">
          {loading && (
            <div className="loading-state">
              <Loader2 className="animate-spin large" />
              <p className="loading-text">DALL-E is bringing your prompt to life...</p>
            </div>
          )}

          {!loading && imageUrl && (
            <div className="image-container">
              <img src={imageUrl} alt={prompt} />
              <div className="actions">
                <a href={imageUrl} target="_blank" rel="noreferrer" className="download-link">
                  <Download size={18} />
                  <span>View Original</span>
                </a>
              </div>
            </div>
          )}

          {!loading && !imageUrl && !error && (
            <div className="empty-state">
              <p>Your digital art will manifest here.</p>
            </div>
          )}
        </div>
      </main>

      <footer>
        <p>Lumina Art • Powered by OpenAI • 2026</p>
      </footer>
    </div>
  );
}

export default App;
