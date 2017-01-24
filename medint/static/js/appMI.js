// JavaScript Document
var patientPanelH;
var _width;
var _height;
var dataPatient= [];
var datasPatient= [];
var dataDoctor= [];
var datasDoctor= [];
var closedPatPanel = false;
var json = false;
var i=0;
var wait = false;
var patientH;
var closedTL=false;
var iconT;
var iconL;
var originW;
var catMenu="";
var oldcatMenu="";


/** PATIENT PANEL FUNCTIONS ***/
function collapsePatientDashboard(){
	$('#patientDashboard').animate({left:'-255px'},300);
	closedPatPanel = true;
	updateModule();
}

function expandPatientDashboard(){
	$('#patientDashboard').animate({left:0},300);
	closedPatPanel = false;
	updateModule();
}

/** TIMELINE FUNCTIONS **/
function collapseTimeline(){
	$('#timeline').animate({bottom:'-195px'},300);
	closedTL = true;
}
 
function expandTimeline(){
	$('#timeline').animate({bottom:0},300);
	closedTL = false;
}



function callLegalDocs(){
		catMenu = "legals";
		$('.mainMenu').fadeIn();
		$('.mainMenu a#btn-'+oldcatMenu).removeClass('active');
		$('.mainMenu a#btn-'+catMenu).addClass('active');
		$("#generalViewer").empty();
		$.ajax({
			/*url:"/static/include/login.html",*/
			url:"legal_documents.html",
			success:function(data){
				$('#generalViewer').hide();
				$('#generalViewer').html(data);
				$('#generalViewer').fadeIn();
				
			}
			});
		oldcatMenu = catMenu;
		return false;
	
}



function updateModule(){
	/*if(closedPatPanel==true){
		$('#timeline,#menu').animate({left:'45px'},300);
		$('#timeline,#timeline .vco-container.vco-main,#menu').css('width',_width-45);
	}
	else{
		//$('#timeline,#menu').animate({left:'301px'},300);
		$('#timeline,#menu').animate({left:0},300);
		$('#timeline,#timeline .vco-container.vco-main,#menu').css('width',_width-300);
	}*/
	if(closedTL==true){
		$('#timeline').css('bottom','-195px');
	}
	else $('#timeline').css('bottom',0);
}


/*** CREATE AND UPDATE SCROLLER FOR PATIENT MODULE ON PATIENT DASHBOARD **/
function createScroll(){
	/*$('#patientModules').each(function() {

			$(this).jScrollPane({autoReinitialise: true}).data('jsp').getContentPane();

		});*/
    /*$('.panel-column2 .message-list,.panel-column3 .message-text').each(function(){
        $(this).jScrollPane({autoReinitialise: true}).data('jsp').getContentPane();

	});*/

    /*$('.panel-column3 #msglist').each(function(){
        $(this).jScrollPane({autoReinitialise: true}).data('jsp').getContentPane();

    });*/
}

/*** DATA CALLED WITH KNOCKOUT.JS ***/
/*function TaskDoctor(data){
	
	for(var value in data){
		
		datasDoctor.push(data[value]);
		
	}
	
	
}

function TaskPatient(data){
	
	for(var value in data){
		
		datasPatient.push(data[value]);
		
	}
	
}

function DataView(){
	var self = this;
    self.tasks = ko.observableArray([]);
	self.tasksP = ko.observableArray([]);
	$.getJSON('/static/js/json/doctor.json', function(allData)
	{
		var mappedTasks = $.map(allData, function(item) { return new TaskDoctor(item.datas) });
        self.tasks(mappedTasks);
		
	});
	
	$.getJSON('/static/js/json/patient.json', function(allData)
	{
		var mappedTasks = $.map(allData, function(item) { return new TaskPatient(item.datas) });
        self.tasksP(mappedTasks);
		
	});
	var compt =tasksP();
	
}


function DataModel(){
	
	
	
	this.firstName = dataDoctor[0];
	this.lastName = dataDoctor[1];
	
	
	this.patientDatas = {firstName:dataPatient[0],lastName:dataPatient[1],age:dataPatient[2],sex:dataPatient[3],weight:dataPatient[4],ethnicity:dataPatient[5],vitals:dataPatient[6]};
	
}*/


function vitalsCount(){
	if( parseInt($('.vitalsCounter').html())<dataPatient[6]){ $('.vitalsCounter').html(parseInt($('.vitalsCounter').html())+i); setTimeout('vitalsCount()',40)}
	if( parseInt($('.vitalsCounter').html())==dataPatient[6]) displayVitalsIcons()
	//else $('.vitalsCounter').html()) = dataPatient[6];
	i=+1;

}

function displayVitalsIcons(){
	$('#lungs').fadeIn(400),function(){$('#hearth').fadeIn(400);};
	$('#o2').delay(800).fadeIn(400);
}


/*** MENU DOCTOR DROPDOWN ***/


/*ko.bindingHandlers.accordion = {
    init: function(element, valueAccessor) {
        var options = valueAccessor() || {};
        setTimeout(function() {
            $(element).accordion(options);
        }, 0);
        
        //handle disposal (if KO removes by the template binding)
          ko.utils.domNodeDisposal.addDisposeCallback(element, function(){
              $(element).accordion("destroy");
          });
    },
    update: function(element, valueAccessor) {
        var options = valueAccessor() || {};
        $(element).accordion("destroy").accordion(options);
    }
}*/

/*function Item(id, name) {
    this.id = ko.observable(id);
    this.name = ko.observable(name);
}*/

function appearIcons(){
	$('#menuIcons img').each(function(){
		$(this).css('opacity',0);
		//originW=$(this).height();
		$(this).css('height','120%');
		//$(this).css('width','120%');
		$(this).delay(700).animate({opacity:1,height:'100%'},500);
		
	});
	}

/**/




$(document).ready(function(e) {
	
	
    _width = $(window).width();
	_height = $(window).height();
	var headerH = $('#header').height();
	
	//$('#generalViewer').css('height',_height-53);
	$('#patientDashboard').css('left','-305px');
	$('#timeline').css('bottom','-300px');
	$('#humanBody,#menu').hide();
	$('#lungs,#hearth,#o2').hide();
	$('#content').css('overflow','hidden');
	$('#menu').css('width',_width-301);
	$('#menuIcons img').css('opacity',0);
//	$('.mainMenu').hide();

    var h2=$('.panel-column1').height()-300;
    $('.composer textarea').css('height',h2);
	
	
	
	appearIcons();


	//initMessages('#message');
	
	
	/*function pageModel (){
            var self = this;
            self.currentSection = 'main';

            function openSection(section){
                /*if($('#main-nav').is(':visible')){
                    $('#main-nav').fadeOut(
                        function(){
                            $('#main-header, #'+section).fadeIn();
                        }
                    );
                } else {*/
                  /* if (section !== self.currentSection){
                        $('.ui-panel').fadeOut(500);
						$('#' + section).fadeIn();
						if(section=="main" || section==""){appearIcons();}
						//$('.ui-panel').fadeOut(function(){$('#' + section).fadeIn();});
                    }
                //}
                self.currentSection = section;
            }

            Sammy(function() {
                this.get('#:part', function() {
                    openSection(this.params.part)
                    console.log(this.params.part);
                });
            }).run();
        }
		
        ko.applyBindings(new pageModel(), $('#main-nav')[0]);*/
	
	
	/*$('.iconsimg').on('click',function(event){
		$('#menuIcons img').each(function(){
			$(this).delay(200).animate({height:'120%',opacity:0},300,function(){$('.iconLists').animate({opacity:0},300);$('#menuIcons').hide();$('.mainMenu').fadeIn();});
		});
		
	});*/
	
	
	
	
	/*$('.doctortpl #btn-MI').on('click',function(event){
		setTimeout(callMenuIcon,1500);
	});
	
	$('.patienttpl #btn-MI').on('click',function(event){
		setTimeout(callPatientMenuIcon,1500);
	});
	
	$('.stafftpl #btn-MI').on('click',function(event){
		setTimeout(callStaffMenuIcon,1500);
	});*/
	
	
	/*$.getJSON('http://preview.sub-tract.com/ojingo/mi/app/json/doctor.json', function(data)
	{
	$.each(data.doctor.datas, function(key, val) { dataDoctor.push(val); });
	});*/
	
	/*$.getJSON('http://preview.sub-tract.com/ojingo/mi/app/json/patient.json', function(data)
	{
	$.each(data.patient.datas, function(key, val) { dataPatient.push(val); });
	json = true;
	
	
		  
	});*/
	//DataModel();
	/*DataView();
	ko.applyBindings(new DataModel());*/
	
	//setTimeout(vitalsCount,1300);
	//ko.applyBindings(new DataModel());
	//ko.applyBindings(new PatientDataModel());
	
	$('#patientDashboard').delay(800).animate({left:0},300);
	$('#humanBody').delay(1100).fadeIn(400);
	$('#menu').delay(1500).fadeIn(400);
	$('#timeline').delay(1600).animate({bottom:0},300);
	createScroll()
	
	function position(){
		iconT = Math.round((_height-$('#menuIcons').height())/2);
		//iconL = Math.round((_width-$('#menuIcons').width())/2);
		
		patientH = _height-$('#header').height()-$('#patientInfo').height()-48;
		$('#patientDashboard,#content,#rightPanel').css('min-height',patientPanelH);
		//$('#generalViewer,#content').css('height',_height-53);
        $('#content').css('height',_height-53);
		$('#patientModules').css('height',patientH);
		$('#timeline,#menu').css('width',_width-300);
		//$('#menuIcons').css('top',iconT);
		//$('#menuIcons').css('left',iconL);
		
		
	}
	
	
	position();
	

	
	$('#btexpandPanel').hide();
	
	/*$('#btexpandPanel').live('click',function(){
		if(closedPatPanel== false){collapsePatientDashboard();$(this).removeClass();$(this).addClass('expanded');}
		else {expandPatientDashboard();$(this).removeClass();$(this).addClass('collapsed');}
		
	});*/
	
	$('#btexpandTimeline').on('click',function(){
		if(closedTL== false){collapseTimeline();$(this).removeClass();$(this).addClass('expanded-vertical');}
		else {expandTimeline();$(this).removeClass();$(this).addClass('collapsed-vertical');}
		
	});
	
	
	$(window).resize(function(e){
		 _width = $(window).width();
		 _height = $(window).height();
		 
		 position();
		 //updateModule();
		 
		 if(wait !== false)

			clearTimeout(wait);

			wait = setTimeout(createScroll, 500);
		
	});
	
	
});

