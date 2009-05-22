<?php
/**
 * Map Action Plugin:   Map Component.
 * 
 * @author     Alberto G. <albergimenez@gmail.com>
 */
 
if(!defined('DOKU_INC')) die();
if(!defined('DOKU_PLUGIN')) define('DOKU_PLUGIN',DOKU_INC.'lib/plugins/');
require_once(DOKU_PLUGIN.'action.php');
 
class action_plugin_mapas_maps extends DokuWiki_Action_Plugin {
 
  /**
   * return some info
   */
  function getInfo(){
    return array(
		 'author' => 'Alberto G.',
		 'email'  => 'albergimenez@gmail.com',
		 'date'   => '2009-05-13',
		 'name'   => 'Maps (action plugin component)',
		 'desc'   => 'Maps action functions.',
		 'url'    => 'http://www.guiadigital.com.py',
		 );
  }
 
  /**
   * Register its handlers with the DokuWiki's event controller
   */
  function register(&$controller) {
    $controller->register_hook('TPL_METAHEADER_OUTPUT', 'BEFORE',  $this, '_hookjs');
  }
 
  /**
   * Hook js script into page headers.
   *
   * @author Alberto G. <albergimenez@gmail.com>
   */
  function _hookjs(&$event, $param) {
    global $conf;
    global $ID;
    $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => DOKU_BASE."media/scripts/prototype.js"
            );
    $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => DOKU_BASE."media/scripts/effects.js"
            );
    if ($ID == "mapa:gmap") {
        $apikey = $this->getConf('gmapapikey');
        $event->data["script"][] = array ("type" => "text/javascript",
                    "charset" => "utf-8",
                    "_data" => "",
                    "src" => "http://maps.google.com/maps?file=api&v=2.x&key=$apikey&hl=es"
                    );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => DOKU_BASE."media/scripts/googlemaps.js"
            );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => DOKU_BASE."media/scripts/dragzoom.pack.js"
            );
    }
    else if ($ID == "mapa:olay") {
        $event->data["script"][] = array ("type" => "text/javascript",
                    "charset" => "utf-8",
                    "_data" => "",
                    "src" => DOKU_BASE."media/scripts/OpenLayers.js"
                    );
        $event->data["script"][] = array ("type" => "text/javascript",
            "charset" => "utf-8",
            "_data" => "",
            "src" => DOKU_BASE."media/scripts/openlayersmap.js"
            );
    }
  }
}