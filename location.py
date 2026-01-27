from flask import Blueprint,request,jsonify
from models import Location

locationBp=Blueprint("locationBp",__name__)

@locationBp.post("/location/new")
def newLocation():
    try:
        location=request.get_json()

        if not location:
            return jsonify({"status":"error","message":"All Fields Required."}), 400

        street=location.get("street")
        city=location.get("city")
        state=location.get("state")
        country=location.get("country")
        pincode=location.get("pincode")

        if not street or not city or not state or not country or not pincode:
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400 

        if not str(pincode).isdigit() or len(str(pincode)) != 6:
            return jsonify({
                "status": "error",
                "message": "Invalid pincode. Must be 6 digits."
            }), 400
    
        locat=Location(
            street=street,
            city=city,
            state=state,
            country=country,
            pincode=pincode
        )
        locat.save()

        return jsonify({"status":"success","message":"Location Added Successfully.","data": { "id": str(locat.id) }}), 201

    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@locationBp.get("/location/getAll")
def allLocations():
    try:
        locations=Location.objects()

        if not locations:
            return jsonify({"status":"error","message":"Location Is Empty."}), 200  
   
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

        return jsonify({"status":"success","message":"Locations Are Retrieved.","data":locationList}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500

@locationBp.get("/location/getSpecific")
def locationSpecific():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id Is Required."}), 400

        location=Location.objects(id=id).first()

        if not location:
            return jsonify({"status":"error","message":"LocationNot Found."}), 404 
        
        data={
                "street":location.street,
                "city":location.city,
                "state":location.state,
                "country":location.country,
                "pincode":location.pincode
             }
        
        return jsonify({"status":"success","message":"Location Retrieved.","data":data}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@locationBp.post("/location/update")
def locationUpdate():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400
        

        location=request.get_json()

        if not location:
            return jsonify({"status":"error","message":"All Fields Required."}), 400

        street=location.get("street")
        city=location.get("city")
        state=location.get("state")
        country=location.get("country")
        pincode=location.get("pincode")

        if not street or not city or not state or not country or not pincode:
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            }), 400 

        if not str(pincode).isdigit() or len(str(pincode)) != 6:
            return jsonify({
                "status": "error",
                "message": "Invalid pincode. Must be 6 digits."
            }), 400
    
        locationUpdate=Location.objects(id=id).first()

        if not locationUpdate:
            return jsonify({"status":"error","message":"Location Not Found."}), 404

        locationUpdate.street=street
        locationUpdate.city=city
        locationUpdate.state=state
        locationUpdate.country=country
        locationUpdate.pincode=pincode

        locationUpdate.save()

        return jsonify({"status":"success","message":"Location Updated Successfully."}), 200 
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500
    
@locationBp.delete("/location/delete")
def deleteLocation():
    try:
        id = request.args.get("id")

        if not id:
            return jsonify({"status": "error", "message": "Id is required."}), 400
        
        location=Location.objects(id=id).first()

        if not location:
            return jsonify({"status":"error","message":"Location Not Found."}), 404
        
        location.delete()

        return jsonify({"status":"success","message":"Location Updated Successfully."}), 200
    
    except Exception as e:
        return jsonify({"status":"error","message":f"Error {str(e)}"}), 500