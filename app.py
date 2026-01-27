from flask import Flask,request
app=Flask(__name__)
@app.route('/extract',methods=["POST"])
def extract():
    try:
        data=request.get_json()
        if data is None:
            return {"error":"Request body is missing or empty."},400
        missing_data=[]
        if "document" not in data:
            missing_data.append("document")
        if "schema" not in data:
            missing_data.append("schema")
        if missing_data:
            return {"error":f"Missing required fields:{','.join(missing_data)}"},400
        if not isinstance(data["document"], str) or not data["document"].strip():
            return {"error": "'document' must be a non-empty string."}, 400
        if not isinstance(data["schema"], dict) or not data["schema"]:
            return {"error": "'schema' must be a non-empty JSON object."}, 400

    except Exception as e:
        return {"error": "Internal server error during validation."}, 500
    else:
        return data,200
if __name__=="__main__":
    app.run(debug=True)