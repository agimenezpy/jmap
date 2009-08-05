var wgtDetalle;
var wgtBuscador;
var results = 'nada';

function create_widgets() {
    wgtDetalle = new YAHOO.widget.Panel("detalle",
                                       { width:"600px",
                                       height: "400px",
                                       fixedcenter:true,
                                       close:true,
                                       draggable:false,
                                       zindex:4,
                                       modal:true,
                                       visible:false
                                       }
                );
    wgtDetalle.setHeader("Informaci&oacute;n Contextual");
    wgtDetalle.setBody("No Info");
    wgtDetalle.render();
    
    wgtBuscador = new YAHOO.widget.Panel("buscador",
                                       { width:"600px",
                                       height: "400px",
                                       fixedcenter:true,
                                       close:true,
                                       draggable:false,
                                       zindex:4,
                                       modal:true,
                                       visible:false
                                       }
                );
    wgtBuscador.setHeader("Buscador");
    wgtBuscador.setBody("No Info");
    wgtBuscador.render();
}

function mostrar_buscador(tipo) {
    if (tipo == "lugares") {
        titulo = "Buscar lugares";
        wiki_id = "forms:buscar_lugar";
    }
    else if (tipo == "espacios") {
        titulo = "Buscar Espacios P&uacute;blicos";
        wiki_id = "forms:buscar_espacio";
    }
    else if (tipo == "limites") {
        titulo = "Buscar L&iacute;mites Pol&iacute;ticos";
        wiki_id = "forms:buscar_limite";
    }
    else if (tipo == "calles") {
        titulo = "Buscar Calles";
        wiki_id = "forms:buscar_calle";
    }
    
    if (results != tipo) {
        wgtBuscador.setHeader(titulo);
        wgtBuscador.setBody('Cargando Formulario <img src="/media/images/busybar.gif" alt="Busybar"/>')
        
        var obj = new Ajax.Request('doku.php',
                {method:'get',
                asynchronous:true,
                parameters:{'id': wiki_id, 'do':'export_xhtmlbody'},
                onFailure:function(request){
                    wgtBuscador.setBody('Ha ocurrido un error inesperado')
                },
                onSuccess: function(request){
                    wgtBuscador.setBody(request.responseText);
                  }
                });
        results = "";
    }
    wgtBuscador.show();
}

function buscar_lugar(form) {
    var obj = new Ajax.Request('lugar.xhr',
            {method:'post',
            asynchronous:true,
            evalScripts:true,
            encoding: 'ISO-8859-1',
            onComplete:function(request){$('progreso').hide(); results = 'lugares' },
            onLoading:function(request){$('lugar_search_results').hide();$('progreso').show();},
            parameters:Form.serialize(form)});
  return false;
}

function buscar_espacio(form) {
    var obj = new Ajax.Request('espacio.xhr',
            {method:'post',
            asynchronous:true,
            evalScripts:true,
            encoding: 'ISO-8859-1',
            onComplete:function(request){$('progreso').hide(); results = 'espacios'},
            onLoading:function(request){$('espacio_search_results').hide();$('progreso').show();},
            parameters:Form.serialize(form)});
  return false;
}

function buscar_limite(form) {
    var obj = new Ajax.Request('limite.xhr',
            {method:'post',
            asynchronous:true,
            evalScripts:true,
            encoding: 'ISO-8859-1',
            onComplete:function(request){$('progreso').hide(); results = 'limites'},
            onLoading:function(request){$('limites_search_results').hide();$('progreso').show();},
            parameters:Form.serialize(form)});
  return false;
}

function buscar_calle(form) {
    var obj = new Ajax.Request('via.xhr',
            {method:'post',
            asynchronous:true,
            evalScripts:true,
            encoding: 'ISO-8859-1',
            onComplete:function(request){$('progreso').hide(); results = 'calles'},
            onLoading:function(request){$('calle_search_results').hide();$('progreso').show();},
            parameters:Form.serialize(form)});
  return false;
}