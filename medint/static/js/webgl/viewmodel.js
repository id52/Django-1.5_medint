document.addEventListener('keydown', function(event)
{
    if(event.keyCode == 49) { //1
        hideBorders();
        setRendermode(0);
    }
    else if(event.keyCode == 50) { //2
        hideBorders();
        setRendermode(1);
    }
    else if(event.keyCode == 51) { //3
        hideBorders();
        setRendermode(2);
    }
    else if(event.keyCode == 52) { //4
        hideBorders();
        setRendermode(3);
    }
    else if(event.keyCode == 53) { //5
        updateBorders();
        setRendermode(4);
    }
    else if(event.keyCode == 37) { //left
        viewerViewModel.camMoveLeft();
    }
    else if(event.keyCode == 39) { //right
        viewerViewModel.camMoveRight();
    }
    else if(event.keyCode == 38) { //up
        viewerViewModel.camMoveUp();
    }
    else if(event.keyCode == 40) { //down
        viewerViewModel.camMoveDown();
    }

    if(camera2.visible == true)
    {
        if(event.keyCode == 87){ //w
            camera2.scissor[1] += 25;
            updateBorders();
            renderer.postRedisplay();
        }
        else if(event.keyCode == 65){ //a
            camera2.scissor[0] -= 25;
            updateBorders();
            renderer.postRedisplay();
        }
        else if(event.keyCode == 83){ //s
            camera2.scissor[1] -= 25;
            updateBorders();
            renderer.postRedisplay();
        }
        else if(event.keyCode == 68){ //d
            camera2.scissor[0] += 25;
            updateBorders();
            renderer.postRedisplay();
        }
    }
});

var viewerViewModel =
{
    objLayer: ko.observableArray(
    [
        {name: "Skin", group: "skin", alpha: ko.observable(1.0)},
        {name: "Muscles", group: "muscles", alpha: ko.observable(1.0)},
        {name: "Skeleton", group: "skeleton", alpha: ko.observable(1.0)},
        {name: "Breast Milk Lobules", group: "breasts_milk", alpha: ko.observable(1.0)},
        {name: "Breast Fatty Tissues", group: "breasts_fatty", alpha: ko.observable(1.0)},
        {name: "Respiratory System", group: "respiratory", alpha: ko.observable(1.0)},
        {name: "Digestive System", group: "digestive", alpha: ko.observable(1.0)},
        {name: "Lymphatic System", group: "lymphatic", alpha: ko.observable(1.0)},
        {name: "Urinary System", group: "urinary", alpha: ko.observable(1.0)},
        {name: "Nervous System", group: "nervous", alpha: ko.observable(1.0)},
        {name: "Circulatory System", group: "circulatory", alpha: ko.observable(1.0)}
    ]),

    markers: ko.observableArray([]),

    camMoveIn: function(){onCamMove(0, 0, -1);},
    camMoveOut: function(){onCamMove(0, 0, 1);},
    camMoveUp: function(){onOriginMove(0, -0.5, 0);},
    camMoveDown: function(){onOriginMove(0, 0.5, 0);},
    camMoveLeft: function(){onOriginMove(right[0]*0.5, 0, right[2]*0.5); },
    camMoveRight: function(){onOriginMove(-right[0]*0.5, 0, -right[2]*0.5);},

    selectionClicked: function(data, event)
                        {
                            if(document.getElementsByName(event.target.getAttribute("name"))[0].getAttribute("fill-opacity") == 1)
                            {
                                setMarkersInactive();
                                var pos = [0, 0, 0];
                                var temp = [0, 0, 0];
                                temp[0] = -1/scale[0];
                                temp[1] = -1/scale[1];
                                temp[2] = -1/scale[2];
                                vec3.multiply(restoreorigin, temp, pos);
                                moveToPosition(pos, restoredist);
                            }
                            else
                            {
                                setMarkersInactive();
                                document.getElementsByName(event.target.getAttribute("name"))[0].setAttribute("fill-opacity", 1);
                                document.getElementsByName(event.target.getAttribute("name"))[1].setAttribute("style", "width: 175px; color: red;");
                                moveToPosition(addMarker.markers[event.target.getAttribute("name")][0], 1.75);
                            }
                        },
    selectionOver: function(data, event){event.target.setAttribute("stroke", "red");},
    selectionOff: function(data, event){event.target.setAttribute("stroke", "darkred");},

    setOrigin: function(){vec3.set(origin, restoreorigin); restoredist = -campos[2];},
    switchModel: function(){if(this.loadbar_visible() == false) toggleModel();},

    camDist: ko.observable(-3.0),
    camOriginX: ko.observable(0.0),
    camOriginY: ko.observable(0.0),
    camOriginZ: ko.observable(0.0),
    objAnglePan: ko.observable(0.0),
    objAngleTilt: ko.observable(0.0),
    currFps: ko.observable(60),

    xray_left: ko.observable(-20.0),
    xray_right: ko.observable(-20.0),
    xray_top: ko.observable(-20.0),
    xray_bottom: ko.observable(-20.0),

    loadbar_visible: ko.observable(true),
    loadbar_width: ko.observable(0.0),
    loadbar_text: ko.observable("0%")
};

for(var i = 0; i < viewerViewModel.objLayer().length; i++)
{
    viewerViewModel.objLayer()[i].alpha.subscribe(function(newValue){setGroupAlpha(this.group, newValue);}, viewerViewModel.objLayer()[i]);
}
ko.applyBindings(viewerViewModel);