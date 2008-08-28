(function(jq){
	
 jq.fn.editable = function(options) { 	
	
	var defaults = {  
    	typex: "text",		
		url: "action_ajax.php",
		fkl: [],
		actionx: "nothing",
		id: -1,
		column: '',
		style_class: "editable",		
		width: "200px"
   };  
   
   var options = jq.extend(defaults, options);  

    return this.each(function() {
		
		var obj = jq(this);
				
		obj.addClass(options.style_class);		
		
		var text_saved = obj.html();
		var namex = this.id + "editMode";
		var items = "";		      		       
											
		obj.click(function() {
			switch (options.typex) {
			 	case "text": {
					var inputx = "<input id='" + namex + "' type='text' style='width: " + options.width/1.8 + "em' value='" + text_saved + "' /><br/>";
					var btnSend = "<input type='submit' id='btnSave" + this.id + "' value='OK' />";
					var btnCancel = "<input type='button' id='btnCancel" + this.id + "' value='Cancel' />";
					items = inputx + btnSend + btnCancel; 
					break;
				}
			 	case "select": {
			 	    var selectx = "<select id='" + namex + "' name='" + namex + "'><option value=''></option>"
                    for (i=0; i<options.fkl.length; i++) {
                        selectx = selectx+"<option value='"+options.fkl[i]+"'>"+options.fkl[i]+"</option>";
                    }
                    selectx = selectx+"</select><br/>";

					/*var inputx = "<input id='" + namex + "' type='text' style='width: " + options.width/1.8 + "em' value='" + text_saved + "' /><br/>";*/
					var btnSend = "<input type='submit' id='btnSave" + this.id + "' value='OK' />";
					var btnCancel = "<input type='button' id='btnCancel" + this.id + "' value='Cancel' />";
					items = selectx + btnSend + btnCancel; 
					break;
				}
			}  
			
		   	obj.html(items);	
		   	obj.unbind();		
			jq("#" + namex).focus().select();			
			jq("#btnSave" + this.id, obj).click(function () {
				jq.ajax({
				    type: "POST", 	
				   	data:	    		 
				   		{value: jq("#" + namex).val(),
				   		 id: options.id,
				   		 column: options.column
				   		},
		    		url: options.url,    		    		
		    		success: function(data, textStatus) {
		    			if (data > '') {
							obj.html(data);							
						} else {
							obj.html('Click to enter text');	
						}
						text_saved = data;		
				    },
					error: function(XMLHttpRequest, textStatus, errorThrown) {
						obj.html(textStatus + " - " + errorThrown);
					}
		  		});				
			})				
			
			jq("#btnCancel" + this.id, obj).click(
			    function () {
				    obj.html(text_saved);		
        			return false;
			    }
			)
				
			return false;
		});		  
    });			
 };
})(jQuery);