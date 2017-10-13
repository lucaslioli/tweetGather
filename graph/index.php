<? if(isset($_GET["userId"]) && !empty(trim($_GET["userId"]))){
	$tipo = $_GET["userId"];
	$nome = $_GET["userName"];
}else{
	$tipo = 0;
	$nome = "Everyone";
} ?>

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
			            	<? $allUsers = allUsers();
			            	foreach ($allUsers as $i => $user){ ?>
								<li class="btn_menu">
				                    <div class="button text-center">
				                    	<a href="?userId=<?= $user["id"]; ?>&userName=<?= $user["nome"]; ?>">
				                            <button type="button" class="btn btn-default">
				                            	<strong><?= $user["nome"]?></strong>
				                            </button>
			                            </a>
				                    </div>
				                </li>
			            	<? } ?>
			            	<li class="btn_menu">
			                    <div class="button text-center">
			                    	<a href="?userId=0&userName=InterestingCase">
			                            <button type="button" class="btn btn-primary">
			                            	<strong>Alex Jones X jimmy fallon</strong>
			                            </button>
		                            </a>
			                    </div>
			                </li>
			            </ul>
			        </div>
			    </div>
			</div>
		</header>
		<main id="mainWelcome" class="footer-align">
			<div id="container">
				<div id="curve_chart"></div>
				<div style="display: none;" id="dataGraph"><?= searchGraphData($tipo); ?></div>
				<div style="display: none;" id="graphName">Oscillation of the followers increase. Account: <?= $nome; ?></div>
		  	</div>
		</main>

		<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
		<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>

		<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
		<script type="text/javascript" src="./js.js"></script>
	</body>
</html>

<? 
function searchGraphData($id){
	try {
	  	$conn = new PDO('mysql:host=localhost;dbname=tweetgather', "root", "");
	    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

	    if($id != 0){
	    	$query = $conn->query("SELECT * FROM user_followers_history WHERE user_id=".$id." ORDER BY datetime");
	    	$dados = [['Count','Difference']];
	    	$count = 0;
		    while($row = $query->fetch(PDO::FETCH_OBJ)){
			  	$dados[] = [$count, (int) $row->difference];
			  	$count++;
		    }
	    }else{
	    	$query = $conn->query("SELECT datetime,
									    (SELECT h1.difference
									     FROM user_followers_history h1
									     WHERE h1.datetime = h.datetime
									         AND user_id = 109065990) AS alex_diff,

									    (SELECT h2.difference
									     FROM user_followers_history h2
									     WHERE h2.datetime = h.datetime
									         AND user_id = 15485441) AS jimmy_diff
									         
									FROM user_followers_history h
									WHERE user_id in (109065990, 15485441)
									GROUP BY datetime
									ORDER BY datetime;");
    		$dados = [['Count','Alex Jones', 'jimmy fallon']];
		    $count = 0;
		    while($row = $query->fetch(PDO::FETCH_OBJ)){
			  	$dados[] = [$count, (int) $row->alex_diff, (int) $row->jimmy_diff];
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