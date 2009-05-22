<?php
/*
  This is an example of how a local.php coul look like.
  Simply copy the options you want to change from dokuwiki.php
  to this file and change them
 */


$conf['start']       = 'Inicio';
$conf['title']          = 'Junta Municipal de Asunci&oacute;n <br> &nbsp;&nbsp;&nbsp;&nbsp;<small>Asunci&oacute;n y sus Calles</small>';
$conf['lang']           = 'es';
$conf['savedir']        = '/home/agimenez/Desktop/jmawiki/dokuwiki/data/';
$conf['recent']         = 0;
$conf['breadcrumbs']    = 0;
$conf['youarehere']     = 1;
$conf['dformat']        = '%d/%m/%Y %H:%M';
$conf['useacl']         = 1;
$conf['disableactions'] = 'register,backlinks,index,recent,revisions,subscribe,subscribens,source';
$conf['updatecheck']    = 0;
$conf['send404']        = true;
$conf['template']    = 'jma';
$conf['userewrite']  = 0;
$conf['htmlok']      = 1;

/* The following options are usefull, if you use a MySQL
 * database as autentication backend. Have a look into
 * mysql.conf.php too and adjust the options to match
 * your database installation.
 */
//$conf['authtype']   = 'mysql';
//require_once ("mysql.conf.php");
$conf['defaultgroup']= 'cms';
$conf['passcrypt']   = 'ssha';
$conf['superuser']   = 'admin';    //The admin can be user or @group or comma separated list user1,@group1,user2
$conf['manager']     = '@manager';    //The manager can be user or @group or comma separated list user1,@group1,user2
