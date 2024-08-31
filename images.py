# import requests




# GOOGLE
# BHNCHOD YE PLACES API PAID HAI






# def get_monument_photos(place_name: str, api_key: str):
#     # Search for the place
#     search_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={place_name}&inputtype=textquery&fields=place_id,photos&key={api_key}"
#     search_response = requests.get(search_url).json()
    
#     if 'candidates' not in search_response or len(search_response['candidates']) == 0:
#         return "No results found."
    
#     place_id = search_response['candidates'][0]['place_id']
    
#     # Get place details
#     details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&fields=photos&key={api_key}"
#     details_response = requests.get(details_url).json()
    
#     if 'result' not in details_response or 'photos' not in details_response['result']:
#         return "No photos found."
    
#     photos = details_response['result']['photos']
#     photo_urls = []
    
#     for photo in photos:
#         photo_reference = photo['photo_reference']
#         photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
#         photo_urls.append(photo_url)
    
#     return photo_urls

# # Example usage
# api_key = 'YOUR_GOOGLE_API_KEY'
# place_name = 'Eiffel Tower'
# print(get_monument_photos(place_name, api_key))
