<?php
if(isset($_GET["userId"]) && !empty(trim($_GET["userId"]))){
	$tipo = $_GET["userId"];
	$nome = $_GET["userName"];
}else{
	$tipo = "15485441";
	$nome = "jimmy fallon";
}

function searchGraphData($id, $table="tweet", $order_by="tweet_id", $sentiment = False){
	try {
	  	$conn = new PDO('mysql:host=localhost;dbname=tweetgather', "root", "");
	    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	    if($id != 0){
	    	if($table == "tweet"){
		    	$query = $conn->query("SELECT user_followers_diff as diff, IF(tweet_datetime, DATE_FORMAT(tweet_datetime, '%d/%m'),'!/!') as date_time, tweet_polarity as polarity FROM tweet WHERE user_id=".$id." ORDER BY tweet_id");

	    		$dados = [['Date','Difference']];
	    	
	    	}else{
		    	$query = $conn->query("SELECT * FROM ".$table." WHERE user_id=".$id." ORDER BY ".$order_by);
	    		
	    		$dados = [['Count','Sentiment']];
	    	}

	    	$count = 0;
		    
		    while($row = $query->fetch(PDO::FETCH_OBJ)){
		    	if($table == "tweet" && !$sentiment)
			  		$dados[] = [$row->date_time, (int) $row->diff];

			  	else if($table == "tweet" && $sentiment)
			  		$dados[] = [$row->date_time, (float) $row->polarity];
			  	
			  	else
			  		$dados[] = [$count, (int) $row->difference];
			  	
			  	$count++;
		    }
	    }
		
	}catch(PDOException $e){
	    echo 'ERROR: ' . $e->getMessage();
	}

	return json_encode($dados);
} 

function allUsers(){
	try {
	  	$conn = new PDO('mysql:host=localhost;dbname=tweetgather', "root", "");
	    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	    $query = $conn->query("SELECT * FROM user ORDER BY user_name");
	    $dados = [];

	    while($row = $query->fetch(PDO::FETCH_OBJ))
		  	$dados[] = ["id" => $row->user_id, "nome" => $row->user_name];
		
	}catch(PDOException $e){
	    echo 'ERROR: ' . $e->getMessage();
	}

	return $dados;
}
?>

<html>
	<head>
		<title>TweetGather</title>
		<!-- Latest compiled and minified CSS -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

		<!-- Optional theme -->
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">
		<link rel="stylesheet" href="./css.css">

		<link rel="icon" type="image/png" href="favicon.png">
	</head>
	<body>
		<header>
			<div id="main-menu" class="navbar navbar-default navbar-fixed-top">
			    <div class="container-fluid">
			        <div class="navbar-menubuilder welcome">
			            <ul class="nav navbar-nav nav-center">
			            	<?php
			            	$users = allUsers();
			            	foreach ($users as $i => $user){ ?>
		            			<li class="btn_menu">
					                    <div class="button text-center">
					                    	<a href="?userId=<?php echo $user["id"];?>&userName=<?php echo $user["nome"];?>">
					                            <button type="button" class="btn btn-default">
					                            	<strong><?php echo $user["nome"];?></strong>
					                            </button>
				                            </a>
					                    </div>
					                </li>
			            	<?php } ?>
			            </ul>
			        </div>
			    </div>
			</div>
		</header>

		<main id="mainWelcome">
			<div id="container">
				<div id="curve_chart_tw" class="chart"></div>
				<div style="display: none;" id="dataGraphTw"><?php echo searchGraphData($tipo); ?></div>
				<div style="display: none;" id="graphNameTw">Oscillation of the followers increase by Tweet. Account: <?php echo $nome; ?></div>
		  	</div>

		  	<div id="container">
				<div id="curve_chart_st" class="chart"></div>
				<div style="display: none;" id="dataGraphSt"><?php echo searchGraphData($tipo, 'tweet', 'tweet_datetime', True); ?></div>
				<div style="display: none;" id="graphNameSt">Oscillation of the sentiments by Tweet. Account: <?php echo $nome; ?></div>
		  	</div>

		  	<div id="container">
				<div id="curve_chart_day" class="chart"></div>
				<div style="display: none;" id="dataGraphDay"><?php echo searchGraphData($tipo, 'user_followers_history', 'date_time'); ?></div>
				<div style="display: none;" id="graphNameDay">Oscillation of the followers increase by Day. Account: <?php echo $nome; ?></div>
		  	</div>
		  	<br/>
		</main>

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<script type="text/javascript" src="./js.js"></script>
	</body>
</html>