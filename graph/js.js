google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

function drawChart() {
	var data = google.visualization.arrayToDataTable($.parseJSON($("#dataGraph").html()));

	// data = new google.visualization.DataTable();
	// data.addColumn('string', 'Topping');
	// data.addColumn('number', 'Slices');
	// data.addRows([
	//   ['Mushrooms', 3],
	//   ['Onions', 1],
	//   ['Olives', 1],
	//   ['Zucchini', 1],
	//   ['Pepperoni', 2]
	// ]);

	var options = {
		title: $("#graphName").html(),
		curveType: 'function',
		legend: { position: 'bottom' }
	};

	var chart = new google.visualization.AreaChart(document.getElementById('curve_chart'));

	chart.draw(data, options);
}