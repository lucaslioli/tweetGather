<?php

if(isset($_GET["select_account"]) && !empty(trim($_GET["select_account"]))){
    $dados = explode(';', $_GET["select_account"]);

    $userId = $dados[0];
    $userName = $dados[1];

}else if(isset($_GET["userId"]) && !empty(trim($_GET["userId"]))){
    $userId = $_GET["userId"];
    $userName = $_GET["userName"];

}else{
    $userId = "15485441";
    $userName = "jimmy fallon";
}

include_once "functions.php";

?>

<html>
    <head>
        <?php
        cabecalho();
        ?>
    </head>
    <body class="users-graph">
        <header>
            <div class="container">
                <div class="row">
                    <div class="col-md-8">
                        <h1>Análise Individual das Contas</h1>
                    </div>
                    <div class="col-md-4 text-right">
                        <a href="./general.php" class="btn btn-dark btn-lg" role="button">Análise Geral dos Dados</a>
                    </div>
                </div>

                <form action="index.php" method="GET">
                    <div id="main-menu" class="navbar navbar-fixed-top">
                        <div class="input-group mb-3">
                            <div class="input-group-prepend">
                                <label class="input-group-text" for="select_account">Account:</label>
                            </div>
                            <select class="custom-select" id="select_account" name="select_account" onchange="this.form.submit()">
                                <?php
                                $users = allUsers();
                                foreach ($users as $i => $user){ ?>
                                    <option value="<?php echo $user["id"];?>;<?php echo $user["nome"];?>" <?php if($user["id"] == $userId) echo "selected"; ?>>
                                        <?php echo $user["nome"];?>
                                    </option>
                                <?php } ?>
                            </select>
                        </div>
                    </div>
                </form>
            </div>
        </header>

        <div class="container">
            <ul class="nav nav-tabs" id="myTab" role="tablist">
                <li class="nav-item">
                    <a class="nav-link active" id="home-tab" data-toggle="tab" href="#home" role="tab" aria-controls="home" aria-selected="true">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" id="byDay-tab" data-toggle="tab" href="#byDay" role="tab" aria-controls="byDay" aria-selected="false">Increasing By Date</a>
                </li>
            </ul>
        </div>
        
        <div class="tab-content">
            <div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
                <div id="container">
                    <div id="curve_chart_st" class="chart"></div>
                    <div style="display: none;" id="dataGraphSt"><?php echo searchGraphData($userId, 'tweet', 'tweet_datetime', true); ?></div>
                    <div style="display: none;" id="graphNameSt">Oscillation of the sentiments by Tweet. Account: <?php echo $userName; ?></div>
                </div>
                
                <div id="container">
                    <div id="curve_chart_rt" class="chart"></div>
                    <div style="display: none;" id="dataGraphRT"><?php echo searchGraphData($userId, 'tweet', 'date_time', false, true); ?></div>
                    <div style="display: none;" id="graphNameRT">Oscillation of the Retweets and Likes by Tweet. Account: <?php echo $userName; ?></div>
                </div>
            </div>
            
            <div class="tab-pane fade active" id="byDay" role="tabpanel" aria-labelledby="byDay-tab">
                <div id="container">
                    <div id="curve_chart_tw" class="chart"></div>
                    <div style="display: none;" id="dataGraphTw"><?php echo searchGraphData($userId); ?></div>
                    <div style="display: none;" id="graphNameTw">Oscillation of the followers increase by Tweet. Account: <?php echo $userName; ?></div>
                </div>

                <div id="container">
                    <div id="curve_chart_day" class="chart"></div>
                    <div style="display: none;" id="dataGraphDay"><?php echo searchGraphData($userId, 'user_followers_history', 'date_time'); ?></div>
                    <div style="display: none;" id="graphNameDay">Oscillation of the followers increase by Day. Account: <?php echo $userName; ?></div>
                </div>
            </div>
        </div>

        <br/>

        <?php 
        rodape();
        ?>

    </body>
</html>