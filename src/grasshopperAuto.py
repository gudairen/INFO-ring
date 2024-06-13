import rhino3dm
import requests
import base64
import json
import compute_rhino3d.Util


def process_grasshopper(CorX, CorY, CorZ, output_file_path, Inner, Outer, Height, NodeSize, StrutSize, KinkAngle):
    compute_rhino3d.Util.url = "http://127.0.0.1:6500/"
    compute_rhino3d.Util.authToken = ""

    post_url = compute_rhino3d.Util.url + "grasshopper"
    gh_file = open("./ring.ghx", mode="r", encoding="utf-8-sig").read()
    data_bytes = gh_file.encode("utf-8")
    encoded = base64.b64encode(data_bytes)
    decoded = encoded.decode("utf-8")

    payload = {
        "algo": decoded,
        "pointer": None,
        "values": [
            {
                "ParamName": "RH_IN:CorX",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": x  # Directly passing the numerical value
                        } for x in CorX
                    ]
                }
            },
            {
                "ParamName": "RH_IN:CorY",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": y  # Directly passing the numerical value
                        } for y in CorY
                    ]
                }
            },
            {
                "ParamName": "RH_IN:CorZ",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": z  # Directly passing the numerical value
                        } for z in CorZ
                    ]
                }
            },
            {
                "ParamName": "RH_IN:Inner",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": Inner  # Directly passing the numerical value
                        }
                    ]
                }
            },
            {
                "ParamName": "RH_IN:Outer",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": Outer  # Directly passing the numerical value
                        }
                    ]
                }
            },
            {
                "ParamName": "RH_IN:Height",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": Height  # Directly passing the numerical value
                        }
                    ]
                }
            },
            {
                "ParamName": "RH_IN:NodeSize",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": NodeSize  # Directly passing the numerical value
                        }
                    ]
                }
            },
            {
                "ParamName": "RH_IN:StrutSize",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": StrutSize  # Directly passing the numerical value
                        }
                    ]
                }
            },
            {
                "ParamName": "RH_IN:KinkAngle",
                "InnerTree": {
                    "{ 0; }": [
                        {
                            "type": "System.Double",  # Changed from System.String to System.Double
                            "data": KinkAngle  # Directly passing the numerical value
                        }
                    ]
                }
            }

        ]
    }

    response = requests.post(post_url, json=payload)
    res = response.content.decode("utf-8")
    res = json.loads(res)
    values = res["values"]
    model = rhino3dm.File3dm()
    for val in values:
        paramName = val['ParamName']
        print(paramName)
        innerTree = val['InnerTree']
        for key, innerVals in innerTree.items():
            print(key)
            for innerVal in innerVals:
                data = json.loads(innerVal['data'])
                geo = rhino3dm.CommonObject.Decode(data)
                model.Objects.Add(geo)
    model.Write(output_file_path)
