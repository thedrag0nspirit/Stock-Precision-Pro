from flask import Flask, render_template, request, jsonify
import time

app = Flask(__name__)

# Sample stock data for demonstration
stock_data = {
    "energy": {
        "low": [
            {"symbol": "ONGC.BO", "description": "Oil & Natural Gas Corporation."},
            {"symbol": "NTPC.BO", "description": "NTPC Limited - India's largest energy conglomerate."}
        ],
        "medium": [
            {"symbol": "RELIANCE.BO", "description": "Reliance Industries."},
            {"symbol": "POWERGRID.BO", "description": "Power Grid Corporation of India."}
        ], 
        "high": [
            {"symbol": "BPCL.BO", "description": "Bharat Petroleum Corporation."},
            {"symbol": "ADANIGREEN.BO", "description": "Adani Green Energy Limited."}
        ]
    },
    "technology": {
        "low": [
            {"symbol": "INFY.BO", "description": "Infosys Limited."},
            {"symbol": "HCLTECH.BO", "description": "HCL Technologies."}
        ],
        "medium": [
            {"symbol": "TCS.BO", "description": "Tata Consultancy Services."},
            {"symbol": "TECHM.BO", "description": "Tech Mahindra Limited."}
        ],
        "high": [
            {"symbol": "WIPRO.BO", "description": "Wipro Limited."},
            {"symbol": "LTIM.BO", "description": "LTI Mindtree."}
        ]
    },
    "healthcare": {
        "low": [
            {"symbol": "CIPLA.BO", "description": "Cipla Limited."},
            {"symbol": "AUROBINDO.BO", "description": "Aurobindo Pharma."}
        ],
        "medium": [
            {"symbol": "SUNPHARMA.BO", "description": "Sun Pharmaceuticals."},
            {"symbol": "DRREDDY.BO", "description": "Dr. Reddy's Laboratories."}
        ],
        "high": [
            {"symbol": "APOLLOHOSP.BO", "description": "Apollo Hospitals."},
            {"symbol": "FORTIS.BO", "description": "Fortis Healthcare Limited."}
        ]
    },
    "finance": {   
        "low": [
            {"symbol": "HDFCBANK.BO", "description": "HDFC Bank Limited."},
            {"symbol": "AXISBANK.BO", "description": "Axis Bank Limited."}
        ],
        "medium": [
            {"symbol": "ICICIBANK.BO", "description": "ICICI Bank Limited."},
            {"symbol": "BAJFINANCE.BO", "description": "Bajaj Finance Limited."}
        ], 
        "high": [
            {"symbol": "SBI.BO", "description": "State Bank of India."},
            {"symbol": "KOTAKBANK.BO", "description": "Kotak Mahindra Bank Limited."}
        ]
    },
    "automobile": {
        "low": [
            {"symbol": "MARUTI.BO", "description": "Maruti Suzuki India Limited."},
            {"symbol": "ASHOKLEY.BO", "description": "Ashok Leyland."}
        ],
        "medium": [
            {"symbol": "TATAMOTORS.BO", "description": "Tata Motors Limited."},
            {"symbol": "M&M.BO", "description": "Mahindra & Mahindra Limited."}
        ],
        "high": [
            {"symbol": "BAJAJ-AUTO.BO", "description": "Bajaj Auto Limited."},
            {"symbol": "HEROMOTOCO.BO", "description": "Hero MotoCorp Limited."}
        ]
    },
    "real_estate": {
        "low": [
            {"symbol": "DLF.BO", "description": "DLF Limited."},
            {"symbol": "GODREJPROP.BO", "description": "Godrej Properties Limited."}
        ],
        "medium": [
            {"symbol": "PRESTIGE.BO", "description": "Prestige Estates Projects."},
            {"symbol": "OBEROIRLTY.BO", "description": "Oberoi Realty Limited."}
        ],
        "high": [
            {"symbol": "PHOENIXLTD.BO", "description": "The Phoenix Mills Limited."},
            {"symbol": "BRIGADE.BO", "description": "Brigade Enterprises Limited."}
        ]
    },
    "consumer_goods": {
        "low": [
            {"symbol": "HINDUNILVR.BO", "description": "Hindustan Unilever Limited."},
            {"symbol": "BRITANNIA.BO", "description": "Britannia Industries."}
        ],
        "medium": [
            {"symbol": "ITC.BO", "description": "ITC Limited."},
            {"symbol": "DABUR.BO", "description": "Dabur India Limited."}
        ],
        "high": [
            {"symbol": "COLPAL.BO", "description": "Colgate-Palmolive (India)."},
            {"symbol": "TITAN.BO", "description": "Titan Company Limited."}
        ]
    },	
	"utilities": {
        "low": [
            {"symbol": "NHPC.BO", "description": "NHPC Limited."},
            {"symbol": "COALINDIA.BO", "description": "Coal India Limited."}
        ],
        "medium": [
            {"symbol": "GAIL.BO", "description": "GAIL (India) Limited."},
            {"symbol": "POWERGRID.BO", "description": "Power Grid Corporation."}
        ],
        "high": [
            {"symbol": "IOCL.BO", "description": "Indian Oil Corporation."},
            {"symbol": "ADANIGAS.BO", "description": "Adani Total Gas Limited."}
        ]
    },
    "telecommunication": {
        "low": [
            {"symbol": "BHARTIARTL.BO", "description": "Bharti Airtel."},
            {"symbol": "MTNL.BO", "description": "Mahanagar Telephone Nigam."}
        ],
        "medium": [
            {"symbol": "VODAFONEIDEA.BO", "description": "Vodafone Idea Limited."},
            {"symbol": "TATACOMM.BO", "description": "Tata Communications Limited."}
        ],
        "high": [
            {"symbol": "RELIANCEJIO.BO", "description": "Reliance Jio Infocomm."},
            {"symbol": "HFCL.BO", "description": "Himachal Futuristic Communications."}
        ]
    },
    "media": {
        "low": [
            {"symbol": "ZEEL.BO", "description": "Zee Entertainment Enterprises."},
            {"symbol": "TV18.BO", "description": "TV18 Broadcast Limited."}
        ],
        "medium": [
            {"symbol": "SUNTV.BO", "description": "Sun TV Network."},
            {"symbol": "NETWORK18.BO", "description": "Network18 Media & Investments."}
        ],
        "high": [
            {"symbol": "PVR.BO", "description": "PVR Limited."},
            {"symbol": "INOXLEISUR.BO", "description": "INOX Leisure Limited."}
        ]
    },
    "metals": {
        "low": [
            {"symbol": "NMDC.BO", "description": "NMDC Limited."},
            {"symbol": "SAIL.BO", "description": "Steel Authority of India."}
        ],
        "medium": [
            {"symbol": "TATASTEEL.BO", "description": "Tata Steel Limited."},
            {"symbol": "JSWSTEEL.BO", "description": "JSW Steel Limited."}
        ],
        "high": [
            {"symbol": "HINDALCO.BO", "description": "Hindalco Industries."},
            {"symbol": "VEDL.BO", "description": "Vedanta Limited."}
        ]
    }
}


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        sector = request.form.get('sector')
        risk = request.form.get('risk')

        # Simulate processing delay
        time.sleep(2)

        if sector and risk and sector in stock_data and risk in stock_data[sector]:
            recommendations = stock_data[sector][risk]
            return jsonify(recommendations)
        return jsonify({"error": "Invalid input. Please try again."})

    return render_template('details.html')

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)

