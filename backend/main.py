from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Aanchal Boutique Support API")

app.add_middleware(
CORSMiddleware,
allow_origins=["http://localhost:3000"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

tickets = [
{
"id": 1,
"subject": "Order delivery delay",
"excerpt": "Customer wants an update about a delayed boutique order."
},
{
"id": 2,
"subject": "Dress size exchange",
"excerpt": "Customer wants to exchange a dress for a different size."
},
{
"id": 3,
"subject": "Payment confirmation",
"excerpt": "Customer has paid but has not received confirmation."
}
]

@app.get("/")
def home():
    return {"message": "Aanchal Boutique Support API is running"}

@app.get("/api/tickets")
def get_tickets():
    return tickets
