<?php

	$file = fopen("ListAssa.html","r") or die("Unable to open file!");
	//echo fread($file,"webdictionnary.txt");
	$f=fread($file,filesize("ListAssa.html"));

	//$xml = new SimpleXMLElement($f);
	echo gettype($f);
	fclose($file);

	//echo $fich;
	//file_put_contents('rendu.xml', 't');
  //file_put_contents('exemple.txt', '**NOUVEAU TEXTE**');
?>
