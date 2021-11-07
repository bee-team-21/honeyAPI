def riskColor (risk: str):
    initResponse = '🔵'
    if risk == 'low':
        initResponse = '🟢'
    elif risk == 'mid':
        initResponse = '🟡'
    elif risk == 'high':
        initResponse = '🔴'
    return initResponse 