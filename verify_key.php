<?php
	
    $key=['CLE A METTRE'];
    $user_key=htmlspecialchars($_GET["key"]);

    if($key==$user_key){
        echo '1';
    }
    else{
        echo '0';
    }
    
?>