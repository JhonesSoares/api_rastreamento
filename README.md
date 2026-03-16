# 📍 Real-Time Tracking API

Uma API robusta de rastreamento geográfico desenvolvida com **Django Rest Framework**, focada em performance e economia de recursos de banco de dados.

## 🚀 Sobre o Projeto

Este sistema permite o rastreamento de dispositivos em tempo real, utilizando uma lógica de persistência inteligente: as coordenadas só são salvas no banco de dados após o dispositivo percorrer uma distância mínima de **10 metros**. Isso evita redundância de dados e sobrecarga no PostgreSQL.

### Diferenciais Técnicos:

- **Otimização de Banco:** Filtro de distância para evitar gravacões desnecessárias.
- **Segurança:** Autenticação via JWT (JSON Web Tokens).
- **Simulação:** Script incluso para simular trajetos reais via terminal.
- **Visualização:** Interface frontend com mapa para monitoramento live.
- **Infraestrutura:** Ambiente 100% containerizado com Docker.

---

## 🛠️ Stack Tecnológica

- **Backend:** Python 3.x, Django, Django Rest Framework (DRF)
- **Banco de Dados:** PostgreSQL
- **Autenticação:** Simple JWT
- **Containerização:** Docker & Docker Compose
- **Frontend (Mapa):** HTML/JS (Leaflet ou Google Maps API)

---

## 📦 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados.

### Passos para Rodar:

1. **Clone o repositório:**

   ```bash
   git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
   cd seu-repositorio

   docker-compose up --build
   ```

script para simular: rastreamentoapp/utils/simulate_location.py
