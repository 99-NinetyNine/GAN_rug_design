
import React, { useState,useRef, useEffect } from 'react';

const Canvas = React.forwardRef((props, ref) => {
    return <canvas ref={ref} {...props} />;
  });
  

const DrawingCanvas = () => {
  const canvasRef=useRef(null);
  const OcanvasRef=useRef(null);
    
  const itemsRef = useRef([]);
  const itemCountRef = useRef(0);
  const dragItemRef = useRef(null);

  // wallpaper specific
  const currentColorRef = useRef("#000000");
  const currentToolRef = useRef(5);
  const currentLineWidthRef = useRef(3);
  const currentLineCapRef = useRef("round");

  const clearedItemsRef = useRef(null);

  const startingRef = useRef(true);
  const colors = ["#000000", "#FF0000", "#00BB00", "#0000FF", "#00BBBB", "#DD00DD",
                  "#FFFF00", "#DDDDDD", "#999999", "#555555"];

  
  const [FREEHAND_TOOL,setFreeHandTool]=useState(5);
  const translation1 = useRef(150);
  const translation2 = useRef(150);
  const rowOffsetRef = useRef(0);
  const groupNum = useRef(11);
  const errorRef = useRef('');


  useEffect(()=>{

    installMouser(canvasRef.current);
    addExtraFunctionsToGraphics(canvasRef.current.getContext("2d"));
    addExtraFunctionsToGraphics(OcanvasRef.current.getContext("2d"));
    console.log("wtf");

    console.log(canvasRef.current);
    
    
    
  },[])


  const checkInputs = () => {
    let newT1, newT2, newRO;
    newT1 = Number(translation1.current.value.trim());
    if (isNaN(newT1) || newT1 < 30 || newT1 > 400) {
      errorRef.current = "Translation must be a number, 30 to 400. Change not applied!";
      return false;
    }
    if (groupNum.current === 1 || groupNum.current === 5) {
      newRO = Number(rowOffsetRef.current.value.trim());
      if (isNaN(newRO)) {
        errorRef.current = "Row Offset must be a number. Change not applied!";
        return false;
      }
      newRO = newRO % newT1;
      if (newRO < 0) newRO += newT1;
      if (newRO > newT1 / 2) newRO -= newT1;
    }
    if (groupNum.current < 10) {
      newT2 = Number(translation2.current.value.trim());
      if (isNaN(newT2) || newT2 < 30 || newT2 > 400) {
        errorRef.current = "2nd Translation must be a number, 30 to 400. Change not applied!";
        return false;
      }
    }
    translation1.current = newT1;
    translation2.current = newT2;
    rowOffsetRef.current = newRO;
    errorRef.current = '';
    return true;
  };


  function addExtraFunctionsToGraphics(graphics) {
    graphics.strokeLine = function(x1,y1,x2,y2) {
       graphics.beginPath();
       graphics.moveTo(x1,y1);
       graphics.lineTo(x2,y2);
       graphics.stroke();
    }
   graphics.fillOval = function(x1,y1,x2,y2) {
       var x,y,horizontalRadius,verticalRadius;
       x = Math.min(x1,x2);
       y = Math.min(y1,y2);
       horizontalRadius = (Math.max(x1,x2) - x) / 2;
       verticalRadius = (Math.max(y1,y2) - y) / 2;
       x += horizontalRadius;
       y += verticalRadius;
       graphics.save();
       graphics.translate(x,y);
       graphics.scale(horizontalRadius,verticalRadius);
       graphics.beginPath();
       graphics.arc(0,0,1,0,2*Math.PI,false);
       graphics.restore();
       graphics.fill();
    }
    graphics.strokeOval = function(x1,y1,x2,y2) {
       var x,y,horizontalRadius,verticalRadius;
       x = Math.min(x1,x2);
       y = Math.min(y1,y2);
       horizontalRadius = (Math.max(x1,x2) - x) / 2;
       verticalRadius = (Math.max(y1,y2) - y) / 2;
       x += horizontalRadius;
       y += verticalRadius;
       graphics.save();
       graphics.translate(x,y);
       graphics.scale(horizontalRadius,verticalRadius);
       graphics.beginPath();
       graphics.arc(0,0,1,0,2*Math.PI,false);
       graphics.restore();
       graphics.stroke();
    }
    graphics.fillRectFromCorners = function(x1,y1,x2,y2) {
       var x,y,width,height;
       x = Math.min(x1,x2);
       y = Math.min(y1,y2);
       width = Math.max(x1,x2) - x;
       height = Math.max(y1,y2) - y;
       graphics.fillRect(x,y,width,height);
    }
    graphics.strokeRectFromCorners = function(x1,y1,x2,y2) {
       var x,y,width,height;
       x = Math.min(x1,x2);
       y = Math.min(y1,y2);
       width = Math.max(x1,x2) - x;
       height = Math.max(y1,y2) - y;
       graphics.strokeRect(x,y,width,height);
    }
    }

    const drawAll = () => {

        OcanvasRef.current.getContext("2d").fillStyle = '#FFFFFF';
        let k2  = OcanvasRef.current.getContext("2d");
        
        
        k2.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height);
        for (let i = 0; i < itemCountRef.current; i++) {
          drawItem(k2, itemsRef.current[i]);
        }
        draw();
      };
    
    
    const draw = () => {
        canvasRef.current.getContext("2d").drawImage(OcanvasRef.current, 0, 0);
        if (dragItemRef.current) {
          drawItem(canvasRef.current.getContext("2d"), dragItemRef.current);
        }
        if (document.getElementById('showGridCB').checked) {
          drawGrid();
        }
      };
      
  

  

  const drawItemToOSC = (item) => {
    drawItem(OcanvasRef.current.getContext("2d"), item);
    canvasRef.current.getContext("2d").drawImage(OcanvasRef.current, 0, 0);
    if (document.getElementById('showGridCB').checked) {
      drawGrid();
    }
  };


      


function drawItem(graphics,item) {  
    if (item.type == FREEHAND_TOOL) {
        for (var i = 0; i < item.lines.length; i++) {
            drawItem(graphics,item.lines[i]);
        }
        return;
    }
    if (item.type > 2) {
        graphics.fillStyle = item.color;
    }
    else {
        graphics.strokeStyle = item.color;
        graphics.lineWidth = item.lineWidth;
        graphics.lineCap = item.lineCap;
    }
    var transY;
    var hOffset;
    if (groupNum.current == 1 || groupNum.current == 5) {
        transY = translation2.current;
        hOffset = rowOffsetRef.current/transY; // horizontal offset per vertical pixel
    }
    else if (groupNum.current < 10) {
        transY = translation2.current;
        hOffset = 0;
    }
    else {
        transY = translation1.current;
        hOffset = 0;
    }
    var a,b,i;
    switch (groupNum.current) {
        case 1:
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            break;
        case 2: // pg
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,item.x1+translation1.current/2,item.x2+translation1.current/2,-item.y1,-item.y2);  // horizontal glide reflection
            break;
        case 3: // pm
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2);  // horizontal reflextion
            break;
        case 4: //cm
            a = translation1.current/2;
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,item.y1+transY/2,item.y2+transY/2); // vertical glide reflection
            drawBasicItem(graphics,item.type,a+item.x1,a+item.x2,item.y1+transY/2,item.y2+transY/2);
            drawBasicItem(graphics,item.type,a-item.x1,a-item.x2,item.y1,item.y2); 
            break;
        case 5: //p2
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,-item.y1,-item.y2); // 180 rotation
            break;
        case 6: // pgg
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,item.x1+translation1.current/2,item.x2+translation1.current/2,-item.y1,-item.y2);  // horizontal glide reflection
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,item.y1+transY/2,item.y2+transY/2); // vertical glide reflection
            drawBasicItem(graphics,item.type,-item.x1+translation1.current/2,-item.x2+translation1.current/2,-(item.y1+transY/2),-(item.y2+transY/2)); // double glide reflection
            break;
        case 7: // pmm
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,-item.y1,-item.y2); // 180 rotation
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2);  // horizontal reflextion
            drawBasicItem(graphics,item.type,item.x1,item.x2,-item.y1,-item.y2);  // vertical reflection
            break;
        case 8: // cmm
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2);
            drawBasicItem(graphics,item.type,item.x1,item.x2,-item.y1,-item.y2);
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,-item.y1,-item.y2);
            a = translation1.current/2;
            b = transY/2;
            drawBasicItem(graphics,item.type,item.x1+a,item.x2+a,item.y1+b,item.y2+b);
            drawBasicItem(graphics,item.type,-item.x1+a,-item.x2+a,item.y1+b,item.y2+b);
            drawBasicItem(graphics,item.type,item.x1+a,item.x2+a,-item.y1+b,-item.y2+b);
            drawBasicItem(graphics,item.type,-item.x1+a,-item.x2+a,-item.y1+b,-item.y2+b);
            break;
        case 9: // pmg
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,-item.y1,-item.y2); // 180 rotation
            drawBasicItem(graphics,item.type,item.x1+translation1.current/2,item.x2+translation1.current/2,-item.y1,-item.y2);  // horizontal glide reflection
            drawBasicItem(graphics,item.type,-(item.x1+translation1.current/2),-(item.x2+translation1.current/2),item.y1,item.y2);  // horizontal glide reflection
            break;
        case 10: // p4
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,-item.y1,-item.y2); // 180 rotation
            drawBasicItem(graphics,item.type,item.y1,item.y2,-item.x1,-item.x2); // -90 rot.
            drawBasicItem(graphics,item.type,-item.y1,-item.y2,item.x1,item.x2); // 90 rot.
            break;
        case 11: // p4m
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,-item.y1,-item.y2); // 180 rotation
            drawBasicItem(graphics,item.type,item.y1,item.y2,-item.x1,-item.x2); // -90 rot.
            drawBasicItem(graphics,item.type,-item.y1,-item.y2,item.x1,item.x2); // 90 rot.
            
            drawBasicItem(graphics,item.type,item.x1,item.x2,-item.y1,-item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2); // 180 rotation
            drawBasicItem(graphics,item.type,-item.y1,-item.y2,-item.x1,-item.x2); // -90 rot.
            drawBasicItem(graphics,item.type,item.y1,item.y2,item.x1,item.x2); // 90 rot.
            
            break;
        case 12: // p4g
            drawBasicItem(graphics,item.type,item.x1,item.x2,item.y1,item.y2);  // Untransformed item
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,-item.y1,-item.y2); // 180 rotation
            drawBasicItem(graphics,item.type,item.y1,item.y2,-item.x1,-item.x2); // -90 rot.
            drawBasicItem(graphics,item.type,-item.y1,-item.y2,item.x1,item.x2); // 90 rot.
            
            drawBasicItem(graphics,item.type,translation1.current/2-item.x1,translation1.current/2-item.x2,translation1.current/2-item.y1,translation1.current/2-item.y2);  
            drawBasicItem(graphics,item.type,translation1.current/2+item.x1,translation1.current/2+item.x2,translation1.current/2+item.y1,translation1.current/2+item.y2); 
            drawBasicItem(graphics,item.type,translation1.current/2-item.y1,translation1.current/2-item.y2,translation1.current/2+item.x1,translation1.current/2+item.x2); 
            drawBasicItem(graphics,item.type,translation1.current/2+item.y1,translation1.current/2+item.y2,translation1.current/2-item.x1,translation1.current/2-item.x2); 
            
            drawBasicItem(graphics,item.type,translation1.current/2-item.x1,translation1.current/2-item.x2,item.y1,item.y2);  
            drawBasicItem(graphics,item.type,translation1.current/2+item.x1,translation1.current/2+item.x2,-item.y1,-item.y2); 
            drawBasicItem(graphics,item.type,translation1.current/2-item.y1,translation1.current/2-item.y2,-item.x1,-item.x2); 
            drawBasicItem(graphics,item.type,translation1.current/2+item.y1,translation1.current/2+item.y2,item.x1,item.x2); 
            
            drawBasicItem(graphics,item.type,item.x1,item.x2,translation1.current/2-item.y1,translation1.current/2-item.y2);  
            drawBasicItem(graphics,item.type,-item.x1,-item.x2,translation1.current/2+item.y1,translation1.current/2+item.y2); 
            drawBasicItem(graphics,item.type,item.y1,item.y2,translation1.current/2+item.x1,translation1.current/2+item.x2); 
            drawBasicItem(graphics,item.type,-item.y1,-item.y2,translation1.current/2-item.x1,translation1.current/2-item.x2); 
            
            break;
        case 13: // p3
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,0);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,2*Math.PI/3);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,-2*Math.PI/3);
            break;
        case 14: // p3m1
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,0);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,2*Math.PI/3);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,-2*Math.PI/3);
            drawBasicItemHex(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2,0);
            drawBasicItemHex(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2,2*Math.PI/3);
            drawBasicItemHex(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2,-2*Math.PI/3);
            break;
        case 15: // p31m
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,0);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,2*Math.PI/3);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,-2*Math.PI/3);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,-item.y1,-item.y2,0);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,-item.y1,-item.y2,2*Math.PI/3);
            drawBasicItemHex(graphics,item.type,item.x1,item.x2,-item.y1,-item.y2,-2*Math.PI/3);
            break;
        case 16: // p6
            for (i = 0; i < 6; i++) {
                drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,i*Math.PI/3);
            }
            break;
        case 17: // p6m
            for (i = 0; i < 6; i++) {
                drawBasicItemHex(graphics,item.type,item.x1,item.x2,item.y1,item.y2,i*Math.PI/3);
                drawBasicItemHex(graphics,item.type,-item.x1,-item.x2,item.y1,item.y2,i*Math.PI/3);
            }
            break;
    }
    function drawBasicItem(graphics,type,x1,x2,y1,y2) {
        var minX = Math.min(x1,x2) - 10;
        var maxX = Math.max(x1,x2) + 10;
        var minY = Math.min(y1,y2) - 10;
        var maxY = Math.max(y1,y2) + 10;
        var startY = -transY * Math.floor(maxY/transY);
        var startX = -translation1.current * Math.floor( maxX/translation1.current );
        var ty = startY;
        while (ty+minY < canvasRef.current.height) {
            graphics.save();
            graphics.translate(0,ty);
            var tx = startX;
            if (hOffset != 0) {
                tx += hOffset * ty;
                while (tx+maxX < 0)
                    tx += translation1.current;
                while (tx+maxX > translation1.current)
                    tx -= translation1.current;
            }
            while (tx+minX < canvasRef.current.width) {
                graphics.save();
                graphics.translate(tx,0);
                if (type == 0)
                    graphics.strokeLine(x1, y1, x2, y2);
                else if (type == 1)
                    graphics.strokeRectFromCorners(x1, y1, x2, y2);
                else if (type == 2)
                    graphics.strokeOval(x1, y1, x2, y2);
                else if (type == 3)
                    graphics.fillRectFromCorners(x1, y1, x2, y2);
                else 
                    graphics.fillOval(x1, y1, x2, y2);
                graphics.restore();
                tx += translation1.current;
            }
            graphics.restore();
            ty += transY;
        }
    }
    function drawBasicItemHex(graphics,type,x1,x2,y1,y2,theta) {
        var s = Math.sin(theta);
        var c = Math.cos(theta);
        var xc = (x1+x2)/2;
        var yc = (y1+y2)/2;
        var radius = Math.sqrt( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) ) / 2;
        
        var temp = c*xc-s*yc; // do rotation of center
        yc = s*xc+c*yc;
        xc = temp;

        var minX = xc - radius - 10;
        var maxX = xc + radius + 10;
        var minY = yc - radius - 10;
        var maxY = yc + radius + 10;
        var trans = translation1.current;
        var transH = trans * 2/ Math.sqrt(3);
        var startY = -trans * Math.floor(maxY/trans);
        var startX = -transH * Math.floor(maxX/transH);
        var ty = startY;
        var hOffset = -Math.sqrt(3);
        while (ty+minY < canvasRef.current.height) {
            graphics.save();
            graphics.translate(0,ty);
            var tx = startX;
            tx -= hOffset * ty;
            while (tx+maxX < 0)
                tx += transH;
            while (tx+maxX > transH)
                tx -= transH;
            while (tx+minX < canvasRef.current.width) {
                graphics.save();
                graphics.translate(tx,0);
                graphics.rotate(theta);
                if (type == 0)
                    graphics.strokeLine(x1, y1, x2, y2);
                else if (type == 1)
                    graphics.strokeRectFromCorners(x1, y1, x2, y2);
                else if (type == 2)
                    graphics.strokeOval(x1, y1, x2, y2);
                else if (type == 3)
                    graphics.fillRectFromCorners(x1, y1, x2, y2);
                else 
                    graphics.fillOval(x1, y1, x2, y2);
                graphics.restore();
                tx += transH;
            }
            graphics.restore();
            ty += trans;
        }
    }
}
    
function drawGrid(graphics) { 
    graphics.save();
    graphics.lineWidth = 1;
    graphics.lineCap = "butt";
    graphics.globalAlpha = 0.5;
    for (var i = 0; i < 2; i++) {
        graphics.save();
        if (i == 1) {
            graphics.strokeStyle = "black";
            graphics.translate(0.5,0.5);
        }
        else {
            graphics.strokeStyle = "white";
            graphics.translate(-0.5,-0.5);
        }
        var y,dy;
        var w = canvasRef.current.width;
        var h = canvasRef.current.height;
        if (groupNum.current < 10) {
            dy = translation2.current;
        }
        else {
            dy = translation1.current;
        }
        y = dy;
        while (y < h) {
            graphics.strokeLine(0,y,w,y);
            y += dy;
        }
        var x,dx;
        if (groupNum.current < 13 && (rowOffsetRef.current == 0 || groupNum.current != 1 && groupNum.current != 5)) {
            x = dx = translation1.current;
            while (x < w) {
                graphics.strokeLine(x,0,x,h);
                x += dx;
            }
        }
        else if (groupNum.current < 13) { // and rowOffsetRef.current is not 0 and groupNum.current is 1 or 5
            var rows = h / translation2.current;
            var offset;
            if (rowOffsetRef.current <= translation1.current/2)
                offset = rows*rowOffsetRef.current;
            else
                offset = rows*(rowOffsetRef.current - translation1.current);
            dx = translation1.current;
            if (offset > 0) {
                x = 0;
                while (x + offset > dx)
                    x -= dx;
                while (x < w) {
                    graphics.strokeLine(x,0,x+offset,h);
                    x += dx;
                }
            }
            else {
                x = dx;
                while (x + offset < w) {
                    graphics.strokeLine(x,0,x+offset,h);
                    x += dx;
                }
            }
        }
        else {
            var offset = h/Math.sqrt(3);
            dx = translation1.current*2/Math.sqrt(3);
            x = 0;
            while (x + offset > dx)
                x -= dx;
            while (x < w) {
                graphics.strokeLine(x,0,x+offset,h);
                x += dx;
            }
            offset = -offset;
            x = dx;
            while (x + offset < w) {
                graphics.strokeLine(x,0,x+offset,h);
                x += dx;
            }
        }
        graphics.restore();
    }
    graphics.restore();
}

function doApply() {
    if (checkInputs()) {
        drawAll();
    }
}

function checkForReturnKey(evt) {
    if (evt.keyCode == 13)
       doApply();
}

 // Undo function
 const undo = () => {
    if (clearedItemsRef.current !== null) {
      itemsRef.current = clearedItemsRef.current;
      itemCountRef.current = itemsRef.current.length;
      drawAll();
      document.getElementById("undo").disabled = false;
      document.getElementById("redo").disabled = true;
      clearedItemsRef.current = null;
    } else if (itemCountRef.current > 0) {
      itemCountRef.current--;
      drawAll();
      if (itemCountRef.current === 0)
        document.getElementById("undo").disabled = true;
      document.getElementById("redo").disabled = false;
    }
    document.getElementById("clear").disabled = itemCountRef.current === 0;
    document.getElementById("savebtn").disabled = itemCountRef.current === 0;
  };

  // Redo function
  const redo = () => {
    if (itemCountRef.current < itemsRef.current.length) {
      itemCountRef.current++;
      drawAll();
      if (itemCountRef.current === itemsRef.current.length)
        document.getElementById("redo").disabled = true;
      document.getElementById("clear").disabled = false;
      document.getElementById("savebtn").disabled = false;
    }
  };

  // Clear drawing function
  const clearDrawing = () => {
    if (itemsRef.current.length === 0)
      return;
    if (itemCountRef.current > 0) {
      if (itemsRef.current.length > itemCountRef.current)
        itemsRef.current.splice(itemCountRef.current, itemsRef.current.length - itemCountRef.current);
      clearedItemsRef.current = itemsRef.current;
    } else {
      clearedItemsRef.current = null;
    }
    itemsRef.current = [];
    itemCountRef.current = 0;
    drawAll();
    document.getElementById("clear").disabled = true;
    document.getElementById("savebtn").disabled = true;
    document.getElementById("redo").disabled = true;
    document.getElementById("undo").disabled = clearedItemsRef.current === null;
  };
//chage this to set curentREf item

const selectColor = (color) => {
    currentColorRef.current = colors[color];
  };

  const selectLineWidth = (lineWidth) => {
    currentLineWidthRef.current = Number(lineWidth);
    if (currentToolRef.current === FREEHAND_TOOL || currentLineWidthRef.current >= 3) {
      currentLineCapRef.current = "round";
    } else {
      currentLineCapRef.current = "butt";
    }
  };

  const selectTool = (tool) => {
    currentToolRef.current = Number(tool);
    if (currentToolRef.current === FREEHAND_TOOL || currentLineWidthRef.current >= 3) {
      currentLineCapRef.current = "round";
    } else {
      currentLineCapRef.current = "butt";
    }
  };

  const selectGroup = (num) => {
    num = Number(num);
    if (num === groupNum.current) {
      return;
    }
    groupNum.current = num;
    if (num === 1 || num === 5) {
    //   offsetHolderRef.current.style.display = "inline";
    //   offsetHolderRef.current.value = "" + rowOffsetRef.current;
    // } else {
    //   offsetHolderRef.current.style.display = "none";
    }
    // if (num < 10) {
    //   trans2HolderRef.current.style.display = "inline";
    //   translation2.current.value = "" + translation2.current;
    // } else {
    //   trans2HolderRef.current.style.display = "none";
    // }
    // // Call your drawAll function here
    drawAll();
  };
  

  function installMouser(theCanvas) {
    function convertX(clientX) { 
        return Math.round(clientX - theCanvas.getBoundingClientRect().left);
    }

    function convertY(clientY) {
        return Math.round(clientY - theCanvas.getBoundingClientRect().top);
    }

    function doMouseDrag(evt){
        console.log("drag");
        if (dragItemRef.current == null)
        {
          console.log("null dragitme")
          return;
        }

        dragItemRef.current.x2 = convertX(evt.clientX);
        dragItemRef.current.y2 = convertY(evt.clientY);

        if (currentToolRef.current === FREEHAND_TOOL) {
            var segment = {};
            segment.type = 0;
            segment.color = currentColorRef.current;
            segment.lineWidth = currentLineWidthRef.current;
            segment.lineCap = currentLineCapRef.current;
            segment.x1 = dragItemRef.current.x1;
            segment.x2 = dragItemRef.current.x2;
            segment.y1 = dragItemRef.current.y1;
            segment.y2 = dragItemRef.current.y2;
            dragItemRef.current.lines.push(segment);
            drawItemToOSC(segment);
            dragItemRef.current.x1 = segment.x2;
            dragItemRef.current.y1 = segment.y2;
        }
        else {
            draw();
        }
        evt.preventDefault();
    }

    function doMouseUp(evt){
        console.log("up");
        if (dragItemRef.current == null){
          console.log("up and null");
          return;
        }

        theCanvas.removeEventListener("mousemove", doMouseDrag);
        theCanvas.removeEventListener("mouseup", doMouseUp);

        if ((currentToolRef.current === FREEHAND_TOOL && dragItemRef.current.lines.length > 0) ||
            (currentToolRef.current === 0 && (dragItemRef.current.x1 !== dragItemRef.current.x2 || dragItemRef.current.y1 !== dragItemRef.current.y2)) ||
            (currentToolRef.current > 0 && currentToolRef.current < FREEHAND_TOOL && dragItemRef.current.x1 !== dragItemRef.current.x2 && dragItemRef.current.y1 !== dragItemRef.current.y2)) {

            if (itemCountRef.current < itemsRef.current.length)
                itemsRef.current.splice(itemCountRef.current, itemsRef.current.length - itemCountRef.current);

            itemsRef.current.push(dragItemRef.current);
            itemCountRef.current = itemsRef.current.length;
            document.getElementById("undo").disabled = false;
            document.getElementById("redo").disabled = true;
            document.getElementById("clear").disabled = false;
            document.getElementById("savebtn").disabled = false;
            clearedItemsRef.current = null;

            if (currentToolRef.current !== FREEHAND_TOOL) {
                drawItemToOSC(dragItemRef.current);
            }
        }

        dragItemRef.current = null;
        evt.preventDefault();
    }

    function doMouseDown(evt){
        console.log("UP");
        if (startingRef.current) {
            drawAll();
            startingRef.current = false;
        }

        if (dragItemRef.current != null || evt.button > 0){
          console.log("down ad null");
          return;
        }

        document.getElementById("error").innerHTML = "&nbsp;";
        theCanvas.addEventListener("mousemove", doMouseDrag);
        document.addEventListener("mouseup", doMouseUp);

        dragItemRef.current = {};
        dragItemRef.current.type = currentToolRef.current;
        dragItemRef.current.color = currentColorRef.current;
        dragItemRef.current.lineWidth = currentLineWidthRef.current;
        dragItemRef.current.lineCap = currentLineCapRef.current;
        dragItemRef.current.x1 = dragItemRef.current.x2 = convertX(evt.clientX);
        dragItemRef.current.y1 = dragItemRef.current.y2 = convertY(evt.clientY);

        if (currentToolRef.current === FREEHAND_TOOL) {
            dragItemRef.current.lines = [];
        }

        evt.preventDefault();
    }

    theCanvas.addEventListener("mousedown", doMouseDown);
}
return (
    <div id="content">
      <h2>Wallpaper Symmetry</h2>
      <Canvas
          ref={canvasRef}
          width={800}
          height={600}
          id="c1"
          />
          <Canvas
          
          ref={OcanvasRef}
          width={800}
          height={600}
          id="c2"
          
          />
          
      <table border={0} cellPadding={5} cellSpacing={5} align="center">
        <tbody>
        <tr>
          <td colSpan={2}><span id="error">&nbsp;</span></td>
        </tr>
        <tr>
          <td colSpan={3} bgcolor="#DDDDDD">
            <label title="Horizontal translation in pixels, in the range 30 to 400. You must click Apply or press Enter for a change to take effect.">
              Translation Amount: <input onChange={checkForReturnKey} type="text" size={3} maxLength={3} value={translation1.current}  />
            </label>
            <span id="trans2holder" style={{ marginLeft: '20px', display: 'none' }}>
              <label title="Vertical translation in pixels, in the range 30 to 400. You must click Apply or press Enter for a change to take effect.">
                2nd Translation: <input onChange={checkForReturnKey} type="text" size={3} maxLength={3} value={translation2.current}  />
              </label>
            </span>
            <span id="offsetholder" style={{ marginLeft: '20px', display: 'none' }}>
              <label title="Amount by which each row is offset horizontally from the previous row. Any value is equivalent to one between plus and minus Translation/2. You must click Apply or press Enter for a change to take effect.">
                Row Offset: <input onChange={checkForReturnKey} type="text" size={3} maxLength={4} value={rowOffsetRef.current} />
              </label>
            </span>
            <button style={{ marginLeft: '20px' }} onClick={doApply} title="Check input and if legal, apply to current image. You can also do this by pressing Enter in an input box.">Apply</button>
          </td>
        </tr>
        <tr>
          <td valign="top" bgcolor="#DDDDDD">
            <p>
              <b>Symmetry<br />Group:</b><br /><br />
              {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17].map((num) => (
                <label key={num}>
                  <input type="radio" name="group" value={num} id={`g${num}`} onClick={() => selectGroup(num)} />
                  {` p${num}`}
                </label>
              ))}
            </p>
          </td>
          <td valign="top">
          <button id="savebtn" onClick={undo} title="Remove the most recently drawn item. Can also undo Clear if used immediately after clearing.">Undo</button>
            <button id="undo" onClick={undo} title="Remove the most recently drawn item. Can also undo Clear if used immediately after clearing.">Undo</button>
            <button id="redo" onClick={redo} title="Restore the draw item that was removed most recently by Undo.">Redo</button>
            <button id="clear" onClick={clearDrawing} title="Clear the current image. This can be undone if you click 'Undo' immediately after clearing.">Clear</button>
            <input type="checkbox" onChange={drawGrid} id="showGridCB" style={{ marginLeft: '30px' }} />
            <label htmlFor="showGridCB" style={{ color: 'white' }}>Show Grid</label>
          </td>
          <td valign="top" bgcolor="#DDDDDD">
            <p>
              <b>Tool:</b><br />
              {[0, 1, 2, 3, 4, 5].map((tool) => (
                <label key={tool}>
                  <input type="radio" name="tool" value={tool} id={`t${tool}`} onClick={() => selectTool(tool)} />
                  {` ${tool === 5 ? 'Freehand' : ` Tool ${tool}`}`}
                </label>
              ))}
            </p>
            <p>
              <b>Line Width:</b><br />
              {[1, 2, 3, 4, 5, 10, 20].map((width) => (
                <label key={width}>
                  <input type="radio" name="linewidth" value={width} id={`lw${width}`} onClick={() => selectLineWidth(width)} />
                  {` ${width}`}
                </label>
              ))}
            </p>
            <p>
              <b>Color:</b><br />
              {[0, 1, 2, 3, 4, 5, 6, 7, 8, 9].map((color) => (
                <label key={color}>
                  <input type="radio" name="color" value={color} id={`c${color}`} onClick={() => selectColor(color)} />
                  {` ${color === 7 ? 'Light Gray' : ` Color ${color}`}`}
                </label>
              ))}
            </p>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  );
};

export default  DrawingCanvas;
