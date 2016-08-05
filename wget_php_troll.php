<?php

// WGet Troll

if(!empty($_SERVER['HTTP_USER_AGENT'])) {
  if (preg_match("/Wget/", $_SERVER['HTTP_USER_AGENT'])) {
    header("Location: ftp://speedtest.tele2.net/1000GB.zip", true, 302);
    exit;
  }

}
