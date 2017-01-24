'use strict';

function Renderer(canvas)
{
  var self = this;
  this.canvas_ = canvas;

  var gl = createContextFromCanvas(canvas);
  this.gl_ = gl;

  // Camera.
  this.zNear_ = Math.sqrt(3);
  this.model_ = mat4.identity(mat4.create());
  this.view_ = mat4.identity(mat4.create());
  this.proj_ = mat4.create();
  this.mvp_ = mat4.create();

  // Meshes.
  this.meshes_ = [];

  this.cameras = [];
  this.devicePixelRatio = window.devicePixelRatio || 1;

  this.dynamicdepthtest = 0;

  // Resize.
  this.maxWidth = 20480;
  this.maxHeight = 20480;
  this.scaleX = 1.0;
  this.scaleY = 1.0;
  window.addEventListener('resize', this.postRedisplay.bind(this));

  // WebGL
  gl.clearColor(0, 0, 0, 0);
  gl.enable(gl.CULL_FACE);
  gl.enable(gl.DEPTH_TEST);
  gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);

  this.then = new Date()*0.001;
  this.timeSinceLastFrame = 0;
}

Renderer.prototype.addCamera = function(cam)
{
  this.cameras.push(cam);
}


Renderer.prototype.setViewport_ = function()
{
  var canvas = this.canvas_;
//  alert(devicePixelRatio);

  var newWidth = Math.round(this.scaleX * canvas.clientWidth*this.devicePixelRatio);
  var newHeight = Math.round(this.scaleY * canvas.clientHeight*this.devicePixelRatio);

  newWidth = clamp(newWidth, 1, this.maxWidth);
  newHeight = clamp(newHeight, 1, this.maxHeight);

  if (canvas.width !== newWidth || canvas.height !== newHeight) {
    canvas.width = newWidth;
    canvas.height = newHeight;

    this.gl_.viewport(0, 0, newWidth, newHeight);
  }
}

Renderer.prototype.setGroupAlpha = function(name, alpha)
{
  var numMeshes = this.meshes_.length;
  for (var i = 0; i < numMeshes; i++)
  {
    if(this.meshes_[i].group == name)
      this.meshes_[i].color[3] = alpha;
  }
}

Renderer.prototype.sortByLayer = function()
{
  this.meshes_.sort(function(a, b){return a.layer-b.layer});
}

Renderer.prototype.drawAll_ = function()
{
  for(var n = 0; n < this.cameras.length; n++)
  {
    var cam = this.cameras[n];
    if(cam.visible == false)
      continue;

    if(cam.scissorTest == true)
    {
      gl.enable(gl.SCISSOR_TEST);
      gl.scissor(cam.scissor[0]*this.devicePixelRatio, cam.scissor[1]*this.devicePixelRatio, cam.scissor[2]*this.devicePixelRatio, cam.scissor[3]*this.devicePixelRatio);
    }
    else
    {
      gl.disable(gl.SCISSOR_TEST);
    }

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT | gl.STENCIL_BUFFER_BIT);

    if(cam.depthTest == true)
      gl.enable(gl.DEPTH_TEST);
    else
      gl.disable(gl.DEPTH_TEST);

    gl.depthMask(cam.depthMask);

    if(cam.blending == true)
    {
      gl.enable(gl.BLEND);
      gl.blendFunc(cam.blendParams[0], cam.blendParams[1]);
    }
    else
      gl.disable(gl.BLEND);

    if(cam.shader != 0)
    {
      renderer.program_ = cam.shader;
      renderer.program_.use();
      renderer.program_.enableVertexAttribArrays(DEFAULT_VERTEX_FORMAT);
    }

    var numMeshes = this.meshes_.length;
    if(this.dynamicdepthtest == 0)
    {
      for (var i = 0; i < numMeshes; i++)
      {
        var hidden = false;
        for(var s = 0; s < cam.hiddenLayers.length; s++)
        {
          if(cam.hiddenLayers[s] == this.meshes_[i].group)
            hidden = true;
        }
        if(this.meshes_[i].color[3] > 0 && hidden == false)
        {
          gl.uniformMatrix4fv(this.program_.set_uniform.u_mvp, false, this.mvp_);
          gl.uniformMatrix3fv(this.program_.set_uniform.u_model, false, 
                      mat4.toMat3(this.model_));

          gl.uniform4f(renderer.program_.set_uniform.u_color, this.meshes_[i].color[0],
            this.meshes_[i].color[1], this.meshes_[i].color[2], this.meshes_[i].color[3]);
          gl.uniform2f(renderer.program_.set_uniform.u_material, this.meshes_[i].material[0],
            this.meshes_[i].material[1]);
          this.meshes_[i].bindAndDraw(this.program_);
        }
      }
    }
    else
    {
      for (var i = 0; i < numMeshes; i++)
      {
        var hidden = false;
        for(var s = 0; s < cam.hiddenLayers.length; s++)
        {
          if(cam.hiddenLayers[s] == this.meshes_[i].group)
            hidden = true;
        }
        if(this.meshes_[i].color[3] > 0 && hidden == false)
        {
          if(this.meshes_[i].color[3] >= 1.0)
          {
  //          gl.enable(gl.DEPTH_TEST);
            gl.depthMask(true);
          }
          else
          {
  //          gl.disable(gl.DEPTH_TEST);
            gl.depthMask(false);
          }

          gl.uniformMatrix4fv(this.program_.set_uniform.u_mvp, false, this.mvp_);
          gl.uniformMatrix3fv(this.program_.set_uniform.u_model, false, 
                      mat4.toMat3(this.model_));

          gl.uniform4f(renderer.program_.set_uniform.u_color, this.meshes_[i].color[0],
            this.meshes_[i].color[1], this.meshes_[i].color[2], this.meshes_[i].color[3]);
          gl.uniform2f(renderer.program_.set_uniform.u_material, this.meshes_[i].material[0],
            this.meshes_[i].material[1]);
          this.meshes_[i].bindAndDraw(this.program_);
        }
      }
    }
    renderer.program_.disableVertexAttribArrays(DEFAULT_VERTEX_FORMAT);
  }
};

Renderer.prototype.draw_ = function()
{
  var now = new Date()*0.001;
  this.timeSinceLastFrame = now-this.then;
  this.then = now;
  if(typeof(window.viewerViewModel) === "undefined")
  {
    window.viewerViewModel.currFps((1.0/this.timeSinceLastFrame).toFixed(0));
  }

  var gl = this.gl_;
  var canvas = this.canvas_;

  var fudge = .01;  // TODO: tighter z-fitting.
  var aspectRatio = fudge*canvas.clientWidth/canvas.clientHeight;
  mat4.frustum(-aspectRatio, aspectRatio, -fudge, fudge,
               fudge*this.zNear_, 100, this.proj_);
  mat4.multiply(this.view_, this.model_, this.mvp_);
  mat4.multiply(this.proj_, this.mvp_, this.mvp_);
  
  this.drawAll_();
};

Renderer.prototype.postRedisplay = function()
{
  var self = this;
  if (!this.frameStart_) {
    this.frameStart_ = Date.now();
    window.requestAnimFrame(function() { 
      self.setViewport_();
      self.draw_();
      self.frameStart_ = 0;
    }, this.canvas_);
  }
};
