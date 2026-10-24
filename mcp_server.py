"""MCP Server for GenPark SimHash Near-Duplicate Detector.
100% Python Standard Library.
"""

import json
import sys
from client import SimHashNearDuplicateDetector

detector = SimHashNearDuplicateDetector()

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "compute_fingerprint",
                        "description": "Compute 64-bit integer SimHash fingerprint for given text",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"text": {"type": "string"}},
                            "required": ["text"]
                        }
                    },
                    {
                        "name": "compare_texts",
                        "description": "Check if two texts are near-duplicates using Hamming distance",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "text1": {"type": "string"},
                                "text2": {"type": "string"},
                                "max_distance": {"type": "integer"}
                            },
                            "required": ["text1", "text2"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "compute_fingerprint":
            txt = args.get("text", "")
            fp = detector.compute_simhash(txt)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"fingerprint": fp, "hex": hex(fp)})}]}
            }
        elif name == "compare_texts":
            t1 = args.get("text1", "")
            t2 = args.get("text2", "")
            max_d = args.get("max_distance", 8)
            res = detector.is_near_duplicate(t1, t2, max_distance=max_d)
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
