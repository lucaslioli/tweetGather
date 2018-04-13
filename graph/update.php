<?php

include_once "functions.php";

try {
    $conn = new PDO('mysql:host=localhost;dbname=tweetgather', "root", "");
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $query = $conn->query("SELECT * from tweet as t1 where t1.tweet_RT = 0 and t1.tweet_language = 'en'");

    while($row = $query->fetch(PDO::FETCH_OBJ)){
        $texto = utf8_decode($row->tweet_text);

        echo "<b>".$row->tweet_id."</b><br/>";

        if($row->tweet_url){
            echo $texto."<br/>";

            $regex = "@(https?://([-\w\.]+[-\w])+(:\d+)?(/([\w/_\.#-]*(\?\S+)?[^\.\s])?)?)@";
            $texto = preg_replace($regex, ' ', $texto);

        }

        $texto = sanitizeString(strtolower($texto));
        
        echo $texto."<br/>";

        $palavras = explode(" ", $texto);

        $banalidade  = [100 => 0, 1000 => 0, 3000 => 0];

        $counter = count($palavras);
        
        foreach ($palavras as $key => $palavra) {
            if(strpos($palavra, '@') === FALSE && strpos($palavra, '#') === FALSE && !in_array($palavra, $stopwords)){
                if(in_array($palavra, $commonwords[100]))
                    $banalidade[100] ++;

                if(in_array($palavra, $commonwords[1000]))
                    $banalidade[1000] ++;

                if(in_array($palavra, $commonwords[3000]))
                    $banalidade[3000] ++;
            }else{
                unset($palavras[$key]);
                $counter--;
            }
        }

        // highlight_string(var_export($palavras, true));

        if($banalidade[100] != 0)
            $banalidade[100] = $banalidade[100]/$counter;

        if($banalidade[1000] != 0)
            $banalidade[1000] = $banalidade[1000]/$counter;

        if($banalidade[3000] != 0)
            $banalidade[3000] = $banalidade[3000]/$counter;

        echo "Banalidade: ".$banalidade[100]." | ".$banalidade[1000]." | ".$banalidade[3000]."<br/>";

        try {
            $update = $conn->prepare('UPDATE tweet SET 
                tweet_text_after = :tweet_text_after, 
                tweet_ban_100    = :tweet_ban_100,
                tweet_ban_1000   = :tweet_ban_1000,
                tweet_ban_3000   = :tweet_ban_3000
                WHERE tweet_id = :tweet_id');
            
            $update->execute(array(
                ':tweet_text_after' => $texto,
                ':tweet_ban_100'    => $banalidade[100],
                ':tweet_ban_1000'   => $banalidade[1000],
                ':tweet_ban_3000'   => $banalidade[3000],
                ':tweet_id'         => $row->tweet_id
            ));
            
            echo "<b>UPDATE OK</b><hr/>";

        } catch (PDOException $e) {
            echo '</b>ERROR: </b>' . $e->getMessage()."<hr/>";
        }

    }
    
}catch(PDOException $e){
    echo 'ERROR: ' . $e->getMessage();
}

?>