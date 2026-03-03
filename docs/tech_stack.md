# 🛠 Tech Stack  
## FutureAGI-Powered Multi-Agent Reliability Benchmark Lab

---

# 1️⃣ Frontend

## Framework
- **Next.js 14 (App Router)**  
  - Server-side rendering support  
  - Modern routing system  
  - Production-ready and Vercel deployable  

## Language
- **TypeScript**  
  - Strong typing for API contracts  
  - Improved maintainability and scalability  

## Styling
- **Tailwind CSS**  
  - Utility-first styling  
  - Fast UI development  
  - Clean SaaS-style dashboard design  

## UI Components
- **shadcn/ui**  
  - Professional component library  
  - Cards, tables, forms, dialogs, dropdowns  
  - Clean and minimal design system  

## Data Visualization
- **Recharts**  
  - Bar charts (Accuracy comparison)  
  - Line charts (Debate rounds vs improvement)  
  - Scatter plots (Tokens vs accuracy)  

## API Communication
- **Axios**  
  - Structured REST API communication  
  - Centralized error handling  
  - Interceptors for authentication or retries  

---

# 2️⃣ Backend

## Framework
- **FastAPI**  
  - High-performance async backend  
  - Automatic OpenAPI documentation  
  - Clean integration with Pydantic models  

## Language
- **Python 3.11+**  
  - Strong ecosystem for LLM tooling  
  - Native support for async workflows  

## LLM Integration
- **OpenAI SDK (or OpenAI-compatible client)**  
  - Model abstraction layer  
  - Token usage tracking  
  - Configurable temperature and model parameters  

## Evaluation Integration
- **FutureAGI API Integration**  
  - Structured reliability scoring  
  - Hallucination detection  
  - Logical consistency evaluation  
  - Safety compliance scoring  

## ORM / Database Access
- **SQLAlchemy**  
  - Industry-standard ORM for Python  
  - Clean integration with FastAPI  
  - Supports relational and JSONB data  

---

# 3️⃣ Database

## Database System
- **PostgreSQL**

### Rationale:
- ACID-compliant  
- Production-grade  
- Supports JSONB for structured logs  
- Scalable and widely adopted  

### Deployment Options:
- Local (Dockerized PostgreSQL)
- Supabase (Managed PostgreSQL)
- Railway (Managed PostgreSQL)

---

# 4️⃣ Observability & Logging

## Structured Logging
- Python `logging` module
- JSON-formatted logs for traceability

## Performance Tracking
- Token usage tracking per agent turn
- Latency measurement using high-resolution timers

## Experiment Trace Storage
- Structured storage of:
  - Debate transcripts
  - Evaluation responses
  - Derived performance metrics

---

# 5️⃣ DevOps & Environment

## Containerization
- **Docker**
  - Backend container
  - PostgreSQL container (local development)
  - Reproducible environments  

## Environment Management
- `.env` files  
- `python-dotenv` for backend  
- Secure environment variables for API keys  

---

# 6️⃣ Deployment Strategy

| Layer      | Deployment Platform |
|------------|--------------------|
| Frontend   | Vercel             |
| Backend    | Railway / Render   |
| Database   | Supabase / Railway |
| Secrets    | Platform Environment Variables |

---

# 7️⃣ Summary

The finalized stack ensures:

- Full-stack TypeScript + Python architecture  
- Evaluation-first backend design  
- Observability and reproducibility  
- Production-grade database system  
- Scalable and deployable infrastructure  

This stack demonstrates strong engineering maturity, AI orchestration capability, and evaluation-driven system design aligned with modern AI infrastructure practices.