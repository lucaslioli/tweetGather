google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChartByTweet);
google.charts.setOnLoadCallback(drawChartByDay);
google.charts.setOnLoadCallback(drawChartBySentiment);

function drawChartByTweet() {
	var data = google.visualization.arrayToDataTable($.parseJSON($("#dataGraphTw").html()));

	var options = {
		title: $("#graphNameTw").html(),
		curveType: 'function',
		legend: { position: 'bottom' }
	};

	var chart = new google.visualization.AreaChart(document.getElementById('curve_chart_tw'));

	chart.draw(data, options);
}

function drawChartByDay() {
	var data = google.visualization.arrayToDataTable($.parseJSON($("#dataGraphDay").html()));

	var options = {
		title: $("#graphNameDay").html(),
		curveType: 'function',
		legend: { position: 'bottom' }
	};

	var chart = new google.visualization.AreaChart(document.getElementById('curve_chart_day'));

	chart.draw(data, options);
}

function drawChartBySentiment() {
	var data = google.visualization.arrayToDataTable($.parseJSON($("#dataGraphSt").html()));

	var options = {
		title: $("#graphNameSt").html(),
		curveType: 'function',
		legend: { position: 'bottom' },
		colors:['red','#f44242']
	};

	var chart = new google.visualization.AreaChart(document.getElementById('curve_chart_st'));

	chart.draw(data, options);
}