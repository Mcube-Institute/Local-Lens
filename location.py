from flask import Blueprint,request,jsonify
from models import Location

locationBp=Blueprint("locationBp",__name__)

@locationBp.post("/location/new")
def newLocation():
    try:
        location=request.get_json()

        if not location:
            return jsonify({"status":"error","message":"All Fields Required."})

        street=location.get("street")
        city=location.get("city")
        state=location.get("state")
        country=location.get("country")
        pincode=location.get("pincode")

        if not len(pincode)==6:
            return jsonify({"status":"error","message":"Invalid Pincode."})
    
        Location(
            street=street,
            city=city,
            state=state,
            country=country,
            pincode=pincode
        ).save()

        return jsonify({"status":"success","message":"Location Added Successfully."})

    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@locationBp.get("/location/getAll")
def allLocations():
    try:
        locations=Location.objects()

        if not locations:
            return jsonify({"status":"error","message":"Location Is Empty."})
   
        locationList=[]
   
        for location in locations:
            data={
                 "street":location.street,
                 "city":location.city,
                 "state":location.state,
                "country":location.country,
                "pincode":location.pincode
             }

            locationList.append(data)

        return jsonify({"status":"success","message":"Locations Are Retrieved.","data":locationList})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})

@locationBp.get("/location/getSpecific")
def locationSpecific():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id Is Required."})

        location=Location.objects(id=id).first()

        if not location:
            return jsonify({"status":"error","message":"Location Is Empty."})
        
        data={
                "street":location.street,
                "city":location.city,
                "state":location.state,
                "country":location.country,
                "pincode":location.pincode
             }
        
        return jsonify({"status":"success","message":"Location Retrieved.","data":data})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@locationBp.post("/location/update")
def locationUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})
        

        location=request.get_json()

        if not location:
            return jsonify({"status":"error","message":"All Fields Required."})

        street=location.get("street")
        city=location.get("city")
        state=location.get("state")
        country=location.get("country")
        pincode=location.get("pincode")

        if not len(pincode)==6:
            return jsonify({"status":"error","message":"Invalid Pincode."})
    
        locationUpdate=Location.objects(id=id).first()

        if not locationUpdate:
            return jsonify({"status":"error","message":"Location Not Found."})

        locationUpdate.street=street
        locationUpdate.city=city
        locationUpdate.state=state
        locationUpdate.country=country
        locationUpdate.pincode=pincode

        locationUpdate.save()

        return jsonify({"status":"success","message":"Location Updated Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})
    
@locationBp.delete("/location/delete")
def deleteLocation():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."})
        
        location=Location.objects(id=id).first()

        if not location:
            return jsonify({"status":"error","message":"Location Not Found."})
        
        location.delete()

        return jsonify({"status":"success","message":"Location Updated Successfully."})
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"})