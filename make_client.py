import requests

INVOICE_WEBHOOK_URL = "https://hook.eu2.make.com/8yi2ttu12jkhndlevia6ts3bhg8ihkyk"
EXPENSE_WEBHOOK_URL = "https://hook.eu2.make.com/2jgn1ajjyl1s2jijd2jsvpfdgiqg838e"


def send_to_make(data, type="invoice"):
    try:
        if type == "invoice":
            res = requests.post(INVOICE_WEBHOOK_URL, json=data)
        elif type == "expense":
            res = requests.post(EXPENSE_WEBHOOK_URL, json=data)
        else:
            return {"success": False, "error": "Invalid type specified"}

        if res.status_code == 200:
            return {
                "success": True,
                "data": res.json() if res.headers.get("content-type") == "application/json" else res.text
            }
        else:
            return {
                "success": False,
                "error": f"Status code {res.status_code}: {res.text}"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
