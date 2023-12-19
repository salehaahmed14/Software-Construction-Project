from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper as db_helper
import generic_helper as generic_helper

app = FastAPI()

@app.post("/")
async def handle_request(request: Request):
    #retrieve the json data from request
    payload = await request.json()

    #extract the necessary info from the payload
    #based on the structure of webhook from dialog flow
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id = generic_helper.extract_session_id(output_contexts[0]['name'])

    intent_handler_dict = {
        'order.add - context: ongoing-order': add_to_order,
        'order.remove - context: ongoing-order': remove_from_order,
        'order-complete - context: ongoing-order': complete_order,
        'track.order - context: ongoing-tracking': track_order
    }

    return intent_handler_dict[intent](parameters, session_id)

inprogess_orders = {}

def add_to_order(parameters: dict, session_id: str):
    food_items = parameters['food-item']
    quantities = parameters['number']

    if len(food_items) != len(quantities):
         fulfillment_text = "Sorry, please specify the items and their respective quantities clearly."
    else:
         new_food_dict = dict(zip(food_items,quantities))
         if session_id in inprogess_orders:
              current_food_dict = inprogess_orders[session_id]
              current_food_dict.update(new_food_dict)
              inprogess_orders[session_id] = current_food_dict
         else:
              inprogess_orders[session_id] = new_food_dict

         print(inprogess_orders)       
         order_str = generic_helper.get_str_from_food_dict(inprogess_orders[session_id])
         fulfillment_text = f"So far you have {order_str} in your cart. Would you like anything else?"

    
    return JSONResponse(content={"fulfillmentText": fulfillment_text})

    


def remove_from_order(parameters: dict, session_id: str):
     if session_id not in inprogess_orders:
          fulfillment_text = "I am having trouble finding your order. Sorry for the inconvenience, please place your order again."
     else:
          current_order = inprogess_orders[session_id]
          removed_items = []
          no_such_items = []
          food_items = parameters["food-item"]
          for item in food_items:
               if item not in current_order:
                    no_such_items.append(item)
               else:
                    removed_items.append(item)
                    del current_order[item]
          if len(removed_items) > 0:
               fulfillment_text = f'Removed {",".join(removed_items)} from your order.'
          if len(no_such_items) > 0:
               fulfillment_text = f'{",".join(no_such_items)} not found in your order.'
          if len(current_order.keys()) == 0:
               fulfillment_text = "Your order is empty"
          else:
               order_str = generic_helper.get_str_from_food_dict(current_order)
               fulfillment_text = f'Items left in your order are {order_str}'
     return JSONResponse(content={"fulfillmentText": fulfillment_text})

def save_to_db(order):
     
    next_order_id = db_helper.get_next_order_id()
    for food_item, quantity in order.items():
          rcode = db_helper.insert_order_item(food_item, quantity, next_order_id)

          if rcode == -1:
               return -1
    db_helper.insert_order_tracking(next_order_id,"in progress")

    return next_order_id

def complete_order(parameters: dict, session_id: str):
     if session_id not in inprogess_orders:
          fulfillment_text = "I am having trouble finding your order. Sorry for the inconvenience, please place your order again."
     else:
          order = inprogess_orders[session_id]
          order_id = save_to_db(order)

          if order_id == -1:
               fulfillment_text = "Sorry I was unable to place your order. Please Try Again!"
          else:
               order_total = db_helper.get_total_order_price(order_id)
               fulfillment_text = f"Your order has been successfully placed!"\
                                   f"Your order id is: {order_id}."\
                                   f"Your total order amount is {order_total}$. Pay upon delivery."
     
     del inprogess_orders[session_id]

     return JSONResponse(content={"fulfillmentText": fulfillment_text})

    
def track_order(parameters: dict, session_id : str):
        order_id = int(parameters['number'])
        order_status = db_helper.get_order_status(order_id)

        if order_status:
            fulfillment_text = f"The order status for order id:{order_id} is: {order_status}"
        else:
             fulfillment_text = f"There is no order corresponding to order id:{order_id}"

        return JSONResponse(content={"fulfillmentText": fulfillment_text})