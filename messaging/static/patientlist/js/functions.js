/*function menuRoll(ptarget){
    $(ptarget).on('rollover',function(e){
        $(this).children().
    }
}*/
var oldView = "option-grid";
var _w = $(window).width();
$('li#option-list').on('mouseover',function(e){

    $(this).children().css('background-position','0 -12px');
});


$('li#option-grid').on('mouseover',function(e){
    $(this).children().css('background-position','0 -26px');
});

$('.list-options-view li').on('mouseout',function(e){
    $(this).children().css('background-position','0 0px');
});

$('.list-options-view li').on('click',function(e){

    var sel = $(this).attr("id");
     $("li#"+oldView).removeClass('active');
    $("li#"+sel).addClass('active');
	if(sel=="option-grid"){
		$('.list-thumbs').removeClass('hidden');
		$('.list-line').addClass('hidden');
	}
	if(sel=="option-list"){
		$('.list-line').removeClass('hidden');
		$('.list-thumbs').addClass('hidden');
	}
    oldView = sel;
    return false;
});

$('.list-line li,.list-thumbs li').on('click',function(e){

    $('.listViewer').addClass('hidden');
    $('.patientViewer').removeClass('hidden');
    $('.mainMenu #btn-patients').removeClass('active');
    $('.list-options-view').addClass('hidden');
    $('.patient-menu').removeClass('hidden');

});
$('.mainMenu #btn-patients,#menuIcons #icon-mi-patient').on('click',function(e){
    $('.list-options-view').removeClass('hidden');
    $('.patient-menu').addClass('hidden');
    $('.listViewer').removeClass('hidden');
    $('.patientViewer').addClass('hidden');
    $(this).addClass('active');

});



function position(){
   if(_w<800){
    $('.list-thumbs li').width('50%');
       $('.list-thumbs li').css('min-width','none');
    }
    if(_w>=800 && _w<1000){
    $('.list-thumbs li').width('33%');
    }
    if(_w>=1000 && _w<=1450){
    $('.list-thumbs li').width('25%');
    }
    if(_w>1450){
    $('.list-thumbs li').width('20%');
    }
}
position();

$(window).resize(function(e){{_w = $(window).width();position()}});


$('.back-list').on('click',function(e){
    $('.patientViewer').addClass('hidden');
    /*$('.patientViewer').css('position','fixed');
    $('.patientViewer').css('-webkit-transition','left 0.5s');
    $('.patientViewer').css('left','-100%');*/
    $('.listViewer').removeClass('hidden');

});

/*** FUNCTION CIRCLE EVOLUTION FOR INTAKE FORM
 *
 */
var timer;
var timerEnd;
var timerLaps;

function drawCircle(id,percent){
    $('.intake-evo').html('<div class="percent"></div>');
    var deg = 360/10*percent;
    $('.pie').css({'-moz-transform':'rotate('+deg+'deg)','-webkit-transform':'rotate('+deg+'deg)','-o-transform':'rotate('+deg+'deg)','transform':'rotate('+deg+'deg)'});
    percent = Math.floor(percent*100)/100;
    arr=percent.toString().split('.');int=arr[0];
    $('#intake_evo .percent').html('<span class="int">'+int+'</span>');
}
function stopNode(id,note){
    var seconds = (timerEnd-(new Date().getTime()))/1000;
    var percent = 10-((seconds/timerLaps)*10);
    percent=Math.floor(percent*100)/100;
    if(percent<=note){drawTimer(id,percent);}
}

$(document).ready(function(){
    var _l = $(window).width();
    var _h  = $(window).height();
    var gH= $('#generalViewer').height()-50;
    $('.patientViewer').height(gH);
    timerLaps =3;
    var basedim;
    //timerEnd = new Date().getTime()+(timerLaps*1000);
    var note='';
    $('.intake-evo').each(function(id){
//        timer=setInterval(stopNote('+id+', '+note+')',0);
    });

    var  pgw = Math.round(_l-$('.patient-static-grid').width() -40);
    var widgetfixedh = 105;
    $(".patients-grid").width(pgw);
	if(_l<1200){basedim = 200}
    else{basedim = Math.round(pgw*0.23);}
	var grid=$(".patients-grid ul").gridster({
        widget_margins: [10, 10],
        widget_base_dimensions: [basedim, widgetfixedh]
});
    var gridster = $(".patients-grid ul").gridster().data('gridster');
    /*$('.patients-grid li.not-draggable').on('mousedown',function(e){
            e.stopPropagation();
    });*/
    function createSlider(){
        $("li.imaging.multipage .slides").slidesjs({
        width:280,height:250,
          pagination: {active: false,effect: "fade"},
          navigation: {active: true,effect: "fade"}
        });
    }
    setTimeout(createSlider,500);


    $(window).resize(function(e){
        _l = $(window).width();
        pgw = Math.round(_l-$('.patient-static-grid').width() -40);
        gH= $('#generalViewer').height()-20;
        $(".patients-grid").width(pgw);
        $('.patientViewer').height(gH);


		if(_l>1200){
            basedim = Math.round(pgw*0.23);
		    gridster.resize_widget_dimensions({widget_base_dimensions: [basedim,  widgetfixedh]});
        }
    });

});
