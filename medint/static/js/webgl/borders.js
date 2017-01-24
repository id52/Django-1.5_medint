function hideBorders()
{
    viewerViewModel.xray_left(-100);
    viewerViewModel.xray_right(-100);
    viewerViewModel.xray_top(-100);
    viewerViewModel.xray_bottom(-100);
}

function updateBorders()
{
    var svg = document.getElementsByTagName("svg")[0];
    var height = canvas.clientHeight;//svg.getAttribute("height");
    viewerViewModel.xray_left(camera2.scissor[0]);
    viewerViewModel.xray_right(camera2.scissor[0]+camera2.scissor[2]);
    viewerViewModel.xray_top(height-camera2.scissor[1]);
    viewerViewModel.xray_bottom(height-camera2.scissor[1]-camera2.scissor[3]);
}