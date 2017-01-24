'use strict';

function Camera()
{
  this.position = [0, 0, 0];
  this.rotation = [0, 0, 0, 0];

  this.scissor = [0, 0, 100, 100];
  this.scissorTest = false;

  this.depthTest = true;
  this.depthMask = true;

  this.shader = 0;
  this.blending = false;
  this.blendParams = [];

  this.visible = true;
  this.hiddenLayers = [];
}