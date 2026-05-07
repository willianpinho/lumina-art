# Lumina Art - AI Image Generator

Este é um protótipo funcional de um gerador de imagens usando OpenAI DALL-E 3, configurado com práticas modernas de segurança (1Password CLI).

## Estrutura
- `backend/`: API FastAPI (Python) que atua como proxy seguro.
- `frontend/`: Interface React (Vite + TypeScript) para experiência do usuário.

## Como rodar com Segurança (1Password)

Este projeto está configurado para não armazenar chaves em texto puro. Utilizaremos o 1Password CLI (`op`).

### 1. Preparar o Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configurar Variável de Ambiente
Crie o arquivo `.env` usando a referência do seu 1Password:
```bash
echo 'OPENAI_API_KEY="op://VaultName/ItemName/credential"' > .env
```
*Substitua `VaultName/ItemName/credential` pelo caminho real no seu 1Password.*

### 3. Iniciar com Segurança
O comando abaixo injeta a chave em memória sem salvá-la no ambiente global:
```bash
op run --env-file=.env -- python main.py
```

### 4. Iniciar o Frontend
Em outro terminal:
```bash
cd frontend
npm install
npm run dev
```

---

## Passo a Passo da Criação (Roteiro)

Para construir este protótipo, segui estes princípios de engenharia:

1.  **Scaffolding Limpo:** Separação clara entre lógica de negócio (Python) e interface (React).
2.  **Proxy de Segurança:** O backend protege a chave de API e evita erros de CORS que ocorreriam se o frontend chamasse a OpenAI diretamente.
3.  **Tipagem Estrita:** Uso de TypeScript no frontend e Pydantic no backend para garantir contratos de dados válidos.
4.  **UX Responsiva:** Implementação de estados de `loading` e `error` para que o usuário saiba exatamente o que está acontecendo durante o processamento da IA.
5.  **Segurança First:** Integração com 1Password para garantir que credenciais nunca sejam commitadas ou expostas em texto puro.
