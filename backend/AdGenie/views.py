import asyncio
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

# AI Services
from AdGenie.Services.prompt_generator import getImagePrompt
from AdGenie.Services.generation_loop import CreateImagesInLoop

# DataBase Service
from AdGenie.db.actions.get_brands import getAllBrandsFromDB
from AdGenie.db.actions.createBrand import createBrandInDB

@csrf_exempt
def getCampaignImages(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        campaign = data.get("campaign_details")
        
        ImageGenprompt = getImagePrompt(campaign)
        response = asyncio.run(CreateImagesInLoop(campaign, ImageGenprompt))
        
        return JsonResponse({"response": response})
      
      
@csrf_exempt
def getAllBrands(request):
    if request.method == "GET":
        response = getAllBrandsFromDB()
        
        return JsonResponse({"Brands": response})
    
@csrf_exempt
def CreateNewBrand(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        
        brand_details = data.get("brand_details")
        
        brand_name = brand_details.get("brand_name")
        brand_type = brand_details.get("brand_type")
        description = brand_details.get("description")
        color_scheme = brand_details.get("color_scheme")
        
        
        createBrandInDB(brand_name, brand_type, description, color_scheme)
        
        response = getAllBrandsFromDB()
        
        return JsonResponse({"brands": response})
        