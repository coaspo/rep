const apiUrl = 'https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=02180&distance=25&API_KEY=EB95D738-3455-4362-80EE-6E992757E8ED';
fetch(apiUrl)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Create arrays to store Parameter Names and AQI values
        const parameterNames = [];
        const aqiValues = [];
        var reportingArea
        var hourObserved='--'
        // Iterate over the data and extract the ParameterName and AQI
        data.forEach(item => {
            if (item.ParameterName && item.AQI !== undefined) {
                parameterNames.push(item.ParameterName);
                aqiValues.push(item.AQI);
                reportingArea = item.ReportingArea
               // hourObserved = item.HourObserved
            }
        });
        let txt =  reportingArea
        for (let i = 0; i < parameterNames.length; i++) {
           txt += ' '+ parameterNames[i]+ ': '+ colorCoded(aqiValues[i])
        }
        html = " &nbsp; &nbsp; <a title='<50 (.054 PPM)' " + hourObserved + ':00'
         "href='https://www.airnow.gov/?city=Lynn&state=MA&country=USA'>" + txt + "</a>"
        document.getElementById("airIndex").innerHTML = html;
    })
    .catch(error => {
        const tableBody = document.querySelector('#aqTable tbody');
        tableBody.innerHTML = `<tr><td colspan="2">Error fetching data: ${error.message}</td></tr>`;
    });

function colorCoded(airIndex) {
    let backColor = '00e400'
    index = parseInt(airIndex);
    if (index > 50 && index <100) {
       backColor = 'ffff00'
    } else if (index >99) {
       backColor = 'ff0000'
    }
    html = '<span style="background-color:#'+ backColor + '">' + airIndex + '</span>'
    return html
}