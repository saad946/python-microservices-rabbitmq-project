import os,requests

def login(request):
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return {"error": "Missing credentials"}, 401
    basicAuth = (auth.username, auth.password)

    response= requests.post(
        f"http://{os.environ.get('AUTH_SERVICE_URL')}/login",
        auth = basicAuth,
    )
    if response.status_code==200:
        return response.text, None
    else:
        return None, (response.status_code,response.text)

    
    

    
    # Validate credentials against the database

    
    
