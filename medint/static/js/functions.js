// JavaScript Document
var $topLoader;
var _height;
var _width;
var oldIE = $.browser.msie && $.browser.version <= 8;

   
   if(!oldIE){
   $topLoader = $("#loader").percentageLoader({
      width: 140,
      height: 140,
      onProgressUpdate : function(val) {
         $topLoader.setValue(Math.round(val * 100.0));
      }
   });
   var topLoaderRunning = false;
   }
   
   
     

function running(){
	   
	   if (topLoaderRunning) {
         return;
      }
      topLoaderRunning = true;
      $topLoader.setProgress(0);
      $topLoader.setValue('0kb');
      var kb = 0;
      var totalKb = 500;
     
      var animateFunc = function() {
         kb += 10;
         $topLoader.setProgress(kb / totalKb);
         $topLoader.setValue(kb.toString() + 'kb');
       
         if (kb < totalKb) {
            setTimeout(animateFunc, 25);
         } else {
            topLoaderRunning = false;
			removeLoader();
         }
      }
      setTimeout(animateFunc, 25);
	   
   }  
   
   function removeLoader(){
		$('#loader').animate({top:0,opacity:0});
		displayPanel();
	}
	
	function displayPanel(){
		
		$('#loginPanel').delay(500).fadeIn('slow');
		$('#menu').delay(1000).show('slow');
		
	}

$(document).ready(function(){
	_width = document.body.clientWidth;
	_height = $(document).height();
	logPanelH = $('#loginPanel').height();
	
	$('#loginPanel').hide();
	$('#menu').hide();
	$('.alert').hide();
	
	
	if(!oldIE){
		//alert('saloperie !!');	
		running();
	}
	else{displayPanel();}
	
	if(oldIE){
		$("input#username").val("User name");
		
		if($("input#username").val()=="User name"){
		$("input#username").focus(function(){
			if($(this).val()=="User name") $(this).val("");
		});
		$("input#username").blur(function(){
			if($(this).val()=="") $(this).val("User name");
		});
		}
	}
	
	
	$("input").each(function(){
			if($(this).val()=="" && $(this).attr("placeholder")!=""){
				$(this).val($(this).attr("placeholder"));
				$(this).focus(function(){
					if($(this).val()==$(this).attr("placeholder")) $(this).val("");
				});
				$(this).blur(function(){
					if($(this).val()=="") $(this).val($(this).attr("placeholder"));
				});
			}
		});
	
	
	$('#loader').css('top',((_height/2)-80));
	$('#loader').css('left',((_width/2)-80));
	$('#loginPanel').css('margin-top',((_height/2)-(logPanelH*0.5)));
	
	if(_width<900){
			$('#menu').css('left',10);	
		}
		
	else{
		$('#menu').css('left',70)
	}
	
	
	$('input#btn-login').bind('click',function(){
		
		$('#alert-error').html("Your username and password are wrong.");
		$('#alert-error').show();
		$('#alert-success').hide();
		$('#alert-error').delay(4000).fadeOut('slow');
		
	});
	
	
	
	$(window).resize(function(e) {
		_width = document.body.clientWidth;
		_height = $(document).height();
        $('#loader').css('top',((_height)/2-80));
		$('#loader').css('left',((_width)/2-80));
		$('#loginPanel').css('margin-top',((_height/2)-(logPanelH*0.5)));
		
		if(_width<900){
			$('#menu').css('left',10);	
		}
		else{
		$('#menu').css('left',70)
		}
    });
	
});