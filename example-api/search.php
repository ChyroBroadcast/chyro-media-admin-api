#!/usr/bin/php
<?php
/*
*	Chyro API Model	
*	<support@chyro.tv>
* 	Install PHP curl 
*		http://php.net/manual/en/book.curl.php
*/


/*
	0 - Setup
*/

// Credential
$url = 'HOST'; // Host, like preprod.mycompany.chyro.fr (without http://)
$login = 'LOGIN'; // Login with API read/write
$passwd = 'PASS'; // Password


/* 
	1 - Authentificate
*/
$cookie = tempnam ("/tmp", "CURLCOOKIE");
$ch = curl_init("http://".$url."/api/auth/gettoken/format/json?user=".$login."&password=".$passwd);
curl_setopt ($ch, CURLOPT_COOKIEJAR, $cookie);
curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
$output = curl_exec ($ch);
print $output.PHP_EOL;

/* 
	2 - Query	
*/
$ch = curl_init("http://".$url."/api/search/program/format/json?query={title=test}&token=".$output);
curl_setopt ($ch, CURLOPT_COOKIEFILE, $cookie);
curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
$output = curl_exec ($ch);
print $output.PHP_EOL;

?>
