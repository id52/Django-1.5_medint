function LoadBar(steps)
{
	this.stepsize = 1/steps;
	this.steps = steps;
	this.currsteps = 0;
}

LoadBar.prototype.addSteps = function(steps)
{
	this.steps += steps;
	this.stepsize = 1/this.steps;
}

LoadBar.prototype.clearAll = function()
{
	this.steps = 0;
	this.stepsize = 0;
	this.currsteps = 0;
}

LoadBar.prototype.update = function(steps)
{
	this.currsteps += steps;
	viewerViewModel.loadbar_width((this.currsteps*this.stepsize*80.0).toFixed(1)+"%");
	viewerViewModel.loadbar_text((this.currsteps*this.stepsize*80.0).toFixed(0)+"%");
	if(this.currsteps >= this.steps)
	{
		viewerViewModel.loadbar_visible(false);
	}
	else
	{
		viewerViewModel.loadbar_visible(true);
	}
}

LoadBar.prototype.setMessage = function(msg)
{

}

var loadBar = new LoadBar(0);

/*
function LoadBar()
{
	this.steps = 0;
	this.substeps = 0;
	this.currsteps = 0;
}

LoadBar.prototype.addSteps = function(steps)
{
	this.steps += steps;
}

LoadBar.prototype.addSubSteps = function(steps)
{
	this.substeps += steps;
}

LoadBar.prototype.update = function(steps)
{
	this.substeps -= 1;
	if(this.substeps <= 0)
	{
		this.currsteps += steps;
		if(this.currsteps >= this.steps)
		{
			alert("finished loading");
		}
	}
}

LoadBar.prototype.setMessage = function(msg)
{

}

var loadBar = new LoadBar(0);
*/