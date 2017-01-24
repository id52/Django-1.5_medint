function addMarker(pos, name)
{
    if(typeof addMarker.markers == 'undefined')
    {
        //contains markers as addMarker.markers[name] = [pos, svgshape]
        addMarker.markers = {};
    }

    viewerViewModel.markers.push(name)

    var shape = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    shape.setAttribute("name", name);
    shape.setAttribute("cx", 25);
    shape.setAttribute("cy", 25);
    shape.setAttribute("r",  10);
    shape.setAttribute("stroke-width", 3);
    shape.setAttribute("stroke", "darkred");
    shape.setAttribute("fill", "red");
    shape.setAttribute("fill-opacity", 0);
    shape.setAttribute("data-bind", "click: selectionClicked, event: {mouseover: selectionOver, mouseout: selectionOff}");
    var svg = document.getElementsByTagName("svg")[0];
    svg.appendChild(shape);
    addMarker.markers[name] = [pos, shape];
    ko.applyBindings(viewerViewModel, shape);
}

function destroyMarkers()
{
    var svg = document.getElementsByTagName("svg")[0];
    for(var i in addMarker.markers)
    {
        var circle = addMarker.markers[i][1];
        svg.removeChild(circle);
    }
    addMarker.markers = {};
    viewerViewModel.markers.removeAll();
}

function updateMarkers()
{
    var transinf = mat4.create();
    mat4.multiply(renderer.view_, renderer.model_, transinf);
    mat4.multiply(renderer.proj_, transinf, transinf);

    var result = vec4.create();
    for(var i in addMarker.markers)
    {
        mat4.multiplyVec4(transinf, addMarker.markers[i][0], result);
        var circle = addMarker.markers[i][1];
        if(result[2] > 0)
        {
            circle.setAttribute("cx", ((result[0]/result[3]+1)*0.5)*canvas.clientWidth);
            circle.setAttribute("cy", (1-(result[1]/result[3]+1)*0.5)*canvas.clientHeight);
        }
        else
        {
            circle.setAttribute("cx", -canvas.clientWidth);
            circle.setAttribute("cy", -canvas.clientHeight);
        }
    }
}

function setMarkersInactive()
{
    for(var i in addMarker.markers)
    {
        var circle = addMarker.markers[i][1];
        circle.setAttribute("fill-opacity", 0);
        document.getElementsByName(i)[1].setAttribute("style", "width: 175px; color: black;");
    }
}
