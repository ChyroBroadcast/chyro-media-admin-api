#!/usr/bin/php
<?php
/*
*       Chyro API Model
*				Copyright (c) 2015:
*						Chyro Conseil <support@chyro.tv>
*						Licensed Under MIT license
*       Install PHP curl
*               http://php.net/manual/en/book.curl.php
*/

/*
        0 - Setup
*/

// Credential
$url = 'HOST'; // Host, like preprod.mycompany.chyro.fr (without http://)
$login = 'LOGIN'; // Login with API read/write
$passwd = 'PASS'; // Password
$output_format = 'json'; // Output format : json or xml


/*
 	1 - Chyro API Class
*/
class ChyroApi {
	private $host;
	private $login;
	private $pass;
	private $cookie = false;
	private $format = 'json';

	public function __construct($host, $login, $pass, $format = 'json') {
		$this->host = $host;
		$this->login = $login;
		$this->pass = $pass;
		$this->format = $format;
	}

	public function auth() {
		$cookie = tempnam ("/tmp", "CURLCOOKIE");
		$ch = curl_init("http://".$this->host."/api/auth/gettoken/format/".$this->format."?user=".$this->login."&password=".$this->pass);
		curl_setopt ($ch, CURLOPT_COOKIEJAR, $cookie);
		curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
		$this->cookie = $cookie;
		return curl_exec ($ch);
	}

	public function search($type, $token, $query) {
		if ((!$this->cookie) || (!$token))
			return False;
		$ch = curl_init("http://".$this->host."/api/search/".$type."/format/".$this->format."?query={title=test}&token=".$token);
		curl_setopt ($ch, CURLOPT_COOKIEFILE, $this->cookie);
		curl_setopt ($ch, CURLOPT_RETURNTRANSFER, true);
		return curl_exec ($ch);
	}
}

/*
	2 - Main : example
*/
$api = new ChyroApi($url, $login, $passwd, $output_format);
$token = $api->auth();
echo $api->search('program', $token, '{title=test}');

?>
