from httpx import AsyncClient, Timeout
from loguru import logger

async def get_eligibility():
    try:
        async with AsyncClient() as client:
            response = await client.post(
                url='https://sandbox.onederful.co/sandbox/eligibility',
                headers={'Content-Type': 'application/json'},
                json={
                    "subscriber": {               
                        "first_name": "TEST",               
                        "last_name": "PERSON",               
                        "dob": "01/01/2011",               
                        "member_id": "1234567890"           
                    },           
                    "provider": {               
                        "npi": "1234567890"           
                    },           
                    "payer": {               
                        "id": "PRINCIPAL"           
                    },           
                    "version": "v2"       
                },
                timeout=Timeout(20.0)
            )
        response.raise_for_status()
        data = response.json()
    except Exception as err:
        logger.error(f'Error requesting eligibility: {err} Error type: {type(err).__name__}')

    return data