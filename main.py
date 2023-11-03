"""
Module illustrating how we can write data (JSON) and files
to Xledger GraphQL.
"""
import json
from pathlib import Path

import requests
from requests_toolbelt import MultipartEncoder


def load_attachment(file_path):
    return open(file_path, "rb")


def get_query():
    query = """
    mutation ($PlaceHolderInput: [AddInvoiceBaseItemsInput!]!) {
      addInvoiceBaseItems(inputs: $PlaceHolderInput) {
        edges {
          node {
            amount
            dbId
          }
        }
      }
    }
    """
    variables = {
        "PlaceHolderInput": [
            {
                "clientId": "p1",
                "node": {
                    "subledger": {"dbId": 6982528},
                    "product": {"dbId": 1915441},
                    "unitPrice": 123,
                    "quantity": 2,
                    "attachment": "attachMe.PNG" # <- has to be aligned to file name in body
                }
            }
        ]
    }
    return {"query": query, "variables": variables}


def test_write_attachment(token: str):
    headers = {
        "Authorization": f"token {token}",
    }
    url = "https://demo.xledger.net/graphql"
    file_path = Path(__file__).parent / "attachMe.PNG"

    encoder = MultipartEncoder(
        # we need to organize the request body in parts
        # specifying which part is the file and which part
        # is the json object where the json object has to come last
        fields={
            'field2': ('attachMe.PNG', open(file_path, 'rb'), 'image/png'),
            'field0': ("file_name", json.dumps(get_query()).encode("utf-8"), "application/json")
        }
    )
    headers["Content-Type"] = encoder.content_type

    response = requests.post(
        url=url,
        data=encoder,
        headers=headers
    )
    print(response.status_code, response.json())


if __name__ == "__main__":
    test_write_attachment(
        token="ADD YOUR TOKEN HERE"
    )
