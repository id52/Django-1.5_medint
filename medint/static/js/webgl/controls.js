function onDrag(dx, dy)
{
  var w = canvas.clientWidth;
  var h = canvas.clientHeight;

  angle[0] += dx/Math.sqrt(w*w + h*h)*5;
  angle[1] += dy/Math.sqrt(w*w + h*h)*5;
  mat4.identity(renderer.model_);
  mat4.rotateX(renderer.model_, angle[1]);
  mat4.rotateY(renderer.model_, angle[0]);
  var rotinv = mat4.create();
  mat4.inverse(renderer.model_, rotinv);
  mat4.multiplyVec3(rotinv, [1, 0, 0], right);
  vec3.normalize(right);

  mat4.translate(renderer.model_, origin);

  mat4.scale(renderer.model_, scale);

  renderer.postRedisplay();
  updateMarkers();

  viewerViewModel.camOriginX(origin[0]);
  viewerViewModel.camOriginY(origin[1]);
  viewerViewModel.camOriginZ(origin[2]);

  viewerViewModel.objAnglePan(angle[0]);
  viewerViewModel.objAngleTilt(angle[1]);
};

addDragHandler(canvassvg, onDrag);

addWheelHandler(window, function(dx, dy, evt)
{
  var WHEEL_SCALE = 1.0/300;
  var view = renderer.view_;
  eyeFromEvt = [0, 0, -1];
  vec3.scale(eyeFromEvt, -WHEEL_SCALE*dy);
  vec3.add(campos, eyeFromEvt);
  mat4.translate(view, eyeFromEvt);
  renderer.postRedisplay();
  updateMarkers();

  viewerViewModel.camDist(campos[2]);

  return false;
});

function onCamMove(x, y, z)
{
  var view = renderer.view_;
  vec3.add(campos, [-x, -y, -z]);
  mat4.translate(view, [-x, -y, -z]);
  renderer.postRedisplay();
  updateMarkers();

  viewerViewModel.camDist(campos[2]);
}

function onOriginMove(x, y, z)
{
  origin[0] += x;
  origin[1] += y;
  origin[2] += z;
  onDrag(0, 0);
}

function moveToPosition(pos, dist)
{
    if(typeof moveToPosition.animation == 'undefined')
    {
        moveToPosition.animation = 0;
    }

    var speed = 5;
    moveToPosition.animation += 1;
    window.requestAnimFrame(function(){move(pos, dist);});
    var timer = new Date()*0.001;
    var timestep = 0;
    function move(pos, dist)
    {
        var now = new Date()*0.001;
        timestep = now-timer;
        timer = new Date()*0.001;

        var diffdist = campos[2]+dist;
        var diffx = -origin[0]-pos[0]*scale[0];
        var diffy = -origin[1]-pos[1]*scale[1];
        var diffz = -origin[2]-pos[2]*scale[2];
        onOriginMove(diffx*timestep*speed, diffy*timestep*speed, diffz*timestep*speed);
        onCamMove(0, 0, diffdist*timestep*speed);
        if(Math.abs(diffx)+Math.abs(diffy)+Math.abs(diffz)+Math.abs(diffdist) > 0.1 && moveToPosition.animation == 1)
            window.requestAnimFrame(function(){move(pos, dist);});
        else
            moveToPosition.animation -= 1;
    }
}