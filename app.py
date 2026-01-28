from flask import Flask,request
import re
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
        if not isinstance(data["document"], dict) or not data["document"]:
            return {"error": "'document' must be a non-empty string."}, 400
        if not isinstance(data["schema"], dict) or not data["schema"]:
            return {"error": "'schema' must be a non-empty JSON object."}, 400

    except Exception as e:
        return {"error": "Internal server error during validation."}, 500
    else:
        return data,200
    
def pre_process(data):
    for key,value in data["document"].items():
        if isinstance(value,str):
            changed=value.strip()
            regexed=re.sub(r'\s+',' ',changed)
            unwanted=['$','₹','€',',']
            wanted=regexed
            for i in unwanted:
                if i in wanted:
                    wanted=wanted.replace(i,'')
            data["document"][key]=wanted
            
            if re.search([1-9],value):
                data["document"][key]=float(value)
    return data

if __name__=="__main__":
    app.run(debug=True)