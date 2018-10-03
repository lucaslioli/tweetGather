<?php

include_once "functions.php";

?>

<html>
    <head>
        <?php
        cabecalho();
        ?>
    </head>
    <body>      
        <!-- SENTIMENT & SIZE -->
        <div class="container">
            <div class="row">
                    <div class="col-md-8">
                        <h1>Análise Geral dos Dados</h1>
                    </div>
                    <div class="col-md-4 text-right">
                        <a href="./index.php" class="btn btn-dark btn-lg" role="button">Análise Individual das Contas</a>
                    </div>
                </div>
            <hr/>
            <div class="row">
                <div class="col-md-6">
                    <table class="table table-hover table-sm">
                        <thead class="thead-light">
                            <tr>
                                <th>Tweet Polarity</th>
                                <th>Sum of Retweets</th>
                                <th>Sum of Likes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php 
                            $dados_sentiment = sentimentByRetweets(25073877);
                        
                            foreach ($dados_sentiment as $key => $value) { ?>
                                <tr>
                                    <th><?php echo $value['sentiment']; ?></td>
                                    <td><?php echo $value['sum_rt']; ?></td>
                                    <td><?php echo $value['sum_likes']; ?></td>
                                </tr>
                            <?php } ?>
                        </tbody>
                    </table>
                </div>
                
                <div class="col-md-6">
                    <table class="table table-hover table-sm">
                        <thead class="thead-light">
                            <tr>
                                <th>Tweet Size</th>
                                <th>Sum of Retweets</th>
                                <th>Sum of Likes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php
                        
                            $dados_size = sizeByRetweets();
                        
                            foreach ($dados_size as $key => $value) { ?>
                                <tr>
                                    <th><?php echo $value['size']; ?></td>
                                    <td><?php echo $value['sum_rt']; ?></td>
                                    <td><?php echo $value['sum_likes']; ?></td>
                                </tr>
                            <?php } ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- URL & HASHTAG -->
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <table class="table table-hover table-sm">
                        <thead class="thead-light">
                            <tr>
                                <th>Use of URL</th>
                                <th>Sum of Retweets</th>
                                <th>Sum of Likes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php 
                            $dados = urlByRetweets(25073877);
                        
                            foreach ($dados as $key => $value) { ?>
                                <tr>
                                    <th><?php echo $value['url']; ?></td>
                                    <td><?php echo $value['sum_rt']; ?></td>
                                    <td><?php echo $value['sum_likes']; ?></td>
                                </tr>
                            <?php } ?>
                        </tbody>
                    </table>
                </div>
                
                <div class="col-md-6">
                    <table class="table table-hover table-sm">
                        <thead class="thead-light">
                            <tr>
                                <th>Use of Hashtag</th>
                                <th>Sum of Retweets</th>
                                <th>Sum of Likes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php
                        
                            $dados = hashtagByRetweets(25073877);
                        
                            foreach ($dados as $key => $value) { ?>
                                <tr>
                                    <th><?php echo $value['hashtag']; ?></td>
                                    <td><?php echo $value['sum_rt']; ?></td>
                                    <td><?php echo $value['sum_likes']; ?></td>
                                </tr>
                            <?php } ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- BANALIDADE -->
        <div class="container">
            <div class="row">
                <div class="col-md-6">
                    <table class="table table-hover table-sm">
                        <thead class="thead-light">
                            <tr>
                                <th>Banality (Dic. 100)</th>
                                <th>Sum of Retweets</th>
                                <th>Sum of Likes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php 
                            $dados = banalityByRetweets("100");
                        
                            foreach ($dados as $key => $value) { ?>
                                <tr>
                                    <th><?php echo $value['banality']; ?></td>
                                    <td><?php echo $value['sum_rt']; ?></td>
                                    <td><?php echo $value['sum_likes']; ?></td>
                                </tr>
                            <?php } ?>
                        </tbody>
                    </table>
                </div>
                
                <div class="col-md-6">
                    <table class="table table-hover table-sm">
                        <thead class="thead-light">
                            <tr>
                                <th>Banality</th>
                                <th>Sum of Retweets</th>
                                <th>Sum of Likes</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php
                        
                            $dados = banalityByRetweets("1000");
                        
                            foreach ($dados as $key => $value) { ?>
                                <tr>
                                    <th><?php echo $value['banality']; ?></td>
                                    <td><?php echo $value['sum_rt']; ?></td>
                                    <td><?php echo $value['sum_likes']; ?></td>
                                </tr>
                            <?php } ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <br/>

        <?php 
        rodape();
        ?>

    </body>
</html>