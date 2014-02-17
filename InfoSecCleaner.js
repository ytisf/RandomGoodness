// ==UserScript==
// @name        InfoSec Resources Ads Removal
// @namespace   https://github.com/yisf
// @description Basic script to get rid of those ads on InfoSec
// @include     http*://resources.infosecinstitute.com/*
// @version     1
// @grant       none
// ==/UserScript==


function removeElementsByClass(className){
    elements = document.getElementsByClassName(className);
    while(elements.length > 0){
        elements[0].parentNode.removeChild(elements[0]);
    }
}

document.body.innerHTML = document.body.innerHTML.replace('<div style="margin:20px 0 25px 0;padding-left:25px;padding-right:25px;background-color:#CEECF5;font-size: medium; border:1px solid">', '<!--<div style="margin:20px 0 25px 0;padding-left:25px;padding-right:25px;background-color:#CEECF5;font-size: medium; border:1px solid">');
document.body.innerHTML = document.body.innerHTML.replace('TRAINING</a></div></center></div>', '-->');

removeElementsByClass('greensidebar');
removeElementsByClass('bluesidebar');
removeElementsByClass('reading-box');
