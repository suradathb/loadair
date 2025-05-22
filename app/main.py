from fastapi import FastAPI
from app.controllers import quotation_controller, customer_controller,avinode_controller

app = FastAPI(title="CRM API")

app.include_router(quotation_controller.router)
app.include_router(customer_controller.router)
app.include_router(avinode_controller.router)

@app.get("/")
def root():
    return {"message": "Welcome to CRM API"}
