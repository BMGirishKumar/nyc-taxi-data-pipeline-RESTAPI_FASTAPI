from fastapi import FastAPI, Request, Response,Query, status, HTTPException,Path, Form, File, UploadFile
from pydantic import BaseModel,Field
from typing import Optional, List

app=FastAPI(title='FastAPI Rest API',description='This is a FastAPI Rest API',version='1.0.0')

class Product(BaseModel):
    id:int =Field(...,description='Unique ID of the product',gt=0)
    name:str =Field(...,min_length=2,example='Wireless mouse')
    price:float=Field(...,gt=0.0,description='Price of the product must be greater than 0')
    category:str=Field(...,example="Accessories")
    instock:bool=Field(default=True,description='Indicates if the product is in stock or not')

class Item(BaseModel):
    id:int=Field(...,description= "Enter the item_id")
    price:float=Field(...,description="Enter the price of the item",gt=1.00)


#Temp to understand the concept of CRUD operations
inventory_db=[
    {"id":1, "name":"Wireless mouse","price":25.99,"category":"Accessories","instock":True},
    {"id":2, "name":"Mechanical keyboard","price":79.99,"category":"Accessories","instock":True},
    {"id":3, "name":"Gaming monitor","price":299.99,"category":"Monitors","instock":False}
]

item_inventory_db=[
    {"id":1, "name":"Wireless mouse","price":25.99},
    {"id":2, "name":"Mechanical keyboard","price":79.99},
    {"id":3, "name":"Gaming monitor","price":299.99}
]

# --- Get endpoint to retrieve all products
@app.get("/")
def home():
    return {"status":"Online","message":"Welcome to the store inventory API"}

# --- Get Endpoint with query paramentes(Filtering & Limits)

@app.get("/products",response_model=List[Product],status_code=status.HTTP_200_OK)
def get_products(category:Optional[str]=Query(None,description="Filter products by category"),limit:int=Query(10,gt=1,le=100,description="Limit the number of returns")):
    results=inventory_db
    if category:
        results=[p for p in results if p["category"].lower()==category.lower()]
    return results[:limit]


# --- Post Endpoint to add a new product (Data creation & Validation)

@app.post("/products",response_model=Product,status_code=status.HTTP_201_CREATED)
def create_product(product: Product):
    if any(p["id"]==product.id for p in inventory_db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Product with ID {product.id} already exists.")
    product_dict=product.dict()
    inventory_db.append(product_dict)
    return product_dict


@app.post("/items",response_model=Item,status_code=status.HTTP_201_CREATED)
def create_item(item:Item):
    if any(i["id"]==item.id for i in item_inventory_db):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Product with ID {product.id} already exists.")
    item_dict=item.dict()
    item_inventory_db.append(item)
    return item