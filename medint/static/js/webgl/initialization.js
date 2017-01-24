'use strict';

var canvas = id('canvas');
var canvassvg = id('canvassvg');
preventSelection(canvassvg);
preventSelection(canvas);

var renderer = new Renderer(canvas);
var camera = new Camera();
var camera2 = new Camera();
camera2.scissorTest = true;
camera2.scissor = [100, 100, 200, 200];
camera2.visible = false;
renderer.addCamera(camera);
renderer.addCamera(camera2);
var gl = renderer.gl_;
//alert(id('SIMPLE_VERTEX_SHADER').textContent);
var shader_base = new Program(gl, [vertexShader(gl, id('VS_BASE').text),
                                     fragmentShader(gl, id('FS_BASE').text)]);
var shader_xray = new Program(gl, [vertexShader(gl, id('VS_XRAY').text),
                                     fragmentShader(gl, id('FS_XRAY').text)]);
var shader_xray2 = new Program(gl, [vertexShader(gl, id('VS_XRAY2').text),
                                     fragmentShader(gl, id('FS_XRAY2').text)]);
var shader_xray3 = new Program(gl, [vertexShader(gl, id('VS_XRAY3').text),
                                     fragmentShader(gl, id('FS_XRAY3').text)]);
renderer.program_ = shader_base;
renderer.program_.use();
renderer.program_.enableVertexAttribArrays(DEFAULT_VERTEX_FORMAT);

var angle = [0, 0, 0];
var campos = [0, 0, -3];
var origin = [0, 0, 0];
var scale = [1, 1, 1];
var right = [1, 0, 0];

var restoreorigin = [0, 0, 0];
var restoredist = 3;

mat4.translate(renderer.view_, campos);

var contentpath = "";
setRendermode(0);

function setRendermode(mode)
{
  gl.clearColor(0.0, 0.0, 0.0, 0.0);
  camera.hiddenLayers = [];
  camera2.visible = false;
  if(mode == 0) //solid and transparent
  {
    camera.depthTest = true;
    camera.depthMask = true;
    camera.blending = true;
    camera.blendParams = [gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA];
    camera.shader = shader_base;
    renderer.dynamicdepthtest = 0;

/*    gl.enable(gl.DEPTH_TEST);
    gl.depthMask(true);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    renderer.dynamicdepthtest = 0;

    renderer.program_ = shader_base;
    renderer.program_.use();
    renderer.program_.enableVertexAttribArrays(DEFAULT_VERTEX_FORMAT);*/
  }
  else if(mode == 1)  //xray
  {
    camera.depthTest = false;
    camera.depthMask = false;
    camera.blending = true;
    camera.blendParams = [gl.ONE, gl.ONE];
    camera.shader = shader_xray;
    renderer.dynamicdepthtest = 0;

/*    gl.disable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE);
    renderer.dynamicdepthtest = 0;

    renderer.program_ = shader_xray;
    renderer.program_.use();
    renderer.program_.enableVertexAttribArrays(DEFAULT_VERTEX_FORMAT);*/
  }
  else if(mode == 2)  //xray2
  {
    camera.depthTest = false;
    camera.depthMask = false;
    camera.blending = true;
    camera.blendParams = [gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA];
    camera.shader = shader_xray2;
    renderer.dynamicdepthtest = 0;

/*    gl.disable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    renderer.dynamicdepthtest = 0;

    renderer.program_ = shader_xray2;
    renderer.program_.use();
    renderer.program_.enableVertexAttribArrays(DEFAULT_VERTEX_FORMAT);*/
  }
  else if(mode == 3)  //xray3
  {
    camera.depthTest = false;
    camera.depthMask = false;
    camera.blending = true;
    camera.blendParams = [gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA];
    camera.shader = shader_xray3;
    renderer.dynamicdepthtest = 0;
    gl.clearColor(1.0, 1.0, 1.0, 1.0);

/*    gl.disable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.clearColor(1.0, 1.0, 1.0, 1.0);
    renderer.dynamicdepthtest = 0;

    renderer.program_ = shader_xray3;
    renderer.program_.use();
    renderer.program_.enableVertexAttribArrays(DEFAULT_VERTEX_FORMAT);*/
  }
  else if(mode == 4)
  {
    camera.hiddenLayers = ["skeleton", "muscles", "lymphatic", "respiratory", "digestive"];
    camera2.visible = true;
    camera.visible = true;

    camera.depthTest = true;
    camera.depthMask = true;
    camera.blending = false;
    camera.shader = shader_base;

    camera2.depthTest = false;
    camera2.depthMask = false;
    camera2.blending = true;
    camera2.blendParams = [gl.ONE, gl.ONE];
    camera2.shader = shader_xray;

    renderer.dynamicdepthtest = 0;
  }

  renderer.postRedisplay();
}

var setGroupAlpha = function(name, alpha)
{
    renderer.setGroupAlpha(name, alpha);
    renderer.postRedisplay();
}

function texturesFromMaterial(gl, material, callback) {
  try {
    var url = MATERIALS[material].map_Kd;  // throw-y.
    if (url === undefined) {
      throw url;
    }
    var url2 = MATERIALS[material].map_Normal;  // throw-y.
    if (url2) {
      return [textureFromUrl(gl, contentpath+url, callback), textureFromUrl(gl, contentpath+url2, callback)];
    }
    return [textureFromUrl(gl, contentpath+url, callback)];
  } catch (e) {
    var color;
    try {
      color = new Uint8Array(MATERIALS[material].Kd);
    } catch (e) {
      color = new Uint8Array([255, 255, 255]);
    }
    var texture = textureFromArray(gl, 1, 1, color);
    callback(gl, texture);
    return [texture];
  }
}

function onLoad(attribArray, indexArray, bboxen, meshEntry) {
    var texture = texturesFromMaterial(gl, meshEntry.material, function(){renderer.postRedisplay();} );
    var mesh = new Mesh(gl, attribArray, indexArray, DEFAULT_VERTEX_FORMAT,
                        texture, meshEntry.names, meshEntry.lengths, bboxen);

    mesh.group = meshEntry.additionalParams.group;
    mesh.color = meshEntry.additionalParams.color;
    mesh.layer = meshEntry.additionalParams.layer;
    mesh.material = meshEntry.additionalParams.material;
    renderer.meshes_.push(mesh);

    for(var i = 0; i < viewerViewModel.objLayer().length; i++)
    {
      if(viewerViewModel.objLayer()[i].group == mesh.group)
      {
        viewerViewModel.objLayer()[i].alpha(mesh.color[3]);
      }
    }

    renderer.sortByLayer();
    renderer.postRedisplay();
    updateMarkers();
}

function loadScene(file)
{
  getJsonRequest(file,
    function(loaded)
    {
      contentpath = loaded.path;
      restoreorigin[0] = origin[0] = -loaded.origin[0];
      restoreorigin[1] = origin[1] = -loaded.origin[1];
      restoreorigin[2] = origin[2] = -loaded.origin[2];
      angle[0] = loaded.angle[0];
      angle[1] = loaded.angle[1];
      campos[2] = loaded.camdist;
      restoredist = -campos[2];

      viewerViewModel.camOriginX(origin[0]);
      viewerViewModel.camOriginY(origin[1]);
      viewerViewModel.camOriginZ(origin[2]);
      viewerViewModel.objAnglePan(angle[0]);
      viewerViewModel.objAngleTilt(angle[1]);
      viewerViewModel.camDist(campos[2]);

      setRendermode(loaded.rendermode);

      for(var i = 0; i < loaded.markers.length; i++)
      {
        addMarker(loaded.markers[i].pos, loaded.markers[i].name);
      }

      scale = loaded.scale;
      for(var prop in loaded.scene)
      {
        if (!loaded.scene.hasOwnProperty(prop))
        {
          continue;
        }
        
        for(var part in loaded.scene[prop])
        {
          var additionalParams =
          {
              group: prop,
              color: loaded.scene[prop][part].color,
              layer: loaded.scene[prop][part].layer,
              material: loaded.scene[prop][part].material
          }
          downloadModelJson(contentpath+loaded.scene[prop][part].file, additionalParams, onLoad);
        }
      }

      mat4.translate(renderer.model_, origin);
      mat4.scale(renderer.model_, scale);
      mat4.identity(renderer.view_);
      mat4.translate(renderer.view_, campos);

      onDrag(0, 0);
  });
}

function destroyScene()
{
  var numMeshes = renderer.meshes_.length;
  for (var i = 0; i < numMeshes; i++)
  {
      renderer.meshes_[i].free();
  }

  renderer.meshes_ = [];
  destroyMarkers();
  loadBar.clearAll();
}
