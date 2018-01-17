<?php
if(isset($_GET["userId"]) && !empty(trim($_GET["userId"]))){
	$tipo = $_GET["userId"];
	$nome = $_GET["userName"];
}else{
	$tipo = 0;
	$nome = "Everyone";
}

function searchGraphData($id){
	try {
	  	$conn = new PDO('mysql:host=localhost;dbname=tweetgather', "root", "");
	    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	    if($id != 0){
	    	$query = $conn->query("SELECT * FROM tweet WHERE user_id=".$id." ORDER BY tweet_datetime");
	    	$dados = [['Count','Difference']];
	    	$count = 0;
		    while($row = $query->fetch(PDO::FETCH_OBJ)){
			  	$dados[] = [$count, (int) $row->user_followers_diff];
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
		<main id="mainWelcome" class="footer-align">
			<div id="container">
				<div id="curve_chart"></div>
				<div style="display: none;" id="dataGraph"><?php echo searchGraphData($tipo); ?></div>
				<div style="display: none;" id="graphName">Oscillation of the followers increase. Account: <?php echo $nome; ?></div>
		  	</div>
		</main>

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<script type="text/javascript" src="./js.js"></script>
	</body>
</html>