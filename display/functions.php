<?php

include_once "dictionary.php";

/**
 * Imprime conteúdo do HEAD da página, inclíndo estilos e scripts
 * @return Void
 */
function cabecalho(){
    echo '<title>TweetGather</title>';
    // Latest compiled and minified CSS
    echo '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">';
    echo '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>';

    // Optional theme;
    echo '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">';
    echo '<link rel="stylesheet" href="./assets/css.css">';

    echo '<link rel="icon" type="image/png" href="./assets/favicon.png">';
}

/**
 * Imprime conteúdo do final da página, inclíndo scripts necessários
 * @return Void
 */
function rodape(){
    echo '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>';
    echo '<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>';
    echo '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>';
    echo '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>';

    echo '<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>';
    echo '<script type="text/javascript" src="./assets/js.js"></script>';
}

/**
 * Realiza conexão com o banco de dados
 * @param  string $base  Nome da Base
 * @param  string $senha Senha
 * @return [type]        [description]
 */
function db_connect($base = 'tweetgather', $senha=""){
    try{
        $conn = new PDO('mysql:host=localhost;dbname='.$base, "root", $senha);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        return $conn;
    
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();

        return false;
    }
}

/**
 * Remove números e caractéres de pontuação para contagem de palavras
 * @param  String $string Texto com números e pontuação
 * @return String         Texto sem números e pontuação
 */
function sanitizeString($string) {
    // matriz de entrada
    $what = array('&nbsp;','&amp;','0','1','2','3','4','5','6','7','8','9','-','(',')','.',',',';',':','|','!','"','$','%','&','/','=','?','~','^','>','<','ª','º','�','…','ampm',' pm ');

    // matriz de saída
    $by   = '';

    // devolver a string
    return cleanWhiteSpaces(str_replace($what, $by, $string));
}

/**
 * Remove as stop words de uma string
 * @param  String $string Texto com as stop words
 * @return String         Texto sem as stop words
 */
function removeStopWords($string, $stopwords) {
    // matriz de entrada
    $what = $stopwords;

    // devolver a string
    return cleanWhiteSpaces(str_replace($what, ' ', $string));
}

/**
 * Limpa os espaços em branco na String
 * @param  String $string String com os espaços em branco
 * @return String         String sem os espaços em branco
 */
function cleanWhiteSpaces($string){
    while($string[strlen($string)-1] == ' ')
        $string = substr($string, 0, -1);

    // devolver a string
    return str_replace('  ', ' ', $string);
}

/**
 * Busca os dados para gerar os gráficos por usuário
 * @param  int     $id        Id do usuário
 * @param  string  $table     Tabela para busca de dados
 * @param  string  $order_by  Critério de Ordenação
 * @param  boolean $sentiment Se o sentimento está será exibido
 * @param  boolean $retweets  Se os retweets serão exibidos
 * @return JSON               Array JSON com os dados
 */
function searchGraphData($id, $table="tweet", $order_by="tweet_id", $sentiment = false, $retweets = false){
    $dados = NULL;
    
    try {
        $conn = db_connect();
        if($conn === false) return false;

        if($id != 0){
            if($table == "tweet"){
                $query = $conn->query("SELECT user_followers_diff as diff, IF(tweet_datetime, DATE_FORMAT(tweet_datetime, '%Y/%m/%d'),'!/!') as date_time, tweet_polarity as polarity, tweet_retweets as retweets, tweet_likes as likes FROM tweet WHERE user_id=".$id." ORDER BY tweet_id");

                if($sentiment)
                    $dados = [['Date','Sentiment']];
                else if ($retweets)
                    $dados = [['Date','Retweets', 'Likes']];
                else
                    $dados = [['Date','Difference']];
            
            }else if($table == "user_followers_history"){
                $query = $conn->query("SELECT t.difference, IF(date_time, DATE_FORMAT(date_time, '%Y/%m/%d'),'!/!') as date_time FROM ".$table." as t WHERE user_id=".$id." ORDER BY ".$order_by);
                
                $dados = [['Date','Difference']];
            
            }else
                return 0;

            $count = 0;
            
            while($row = $query->fetch(PDO::FETCH_OBJ)){
                if($table == "tweet" && !$sentiment && !$retweets)
                    $dados[] = [$row->date_time, (int) $row->diff];

                else if ($table == "tweet" && $retweets)
                    $dados[] = [$row->date_time, (int) $row->retweets, (int) $row->likes];

                else if($table == "tweet" && $sentiment)
                    $dados[] = [$row->date_time, (float) $row->polarity];
                
                else
                    $dados[] = [$row->date_time, (int) $row->difference];
                
                $count++;
            }
        }
        
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();
    }

    return json_encode($dados);
}

/**
 * Busca os índices de retweets e likes normalizados por sentimento
 * @param  int   $userId Id do usuário, caso seja considerado
 * @return Array         Array com os índices e sentimentos
 */
function sentimentByRetweets($userId = NULL){
    $dados = NULL;
   
    try {
        $conn = db_connect();
        if($conn === false) return false;

        $where = ($userId != NULL) ? 'where t1.user_id = '.$userId : "";

        $query = $conn->query("SELECT 
                DISTINCT FORMAT(t1.tweet_polarity, 1) as sentiment,
                format((select sum(t2.tweet_retweets) from tweet as t2 where FORMAT(t1.tweet_polarity, 1) = FORMAT(t2.tweet_polarity, 1))/count(*), 0) as sum_rt,
                format((select sum(t2.tweet_likes) from tweet as t2 where FORMAT(t1.tweet_polarity, 1) = FORMAT(t2.tweet_polarity, 1))/count(*), 0) as sum_likes    
            from tweet as t1 
            $where
            group by 1
            order by 1 desc");

        $dados = [];

        while($row = $query->fetch(PDO::FETCH_OBJ))
            $dados[] = ["sentiment" => $row->sentiment, "sum_rt" => $row->sum_rt, "sum_likes" => $row->sum_likes];
        
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();
    }

    return $dados;
}

/**
 * Busca os índices de retweets e likes normalizados por banalidade
 * @param  String $banality Corresponde ao tamanho do dicionario de palavras utilizado (100, 1000, 3000)
 * @param  int    $userId   Id do usuário, caso seja considerado
 * @return Array            Array com os índices e banalidade
 */
function banalityByRetweets($banality = "1000", $userId = NULL){
    $dados = NULL;
   
    try {
        $conn = db_connect();
        if($conn === false) return false;

        $where = ($userId != NULL) ? 'where t1.user_id = '.$userId : "";

        $query = $conn->query("SELECT 
                DISTINCT FORMAT(t1.tweet_ban_$banality, 1) as banality,
                format((select sum(t2.tweet_retweets) from tweet as t2 where FORMAT(t1.tweet_ban_$banality, 1) = FORMAT(t2.tweet_ban_$banality, 1))/count(*), 0) as sum_rt,
                format((select sum(t2.tweet_likes) from tweet as t2 where FORMAT(t1.tweet_ban_$banality, 1) = FORMAT(t2.tweet_ban_$banality, 1))/count(*), 0) as sum_likes    
            from tweet as t1 
            $where
            group by 1
            order by 1 desc");

        $dados = [];

        while($row = $query->fetch(PDO::FETCH_OBJ))
            $dados[] = ["banality" => $row->banality, "sum_rt" => $row->sum_rt, "sum_likes" => $row->sum_likes];
        
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();
    }

    return $dados;
}

/**
 * Busca os índices de retweets e likes normalizados por tamanho de mensagem
 * @param  int   $userId Id do usuário, caso seja considerado
 * @return Array         Array com os índices e tamanhos
 */
function sizeByRetweets($userId = NULL){
    $dados = NULL;
    
    try {
        $conn = db_connect();
        if($conn === false) return false;

        $where = ($userId != NULL) ? 'where t1.user_id = '.$userId : "";

        $query = $conn->query("SELECT 
                DISTINCT t1.tweet_size, concat((t1.tweet_size - 10), ' - ', t1.tweet_size) as size, 
                format((select sum(t2.tweet_retweets) from tweet as t2 where t1.tweet_size = t2.tweet_size)/count(*), 0) as sum_rt,
                format((select sum(t2.tweet_likes) from tweet as t2 where t1.tweet_size = t2.tweet_size)/count(*), 0) as sum_likes
            from tweet as t1 
            $where
            group by 1
            order by 1 desc");
        $dados = [];

        while($row = $query->fetch(PDO::FETCH_OBJ))
            $dados[] = ["size" => $row->size, "sum_rt" => $row->sum_rt, "sum_likes" => $row->sum_likes];
        
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();
    }

    return $dados;
}

/**
 * Busca os índices de retweets e likes normalizados pelo uso de URLs
 * @param  int   $userId Id do usuário, caso seja considerado
 * @return Array         Array com os índices e uso de URLs
 */
function urlByRetweets($userId = NULL){
    $dados = NULL;
    
    try {
        $conn = db_connect();
        if($conn === false) return false;

        $where = ($userId != NULL) ? 'where t1.user_id = '.$userId : "";

        $query = $conn->query("SELECT 
                DISTINCT t1.tweet_url, if(t1.tweet_url, 'With URL', 'Without URL') as url, 
                format((select sum(t2.tweet_retweets) from tweet as t2 where t1.tweet_url = t2.tweet_url)/count(*), 0) as sum_rt,
                format((select sum(t2.tweet_likes) from tweet as t2 where t1.tweet_url = t2.tweet_url)/count(*), 0) as sum_likes,
                count(t1.tweet_id) as count_tw
            from tweet as t1 
            $where
            group by 1
            order by 1 desc");
        $dados = [];

        while($row = $query->fetch(PDO::FETCH_OBJ))
            $dados[] = ["url" => $row->url, "sum_rt" => $row->sum_rt, "sum_likes" => $row->sum_likes];
        
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();
    }

    return $dados;
}

/**
 * Busca os índices de retweets e likes normalizados pelo uso de hashtags
 * @param  int   $userId Id do usuário, caso seja considerado
 * @return Array         Array com os índices e uso de hastags
 */
function hashtagByRetweets($userId = NULL){
    $dados = NULL;

    try {
        $conn = db_connect();
        if($conn === false) return false;

        $where = ($userId != NULL) ? 'where t1.user_id = '.$userId : "";

        $query = $conn->query("SELECT 
                DISTINCT t1.tweet_hashtag, if(t1.tweet_hashtag, 'With Hashtag', 'Without Hashtag') as hashtag, 
                format((select sum(t2.tweet_retweets) from tweet as t2 where t1.tweet_hashtag = t2.tweet_hashtag)/count(*), 0) as sum_rt,
                format((select sum(t2.tweet_likes) from tweet as t2 where t1.tweet_hashtag = t2.tweet_hashtag)/count(*), 0) as sum_likes
            from tweet as t1 
            $where
            group by 1
            order by 1 desc");
        $dados = [];

        while($row = $query->fetch(PDO::FETCH_OBJ))
            $dados[] = ["hashtag" => $row->hashtag, "sum_rt" => $row->sum_rt, "sum_likes" => $row->sum_likes];
        
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();
    }

    return $dados;
}

/**
 * Retorna lista de tweets em inglês que não são retweets. Pode ser geral, ou de um usuário
  * @param  int   $userId Id do usuário, caso seja considerado
  * @return Array         Array com o tweet, retweets e likes
 */
function tweetList($userId = NULL){
    $dados = NULL;

    try {
        $conn = db_connect();
        if($conn === false) return false;

        $where = ($userId != NULL) ? 'and t1.user_id = '.$userId : "";

        $query = $conn->query("SELECT * from tweet as t1 where t1.tweet_RT = 0 and t1.tweet_language = 'en' $where");
        $dados = [];

        while($row = $query->fetch(PDO::FETCH_OBJ))
            $dados[] = ["text" => $row->tweet_text, "retweets" => $row->tweet_retweets, "likes" => $row->tweet_likes];
        
    }catch(PDOException $e){
        echo 'ERROR: ' . $e->getMessage();
    }

    return $dados;
}

/**
 * Busca lista de todos os usuários autores cadastrados
 * @return Array Lista de todos os usuários com nome e ID
 */
function allUsers(){
    $dados = NULL;

    try {
        $conn = db_connect();
        if($conn === false) return false;

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